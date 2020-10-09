    # -*- coding: utf-8 -*-
from odoo import api, fields, models, SUPERUSER_ID, _


class fleximaticproduct(models.Model):
    
    _inherit = 'product.template'

    vender_puntos = fields.Boolean('Puede venderse con puntos')
    puntos_venta = fields.Float('Puntos para venta')
    puntos_genera = fields.Float('Cantidad de puntos que genera(%)')
    upc_13 = fields.Char('UPC 13')
    dun_14 = fields.Char('DUN14')
    item = fields.Char('ITEM')

    def find_products(self,args):
        try:
            products = self.env['product.template'].search([('item','in',args)])
            data = [{
                    '%s' % (x['item']) : {
                                    'dun14':x["dun_14"],
                                    'codigo':x["barcode"],
                                    'descripcion':x["description_sale"]
                                    }
                    } for x in products ]
        except:  
            return {
                    
                            'success':204,
                            'data':[],
                            'message':"Something went wrong check the params."
                    }
        
        return  {
                        
                            'success': 200 if products else 204,
                            'data':data  if products else [],
                            'message': "Succces" if products else "There is not records.",
                    }