# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime as dt
import math


class ProjectTarget(models.Model):
    _name = 'bdo.project.target'
    _order = 'date_period_start desc'

    project_line_id = fields.Many2one(comodel_name='bdo.project.lines',string='Project Code',required=True)
    employee_id = fields.Many2one(comodel_name='hr.employee',string='PIC',readonly=True,
                                  default=lambda self: self.env.user.employee_id.id)
    user_id = fields.Many2one(comodel_name='res.users',default=lambda self: self.env.user.id,string='PIC',
                              readonly=True)
    date_on_scheduled = fields.Date(string='Scheduled on', required=True)
    date_period_start = fields.Date(string='From', required=True)
    date_period_end = fields.Date(string='To', required=True)
    date_period_month_total = fields.Integer(compute='_compute_period_month_total',string='Total Month',readonly=True,store=True)
    year_period = fields.Char(string='Year', size=4, store=True, readonly=True)
    amount = fields.Float(compute='_compute_period_month_total',string='Amount',readonly=True, store=True,digits=(16, 2))
    amount_equivalent = fields.Float(compute='_compute_period_month_total',string='Amount Equivalent', readonly=True, store=True,digits=(16, 2))
    remarks = fields.Text(string='Remarks')
    state = fields.Selection(
        [('draft', 'Draft'),('invoice', 'Invoice'),('paid','Paid')], 'Status', readonly=True, copy=False,
        default='draft')
    total_due = fields.Integer(string='Term of payment (days)')
    date_payment_due = fields.Date(compute=' _compute_date_due',string='Expected payment date',readonly=True,store=True)
    date_payment_actual = fields.Date(string='Actual payment date', readonly=True,store=True)

    #related field
    partner_id = fields.Char(related='project_line_id.client_name',string='Name of the Company',readonly=True)
    service_id = fields.Char(related='project_line_id.service_id.name',string='Service',readonly=True)
    date_engagement = fields.Date(related='project_line_id.date_engagement', string='Date of engagement',readonly=True)
    currency_id = fields.Char(related='project_line_id.currency_id', string='Currency',readonly=True)
    amount_project_total = fields.Float(related='project_line_id.amount', string='Amount Project',readonly=True)
    amount_project_equivalent = fields.Float(related='project_line_id.amount_equivalent', string='Amount Project Equivalent', readonly=True)

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            name = record.partner_id + ' > ' + record.service_id
            result.append((record.id, name))
        return result

    @api.multi
    @api.depends('date_period_start','date_period_end','project_line_id')
    def _compute_period_month_total(self):
        koef = 0.0833333333333333
        for target in self:
            if target.project_line_id and target.date_period_start and target.date_period_end:
                month_total = self._month_between(target.date_period_start, target.date_period_end)
                target.date_period_month_total = month_total
                target.amount = (koef * month_total) * target.amount_project_total
                target.amount_equivalent = (koef * month_total) * target.amount_project_total


    def _month_between(self,date_from,date_to):
        date_from = dt.strptime(date_from,"%Y-%m-%d")
        date_to = dt.strptime(date_to,"%Y-%m-%d")
        total_days =  abs((date_to - date_from).days)
        if(total_days > 0):
            return math.ceil(total_days/30)
        else:
            return 0

    @api.onchange('date_period_start','date_period_end','project_line_id')
    def _onchange_date_period(self):
        koef = 0.0833333333333333
        for target in self:
            if target.project_line_id and target.date_period_start and target.date_period_end:
                month_total = self._month_between(target.date_period_start, target.date_period_end)
                target.date_period_month_total = month_total
                target.amount = (koef * month_total) * target.amount_project_total
                target.amount_equivalent = (koef * month_total) * target.amount_project_total

