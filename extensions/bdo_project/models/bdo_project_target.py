# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime as dt


class ProjectTarget(models.Model):
    _name = 'bdo.project.target'
    _order = 'date_period_start desc'

    project_line_id = fields.Many2one(comodel_name='bdo.project.lines',string='Project Code')
    date_on_scheduled = fields.Date(string='Scheduled on', required=True)
    date_period_start = fields.Date(string='From', required=True)
    date_period_end = fields.Date(string='To', required=True)
    date_period_month_total = fields.Integer(string='Total Month',readonly=True)
    year_period = fields.Char(string='Year', size=4, store=True, readonly=True)
    amount = fields.Float(string='Amount', digits=0, readonly=True, store=True)
    amount_equivalent = fields.Float(string='Amount Equivalent', digits=0, readonly=True, store=True)
    remarks = fields.Text(string='Remarks')
    state = fields.Selection(
        [('pending', 'Pending'),('received', 'Received')], 'Status', readonly=True, copy=False,
        default='pending')
    total_due = fields.Integer(string='Term of payment (days)')
    date_payment_due = fields.Date(string='Expected payment date')

    #related field
    partner_id = fields.Char(related='project_line_id.client_name',string='Name of the Company',readonly=True)
    service_id = fields.Char(related='project_line_id.service_id.name',string='Service',readonly=True)
    date_engagement = fields.Date(related='project_line_id.date_engagement', string='Date of engagement',readonly=True)
    currency_id = fields.Char(related='project_line_id.currency_id', string='Currency',readonly=True)

    def _month_betwwen(self,date_from,date_to):
        date_from = dt.strptime(date_from,"%Y-%m-%d")
        date_to = dt.strptime(date_to,"%Y-%m-%d")
        return abs((date_to - date_from).days)

    @api.onchange('date_period_start','date_period_end')
    def _onchange_date_period(self):
        if(self.date_period_start and self.date_period_end):
            self.amount = self._month_betwwen(self.date_period_start,self.date_period_end)

