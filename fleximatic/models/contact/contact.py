    # -*- coding: utf-8 -*-
from odoo import api, fields, models, SUPERUSER_ID, _


class fleximaticcontact(models.Model):
    
    _inherit = 'res.partner'

    x_credit = fields.Monetary('Available Credit',compute = 'compute_total_credit')
    x_sale = fields.One2many('sale.order','partner_id',string='Orders to invoiced',domain=[('state','=','sale'),('invoice_status','!=','invoiced')])

    @api.depends('x_credit','credit_limit','credit','x_sale','x_sale.invoice_status')
    def compute_total_credit(self):
        for record in self:
            reg =  record.x_sale.filtered( lambda x : (x.state == 'sale' and x.invoice_status != 'invoiced' ))
            sum_total = sum(reg.mapped('amount_total'))
            record['x_credit'] = record.credit_limit - record.credit - sum_total
    @api.onchange('category_id')
    def _onchange_tag(self):
        if self.category_id:
            if len(self.category_id ) > 1:
                last = self.category_id[-1].id
                self.category_id = [ (6, 0, [last] ) ] 
