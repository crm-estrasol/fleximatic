
    # -*- coding: utf-8 -*-
from odoo import api, fields, models, SUPERUSER_ID, _
from datetime import datetime, timedelta
from functools import partial
from itertools import groupby

from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools.misc import formatLang, get_lang
from odoo.osv import expression
from odoo.tools import float_is_zero, float_compare

class fleximaticsale(models.Model):
    _inherit = 'sale.order'

    x_approve = fields.Selection([
        ('por aprobar','To Approve'),
        ('aprobado','Approved'),
        ('no aprobado','Not approved')],
        string='Approve')
    state = fields.Selection(selection_add=[('por aprobar','To Approve'),
        ('aprobado','Approved'),
        ('no aprobado','Not approved')],readonly=True, copy=False, index=True, tracking=3, default='draft')
    x_credit = fields.Monetary(related='partner_id.x_credit',string='Available Credit')
    x_credit_after_sale = fields.Monetary('Credit After Sale',compute = 'compute_credit_after_sale')
    points = fields.Float('Points',digits=(32, 2), compute='_compute_total_points',store=True)
    r_points = fields.Float('Remaining points',digits=(32,2), compute='_compute_total_remaining_points')
    def action_draft(self):
        orders = self.filtered(lambda s: s.state in ['cancel', 'sent'])
        return orders.write({
            'x_approve': False,
            'state': 'draft',
            'signature': False,
            'signed_by': False,
            'signed_on': False,
        })    
    def show_pricelistAvaible(self):
        if self.order_line:   
            view_id = self.env.ref('fleximatic.view_sale_pricelist_wizard').id
            view = {
                'name': ('Descuento'),
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'fleximatic.sale.pricelist.wizard',
                'views':  [(view_id,'form')],
                'type': 'ir.actions.act_window',
                'target': 'new',
                'context':{'default_sale':self.id,'default_date_order':self.date_order,'default_product_id':self.order_line[0].product_id.id},
                }
        return view 

    @api.depends('order_line','state')
    def _compute_total_points(self):
        for sale in self:
            puntos = 0.0
            if sale.order_line:
                for line in sale.order_line:
                    if line.is_promotional == False:
                        puntos += line.price_subtotal *(line.product_id.puntos_genera/100)
            if sale.state in ['done','cancel']: 
                sale.points = 0
            else:
                sale.points = puntos

    @api.depends('x_credit_after_sale','x_credit','amount_total')
    def compute_credit_after_sale(self):
        for record in self:
            record['x_credit_after_sale'] = record.x_credit - record.amount_total

    def open_wizard_promotional(self):
        view_id = self.env.ref('fleximatic.view_sale_products_wizard').id
        promotionals = [ (0,0,{'product_id':item.product_id.id,
                                'product_template_id':item.product_template_id.id,
                                'qty':item.product_uom_qty,
                                'uom_id':item.product_uom.id,
                                'price_points':item.product_id.puntos_venta,
                                'total':item.product_uom_qty*item.product_id.puntos_venta
        } ) for item in self.order_line if item.is_promotional  ]

        view = {
            'name': ('Agregar productos promocionales'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'product.promotional',
            'type': 'ir.actions.act_window',
            'target':'new',
            'context':{'default_sale_id':self.id,
            'default_points':self.points,
            'default_promotional_line':promotionals,
            'default_points_to_sale':sum([x[2]['total'] for x in promotionals])
            }
        }
        return view
       


    @api.depends('points','order_line','state')    
    def _compute_total_remaining_points(self):
        for sale in self:
            puntos_gastados = 0
            if sale.order_line and sale.state not in ['done','cancel']:
                for line in sale.order_line:
                    if line.is_promotional == True:
                        puntos_gastados += line.puntos_venta * line.product_uom_qty
                self.r_points = self.points - puntos_gastados
            else:
                self.r_points = self.points

    
    def write(self, vals):
        status = ['draft','sent','por aprobar','aprobado','no aprobado']
        if  'x_approve' in vals and self.state in status and self.x_credit_after_sale < 0 and self.payment_term_id != 1  :
                vals['state'] = vals['x_approve'] 
        res = super(fleximaticsale, self).write(vals)
        if self.r_points < 0:
            raise ValidationError(('Error! Not enough points to complete the sale'))
        else:
            return res
    
#x
    def remove_promotional_products(self):

        if self.order_line:
            for products in self.order_line:
                if products.is_promotional == True:
                    products.with_context(allow_delete=True).unlink()