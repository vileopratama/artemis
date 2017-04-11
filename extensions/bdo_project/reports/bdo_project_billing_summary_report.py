# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools

class ReportBillingSummary(models.Model):
	_name = "report.billing.summary"
	_auto = False
	_order = 'partner_id asc'

	partner_id = fields.Many2one(comodel_name='res.partner',string='Client')
	service_id = fields.Many2one(comodel_name='bdo.project.service',string='Service')
	year_invoice = fields.Char(string='Year',size=8)
	jan = fields.Integer(string='Jan',default=0,size=2)
	jan_paid = fields.Integer(string='Jan Paid',default=0,size=2)
	jan_aging = fields.Integer(string='Jan Aging', default=0, size=3)
	feb = fields.Integer(string='Feb',default=0,size=2)
	feb_paid = fields.Integer(string='Feb Paid',default=0,size=2)
	feb_aging = fields.Integer(string='Feb Aging', default=0, size=3)
	mar = fields.Integer(string='Mar',default=0,size=2)
	mar_paid = fields.Integer(string='Mar Paid',default=0,size=2)
	mar_aging = fields.Integer(string='Mar Aging', default=0, size=3)
	apr = fields.Integer(string='Apr',default=0,size=2)
	apr_paid = fields.Integer(string='Apr Paid',default=0,size=2)
	apr_aging= fields.Integer(string='Apr Aging', default=0, size=3)
	may = fields.Integer(string='May',default=0,size=2)
	may_paid = fields.Integer(string='May Paid',default=0,size=2)
	may_aging = fields.Integer(string='May Aging', default=0, size=3)
	jun = fields.Integer(string='Jun',default=0,size=2)
	jun_paid = fields.Integer(string='Jun Paid',default=0,size=2)
	jun_paid = fields.Integer(string='Jun Aging', default=0, size=3)
	jul = fields.Integer(string='Jul',default=0,size=2)
	jul_paid = fields.Integer(string='Jul Paid',default=0,size=2)
	jul_aging = fields.Integer(string='Jul Aging', default=0, size=3)
	aug = fields.Integer(string='Aug',default=0,size=2)
	aug_paid = fields.Integer(string='Aug Paid',default=0,size=2)
	aug_aging = fields.Integer(string='Aug Aging', default=0, size=3)
	sept = fields.Integer(string='Sept',default=0,size=2)
	sept_paid = fields.Integer(string='Sept Paid',default=0,size=2)
	sept_aging = fields.Integer(string='Sept Aging', default=0, size=3)
	oct = fields.Integer(string='Oct',default=0,size=2)
	oct_paid = fields.Integer(string='Oct Paid',default=0,size=2)
	oct_aging = fields.Integer(string='Oct Aging', default=0, size=3)
	nov = fields.Integer(string='Nov',default=0,size=2)
	nov_paid = fields.Integer(string='Nov Paid',default=0,size=2)
	nov_aging = fields.Integer(string='Nov Aging', default=0, size=3)
	dec = fields.Integer(string='Dec',default=0,size=2)
	dec_paid = fields.Integer(string='Dec Paid',default=0,size=2)
	dec_aging = fields.Integer(string='Dec Aging', default=0, size=3)
	
	@api.model_cr
	def init(self):
		tools.drop_view_if_exists(self._cr, 'report_billing_summary')
		self._cr.execute("""
			CREATE OR REPLACE VIEW report_billing_summary AS (
				SELECT
					MIN(bp.partner_id) AS id,
				    bp.partner_id AS partner_id,
					bpl.service_id AS service_id,
					EXTRACT(YEAR FROM bpi.date_invoice) as year_invoice,
					SUM(CASE WHEN bpi.jan_period<>0 THEN EXTRACT(MONTH FROM bpi.date_invoice) ELSE 0 END) AS jan,
                    SUM(CASE WHEN bpi.jan_period<>0 AND bpi.state='paid' THEN 1 ELSE 0 END) AS jan_paid,
                    SUM(CASE WHEN bpi.jan_period<>0 AND bpi.state<>'paid' THEN DATE_PART('day', now() - bpi.date_invoice) ELSE 0 END) AS jan_aging,
                    
                    SUM(CASE WHEN bpi.feb_period<>0 THEN EXTRACT(MONTH FROM bpi.date_invoice) ELSE 0 END) AS feb,
                    SUM(CASE WHEN bpi.feb_period<>0 AND bpi.state='paid' THEN 1 ELSE 0 END) AS feb_paid,
                    SUM(CASE WHEN bpi.feb_period<>0 AND bpi.state<>'paid' THEN DATE_PART('day', now() - bpi.date_invoice) ELSE 0 END) AS feb_aging,
                    
					SUM(CASE WHEN bpi.mar_period<>0 THEN EXTRACT(MONTH FROM bpi.date_invoice) ELSE 0 END) AS mar,
                    SUM(CASE WHEN bpi.mar_period<>0 AND bpi.state='paid 'THEN 1 ELSE 0 END) AS mar_paid,
                    SUM(CASE WHEN bpi.mar_period<>0 AND bpi.state<>'paid' THEN DATE_PART('day', now() - bpi.date_invoice) ELSE 0 END) AS mar_aging,
                    
                    SUM(CASE WHEN bpi.apr_period<>0 THEN EXTRACT(MONTH FROM bpi.date_invoice) ELSE 0 END) AS apr,
                    SUM(CASE WHEN bpi.apr_period<>0 AND bpi.state='paid' THEN 1 ELSE 0 END) AS apr_paid,
                    SUM(CASE WHEN bpi.apr_period<>0 AND bpi.state<>'paid' THEN DATE_PART('day', now() - bpi.date_invoice) ELSE 0 END) AS apr_aging,
                    
                    SUM(CASE WHEN bpi.may_period<>0 THEN EXTRACT(MONTH FROM bpi.date_invoice) ELSE 0 END) AS may,
                    SUM(CASE WHEN bpi.may_period<>0 AND bpi.state='paid' THEN 1 ELSE 0 END) AS may_paid,
                    SUM(CASE WHEN bpi.may_period<>0 AND bpi.state<>'paid' THEN DATE_PART('day', now() - bpi.date_invoice) ELSE 0 END) AS may_aging,
                    
                    SUM(CASE WHEN bpi.jun_period<>0 THEN EXTRACT(MONTH FROM bpi.date_invoice) ELSE 0 END) AS jun,
                    SUM(CASE WHEN bpi.jun_period<>0 AND bpi.state='paid' THEN 1 ELSE 0 END) AS jun_paid,
                    SUM(CASE WHEN bpi.jun_period<>0 AND bpi.state<>'paid' THEN DATE_PART('day', now() - bpi.date_invoice) ELSE 0 END) AS jun_aging,
                    
                    SUM(CASE WHEN bpi.jul_period<>0 THEN EXTRACT(MONTH FROM bpi.date_invoice) ELSE 0 END) AS jul,
                    SUM(CASE WHEN bpi.jul_period<>0 AND bpi.state='paid' THEN 1 ELSE 0 END) AS jul_paid,
                    SUM(CASE WHEN bpi.jul_period<>0 AND bpi.state<>'paid' THEN DATE_PART('day', now() - bpi.date_invoice) ELSE 0 END) AS jul_aging,
                    
                    SUM(CASE WHEN bpi.aug_period<>0 THEN EXTRACT(MONTH FROM bpi.date_invoice) ELSE 0 END) AS aug,
                    SUM(CASE WHEN bpi.aug_period<>0 AND bpi.state='paid' THEN 1 ELSE 0 END) AS aug_paid,
                    SUM(CASE WHEN bpi.aug_period<>0 AND bpi.state<>'paid' THEN DATE_PART('day', now() - bpi.date_invoice) ELSE 0 END) AS aug_aging,
                    
                    SUM(CASE WHEN bpi.sept_period<>0 THEN EXTRACT(MONTH FROM bpi.date_invoice) ELSE 0 END) AS sept,
                    SUM(CASE WHEN bpi.sept_period<>0 AND bpi.state='paid' THEN 1 ELSE 0 END) AS sept_paid,
                    SUM(CASE WHEN bpi.sept_period<>0 AND bpi.state<>'paid' THEN DATE_PART('day', now() - bpi.date_invoice) ELSE 0 END) AS sept_aging,
                    
                    SUM(CASE WHEN bpi.oct_period<>0 THEN EXTRACT(MONTH FROM bpi.date_invoice) ELSE 0 END) AS oct,
                    SUM(CASE WHEN bpi.oct_period<>0 AND bpi.state='paid' THEN 1 ELSE 0 END) AS oct_paid,
                    SUM(CASE WHEN bpi.oct_period<>0 AND bpi.state<>'paid' THEN DATE_PART('day', now() - bpi.date_invoice) ELSE 0 END) AS oct_aging,
                    
                    SUM(CASE WHEN bpi.nov_period<>0 THEN EXTRACT(MONTH FROM bpi.date_invoice) ELSE 0 END) AS nov,
                    SUM(CASE WHEN bpi.nov_period<>0 AND bpi.state='paid' THEN 1 ELSE 0 END) AS nov_paid,
                    SUM(CASE WHEN bpi.nov_period<>0 AND bpi.state<>'paid' THEN DATE_PART('day', now() - bpi.date_invoice) ELSE 0 END) AS nov_aging,
                    
                    SUM(CASE WHEN bpi.dec_period<>0 THEN EXTRACT(MONTH FROM bpi.date_invoice) ELSE 0 END) AS dec,
                    SUM(CASE WHEN bpi.dec_period<>0 AND bpi.state='paid' THEN 1 ELSE 0 END) AS dec_paid,
					SUM(CASE WHEN bpi.dec_period<>0 AND bpi.state<>'paid' THEN DATE_PART('day', now() - bpi.date_invoice) ELSE 0 END) AS dec_aging
					
				FROM
					bdo_project_invoice AS bpi
				INNER JOIN
					bdo_project_lines AS bpl ON (bpl.id = bpi.project_line_id)
				INNER JOIN
					bdo_project AS bp ON (bp.id = bpl.project_id)
				INNER JOIN
					res_partner AS rp ON (rp.id = bp.partner_id)
				GROUP BY 
					bp.partner_id,rp.name,bpl.service_id,EXTRACT(YEAR FROM bpi.date_invoice)
				ORDER BY 
					rp.name ASC,EXTRACT(YEAR FROM bpi.date_invoice) ASC
			)
		""")

