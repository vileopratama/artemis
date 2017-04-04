# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools

class ReportBillingSummary(models.Model):
	_name = "report.billing.summary"
	_auto = False
	_order = 'partner_id asc'

	partner_id = fields.Many2one(comodel_name='res.partner',string='Client')

	@api.model_cr
	def init(self):
		tools.drop_view_if_exists(self._cr, 'report_billing_summary')
		self._cr.execute("""
			CREATE OR REPLACE VIEW report_billing_summary AS (
				SELECT
					bpi.id AS id,
				    bp.partner_id AS partner_id
				FROM
					bdo_project_invoice AS bpi
				INNER JOIN
					bdo_project_lines AS bpl ON (bpl.id = bpi.project_line_id)
				INNER JOIN
					bdo_project AS bp ON (bp.id = bpl.project_id)
				INNER JOIN
					res_partner AS rp ON (rp.id = bp.partner_id)
				ORDER BY rp.name ASC
			)
		""")

