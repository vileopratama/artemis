# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools

class ProjectSummaryReport(models.Model):
	_name = "report.project.summary"
	_description = "Project Summary"
	_auto = False
	_order = 'date_period asc'
	
	date_period = fields.Date(string='Date Period', readonly=True)
	total_target = fields.Float(string='Total Target', readonly=True)
	total_amount = fields.Float(string='Total Amount', readonly=True)
	
	@api.model_cr
	def init(self):
		tools.drop_view_if_exists(self._cr, 'report_project_summary')
		self._cr.execute("""
			CREATE OR REPLACE VIEW report_project_summary AS (
				SELECT
					MIN(bpt.id) as id,
					bpt.date_period as date_period,
					bpt.amount_total as total_target,
					(SELECT
						SUM(bpi.amount_total)
					FROM
						bdo_project_invoice bpi
					WHERE
						EXTRACT(MONTH FROM bpi.date_invoice) = EXTRACT(MONTH FROM bpt.date_period)
					AND
						EXTRACT(YEAR FROM bpi.date_invoice) = EXTRACT(YEAR FROM bpt.date_period)
					) as total_amount
				FROM
					bdo_project_target as bpt
				GROUP BY
					bpt.id
		    )
		""")