# -*- coding: utf-8 -*-

from odoo import fields, models

class view(models.Model):
    _inherit = 'ir.ui.view'

    type = fields.Selection([
        ('tree', 'Tree'),
        ('form', 'Form'),
        ('graph', 'Graph'),
        ('pivot', 'Pivot'),
        ('calendar', 'Calendar'),
        ('diagram', 'Diagram'),
        ('gantt', 'Gantt'),
        ('kanban', 'Kanban'),
        ('sales_team_dashboard', 'Sales Team Dashboard'),
        ('search', 'Search'),
        ('xchart', 'Xchart'),
        ('qweb', 'QWeb')], string='View Type'
)