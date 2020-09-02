# -*- coding: utf-8 -*-
from odoo import models, fields, api ,_
import logging
_logger = logging.getLogger(__name__)
from odoo.tools.misc import clean_context
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
import sys
class fleximaticstockbatch(models.Model):
    _inherit = 'stock.picking.batch'
    x_purchase = fields.Many2one('purchase.order',string='Logistics purchase')
    total_sales = fields.Float('Total ventas', compute='_compute_total_sales')
    x_freight = fields.Float('freight %', digits=(32, 2), compute='compute_total_porcent', store=True,)
    x_freight_cost = fields.Monetary('Freight cost',related='x_purchase.amount_total')
    x_total = fields.Monetary('Sale amount',related='total_sales')
    @api.depends('x_freight','x_total','x_freight_cost')
    def compute_total_porcent(self):
        for record in self:
            record['x_freight'] = record.x_freight_cost / (record.x_total and record.x_total or 1)
    @api.constrains('x_purchase')
    def _check_purchase(self):
        if len(self.env['stock.picking.batch'].search([('x_purchase','=',self.x_purchase.id)])) > 1 and self.x_purchase:
            raise ValidationError(_('Ya existe un albaran con la misma compra.'))
    @api.onchange('picking_ids')
    def _onchange_pickings(self):
      
        if self.x_purchase:
            ids = self.picking_ids.filtered(lambda x:self.x_purchase == x.x_logistics ).mapped('id')
            self.picking_ids = [( 6, 0, [x for x in ids] ) ]
        else: 
            ids = self.picking_ids.filtered(lambda x: not x.x_logistics  ).mapped('id')
            self.picking_ids = [( 6, 0, [x for x in ids] ) ]
                
    @api.onchange('x_purchase')  
    def _onchange_purchase(self):    
        self.picking_ids = False
        if self.x_purchase :
            return {
            'domain': { 'picking_ids':  [('x_logistics', '=', self.x_purchase.id)] ,
                        
                      }                   }
        else:
            return {
            'domain': { 'picking_ids':  [('x_logistics', '=', False)] 
                        
                      }  
            }
    @api.depends('picking_ids','picking_ids.x_total','picking_ids.x_logistics')    
    def _compute_total_sales(self):
        for pick in self:
            if not self.x_purchase:
                pick.total_sales = 0 
            elif pick.picking_ids:
               if len(set( pick.picking_ids.mapped('x_logistics') )) != 1 or  len(pick.picking_ids) == 1 and pick.picking_ids[0].x_logistics.id != pick.x_purchase.id :
                  raise UserError(_("No puedes modificar una transfererenica que ya esta asociada a un albaran con compra asociada."))  
               pick.total_sales = sum(pick.picking_ids.mapped('x_total'))
            else:
               pick.total_sales = 0 
#aaa