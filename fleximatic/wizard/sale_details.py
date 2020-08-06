# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)


class ItemPricelist(models.TransientModel):
    _name = 'fleximatic.sale.pricelist.wizard'
    _description = 'Descuentos '
    product_id =  fields.Many2one('product.template', string='Products')
    sale = fields.Many2one('sale.order', string='Venta')
    pricelist_id =   fields.Many2one('product.pricelist', string='Products')
    pricelist_avaible =  fields.Many2many(comodel_name='product.pricelist.item', relation='table_many_pricelist_item', column1='product_id', column2='',string="Tarifas disponibles")
    #partner =  fields.Many2many(comodel_name='res.partner', relation='table_many_partner', column1='partner_id', column2='',string="Proveedor")
    
    """
    def generate_report(self):    
        for prod in self.sale.order_line:
            goal = []
            if self.projects:
                goal.append( True if prod.project in self.projects  else False )
            if self.ubications:
                goal.append( True if prod.ubication  in self.ubications  else False )
            if self.brand:
                goal.append( True if prod.product_id.brand in self.brand  else False )
            if self.partner:
                sellers = []
                for seller in prod.product_id.seller_ids:
                        sellers.append(seller.name.id)     
                goal.append( True if  any(i in sellers for i in self.partner.ids) else False )
            
            prod.discount = self.discount  if all(goal if goal else False)  else prod.discount
        return self.sale
   
       
    @api.onchange('sale')
    def on_change_sale(self):
        sistemas = [item.project.id for item in self.sale.order_line if item.product_id and item.project  ]
        marcas = [item.product_id.brand.id for item in self.sale.order_line if item.product_id and item.product_id.brand  ]
        ubicaciones = [ item.ubication.id for item in self.sale.order_line if item.product_id and item.ubication  ]
        sellers = []
        for item in self.sale.order_line: 
            if item.product_id:
                for seller in item.product_id.seller_ids:
                    sellers.append(seller.name.id) 
        sellers = list(set(sellers))
        return {
            'domain': { 'projects': [('id', 'in', sistemas)], 
                        'ubications': [('id', 'in', ubicaciones)],
                        'brand': [('id', 'in', marcas)],
                        'partner': [('id', 'in', sellers)],
                      }                     
        }
    """