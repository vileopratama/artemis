# -*- coding: utf-8 -*-
from odoo import models,fields

class ProjectInvoice(models.Model):
	_name = 'bdo.project.service'
	
	name = fields.Char(string='Service Name', required=True)
	state = fields.Selection([
		('active', 'Active'),
		('inactive', 'Inactive'),
	], string='State',default='active')
	description = fields.Text(string='Description')
	sequence = fields.Integer()