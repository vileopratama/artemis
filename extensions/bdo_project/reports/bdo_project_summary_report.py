# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools


class ProjectSummaryReport(models.Model):
    _name = "report.project.summary"
    _description = "Project Summary"
    _auto = False
    _order = 'year_invoice asc'

    year_invoice = fields.Char(string='Year', readonly=True)
    total_target = fields.Float(string='Total Target', readonly=True)
    total_pending = fields.Float(string='Total Pending', readonly=True)
    total_paid = fields.Float(string='Total Paid', readonly=True)

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self._cr, 'report_project_summary')
        self._cr.execute("""
			CREATE OR REPLACE VIEW report_project_summary AS (
				SELECT
					MIN(bpi.id) as id,
					date_part('year',bpi.date_invoice) AS year_invoice,
					SUM(amount_equivalent) as total_target,
					SUM(CASE WHEN state <> 'paid' THEN amount_equivalent ELSE 0 END) as total_pending,
					SUM(CASE WHEN state = 'paid' THEN amount_equivalent ELSE 0 END) as total_paid
				FROM
					bdo_project_invoice as bpi
				GROUP BY
					EXTRACT(YEAR FROM bpi.date_invoice)
		    )
		""")
