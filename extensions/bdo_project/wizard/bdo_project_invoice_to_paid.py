# -*- coding: utf-8 -*-
from odoo import fields, models,api
from datetime import timedelta, datetime


class ProjectInvoice(models.TransientModel):
    _name = 'bdo.project.invoice.paid'
    _description = 'Project Invoice to Paid'

    def _default_project_invoice_id(self):
        active_id = self.env.context.get('active_id')
        if active_id:
            project = self.env['bdo.project.invoice'].browse(active_id)
            return project.id
        return False

    project_invoice_id = fields.Many2one('bdo.project.invoice', string='Project Invoice', required=True,
                                        readonly=True,store=True, default=_default_project_invoice_id)
    tax_invoice_number = fields.Char(string='No.Tax Invoice',required=True)
    date_payment_actual = fields.Date(string='Actual payment date',required=True)

    _sql_constraints = [
        ('unique_name', 'unique (tax_invoice_number )', 'No.Tax Invoice must be unique!'),
    ]


    @api.multi
    def check(self):
        self.ensure_one()
        invoice = self.env['bdo.project.invoice'].browse(self.env.context.get('active_id', False))
        project_invoice_id = invoice.id
        data = self.read()[0]
        if project_invoice_id:
            invoice.action_set_paid(data)
            return {'type': 'ir.actions.act_window_close'}
        return self.launch_set_paid()

    def launch_set_paid(self):
        return {
            'name': _('Set Invoice to Paid'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'bdo.project.invoice.paid',
            'view_id': False,
            'target': 'new',
            'views': False,
            'type': 'ir.actions.act_window',
            'context': self.env.context,
        }







