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
        products = self.sale.order_line.filtered(lambda x: x.product_id.id == self.product_id.id and x.is_promotional == False)
        for prod in products:
            prod.pricelist_id = self.pricelist_id
            prod.product_uom_change()
        return self.sale
    def generate_apply_next(self):
        products = self.sale.order_line.filtered(lambda x: x.product_id.id == self.product_id.id and x.is_promotional == False )
        for prod in products:
            prod.pricelist_id = self.pricelist_id
            prod.product_uom_change()
        view_id = self.env.ref('fleximatic.view_sale_pricelist_wizard').id
        
        products = [ x  for x in self.sale.order_line.filtered( lambda x: x.is_promotional == False)]
        orginal_product = self.sale.order_line.filtered(lambda x: self.product_id.id == x.product_id.id)
        products_len = len(products)
        index_prod = products.index(orginal_product[0])
        new_elemnt = {}
        if index_prod == 0 and products_len == 1 or index_prod ==  products_len-1 :
            new_elemnt = products[0]
        else:
             new_elemnt = products[index_prod+1]

        view = {
                'name': ('Descuento'),
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'fleximatic.sale.pricelist.wizard',
                'views':  [(view_id,'form')],
                'type': 'ir.actions.act_window',
                'target': 'new',
                'context':{'default_sale':self.sale.id,
                'default_date_order':self.date_order,
                'default_product_id':new_elemnt.product_id.id  },

                }
        return view 
    @api.onchange('sale','product_id')
    def on_change_sale(self):
        pricelist_avaible = self.env['product.pricelist.item'].search( [
             '&',
             '|',('product_id','=',self.product_id.product_tmpl_id.id), ('product_tmpl_id','=',self.product_id.id),
             '|',('applied_on','=','1_product'),('applied_on','=','0_product_variant'),
             '&',
             '|', ('date_start', '<=', self.date_order ), ('date_start', '=', False),
             '|', ('date_end', '>=', self.date_order ), ('date_end', '=', False),
            ] )

        
       
        if pricelist_avaible:
           
            self.pricelist_avaible = [ (6, 0, pricelist_avaible.ids ) ]  if pricelist_avaible else False
            #
        else:
             self.pricelist_avaible = False
        pricelist_domain = [item.pricelist_id.id for item in pricelist_avaible]   
        self.pricelist_id = pricelist_domain[0] if pricelist_domain else False
        #setattr(self, 'pricelist_avaible', [(6, 0, pricelist_avaible.ids ) ])  
        
        return {
            'domain': { 'product_id': [('id', 'in', [item.product_id.id for item in self.sale.order_line if  item.is_promotional == False] )] ,
                        'pricelist_id': [('id', 'in', pricelist_domain  )] , 
                      }                     
        }
  