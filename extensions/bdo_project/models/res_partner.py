# -*- coding: utf-8 -*-
from odoo import api, fields, models

class ResPartner(models.Model):
	_inherit = 'res.partner'
	
	project_count = fields.Integer("Project", compute='_compute_project_count')
	
	@api.multi
	def _compute_project_count(self):
		for partner in self:
			operator = 'child_of' if partner.is_company else '='
			partner.project_count = self.env['bdo.project'].search_count(
				[('partner_id', operator, partner.id)])
