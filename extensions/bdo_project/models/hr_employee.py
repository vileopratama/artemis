# -*- coding: utf-8 -*-
from odoo import models,fields

class HREmployee(models.Model):
    _inherit = 'hr.employee'
    _description = 'HR Employee'
    _order = 'initial asc'

    initial = fields.Char(string='Initial',required=True,size=3)

