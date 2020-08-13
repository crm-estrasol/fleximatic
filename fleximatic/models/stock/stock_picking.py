# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning
import logging
_logger = logging.getLogger(__name__)

class fleximaticstock(models,Model):
    
    _inherit = 'stock.picking'
    
    x_approve_freight = fields.Selection([
        ('Por aprobar','To Approve'),
        ('Aprobado','Approved'),
        ('No aprobado','Not approved')
        ],string='Approve freight')
    #x_currency_id = fields.Many2one('res.currency',string='Currency',related='sale_id.currency_id')
    #x_freight = fields.Float('freight %', digits=(32, 2), compute='compute_total_porcent', store = True,)
    x_freight_cost = fields.Monetary('Freight cost',related='x_logistics.amount_total')
    x_logistics = fields.Many2one('purchase.order',string='Logistics purchase')
    x_total = fields.Monetary('Sale amount',related='sale_id.amount_total')

    #@api.depends('x_freight','x_total','x_freight_cost')
    #def compute_total_porcent(self):
    #    for record in self:
    #        record['x_freight'] = record.x_freight_cost / (record.x_total and record.x_total or 1)