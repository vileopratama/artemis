# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools

class ExistingClientsListReport(models.Model):
	_name = "report.existing.clients.list"
	_auto = False
	_order = 'client_name asc'
	
	client_name = fields.Char(string='Company\'s Name', readonly=True)
	source = fields.Char(string='Source', readonly=True)
	el_number = fields.Char(string='No. Of EL', readonly=True)
	amount_total = fields.Float(string='Revenue (IDR)', readonly=True)
	
	@api.model_cr
	def init(self):
		tools.drop_view_if_exists(self._cr, 'report_existing_clients_list')
		self._cr.execute("""
			CREATE OR REPLACE VIEW report_existing_clients_list AS (
				SELECT
					bpi.id as id,
					rp.name as client_name,
					bpel.source as source,
					bpel.name as el_number,
					bpi.amount_total as amount_total
				FROM
					bdo_project_invoice as bpi
				INNER JOIN
					res_partner rp  ON (rp.id = bpi.partner_id)
				INNER JOIN
					bdo_project_engagement_letter bpel ON (bpel.invoice_id = bpi.id)
			)
		""")