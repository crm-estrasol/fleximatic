# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning
import logging
_logger = logging.getLogger(__name__)


class productPromotional(models.TransientModel):
    _name = 'product.promotional'

    name = fields.Char('name')
    sale_id = fields.Many2one('sale.order',string='Sale')
    points = fields.Float(string='Points')
    points_to_sale = fields.Float(string='Points to sale')
    promotional_line = fields.One2many('product.promotional.line','promotional_id')


class productPromotionalLine(models.TransientModel):
    _name = 'product.promotional.line'

    product_template_id = fields.Many2one('product.template', string='Product', domain=[('sale_ok', '=', True),('vender_puntos','=',True)])
    qty  = fields.Integer('Quantity')
    price_points = fields.Float('Points for sale',related='product_template_id.puntos_venta')
    uom_id =fields.Many2one('uom.uom',stirng='UoM',related='product_template_id.uom_id')
    total = fields.Float('Total',compute='_compute_total_points')
    promotional_id = fields.Many2one('product.promotional')

    @api.depends('product_template_id','qty','price_points')
    def _compute_total_points(self):
        for value in self:
            if value.product_template_id:
                value.total = value.qty * price_points
    
    