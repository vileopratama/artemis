# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    project_count = fields.Integer("Project", compute='_compute_project_count')
    invoice_count = fields.Integer("Invoice", compute='_compute_invoice_count')

    @api.multi
    def _compute_project_count(self):
        for partner in self:
            operator = 'child_of' if partner.is_company else '='
            partner.project_count = self.env['bdo.project'].search_count(
                [('partner_id', operator, partner.id)])

    @api.multi
    def _compute_invoice_count(self):
        for partner in self:
            partner.invoice_count = self.env['bdo.project.invoice'].search_count(
                [('partner_id', '=', partner.name)])
