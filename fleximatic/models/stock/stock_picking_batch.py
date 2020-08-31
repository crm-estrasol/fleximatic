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
        pass
            