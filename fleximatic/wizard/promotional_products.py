# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning
import logging
_logger = logging.getLogger(__name__)


class productPromotional(models.TransientModel):
    _name = 'product.promotional'

    sale_id = fields.Many2one('sale.order','Venta')
    points = fields.Float(string='Points',related='sale.points')
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

    def agregar(self):
        if self.points_to_sale > points:
            raise ValidationError(('Error ! Insufficient points to add product(s)'))
        else:
            for line in promotional_line:
                self.sale_id.order_line.write(0,0,{
                    'product_id':line.product_template_id.product_variant_id.id,
                    'product_template_id':line.product_template_id.id,
                    'is_promotional':True,
                    'product_uom_qty':line.qty,
                    'product_uom':line.uom_id,
                    'price_unit':0.01,
                    'tax_id':False,
                    'discount':0.00
                })
            return {'type': 'ir.actions.act_window_close'}

    def cancelar(self):
        return {'type': 'ir.actions.act_window_close'}


class productPromotionalLine(models.TransientModel):
    _name = 'product.promotional.line'

    product_template_id = fields.Many2one('product.template', string='Product', 
        domain="[('sale_ok', '=', True),('vender_puntos','=',True),('puntos_venta','<=',promotional_id.points)]")
    qty  = fields.Integer('Quantity')
    price_points = fields.Float('Points for sale',related='product_template_id.uom_id')
    uom_id =fields.Many2one('uom.uom',stirng='UoM',related='product_template_id.uom_id')
    total = fields.Float('Total',compute='_compute_total_points')
    promotional_id = fields.Many2one('product.promotional')

    @api.depends('product_template_id','qty','price_points')
    def _compute_total_points(self):
        for value in self:
            if value.product_template_id:
                value.total = value.qty * price_points
    
    