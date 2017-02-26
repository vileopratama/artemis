# -*- coding: utf-8 -*-
from odoo import fields, models,api
from datetime import timedelta, datetime


class ProjectInvoice(models.TransientModel):
    _name = 'bdo.project.invoice.logs'
    _description = 'Project Target to Invoice Logs'

    def _default_project_invoice_id(self):
        active_id = self.env.context.get('active_id')
        if active_id:
            project = self.env['bdo.project.invoice'].browse(active_id)
            return project.id
        return False

    project_invoice_id = fields.Many2one('bdo.project.invoice', string='Project Target', required=True,
                                        readonly=True,store=True, default=_default_project_invoice_id)
    name = fields.Char(string='Invoice No',required=True)
    date_invoice = fields.Date(string='Invoice Date',required=True)
    total_due = fields.Integer(string='Term of payment (days)',required=True)
    date_payment_due = fields.Date(compute='_compute_date_due', string='Expected payment date',
                                   readonly=True, store=True)

    _sql_constraints = [
        ('unique_name', 'unique (name)', 'Invoice number must be unique!'),
    ]

    def _calculate_date_payment_due(self,invoice_date,total_due):
        date_object = datetime.strptime(invoice_date, '%Y-%m-%d')
        return date_object + timedelta(days=total_due)

    @api.onchange('total_due')
    def onchange_total_due(self):
        for invoice in self:
            if invoice.date_invoice and invoice.total_due:
                invoice.date_payment_due = invoice._calculate_date_payment_due(invoice.date_invoice,invoice.total_due)

    @api.multi
    @api.depends('total_due')
    def _compute_date_due(self):
        for invoice in self:
            if invoice.date_invoice and invoice.total_due:
                invoice.date_payment_due = invoice._calculate_date_payment_due(invoice.date_invoice,invoice.total_due)

    @api.multi
    def check(self):
        self.ensure_one()
        target = self.env['bdo.project.invoice'].browse(self.env.context.get('active_id', False))
        project_target_id = target.id
        data = self.read()[0]
        if project_target_id:
            target.action_set_invoice(data)
            return {'type': 'ir.actions.act_window_close'}
        return self.launch_set_invoice()

    def launch_set_invoice(self):
        return {
            'name': _('Set Invoice'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'bdo.project.invoice.logs',
            'view_id': False,
            'target': 'new',
            'views': False,
            'type': 'ir.actions.act_window',
            'context': self.env.context,
        }







