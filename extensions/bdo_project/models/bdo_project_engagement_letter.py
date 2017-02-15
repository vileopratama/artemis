# -*- coding: utf-8 -*-
from odoo import models,fields,api

class ProjectEngagementLetter(models.Model):
	_name = 'bdo.project.engagement.letter'
	
	name = fields.Char(string='No. Of EL',size=50)
	state = fields.Selection([('draft', 'New'), ('cancel', 'Cancelled'),  ('done', 'Posted')],'Status', readonly=True,
	                         copy=False, default='draft')
	source = fields.Selection([('local','Local'),('global','Global')],string='Project',default='local')
	date_engagement_letter = fields.Date(string='Date of engagement',index=True,default=fields.Datetime.now)
	date_expiry_engagement_letter = fields.Date(string='Expiry date', index=True, default=fields.Datetime.now)
	date_reminder_engagement_letter = fields.Date(string='Reminder Date', index=True,default=fields.Datetime.now)
	type = fields.Selection([('recurring services', 'Recurring Services'),('non-recurring services', 'Non-Recurring Services')],
	                        string='Type', default='recurring services')
	invoice_id = fields.Many2one(comodel_name='bdo.project.invoice',string='Invoice',required=True, index=True)
	client_name = fields.Char(related='invoice_id.partner_id.name',string='Company\'s name', store=False)
	currency = fields.Char(related='invoice_id.currency_id.name', string='Currency', store=False)
	amount = fields.Float(related='invoice_id.amount', string='Amount', store=False)
	rate = fields.Float(related='invoice_id.rate', string='Rate', store=False,digit=0)
	amount_eq = fields.Float(related='invoice_id.amount_total', string='Amount Total', store=False, digit=0)
	remarks = fields.Text(string='Remarks')
	employees = fields.One2many('bdo.project.engagement.letter.employees',inverse_name='engagement_letter_id', string='EL Lines',
	                            copy=True)
	invoices = fields.One2many(related='invoice_id.lines',string='Invoice Lines',readonly=True)
	employee_id = fields.Many2one(comodel_name='hr.employee', string='PIC', compute='_compute_acl', readonly=True, store=True)
	
	@api.multi
	@api.depends('employees.employee_id')
	def _compute_acl(self):
		for el in self:
			for line in el.employees:
				if line.acl == 'in-charge':
					el.employee_id = line.employee_id
			
class ProjectEngagementLetterEmployees(models.Model):
	_name = "bdo.project.engagement.letter.employees"
	_description = "Employee of Project"
	_rec_name = "employee_id"
	
	engagement_letter_id = fields.Many2one(comodel_name='bdo.project.engagement.letter', string='Employee Ref', ondelete='cascade')
	employee_id = fields.Many2one(comodel_name='hr.employee', string='Employee',required=True,change_default=True)
	acl = fields.Selection([('in-charge', 'In Charge'), ('assistant', 'Assistant')], string='Access Control List')