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
        return {'Hola':args}