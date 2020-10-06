# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging
from odoo import models, fields

# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging
from odoo import models, fields

class SaleReportFlexi(models.Model):
    _inherit = 'sale.report'
    #invoice_line_id = fields.Many2one('account.move.line', 'Invoice reference', readonly=True)
    acount_move = fields.Char(string='Facturas')
    #acount_moves = fields.Char(string='Facturas')
    #invoice_date = fields.Date(string="Fecha factura")
    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        #fields['invoice_line_id'] = ', soli.invoice_line_id as invoice_line_id's
        fields['acount_move']  = ', invoic.acount_move as acount_move'
        #fields['invoice_date'] = ', aci.invoice_date as invoice_date'
       
        
        groupby += ',invoic.acount_move '
        from_clause  +=  """
                            left join  (
                                    SELECT l.id, string_agg(aci.name::varchar(255) , ', ') as acount_move FROM 
                                    sale_order_line l
                                    left join sale_order_line_invoice_rel soli on (l.id = soli.order_line_id)
                                    left join account_move_line acil on (acil.id = soli.invoice_line_id )
                                    left join account_move aci on (aci.id = acil.move_id) 

                                    GROUP BY
                                        soli.order_line_id,
                                        l.id
                           ) as invoic on (l.id = invoic.id)
                            """
        return super(SaleReportFlexi, self)._query(with_clause, fields, groupby, from_clause)

#class SaleReportFlexi(models.Model):
    #_inherit = 'sale.report'
    #invoice_line_id = fields.Many2one('account.move.line', 'Invoice reference', readonly=True)
    #acount_move = fields.Char(string='Facturas')
    #invoice_date = fields.Date(string="Fecha factura")
    #def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
    #    #fields['invoice_line_id'] = ', soli.invoice_line_id as invoice_line_id'
    #    fields['acount_move'] = ', aci.name as acount_move'
    #   fields['invoice_date'] = ', aci.invoice_date as invoice_date'
    #    groupby += ', aci.name , aci.invoice_date'
    #    from_clause  +=  """
    #                        left join sale_order_line_invoice_rel soli on (l.id = soli.order_line_id)
    #                        left join account_move_line acil on (acil.id = soli.invoice_line_id )
    #                        left join account_move aci on (aci.id = acil.move_id) 
    #                        """
    #    return super(SaleReportFlexi, self)._query(with_clause, fields, groupby, from_clause)

    
