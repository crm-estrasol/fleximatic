    # -*- coding: utf-8 -*-
from odoo import api, fields, models, SUPERUSER_ID, _


class fleximaticproduct(models.Model):
    
    _inherit = 'product.template'

    vender_puntos = fields.Boolean('Puede venderse con puntos')
    puntos_venta = fields.Float('Puntos para venta')
    puntos_genera = fields.Float('Cantidad de puntos que genera(%)')
    upc_13 = fields.Integer('UPC 13')
    dun_14 = fields.Integer('DUN14')
    item = fields.Integer('ITEM')