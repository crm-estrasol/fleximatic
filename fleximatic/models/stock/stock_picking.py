# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning
import logging
_logger = logging.getLogger(__name__)
from odoo.exceptions import UserError

class fleximaticstock(models.Model):
    
    _inherit = 'stock.picking'
    
    x_approve_freight = fields.Selection([
        ('por aprobar','To Approve'),
        ('aprobado','Approved'),
        ('no aprobado','Not approved')
        ],string='Approve freight')
    x_currency_id = fields.Many2one('res.currency',string='Currency')
    x_freight = fields.Float('freight %', digits=(32, 2), compute='compute_total_porcent', store=True,)
    x_freight_cost = fields.Monetary('Freight cost',related='x_logistics.amount_total')
    x_logistics = fields.Many2one('purchase.order',string='Logistics purchase',domain=[('is_freight','=',True)])
    x_total = fields.Monetary('Sale amount',related='sale_id.amount_total')

    @api.depends('x_freight','x_total','x_freight_cost')
    def compute_total_porcent(self):
        for record in self:
            record['x_freight'] = record.x_freight_cost / (record.x_total and record.x_total or 1)
    def write(self, vals): 
        for mov in self:
            items = self.env['stock.picking.batch'].search([('picking_ids','=',mov.id )])
            for item in items:
                if mov.x_logistics.id != item.x_purchase.id:
                    raise UserError(_("No puedes cambiar la compra en una transferencia asociada a un batch ."))  
            res = super(fleximaticstock, self).write(vals)