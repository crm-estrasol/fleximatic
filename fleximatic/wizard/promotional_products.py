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
    points_to_sale = fields.Float(string='Points to sale', compute = 'total_points_to_sale')
    promotional_line = fields.One2many('product.promotional.line','promotional_id')

    @api.depends('promotional_line')
    def total_points_to_sale(self):
        for value in self:
            total = 0.0
            if value.promotional_line:
                for line in value.promotional_line:
                    total += line.total
            value.points_to_sale = total

    def add_promotional_products(self):
        if self.points_to_sale > self.points:
            raise ValidationError(('Error ! Insufficient points to add product(s)'))
        else:
            order_line = self.env['sale.order.line'].search([('order_id','=',self.sale_id.id),('is_promotional','=',True)])
            if order_line:
                for products in order_line:
                    if products.is_promotional == True:
                        products.unlink()
            for line in self.promotional_line:
                if line.qty > 0:
                    self.sale_id.write({
                        'order_line':[(0,0,{
                            'product_id':line.product_template_id.product_variant_id.id,
                            'product_template_id':line.product_template_id.id,
                            'is_promotional':True,
                            'product_uom_qty':line.qty,
                            'product_uom':line.uom_id.id,
                            'price_unit':0.00,
                            'tax_id':False,
                            'discount':0.00
                        })]
                    })
            return {'type': 'ir.actions.act_window_close'}

    def cancel(self):
        return {'type': 'ir.actions.act_window_close'}
    
    @api.onchange('points_to_sale')
    def change_point(self):
        if self.sale_id:
            self.points = self.sale_id.points - self.points_to_sale



class productPromotionalLine(models.TransientModel):
    _name = 'product.promotional.line'

    product_template_id = fields.Many2one('product.template', string='Product', domain=[('sale_ok', '=', True),('vender_puntos','=',True)])
    qty  = fields.Integer('Quantity',default=1)
    price_points = fields.Float('Points for sale',related='product_template_id.puntos_venta')
    uom_id =fields.Many2one('uom.uom',stirng='UoM',related='product_template_id.uom_id')
    total = fields.Float('Total',compute='_compute_total_points')
    promotional_id = fields.Char('Promotional')

    @api.depends('product_template_id','qty','price_points')
    def _compute_total_points(self):
        for value in self:
            if value.product_template_id:
                value.total = value.qty * value.price_points
            else:
                value.total = 0
    