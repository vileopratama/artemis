# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)


class Project(models.Model):
    _name = 'bdo.project'
    _inherit = ['mail.thread']
    _description = 'BDO Project'

    def _get_currency(self):
        currency = False
        if self.env.user.company_id.currency_id.id:
            currency = self.env.user.company_id.currency_id.id
        return currency

    code = fields.Char(string='Project Code', size=60, required=True,
                       help='This Project Code can reference to Timesheeet Project Code')
    partner_id = fields.Many2one(comodel_name='res.partner', string='Client', index=True,
                                 domain=[('is_company', '=', True)],required=True)
    proposal_id = fields.Many2one(comodel_name='crm.proposal', string='Proposal No', index=True)
    type = fields.Selection(
        [('recurring services', 'Recurring Services'), ('non-recurring services', 'Non-Recurring Services')],
        string='Type', required=True, default='recurring services')
    source = fields.Selection([('local', 'Local'), ('global', 'Global')], string='Project',
                              required=True, default='local')
    date_engagement = fields.Date(string='Date of engagement', index=True, default=fields.Datetime.now)
    name = fields.Char(string='No. Of EL', size=100)
    #el = fields.Char(string='EL File')
    #el_attachment = fields.Binary(string='Attachment')
    el_attachment_ids = fields.Many2many(comodel_name='ir.attachment', string='EL Attachments')
    date_expiry_engagement = fields.Date(string='Expiry date', index=True, default=fields.Datetime.now)
    currency_id = fields.Many2one(comodel_name='res.currency', string='Currency', required=True, index=True,
                                  default=_get_currency)
    conflict_check = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Conflict Check', default='no')
    lines = fields.One2many(comodel_name='bdo.project.lines', inverse_name='project_id', string='Project Lines')
    amount_total = fields.Float(compute='_compute_amount_all', string='Amount Total', readonly=True, store=True)
    rate = fields.Float(string='Rate')
    amount_equivalent = fields.Float(compute='_compute_amount_all', string='Amount Total Equiv', readonly=True,
                                     store=True)
    employee_id = fields.Many2one(comodel_name='hr.employee', string='PIC', compute='_compute_acl', readonly=True,
                                  store=True)
    user_id = fields.Many2one(comodel_name='res.users', string='User Related', compute='_compute_acl', readonly=True,
                              store=True)
    date_reminder = fields.Date(string='Reminder Date', index=True, default=fields.Datetime.now)
    employees = fields.One2many('bdo.project.employees', inverse_name='project_id', string='Team Member')
    remarks = fields.Text(string='Remarks')
    attachment_ids = fields.Many2many(comodel_name='ir.attachment', string='Attachments')
    state = fields.Selection([('active', 'Active'), ('inactive', 'In-Active')], 'Status', readonly=True,
                             default='active', required=True)

    _sql_constraints = [
        ('unique_code', 'unique (code)', 'Project code must be unique!'),
    ]

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            name = record.code + ' > ' + record.partner_id.name
            result.append((record.id, name))
        return result

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id:
            return {'domain': {'proposal_id': [('partner_id', '=', self.partner_id.id)]}}
        else:
            return {'domain': {'proposal_id': [('partner_id', '=', 0)]}}

    @api.multi
    @api.depends('lines.amount_equivalent')
    def _compute_amount_all(self):
        for project in self:
            total = sum(line.amount for line in project.lines)
            # total amount original currency
            project.amount_total = total
            # total amount equiv currency
            total_equiv = sum(line.amount_equivalent for line in project.lines)
            project.amount_equivalent = total_equiv

    @api.onchange('currency_id')
    def _onchange_currency_id(self):
        if self.currency_id:
            date = self._context.get('date') or fields.Datetime.now()
            company_id = self._context.get('company_id') or self.env['res.users']._get_company().id
            query = """SELECT c.id, (SELECT r.rate FROM res_currency_rate r
            WHERE r.currency_id = c.id AND r.name <= %s
            AND (r.company_id IS NULL OR r.company_id = %s)
            ORDER BY r.company_id, r.name DESC
            LIMIT 1) AS rate
            FROM res_currency c
            WHERE c.id = %s"""

            self.env.cr.execute(query, (date, company_id, self.currency_id.id))
            currency_rates = dict(self._cr.fetchall())
            for project in self:
                project.rate = currency_rates.get(project.currency_id.id) or 1.0

    @api.multi
    def set_active(self):
        return self.write({'state': 'active'})

    @api.multi
    def set_inactive(self):
        return self.write({'state': 'inactive'})

    @api.multi
    @api.depends('employees.employee_id')
    def _compute_acl(self):
        for el in self:
            for line in el.employees:
                if line.acl == 'in-charge':
                    el.employee_id = line.employee_id
                    users = self.env['res.users'].search([('employee_id', '=', line.employee_id.id)], limit=1)
                    # for user in users:
                    el.user_id = users

    
class ProjectLines(models.Model):
    _name = 'bdo.project.lines'
    _description = "Project Line Invoice"
    _rec_name = "project_id"

    project_id = fields.Many2one(comodel_name='bdo.project', string='Project Ref', ondelete='cascade')
    client_name = fields.Char(related='project_id.partner_id.name', string='Client')
    date_engagement = fields.Date(related='project_id.date_engagement', string='Date of engagement')
    service_id = fields.Many2one(comodel_name='bdo.project.service', string='Service',
                                 change_default=True, domain=[('state', '=', 'active')])
    currency_id = fields.Char(related='project_id.currency_id.name', string='Currency')
    amount = fields.Float(string='Amount', default=1, store=True)
    amount_equivalent = fields.Float(compute='_compute_amount_line_all', digits=0, string='Amount Equivalent',
                                     store=True,
                                     readonly=True)
    employee_id = fields.Integer(related='project_id.employee_id.id', string='Sync Employee ID')
    user_id = fields.Integer(related='project_id.user_id.id', string='Related User')

    _sql_constraints = [('unique_service', 'unique(project_id, service_id)',
                         'Cannot Use one tracker twice!\nPlease, select a different service')]

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            name = record.client_name + ' > ' + record.service_id.name
            result.append((record.id, name))
        return result

    @api.onchange('amount')
    def _onchange_amount(self):
        if self.service_id and self.project_id.rate:
            self.amount_equivalent = self.project_id.rate * self.amount

    @api.multi
    @api.depends('amount', 'project_id.rate')
    def _compute_amount_line_all(self):
        for line in self:
            line.amount_equivalent = (line.project_id.rate or 1.0) * line.amount


class ProjectEmployees(models.Model):
    _name = "bdo.project.employees"
    _description = "Employee of Project"
    _rec_name = "employee_id"

    project_id = fields.Many2one(comodel_name='bdo.project', string='Employee Ref', ondelete='cascade')
    employee_id = fields.Many2one(comodel_name='hr.employee', string='Employee', change_default=True)
    acl = fields.Selection([('in-charge', 'In Charge'), ('assistant', 'Assistant')], string='Access Control List')
