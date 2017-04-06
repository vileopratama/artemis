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
				    bp.partner_id AS partner_id,
					rp.name as client_name
					jan_period as jan,
					feb_period as feb,
					mar_period as mar,
					apr_period as apr,
					may_period as may,
					jun_period as jun,
					jul_period as jul,
					aug_period as aug,
					sept_period as sept,
					oct_period as oct,
					nov_period as nov,
					dec_period as dec
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

