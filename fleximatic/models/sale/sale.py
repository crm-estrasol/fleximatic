
    # -*- coding: utf-8 -*-
from odoo import api, fields, models, SUPERUSER_ID, _


class fleximaticsale(models.Model):
    _inherit = 'sale.order'

    x_approve = fields.Selection([
        ('to_approve','To Approve'),
        ('approved','Approved'),
        ('not_approve','Not Approve')],
        string='Approve')
    x_credit = fields.Monetary(related='partner_id.x_credit',string='Available Credit')
    x_credit_after_sale = fields.Monetary('Credit After Sale',compute = 'compute_credit_after_sale')
    points = fields.Float('Points',digits=(32, 2),compute='_compute_total_points',store=True)

    @api.depends('order_line')
    def _compute_total_points(self):
        puntos = 0
        for sale in self:
            if sale.order_line:
                for line in sale.order_line:
                    puntos += line.price_subtotal *(1/100)
            sale.points = puntos

    @api.depends('x_credit_after_sale','x_credit','amount_total')
    def compute_credit_after_sale(self):
        for record in self:
            record['x_credit_after_sale'] = record.x_credit - record.amount_total   