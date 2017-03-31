# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class CalendarEvent(models.Model):
	_inherit = 'calendar.event'
	
	proposal_id = fields.Many2one('crm.proposal', 'Proposal')
	
	@api.model
	def create(self, vals):
		event = super(CalendarEvent, self).create(vals)
		if event.proposal_id:
			event.opportunity_id.log_meeting(event.name, event.start, event.duration)
		return event
