# -*- coding: utf-8 -*-
import logging
from odoo import fields, models, api

_logger = logging.getLogger(__name__)


class Proposal(models.Model):
    _name = "crm.proposal"
    _inherit = ['mail.thread']
    _description = "CRM/Proposal"
    _order = "date_create asc"

    def _get_currency(self):
        currency = False
        if self.env.user.company_id.currency_id.id:
            currency = self.env.user.company_id.currency_id.id
        return currency

    name = fields.Char(string='Proposal No', required=True, index=True)
    date_create = fields.Datetime(string='Create Date')
    partner_id = fields.Many2one(comodel_name='res.partner', string='Client', track_visibility='onchange', index=True,
                                 help="Linked partner (optional). Usually created when converting the lead.")
    date_end = fields.Datetime(string='Year End')
    currency_id = fields.Many2one(comodel_name='res.currency', string='Currency', required=True, index=True,
                                  default=_get_currency)
    total_amount = fields.Float(string='Total Amount', track_visibility='always')
    description = fields.Text(string='Description')
    stage_id = fields.Many2one(comodel_name='crm.stage', string='Stage', track_visibility='onchange', index=True)
    activity_count = fields.Integer(string='# Activity', compute='_compute_activity_count')

    @api.multi
    def _compute_activity_count(self):
        activity_data = self.env['calendar.event'].read_group([('proposal_id', 'in', self.ids)], ['proposal_id'],
                                                             ['proposal_id'])
        mapped_data = {m['proposal_id'][0]: m['proposal_id_count'] for m in activity_data}
        for activity in self:
            activity.meeting_count = mapped_data.get(activity.id, 0)