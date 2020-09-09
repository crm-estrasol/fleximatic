# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class MergeOpportunity(models.TransientModel):

    _name = 'fleximatic.multi.confirm.sale'
    _description = 'Confirmar masivo'
"""
    @api.model
    def default_get(self, fields):
    
        record_ids = self._context.get('active_ids')
        result = super(MergeOpportunity, self).default_get(fields)

        if record_ids:
            if 'opportunity_ids' in fields:
                opp_ids = self.env['crm.lead'].browse(record_ids).filtered(lambda opp: opp.probability < 100).ids
                result['opportunity_ids'] = opp_ids

        return result

    opportunity_ids = fields.Many2many('crm.lead', 'merge_opportunity_rel', 'merge_id', 'opportunity_id', string='Leads/Opportunities')
    user_id = fields.Many2one('res.users', 'Salesperson', index=True)
    team_id = fields.Many2one('crm.team', 'Sales Team', index=True)

    def action_merge(self):
        self.ensure_one()
        merge_opportunity = self.opportunity_ids.merge_opportunity(self.user_id.id, self.team_id.id)
        return merge_opportunity.redirect_lead_opportunity_view()

    @api.onchange('user_id')
    def _onchange_user(self):
      
        team_id = False
        if self.user_id:
            user_in_team = False
            if self.team_id:
                user_in_team = self.env['crm.team'].search_count([('id', '=', self.team_id.id), '|', ('user_id', '=', self.user_id.id), ('member_ids', '=', self.user_id.id)])
            if not user_in_team:
                team_id = self.env['crm.team'].search(['|', ('user_id', '=', self.user_id.id), ('member_ids', '=', self.user_id.id)], limit=1)
        self.team_id = team_id
"""