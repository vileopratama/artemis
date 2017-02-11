# -*- coding: utf-8 -*-
from odoo import models,fields,api

class ProjectInvoice(models.Model):
    _name = 'bdo.project.invoice'

    def _get_currency(self):
        currency = False
        if self.env.user.company_id.currency_id.id:
            currency = self.env.user.company_id.currency_id.id
        return currency
            
    number_invoice = fields.Char(string='Invoice Number',required=True)
    date_invoice = fields.Date(string='Date of Invoice', required=True)
    state = fields.Selection([
        ('pending', 'Pending'),
        ('received', 'Received'),
    ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='pending')
    partner_id = fields.Many2one(comodel_name='res.partner',string='Client')
    service_id  = fields.Many2one(comodel_name='bdo.project.service',string='Service',required=True)
    date_on_scheduled = fields.Date(string='On Scheduled',required=True)
    date_periode_from = fields.Date(string='Periode From', required=True)
    date_periode_to = fields.Date(string='Periode To', required=True)
    remarks = fields.Text(string='Remarks')
    attachment_ids = fields.Many2many(comodel_name='ir.attachment', string='Attachments')
    currency_id = fields.Many2one(comodel_name='res.currency',string='Currency',default=_get_currency,
                                  help='The optional other currency if it is a multi-currency entry.')
    rate = fields.Float(string='Current Rate',digits=(12, 2),
                        help='The rate of the currency to the currency of rate 1.')
    amount = fields.Monetary(string='Amount',default=0.0)
    amount_rate = fields.Float(compute='_compute_amount_rate' ,digits=(12, 2),string='Amount Rate',readonly=True)

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
            