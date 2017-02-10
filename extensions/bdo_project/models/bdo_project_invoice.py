# -*- coding: utf-8 -*-
from odoo import models,fields

class BDOProjectInvoice(models.Model):
    _name = 'bdo.project.invoice'

    number_invoice = fields.Char(string='Invoice Number',required=True)
    date_invoice = fields.Date(string='Date of Invoice', required=True)
    state = fields.Selection([
        ('process', 'On Process'),
        ('paid', 'Paid'),
    ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='process')
    partner_id = fields.Many2one(comodel_name='res.partner',string='Client')
    service  = fields.Char(string='Service',required=True)
    date_on_scheduled = fields.Date(string='On Scheduled',required=True)
    date_periode_from = fields.Date(string='Periode From', required=True)
    date_periode_to = fields.Date(string='Periode To', required=True)
    remarks = fields.Text(string='Remarks')
