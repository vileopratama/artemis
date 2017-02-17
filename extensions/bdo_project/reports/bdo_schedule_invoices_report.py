# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools

class ScheduleInvoicesReport(models.Model):
    _name = "report.schedule.invoices"
    _auto = False
    _order = 'date_on_scheduled'

    employee_id = fields.Many2one(comodel_name='hr.employee', string='PIC', readonly=True)
    partner_id = fields.Many2one(comodel_name='res.partner', string='Company\'s Name', readonly=True)
    service_id = fields.Many2one(comodel_name='bdo.project.service', string='Description', readonly=True)
    date_on_scheduled = fields.Char(string='Scheduled on', readonly=True)
    date_period = fields.Char(string='Month',readonly=True)
    date_invoice = fields.Date(string='Date of Invoice', required=True)
    no_invoice = fields.Char(string='Invoice Number', required=True)
    currency_id = currency_id = fields.Many2one(comodel_name='res.currency',string='Currency')
    amount = fields.Float(string='Amount', digits=0)
    amount_total = fields.Float(string=' (USD)', digits=0)
    remarks = fields.Text(string='Remarks')

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self._cr, 'report_schedule_invoices')
        self._cr.execute("""
            CREATE OR REPLACE VIEW report_schedule_invoices AS (
                SELECT
                    bpil.id as id,
                    bpel.employee_id,
                    bpi.partner_id as partner_id,
                    bpil.service_id as service_id,
                    CONCAT(to_char(to_timestamp(to_char(EXTRACT(MONTH FROM bpi.date_on_scheduled), '999'), 'MM'), 'Mon'),' ',EXTRACT(ISOYEAR FROM bpi.date_on_scheduled)) as date_on_scheduled,
                    bpi.date_period as date_period,
                    bpi.date_invoice as date_invoice,
                    bpi.name as no_invoice,
                    bpil.amount as amount,
                    bpil.amount_subtotal as amount_total,
                    bpi.state as state,
                    bpi.remarks as remarks
                FROM
                    bdo_project_invoice_line bpil
                INNER JOIN
                    bdo_project_invoice bpi ON (bpi.id = bpil.invoice_id)
                LEFT JOIN
                    bdo_project_engagement_letter bpel ON (bpel.invoice_id = bpi.id)
            )
        """)