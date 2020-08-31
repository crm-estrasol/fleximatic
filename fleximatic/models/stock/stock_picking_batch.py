# -*- coding: utf-8 -*-
from odoo import models, fields, api ,_
import logging
_logger = logging.getLogger(__name__)
from odoo.tools.misc import clean_context
from odoo.exceptions import UserError
import sys
class fleximaticstockbatch(models.Model):
    _inherit = 'stock.picking.batch'
    x_purchase = fields.Many2one('purchase.order',string='Logistics purchase')
    total_sales = fields.Float('Total ventas', compute='_compute_total_sales')
    """
    @api.onchange('picking_ids')
    def _onchange_pickings(self):
        if len(self.picking_ids) == len(self.picking_ids.filtered(lambda x:self.x_purchase == x.x_logistics ) ) :
            pass
        else:
            raise UserError(_("Exediste el tamaño permitido (1mb/10000) para la imagen ."))
    """  
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
            if pick.picking_ids:
               if len(set( pick.picking_ids.mapped('x_logistics') )) != 1 or  len(pick.picking_ids) == 1 and pick.picking_ids[0].x_logistics.id != pick.x_purchase.id :
                  raise UserError(_("No puedes modificar una transfererenica ."))  
               pick.total_sales = sum(pick.picking_ids.mapped('x_total'))
            else:
               pick.total_sales = 0 
