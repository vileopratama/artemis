# -*- coding: utf-8 -*-
from odoo import models,fields,api

class ProjectTarget(models.Model):
	_name = 'bdo.project.target'
	_order = 'period desc'
	
	period = fields.Date(string = 'Period',required = True)
	name = fields.Text(string='Description')
	state = fields.Selection(
		[('draft', 'Draft'), ('cancel', 'Cancel'),('posted', 'Posted')],'Status', readonly=True, copy=False, default='draft')
	lines = fields.One2many(comodel_name='bdo.project.target.line', inverse_name='target_id',
	                        string='Target Lines',states={'draft': [('readonly', False)]}, readonly=True, copy=True)
	amount_total = fields.Float(string='Total', digits=0,compute='_compute_amount_all',readonly=True,store=True)
	
	@api.multi
	@api.depends('lines.amount_rate')
	def _compute_amount_all(self):
		for target in self:
			total = sum(line.amount_rate for line in target.lines)
			target.amount_total = total
	
class ProjectTargetLine(models.Model):
	_name = "bdo.project.target.line"
	_description = "Lines of Project Target"
	_rec_name = "currency_id"
	
	target_id = fields.Many2one(comodel_name='bdo.project.target', string='Target Ref', ondelete='cascade')
	currency_id = fields.Many2one(comodel_name='res.currency',string='Currency',change_default=True)
	rate = fields.Float(string='Rate', digits=0)
	amount = fields.Float(digits=0, string='Amount')
	amount_rate = fields.Float(digits=0, string='Amount Total',compute='_compute_amount_line_all',readonly=True)
	
	@api.depends('rate', 'amount')
	def _compute_amount_line_all(self):
		for line in self:
			line.amount_rate = line.rate * line.amount
		
	@api.onchange('currency_id')
	def _onchange_currency_id(self):
		if self.currency_id:
			date = self._context.get('date') or fields.Datetime.now()
			company_id = self._context.get('company_id') or self.env['res.users']._get_company().id
			query = """ SELECT c.id, (SELECT r.rate FROM res_currency_rate r
			            WHERE r.currency_id = c.id AND r.name <= %s
			            AND (r.company_id IS NULL OR r.company_id = %s)
			            ORDER BY r.company_id, r.name DESC
			            LIMIT 1) AS rate
			            FROM res_currency c
			            WHERE c.id = %s
			            """
			
			self.env.cr.execute(query, (date, company_id, self.currency_id.id))
			currency_rates = dict(self._cr.fetchall())
			self._onchange_amount()
			self.rate = currency_rates.get(self.currency_id.id) or 1.0
	
	@api.onchange('amount','rate')
	def _onchange_amount(self):
		if self.currency_id:
			self.amount_rate =  self.rate * self.amount
