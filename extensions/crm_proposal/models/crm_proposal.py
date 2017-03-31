# -*- coding: utf-8 -*-
import logging
from odoo import fields, models, api, SUPERUSER_ID
from odoo.addons.crm.models import crm_stage

_logger = logging.getLogger(__name__)


class Proposal(models.Model):
	_name = "crm.proposal"
	_inherit = ['mail.thread']
	_description = "CRM/Proposal"
	_order = "date_create asc"
	
	def _default_probability(self):
		stage_id = self._default_stage_id()
		if stage_id:
			return self.env['crm.stage'].browse(stage_id).probability
		return 10
	
	def _default_stage_id(self):
		team = self.env['crm.team'].sudo()._get_default_team_id(user_id=self.env.uid)
		return self._stage_find(team_id=team.id, domain=[('fold', '=', False)]).id
	
	def _get_currency(self):
		currency = False
		if self.env.user.company_id.currency_id.id:
			currency = self.env.user.company_id.currency_id.id
		return currency
	
	name = fields.Char(string='Proposal No', required=True, index=True)
	active = fields.Boolean('Active', default=True)
	priority = fields.Selection(crm_stage.AVAILABLE_PRIORITIES,
	                            string='Rating', index=True,
	                            default=crm_stage.AVAILABLE_PRIORITIES[0][0])
	date_create = fields.Datetime(string='Create Date')
	partner_id = fields.Many2one(comodel_name='res.partner', string='Client', track_visibility='onchange', index=True,
	                             help="Linked partner (optional). Usually created when converting the lead.")
	team_id = fields.Many2one(comodel_name='crm.team', string='Sales Team', oldname='section_id',
	                          default=lambda self: self.env['crm.team'].sudo()._get_default_team_id(
		                          user_id=self.env.uid),
	                          index=True, track_visibility='onchange',
	                          help='When sending mails, the default email address is taken from the sales team.')
	date_end = fields.Date(string='Year End')
	date_follow_up = fields.Date(string='Year Follow Up')
	currency_id = fields.Many2one(comodel_name='res.currency', string='Currency', required=True, index=True,
	                              default=_get_currency)
	total_amount = fields.Float(string='Total Amount', track_visibility='always')
	description = fields.Text(string='Description')
	stage_id = fields.Many2one(comodel_name='crm.stage', string='Stage', track_visibility='onchange', index=True,
	                           group_expand='_read_group_stage_ids', default=lambda self: self._default_stage_id())
	probability = fields.Float('Probability', group_operator="avg", default=lambda self: self._default_probability())
	activity_count = fields.Integer(string='# Activity', compute='_compute_activity_count')
	color = fields.Integer(string='Color Index', default=0)
	lost_reason = fields.Many2one('crm.proposal.lost.reason', string='Lost Reason', index=True, track_visibility='onchange')
	user_id = fields.Many2one('res.users', string='PIC', index=True, track_visibility='onchange',
	                          default=lambda self: self.env.user)
	
	_sql_constraints = [
		('check_probability', 'check(probability >= 0 and probability <= 100)',
		 'The probability of closing the deal should be between 0% and 100%!')
	]
	
	@api.multi
	def _compute_activity_count(self):
		activity_data = self.env['calendar.event'].read_group([('proposal_id', 'in', self.ids)], ['proposal_id'],
		                                                      ['proposal_id'])
		mapped_data = {m['proposal_id'][0]: m['proposal_id_count'] for m in activity_data}
		for activity in self:
			activity.meeting_count = mapped_data.get(activity.id, 0)
	
	@api.model
	def _read_group_stage_ids(self, stages, domain, order):
		team_id = self._context.get('default_team_id')
		if team_id:
			search_domain = ['|', ('id', 'in', stages.ids), '|', ('team_id', '=', False), ('team_id', '=', team_id)]
		else:
			search_domain = ['|', ('id', 'in', stages.ids), ('team_id', '=', False)]
		
		# perform search
		stage_ids = stages._search(search_domain, order=order, access_rights_uid=SUPERUSER_ID)
		return stages.browse(stage_ids)
	
	def _stage_find(self, team_id=False, domain=None, order='sequence'):
		team_ids = set()
		if team_id:
			team_ids.add(team_id)
		for proposal in self:
			if proposal.team_id:
				team_ids.add(proposal.team_id.id)
		# generate the domain
		if team_ids:
			search_domain = ['|', ('team_id', '=', False), ('team_id', 'in', list(team_ids))]
		else:
			search_domain = [('team_id', '=', False)]
		# AND with the domain in parameter
		if domain:
			search_domain += list(domain)
		# perform search, return the first found
		return self.env['crm.stage'].search(search_domain, order=order, limit=1)
	
	@api.multi
	def close_dialog(self):
		return {'type': 'ir.actions.act_window_close'}
	
	@api.multi
	def action_set_active(self):
		return self.write({'active': True})
	
	@api.multi
	def action_set_unactive(self):
		return self.write({'active': False})
	
	@api.multi
	def action_set_won(self):
		""" Won semantic: probability = 100 (active untouched) """
		for proposal in self:
			stage_id = proposal._stage_find(domain=[('probability', '=', 100.0), ('on_change', '=', True)])
			proposal.write({'stage_id': stage_id.id, 'probability': 100})
		return True
	
	@api.multi
	def action_set_lost(self):
		""" Lost semantic: probability = 0, active = False """
		return self.write({'probability': 0, 'active': False})
	
	
class LostReason(models.Model):
    _name = "crm.proposal.lost.reason"
    _description = 'Reason for loosing proposal'

    name = fields.Char('Name', required=True, translate=True)
    active = fields.Boolean('Active', default=True)