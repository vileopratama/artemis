# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools

class ReportBillingSummary(models.Model):
	_name = "report.billing.summary"
	_auto = False
	_order = 'partner_id asc'

	partner_id = fields.Many2one(comodel_name='res.partner',string='Client')
	service_id = fields.Many2one(comodel_name='bdo.project.service',string='Service')
	jan = fields.Integer(string='Jan',default=0,size=1)
	jan_paid = fields.Integer(string='Jan Paid',default=0,size=1)
	feb = fields.Integer(string='Feb',default=0,size=1)
	feb_paid = fields.Integer(string='Feb Paid',default=0,size=1)
	mar = fields.Integer(string='Mar',default=0,size=1)
	mar_paid = fields.Integer(string='Mar Paid',default=0,size=1)
	apr = fields.Integer(string='Apr',default=0,size=1)
	apr_paid = fields.Integer(string='Apr Paid',default=0,size=1)
	may = fields.Integer(string='May',default=0,size=1)
	may_paid = fields.Integer(string='May Paid',default=0,size=1)
	jun = fields.Integer(string='Jun',default=0,size=1)
	jun_paid = fields.Integer(string='Jun',default=0,size=1)
	jul = fields.Integer(string='Jul',default=0,size=1)
	jul_paid = fields.Integer(string='Jul Paid',default=0,size=1)
	aug = fields.Integer(string='Aug',default=0,size=1)
	aug_paid = fields.Integer(string='Aug Paid',default=0,size=1)
	sept = fields.Integer(string='Sept',default=0,size=1)
	sept_paid = fields.Integer(string='Sept Paid',default=0,size=1)
	oct = fields.Integer(string='Oct',default=0,size=1)
	oct_paid = fields.Integer(string='Oct',default=0,size=1)
	nov = fields.Integer(string='Nov',default=0,size=1)
	nov_paid = fields.Integer(string='Nov Paid',default=0,size=1)
	dec = fields.Integer(string='Dec',default=0,size=1)
	dec_paid = fields.Integer(string='Dec Paid',default=0,size=1)
	
	@api.model_cr
	def init(self):
		tools.drop_view_if_exists(self._cr, 'report_billing_summary')
		self._cr.execute("""
			CREATE OR REPLACE VIEW report_billing_summary AS (
				SELECT
					MIN(bp.partner_id) AS id,
				    bp.partner_id AS partner_id,
					bpl.service_id AS service_id,
					SUM(CASE WHEN bpi.jan_period<>0 THEN EXTRACT(MONTH FROM bpi.date_invoice) ELSE 0 END) AS jan,
                    SUM(CASE WHEN bpi.jan_period<>0 AND bpi.state='paid' THEN 1 ELSE 0 END) AS jan_paid,
                    SUM(CASE WHEN bpi.feb_period<>0 THEN EXTRACT(MONTH FROM bpi.date_invoice) ELSE 0 END) AS feb,
                    SUM(CASE WHEN bpi.feb_period<>0 AND bpi.state='paid' THEN 1 ELSE 0 END) AS feb_paid,
					SUM(CASE WHEN bpi.mar_period<>0 THEN EXTRACT(MONTH FROM bpi.date_invoice) ELSE 0 END) AS mar,
                    SUM(CASE WHEN bpi.mar_period<>0 AND bpi.state='paid 'THEN 1 ELSE 0 END) AS mar_paid,
                    SUM(CASE WHEN bpi.apr_period<>0 THEN EXTRACT(MONTH FROM bpi.date_invoice) ELSE 0 END) AS apr,
                    SUM(CASE WHEN bpi.apr_period<>0 AND bpi.state='paid' THEN 1 ELSE 0 END) AS apr_paid,
                    SUM(CASE WHEN bpi.may_period<>0 THEN EXTRACT(MONTH FROM bpi.date_invoice) ELSE 0 END) AS may,
                    SUM(CASE WHEN bpi.may_period<>0 AND bpi.state='paid' THEN 1 ELSE 0 END) AS may_paid,
                    SUM(CASE WHEN bpi.jun_period<>0 THEN EXTRACT(MONTH FROM bpi.date_invoice) ELSE 0 END) AS jun,
                    SUM(CASE WHEN bpi.jun_period<>0 AND bpi.state='paid' THEN 1 ELSE 0 END) AS jun_paid,
                    SUM(CASE WHEN bpi.jul_period<>0 THEN EXTRACT(MONTH FROM bpi.date_invoice) ELSE 0 END) AS jul,
                    SUM(CASE WHEN bpi.jun_period<>0 AND bpi.state='paid' THEN 1 ELSE 0 END) AS jul_paid,
                    SUM(CASE WHEN bpi.aug_period<>0 THEN EXTRACT(MONTH FROM bpi.date_invoice) ELSE 0 END) AS aug,
                    SUM(CASE WHEN bpi.jun_period<>0 AND bpi.state='paid' THEN 1 ELSE 0 END) AS aug_paid,
                    SUM(CASE WHEN bpi.sept_period<>0 THEN EXTRACT(MONTH FROM bpi.date_invoice) ELSE 0 END) AS sept,
                    SUM(CASE WHEN bpi.jun_period<>0 AND bpi.state='paid' THEN 1 ELSE 0 END) AS sept_paid,
                    SUM(CASE WHEN bpi.oct_period<>0 THEN EXTRACT(MONTH FROM bpi.date_invoice) ELSE 0 END) AS oct,
                    SUM(CASE WHEN bpi.jun_period<>0 AND bpi.state='paid' THEN 1 ELSE 0 END) AS oct_paid,
                    SUM(CASE WHEN bpi.nov_period<>0 THEN EXTRACT(MONTH FROM bpi.date_invoice) ELSE 0 END) AS nov,
                    SUM(CASE WHEN bpi.nov_period<>0 AND bpi.state='paid' THEN 1 ELSE 0 END) AS nov_paid,
                    SUM(CASE WHEN bpi.dec_period<>0 THEN EXTRACT(MONTH FROM bpi.date_invoice) ELSE 0 END) AS dec,
                    SUM(CASE WHEN bpi.dec_period<>0 AND bpi.state='paid' THEN 1 ELSE 0 END) AS dec_paid
				FROM
					bdo_project_invoice AS bpi
				INNER JOIN
					bdo_project_lines AS bpl ON (bpl.id = bpi.project_line_id)
				INNER JOIN
					bdo_project AS bp ON (bp.id = bpl.project_id)
				INNER JOIN
					res_partner AS rp ON (rp.id = bp.partner_id)
				GROUP BY 
					bp.partner_id,rp.name,bpl.service_id
				ORDER BY 
					rp.name ASC
			)
		""")

