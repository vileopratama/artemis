# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools

class ReportBillingSummary(models.Model):
	_name = "report.billing.summary"
	_auto = False
	_order = 'partner_id asc'
	
	date_invoice = fields.Date(string='Invoice Date',readonly=True)
	partner_id = fields.Many2one(comodel_name='res.partner',string='Client')

	@api.model_cr
	def init(self):
		tools.drop_view_if_exists(self._cr, 'report_billing_summary')
		self._cr.execute("""
			CREATE OR REPLACE VIEW report_billing_summary AS (
				SELECT
					bp.id as id,
					bp.partner_id as partner_id,
					bp.date_engagement as date_invoice
				FROM
					bdo_project as bp
				INNER JOIN
					res_partner rp  ON (rp.id = bp.partner_id)
			)
		""")

