# -*- coding: utf-8 -*-
from odoo import models,fields


class ProjectInvoice(models.Model):
    _name = 'bdo.project.invoice'

    tax_invoice = fields.Char(string='Tax Invoice Number', required=True)








