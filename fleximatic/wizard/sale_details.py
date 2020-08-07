# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)


class ItemPricelist(models.TransientModel):
    _name = 'fleximatic.sale.pricelist.wizard'
    _description = 'Descuentos '
    product_id =  fields.Many2one('product.product', string='Products')
    sale = fields.Many2one('sale.order', string='Venta')
    pricelist_id =   fields.Many2one('product.pricelist', string='Pricelist')
    pricelist_avaible =  fields.Many2many(comodel_name='product.pricelist.item', relation='table_many_pricelist_item', column1='product_id', column2='',string="Tarifas disponibles")
    date_order =  fields.Datetime(string='Date', readonly=True, default=fields.Datetime.now)
  
    def generate_apply(self):
        products = self.sale.order_line.filtered(lambda x: x.product_id == self.product_id.id)
        products[0].price_subtotal=str(products[0].product_id.name)
        for prod in products:
            prod.pricelist_id = self.pricelist_id
        return self.sale
    def generate_apply_next(self):
        products = self.sale.order_line.filtered(lambda x: x.product_id == self.product_id.id)
        for prod in products:
            prod.pricelist_id = self.pricelist_id
    @api.onchange('sale','product_id')
    def on_change_sale(self):
        self.pricelist_id = False
        pricelist_avaible = self.env['product.pricelist.item'].search( [
            ('product_tmpl_id','=',self.product_id.id),
            '|', ('date_start', '<=', self.date_order ), ('date_start', '=', False),
            '|', ('date_end', '>=', self.date_order ), ('date_end', '=', False)  
            ] )
        if pricelist_avaible:
            self.pricelist_avaible = [ (6, 0, pricelist_avaible.ids ) ]
        else:
             self.pricelist_avaible = False 
        pricelist_domain = [item.pricelist_id.id for item in pricelist_avaible]   
        self.pricelist_id = pricelist_domain[0] if pricelist_domain else False
        #setattr(self, 'pricelist_avaible', [(6, 0, pricelist_avaible.ids ) ])  
        return {
            'domain': { 'product_id': [('id', 'in', [item.product_id.id for item in self.sale.order_line] )] ,
                        'pricelist_id': [('id', 'in', pricelist_domain  )] , 
                      }                     
        }
  