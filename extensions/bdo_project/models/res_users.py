# -*- coding: utf-8 -*-
from odoo import models,fields

class ResUser(models.Model):
    _inherit = 'res.users'

    employee_id = fields.Many2one(comodel_name='hr.employee',string='Related Employee',index=True,required=True)

    _sql_constraints = [
        ('unique_employee_id', 'unique (employee_id)', 'One user only for one employee!'),
    ]