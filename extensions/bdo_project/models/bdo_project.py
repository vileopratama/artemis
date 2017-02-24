# -*- coding: utf-8 -*-
from odoo import models,fields,api

class Project(models.Model):
	_name = 'bdo.project'
	_order = 'code asc'
	_description = 'BDO Project'
	
	code = fields.Char(string='Project Code',size=60,help='This Project Code can reference to Timesheeet Project Code')
	partner_id = fields.Many2one(comodel_name='res.partner', string='Client', required=True, index=True)
	type = fields.Selection([('recurring services', 'Recurring Services'),('non-recurring services', 'Non-Recurring Services')],
	                        string='Type', default='recurring services')
	source = fields.Selection([('local', 'Local'), ('global', 'Global')], string='Project', default='local')
	date_engagement = fields.Date(string='Date of engagement', index=True, default=fields.Datetime.now)
	name = fields.Char(string='No. Of EL', size=60)
	date_expiry_engagement = fields.Date(string='Expiry date', index=True, default=fields.Datetime.now)
	currency_id = fields.Many2one(comodel_name='res.currency', string='Currency', required=True, index=True)
	conflict_check = fields.Selection([('yes', 'Yes'), ('no', 'No')],string='Conflict Check', default='no')
	lines = fields.One2many(comodel_name='bdo.project.lines', inverse_name='project_id', index=True,string='Project Lines',copy=True)
	amount_total = fields.Float(string='Amount Total')
	rate = fields.Float(string='Rate')
	amount_equivalent = fields.Float(string='Amount Total Equiv')
	employee_id = fields.Many2one(comodel_name='hr.employee', string='PIC', compute='_compute_acl', readonly=True,store=True)
	date_reminder = fields.Date(string='Reminder Date', index=True, default=fields.Datetime.now)
	employees = fields.One2many('bdo.project.employees', inverse_name='project_id', string='Team Member')
	remarks = fields.Text(string='Remarks')
	attachment_ids = fields.Many2many(comodel_name='ir.attachment', string='Attachments')
	#state = fields.Selection([('draft', 'New'), ('cancel', 'Cancelled'),  ('done', 'Posted')],'Status', readonly=True,
	                         #copy=False, default='draft')
	
	#
	#
	#date_reminder_engagement_letter = fields.Date(string='Reminder Date', index=True,default=fields.Datetime.now)
	#
	#
    #
	#
    #rate = fields.Float(string='Rate')
    #remarks = fields.Text(string='Remarks')
    #employees = fields.One2many('bdo.project.engagement.letter.employees', inverse_name='project_id', string='EL Lines')
    #client_name = fields.Char(related='invoice_id.partner_id.name',string='Company\'s name', store=False)
    #amount = fields.Float(related='invoice_id.amount', string='Amount', store=False)
	#rate = fields.Float(related='invoice_id.rate', string='Rate', store=False,digit=0)
	#amount_eq = fields.Float(related='invoice_id.amount_total', string='Amount Total', store=False, digit=0,copy=True)
	#invoices = fields.One2many(related='invoice_id.lines',string='Invoice Lines',readonly=True)

	@api.multi
	@api.depends('employees.employee_id')
	def _compute_acl(self):
		for el in self:
			for line in el.employees:
				if line.acl == 'in-charge':
					el.employee_id = line.employee_id
					
class ProjectLines(models.Model):
    _name = 'bdo.project.lines'
    _description = "Project Line Invoice"
    _rec_name = "service_id"

    project_id = fields.Many2one(comodel_name='bdo.project', string='Project Ref', ondelete='cascade')
    service_id = fields.Many2one(comodel_name='bdo.project.service', string='Service', required=True,change_default=True)
    amount = fields.Float(string='Amount',default=1,store=True)
    amount_equivalent = fields.Float(digits=0, string='Total',store=True)
			
class ProjectEmployees(models.Model):
	_name = "bdo.project.employees"
	_description = "Employee of Project"
	_rec_name = "employee_id"
	
	project_id = fields.Many2one(comodel_name='bdo.project', string='Employee Ref', ondelete='cascade')
	employee_id = fields.Many2one(comodel_name='hr.employee', string='Employee',required=True,change_default=True)
	acl = fields.Selection([('in-charge', 'In Charge'), ('assistant', 'Assistant')], string='Access Control List')