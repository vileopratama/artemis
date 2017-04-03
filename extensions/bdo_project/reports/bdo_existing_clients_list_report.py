# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools

class ExistingClientsListReport(models.Model):
	_name = "report.existing.clients.list"
	_auto = False
	_order = 'client_name asc'
	
	client_name = fields.Char(string='Company\'s Name', readonly=True)
	type = fields.Selection(
		[('recurring services', 'Recurring Services'), ('non-recurring services', 'Non-Recurring Services')],
		string='Type', readonly=True)
	source = fields.Char(string='Source', readonly=True)
	date_engagement_letter = fields.Date(string='Date of EL',readonly=True)
	el_number = fields.Char(string='No. Of EL', readonly=True)
	date_expiry_engagement_letter = fields.Date(string='Expiry of EL',readonly=True)
	currency_id = fields.Many2one(comodel_name='res.currency',string='Currency',readonly=True)
	amount_rate = fields.Float(string='Rate', digits=(16, 2), readonly=True)
	amount = fields.Float(string='Annual Fee (Original)',digits=(16,2), readonly=True)
	amount_total = fields.Float(string='Annual Fee (IDR)',digits=(16,2),readonly=True)
	employee_id = fields.Many2one(comodel_name='hr.employee', string='PIC', compute='_compute_acl', readonly=True,
								  store=True)
	date_reminder_engagement_letter = fields.Date(string='Reminder Client', readonly=True)
	remarks = fields.Text(string='Remarks')

	@api.model_cr
	def init(self):
		tools.drop_view_if_exists(self._cr, 'report_existing_clients_list')
		self._cr.execute("""
			CREATE OR REPLACE VIEW report_existing_clients_list AS (
				SELECT
					bpi.id as id,
					rp.name as client_name,
					bpel.date_engagement_letter as date_engagement_letter,
					bpel.source as source,
					bpel.name as el_number,
					bpel.date_expiry_engagement_letter as date_expiry_engagement_letter,
					bpi.currency_id as currency_id,
					bpi.rate as amount_rate,
					bpi.amount as amount,
					bpi.amount_total as amount_total,
					bpel.employee_id as employee_id,
					bpel.date_reminder_engagement_letter as date_reminder_engagement_letter,
					bpel.remarks as remarks
				FROM
					bdo_project_invoice as bpi
				INNER JOIN
					res_partner rp  ON (rp.id = bpi.partner_id)
			)
		""")

