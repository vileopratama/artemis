# -*- coding: utf-8 -*-
from odoo import models,fields,api

class Project(models.Model):
	_name = 'bdo.project'
	_order = 'code asc'
	_description = 'BDO Project'
	
	def _get_currency(self):
		currency = False
		if self.env.user.company_id.currency_id.id:
			currency = self.env.user.company_id.currency_id.id
		return currency
	
	code = fields.Char(string='Project Code',size=60,help='This Project Code can reference to Timesheeet Project Code')
	partner_id = fields.Many2one(comodel_name='res.partner', string='Client', required=True, index=True)
	type = fields.Selection([('recurring services', 'Recurring Services'),('non-recurring services', 'Non-Recurring Services')],
	                        string='Type', default='recurring services')
	source = fields.Selection([('local', 'Local'), ('global', 'Global')], string='Project', default='local')
	date_engagement = fields.Date(string='Date of engagement', index=True, default=fields.Datetime.now)
	name = fields.Char(string='No. Of EL', size=60)
	date_expiry_engagement = fields.Date(string='Expiry date', index=True, default=fields.Datetime.now)
	currency_id = fields.Many2one(comodel_name='res.currency', string='Currency', required=True, index=True,default=_get_currency)
	conflict_check = fields.Selection([('yes', 'Yes'), ('no', 'No')],string='Conflict Check', default='no')
	lines = fields.One2many(comodel_name='bdo.project.lines', inverse_name='project_id',string='Project Lines')
	amount_total = fields.Float(string='Amount Total',readonly=True,store=True)
	rate = fields.Float(string='Rate')
	amount_equivalent = fields.Float(string='Amount Total Equiv',readonly=True,store=True)
	employee_id = fields.Many2one(comodel_name='hr.employee', string='PIC', compute='_compute_acl', readonly=True,store=True)
	date_reminder = fields.Date(string='Reminder Date', index=True, default=fields.Datetime.now)
	employees = fields.One2many('bdo.project.employees', inverse_name='project_id', string='Team Member')
	remarks = fields.Text(string='Remarks')
	attachment_ids = fields.Many2many(comodel_name='ir.attachment', string='Attachments')
	state = fields.Selection([('active', 'Active'), ('inactive', 'In-Active')], 'Status', readonly=True,default='active')
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
	
	_sql_constraints = [
		('unique_code', 'unique (code)', 'Project code must be unique!'),
	]
	
	@api.multi
	@api.depends('lines.amount_equivalent')
	def _compute_amount_all(self):
		for project in self:
			total = sum(line.amount for line in project.lines)
			#total amount original currency
			project.amount = total
			#total amount equiv currency
			total_equiv = sum(line.amount_equivalent for line in project.lines)
			project.amount_equivalent = total_equiv
	
	@api.onchange('currency_id')
	def _onchange_currency_id(self):
		if self.currency_id:
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
			for project in self:
				project.rate = currency_rates.get(project.currency_id.id) or 1.0
	
	@api.depends('currency_id','rate')
	def _compute_amount_rate(self):
		for project in self:
			if (project.rate and project.currency_id):
				project.amount_equivalent = project.rate * project.amount_total

	@api.multi
	@api.depends('employees.employee_id')
	def _compute_acl(self):
		for el in self:
			for line in el.employees:
				if line.acl == 'in-charge':
					el.employee_id = line.employee_id
	
	@api.multi
	def set_active(self):
		return self.write({'state': 'active'})
	
	@api.multi
	def set_inactive(self):
		return self.write({'state': 'inactive'})
					
class ProjectLines(models.Model):
    _name = 'bdo.project.lines'
    _description = "Project Line Invoice"
    _rec_name = "service_id"

    project_id = fields.Many2one(comodel_name='bdo.project', string='Project Ref', ondelete='cascade')
    service_id = fields.Many2one(comodel_name='bdo.project.service', string='Service', required=True,change_default=True)
    amount = fields.Float(string='Amount',default=1,store=True)
    amount_equivalent = fields.Float(digits=0, string='Total',store=True,readonly=True)

    @api.multi
    @api.depends('amount','project_id.rate')
    def _compute_amount_line_all(self):
	    for line in self:
		    line.amount = line.amount
		    line.amount_equivalent = (line.project_id.rate or 1.0) * line.amount
			
class ProjectEmployees(models.Model):
	_name = "bdo.project.employees"
	_description = "Employee of Project"
	_rec_name = "employee_id"
	
	project_id = fields.Many2one(comodel_name='bdo.project', string='Employee Ref', ondelete='cascade')
	employee_id = fields.Many2one(comodel_name='hr.employee', string='Employee',required=True,change_default=True)
	acl = fields.Selection([('in-charge', 'In Charge'), ('assistant', 'Assistant')], string='Access Control List')