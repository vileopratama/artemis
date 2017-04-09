# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime as dt
import math


class ProjectTarget(models.Model):
    _name = 'bdo.project.invoice'
    _inherit = ['mail.thread']
    _order = 'date_period_start desc'

    project_id = fields.Many2one(comodel_name='bdo.project', string='Project', ondelete='restrict', store=True,
                                 required=True)
    project_line_id = fields.Many2one(comodel_name='bdo.project.lines', string='Service', required=True,
                                      states={'draft': [('readonly', False)]}, readonly=True, store=True)
    date_invoice = fields.Date(string='Date Invoice', store=True)
    name = fields.Char(string='Invoice No', readonly=True)
    name_file = fields.Char(string='File')
    name_file_attachment = fields.Binary(string='Attachment')
    employee_id = fields.Many2one(comodel_name='hr.employee', string='PIC', readonly=True,
                                  default=lambda self: self.env.user.employee_id.id)
    user_id = fields.Many2one(comodel_name='res.users', default=lambda self: self.env.user.id, string='PIC',
                              readonly=True)
    date_on_scheduled = fields.Date(string='Scheduled on', required=True, states={'draft': [('readonly', False)]},
                                    readonly=True)
    date_period_start = fields.Date(string='From', required=True, states={'draft': [('readonly', False)]},
                                    readonly=True)
    date_period_end = fields.Date(string='To', required=True, states={'draft': [('readonly', False)]}, readonly=True)
    date_period_month_total = fields.Integer(compute='_compute_period_month_total', string='Total Month', readonly=True,
                                             store=True)
    jan_period = fields.Integer(compute='_compute_period_month', string='Jan', readonly=True, store=True, default=0)
    feb_period = fields.Integer(compute='_compute_period_month', string='Feb', readonly=True, store=True, default=0)
    mar_period = fields.Integer(compute='_compute_period_month', string='Mar', readonly=True, store=True, default=0)
    apr_period = fields.Integer(compute='_compute_period_month', string='Apr', readonly=True, store=True, default=0)
    may_period = fields.Integer(compute='_compute_period_month', string='May', readonly=True, store=True, default=0)
    jun_period = fields.Integer(compute='_compute_period_month', string='Jun', readonly=True, store=True, default=0)
    jul_period = fields.Integer(compute='_compute_period_month', string='Jul', readonly=True, store=True, default=0)
    aug_period = fields.Integer(compute='_compute_period_month', string='Aug', readonly=True, store=True, default=0)
    sept_period = fields.Integer(compute='_compute_period_month', string='Sept', readonly=True, store=True,
                                 default=False)
    oct_period = fields.Integer(compute='_compute_period_month', string='Oct', readonly=True, store=True, default=0)
    nov_period = fields.Integer(compute='_compute_period_month', string='Nov', readonly=True, store=True, default=0)
    dec_period = fields.Integer(compute='_compute_period_month', string='Dec', readonly=True, store=True, default=0)
    year_period = fields.Char(string='Year', size=4, store=True, readonly=True)
    amount = fields.Float(compute='_compute_period_month_total', string='Amount', readonly=True, store=True,
                          digits=(16, 2))
    amount_equivalent = fields.Float(compute='_compute_period_month_total', string='Amount Equivalent', readonly=True,
                                     store=True, digits=(16, 2))
    remarks = fields.Text(string='Remarks', states={'draft': [('readonly', False)]}, readonly=True)
    state = fields.Selection(
        [('draft', 'Draft'), ('invoice', 'Invoice'), ('paid', 'Paid')], 'Status', readonly=True, copy=False,
        default='draft')

    total_due = fields.Integer(string='Term of payment (days)', readonly=True)
    date_payment_due = fields.Date(string='Expected payment date', readonly=True, store=True)
    number_invoice = fields.Char(string='Invoice No.', readonly=True, store=True)
    partner_id = fields.Char(related='project_line_id.client_name', string='Name of the Company', readonly=True)
    service_id = fields.Char(related='project_line_id.service_id.name', string='Service', readonly=True)
    date_engagement = fields.Date(related='project_line_id.date_engagement', string='Date of engagement', readonly=True)
    currency_id = fields.Char(related='project_line_id.currency_id', string='Currency', readonly=True)
    amount_project_total = fields.Float(related='project_line_id.amount', string='Amount Project', readonly=True)
    amount_project_equivalent = fields.Float(related='project_line_id.amount_equivalent',
                                             string='Amount Project Equivalent', readonly=True)

    _sql_constraints = [
        ('unique_jan', 'unique(project_line_id, jan_period', 'January Period is ready to schedule for this project!'),
        ('unique_feb', 'unique(project_line_id, feb_period', 'February Period is ready to schedule for this project!'),
        ('unique_mar', 'unique(project_line_id, mar_period', 'March Period is ready to schedule for this project!'),
        ('unique_apr', 'unique(project_line_id, apr_period', 'April Period is ready to schedule for this project!'),
        ('unique_may', 'unique(project_line_id, may_period', 'May Period is ready to schedule for this project!'),
        ('unique_jun', 'unique(project_line_id, jun_period', 'June Period is ready to schedule for this project!'),
        ('unique_jul', 'unique(project_line_id, jul_period', 'July Period is ready to schedule for this project!'),
        ('unique_aug', 'unique(project_line_id, aug_period', 'August Period is ready to schedule for this project!'),
        ('unique_sept', 'unique(project_line_id, sept_period',
         'September Period is ready to schedule for this project!'),
        ('unique_oct', 'unique(project_line_id, oct_period', 'October Period is ready to schedule for this project!'),
        ('unique_nov', 'unique(project_line_id, nov_period', 'November Period is ready to schedule for this project!'),
        ('unique_dec', 'unique(project_line_id, dec_period', 'December Period is ready to schedule for this project!')
    ]

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            name = record.partner_id + ' > ' + record.service_id
            result.append((record.id, name))
        return result

    @api.onchange('project_id')
    def _onchange_project_id(self):
        if self.project_id:
            return {'domain': {'project_line_id': [('project_id', '=', self.project_id.id)]}}
        else:
            return {'domain': {'project_line_id': [('project_id', '=', 0)]}}

    @api.multi
    @api.depends('date_period_start', 'date_period_end', 'project_line_id')
    def _compute_period_month_total(self):
        koef = 0.0833333333333333
        for target in self:
            if target.project_line_id and target.date_period_start and target.date_period_end:
                month_total = self._month_between(target.date_period_start, target.date_period_end)
                target.date_period_month_total = month_total
                target.amount = (koef * month_total) * target.amount_project_total
                target.amount_equivalent = (koef * month_total) * target.amount_project_equivalent

    def _month_between(self, date_from, date_to):
        date_from = dt.strptime(date_from, "%Y-%m-%d")
        date_to = dt.strptime(date_to, "%Y-%m-%d")
        total_days = abs((date_to - date_from).days)
        if (total_days > 0):
            return math.ceil(total_days / 30)
        else:
            return 0

    @api.onchange('date_period_start', 'date_period_end', 'project_line_id')
    def _onchange_date_period(self):
        koef = 0.0833333333333333
        for target in self:
            if target.project_line_id and target.date_period_start and target.date_period_end:
                month_total = self._month_between(target.date_period_start, target.date_period_end)
                target.date_period_month_total = month_total
                target.amount = (koef * month_total) * target.amount_project_total
                target.amount_equivalent = (koef * month_total) * target.amount_project_equivalent

    @api.multi
    @api.depends('date_period_start', 'date_period_end', 'project_line_id')
    def _compute_period_month(self):
        for target in self:
            if target.project_line_id and target.date_period_start and target.date_period_end:
                # default to false
                self.jan_period = 0
                self.feb_period = 0
                self.mar_period = 0
                self.apr_period = 0
                self.may_period = 0
                self.jun_period = 0
                self.jul_period = 0
                self.aug_period = 0
                self.sept_period = 0
                self.oct_period = 0
                self.nov_period = 0
                self.dec_period = 0

                month_start = dt.strptime(target.date_period_start, "%Y-%m-%d")
                month_start = month_start.month
                # month_start = month_start.strip("0","")
                month_total = self._month_between(target.date_period_start, target.date_period_end)

                i = month_start
                total = i + month_total
                while (i < total):
                    if i == 1:
                        self.jan_period = target.project_line_id.id
                    elif i == 2:
                        self.feb_period = target.project_line_id.id
                    elif i == 3:
                        self.mar_period = target.project_line_id.id
                    elif i == 4:
                        self.apr_period = target.project_line_id.id
                    elif i == 5:
                        self.may_period = target.project_line_id.id
                    elif i == 6:
                        self.jun_period = target.project_line_id.id
                    elif i == 7:
                        self.jul_period = target.project_line_id.id
                    elif i == 8:
                        self.aug_period = target.project_line_id.id
                    elif i == 9:
                        self.sept_period = target.project_line_id.id
                    elif i == 10:
                        self.oct_period = target.project_line_id.id
                    elif i == 11:
                        self.nov_period = target.project_line_id.id
                    elif i == 12:
                        self.dec_period = target.project_line_id.id

                    i = i + 1

    def action_set_invoice(self, data):
        args = {
            'state': 'invoice',
            'date_invoice': data.get('date_invoice', fields.Date.today()),
            'name': data.get('name', ''),
            'name_file': data.get('name_file', ''),
            'name_file_attachment': data.get('name_file_attachment', ''),
            'total_due': data.get('total_due', 0),
            'date_payment_due': data.get('date_payment_due', fields.Date.today()),
            'number_invoice': data.get('payment_name', '')
        }
        self.write(args)
