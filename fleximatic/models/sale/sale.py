
    # -*- coding: utf-8 -*-
from odoo import api, fields, models, SUPERUSER_ID, _


class fleximaticsale(models.Model):
    _inherit = 'sale.order'


    points = fields.Float('Points',digits=(32, 2),compute='_compute_total_points',store=True)

    @api.depends('order_line')
    def _compute_total_points(self):
        puntos = 0
        for sale in self:
            if sale.order_line:
                for line in sale.order_line:
                    puntos += line.price_subtotal *(1/100)
            sale.points = puntos
                        