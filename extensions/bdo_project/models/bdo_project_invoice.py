# -*- coding: utf-8 -*-
from odoo import models,fields,api
from datetime import datetime as dt

class ProjectInvoice(models.Model):
    _name = 'bdo.project.invoice'

    def _get_currency(self):
        currency = False
        if self.env.user.company_id.currency_id.id:
            currency = self.env.user.company_id.currency_id.id
        return currency

    name = fields.Char(string='Invoice Number',required=True,size=50)
    tax_invoice_number = fields.Char(string='Tax Invoice No',size=30)
    date_invoice = fields.Date(string='Date of Invoice', required=True)
    state = fields.Selection([
        ('pending', 'Pending'),
        ('received', 'Received'),
    ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='pending')
    partner_id = fields.Many2one(comodel_name='res.partner',string='Client')
    date_on_scheduled = fields.Date(string='Scheduled On',required=True)
    date_month_on_scheduled = fields.Char(string='Scheduled On', compute='_get_date_month_on_scheduled', store=True, readonly=True)
    date_period_from = fields.Date(string='Period From', required=True)
    date_period_to = fields.Date(string='Period To', required=True)
    date_period = fields.Char(string='Month', compute='_get_date_period', store=True,readonly=True)
    remarks = fields.Text(string='Remarks')
    attachment_ids = fields.Many2many(comodel_name='ir.attachment', string='Attachments')
    currency_id = fields.Many2one(comodel_name='res.currency',string='Currency',default=_get_currency,
                                  help='The optional other currency if it is a multi-currency entry.')
    rate = fields.Float(string='Current Rate',digits=(12, 2),
                        help='The rate of the currency to the currency of rate 1.')
    lines = fields.One2many(comodel_name='bdo.project.invoice.line',inverse_name='invoice_id',index=True,
                            string='Invoice Lines', states={'pending': [('readonly', False)]},readonly=True, copy=True)
    amount = fields.Float(compute='_compute_amount_all', string='Amount', digits=0,store=True)
    amount_total = fields.Float(compute='_compute_amount_all',string='Amount Total', digits=0,store=True)
    
    @api.multi
    def do_received(self):
	    return self.write({'state': 'received'})

    @api.multi
    def do_pending(self):
	    return self.write({'state': 'pending'})

    @api.multi
    @api.depends('lines.amount_subtotal')
    def _compute_amount_all(self):
        for invoice in self:
            total = sum(line.amount for line in invoice.lines)
            invoice.amount = total
            total_eq = sum(line.amount_subtotal for line in invoice.lines)
            invoice.amount_total = total_eq

    _sql_constraints = [
        ('unique_invoice_number', 'unique (name)', 'Invoice Number must be unique!'),
    ]

    @api.onchange('currency_id')
    def _onchange_currency_id(self):
        if self.currency_id.id:
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
            for project_invoice in self:
                project_invoice.rate = currency_rates.get(project_invoice.currency_id.id) or 1.0

    @api.depends('currency_id', 'rate', 'amount')
    def _compute_amount_rate(self):
        for project_invoice in self:
            if(project_invoice.rate and project_invoice.amount):
                project_invoice.amount_rate = project_invoice.rate * project_invoice.amount

    @api.depends('date_on_scheduled')
    def _get_date_month_on_scheduled(self):
        self.date_month_on_scheduled = dt.strptime(self.date_on_scheduled, '%Y-%m-%d').strftime('%B %Y')

    @api.depends('date_period_from','date_period_to')
    def _get_date_period(self):
        month_from = dt.strptime(self.date_period_from, '%Y-%m-%d').strftime('%B %Y')
        month_to = dt.strptime(self.date_period_to, '%Y-%m-%d').strftime('%B %Y')
        self.date_period = month_from + "-" + month_to
	    
   
	
class ProjectInvoiceLine(models.Model):
    _name = 'bdo.project.invoice.line'
    _description = "Lines of Invoice"
    _rec_name = "service_id"

    invoice_id = fields.Many2one(comodel_name='bdo.project.invoice', string='Invoice Ref', ondelete='cascade')
    service_id = fields.Many2one(comodel_name='bdo.project.service', string='Service', required=True,change_default=True)
    amount = fields.Float(string='Amount',default=1,store=True)
    amount_subtotal = fields.Float(compute='_compute_amount_line_all', digits=0, string='Total',store=True)

    _sql_constraints = [
	    ('unique_service_id', 'unique (invoice_id,service_id)', 'Service cannot multiple in this line!')
    ]
    
    @api.multi
    @api.depends('amount', 'amount_subtotal','invoice_id.rate')
    def _compute_amount_line_all(self):
        for line in self:
            line.amount = line.amount
            line.amount_subtotal = (line.invoice_id.rate or 1.0)* line.amount