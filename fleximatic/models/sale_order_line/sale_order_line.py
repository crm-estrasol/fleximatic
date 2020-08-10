# -*- coding: utf-8 -*-
from odoo import models,fields, api


class fleximaticsaleorderline(models.Model):
    _inherit = 'sale.order.line'

    
    pricelist_id = fields.Many2one('product.pricelist',string='Pricelist'
    ,domain="[('item_ids.product_tmpl_id', '=', product_id.product_tmpl_id)]"
    )
    #s