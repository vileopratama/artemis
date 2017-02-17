# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools

class ListOfTaxInvoicesReport(models.Model):
    _name = "report.list.of.tax.invoices"
    _auto = False
    _order = 'partner_id asc'

    partner_id = fields.Many2one(comodel_name='res.partner', string='Company\'s Name', readonly=True)
    service_id = fields.Many2one(comodel_name='bdo.project.service', string='Services', readonly=True)
    date_period = fields.Char(string='Period',readonly=True)
    date_invoice = fields.Date(string='Date', readonly=True)
    tax_invoice_number = fields.Char(string=' No.Tax Invoice', readonly=True)
    amount_total = fields.Float(string='Amount', digits=0, store=True)
    service_code = fields.Char(related='service_id.code', string='Service Code', readonly=True)
    state = fields.Selection([ ('pending', 'Pending'),('received', 'Received')],string='Status', readonly=True)
    employee_id = fields.Many2one(comodel_name='hr.employee', string='PIC', readonly=True)

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self._cr, 'report_list_of_tax_invoices')
        self._cr.execute("""
            CREATE OR REPLACE VIEW report_list_of_tax_invoices AS (
                SELECT
                    bpil.id as id,
                    bpi.partner_id as partner_id,
                    bpil.service_id as service_id,
                    bpi.date_period as date_period,
                    bpi.date_invoice as date_invoice,
                    bpi.tax_invoice_number as tax_invoice_number,
                    bpil.amount_subtotal as amount_total,
                    bpi.state as state,
                    bpel.employee_id

                FROM
                    bdo_project_invoice_line bpil
                INNER JOIN
                    bdo_project_invoice bpi ON (bpi.id = bpil.invoice_id)
                LEFT JOIN
                    bdo_project_engagement_letter bpel ON (bpel.invoice_id = bpi.id)
            )
        """)







