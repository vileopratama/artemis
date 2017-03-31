# -*- coding: utf-8 -*-

from odoo import api, fields, models

class ProposalLost(models.TransientModel):
    _name = 'crm.proposal.lost'
    _description = 'Get Lost Reason'

    lost_reason_id = fields.Many2one('crm.proposal.lost.reason', 'Lost Reason')

    @api.multi
    def action_lost_reason_apply(self):
        proposal = self.env['crm.proposal'].browse(self.env.context.get('active_ids'))
        proposal.write({'lost_reason': self.lost_reason_id.id})
        return proposal.action_set_lost()
