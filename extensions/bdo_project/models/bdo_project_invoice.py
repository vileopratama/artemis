# -*- coding: utf-8 -*-
from odoo import models, fields


class ProjectInvoice(models.Model):
	_name = 'bdo.project.invoice'
	_inherit = 'bdo.project.invoice'
	
	tax_invoice = fields.Char(string='Tax Invoice Number')
	tax_invoice_file = fields.Char(string='File')
	tax_invoice_attachment = fields.Binary(string='Attachment')
	date_payment_actual = fields.Date(string='Actual payment date')
	
	def action_set_paid(self, data):
		args = {
			'state': 'paid',
			'date_payment_actual': data.get('date_actual', fields.Date.today()),
			'tax_invoice': data.get('tax_invoice_number', ''),
			'tax_invoice_file': data.get('tax_invoice_file', ''),
			'tax_invoice_attachment': data.get('tax_invoice_attachment', ''),
		}
		self.write(args)
