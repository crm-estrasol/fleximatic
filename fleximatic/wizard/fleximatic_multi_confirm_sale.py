# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import AccessError, UserError, ValidationError

class ConfirmSales(models.TransientModel):

    _name = 'fleximatic.multi.confirm.sale'
    _description = 'Confirmar masivo'

    @api.model
    def default_get(self, fields):
        raise ValidationError(('Error! Not enough points to complete the sale'))
        record_ids = self._context.get('active_ids')
        result = super(ConfirmSales, self).default_get(fields)

        if record_ids:
            if 'sales_ids' in fields:

                sales_ids = self.env['sale.order'].browse(record_ids)
                for sale in sales_ids:
                    if sale.state not in ['draft','sent']:
                        raise ValidationError(("""This sale status is not draft or sent  """ % (sale.name)))
                result['sales_ids'] = [ (6, 0, sales_ids.ids ) ]

        return result

    sales_ids = fields.Many2many('sale.order', 'multi_sale_confirm_rel', 'confirm_id', 'sale_id', string='Sales')
    

    def action_confirm(self):
        
        for sale in self.env['sale.order'].browse(self.sales_ids.ids):
            sale.action_confirm()
        

   