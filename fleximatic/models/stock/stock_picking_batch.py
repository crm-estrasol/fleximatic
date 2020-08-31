# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning
import logging
_logger = logging.getLogger(__name__)

class fleximaticstockbatch(models.Model):
    _inherit = 'stock.picking.batch'
    x_purchase = fields.Many2one('purchase.order',string='Logistics purchase')
    total_sales = fields.Float('Total ventas', compute='_compute_total_sales')
    @api.onchange('picking_ids')
    def _onchange_pickings(self):
        if len(self.picking_ids) == len(self.picking_ids.filtered(lambda x:self.x_purchase == x.x_logistics ) ) :
            pass
        else:
            pass

            