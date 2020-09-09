# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ConfirmSales(models.TransientModel):

    _name = 'fleximatic.multi.confirm.sale'
    _description = 'Confirmar masivo'
"
    @api.model
    def default_get(self, fields):
    
        record_ids = self._context.get('active_ids')
        result = super(ConfirmSales, self).default_get(fields)

        if record_ids:
            if 'sales_ids' in fields:
                sales_ids = self.env['sale.order'].browse(record_ids)
                result['sales_ids'] = sales_ids

        return result

    sales_ids = fields.Many2many('sale.order', 'multi_sale_confirm_rel', 'confirm_id', 'sale_id', string='Sales')
    

    def action_confirm(self):
        self.ensure_one()
        for sale in self.sales_ids:
            sale.action_confirm()
        

   