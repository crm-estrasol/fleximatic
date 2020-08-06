# -*- coding: utf-8 -*-
from odoo import models,fields, api


class fleximaticsaleorderline(models.Model):
    _inherit = 'sale.order.line'

    
    pricelist_id = fields.Many2one('product.pricelist',string='Pricelist',domain="[('item_ids.product_tmpl_id', '=', product_template_id)]")


    @api.onchange('product_id', 'price_unit', 'product_uom', 'product_uom_qty', 'tax_id')
    def _onchange_discount(self):
        if not (self.product_id and self.product_uom and
                self.order_id.partner_id and self.pricelist_id and
                self.pricelist_id.discount_policy == 'without_discount' and
                self.env.user.has_group('product.group_discount_per_so_line')):
            return

        self.discount = 0.0
        product = self.product_id.with_context(
            lang=self.order_id.partner_id.lang,
            partner=self.order_id.partner_id,
            quantity=self.product_uom_qty,
            date=self.order_id.date_order,
            pricelist=self.pricelist_id.id,
            uom=self.product_uom.id,
            fiscal_position=self.env.context.get('fiscal_position')
        )

        product_context = dict(self.env.context, partner_id=self.order_id.partner_id.id, date=self.order_id.date_order, uom=self.product_uom.id)

        price, rule_id = self.pricelist_id.with_context(product_context).get_product_price_rule(self.product_id, self.product_uom_qty or 1.0, self.order_id.partner_id)
        new_list_price, currency = self.with_context(product_context)._get_real_price_currency(product, rule_id, self.product_uom_qty, self.product_uom, self.pricelist_id.id)

        if new_list_price != 0:
            if self.pricelist_id.currency_id != currency:
                # we need new_list_price in the same currency as price, which is in the SO's pricelist's currency
                new_list_price = currency._convert(
                    new_list_price, self.pricelist_id.currency_id,
                    self.order_id.company_id or self.env.company, self.order_id.date_order or fields.Date.today())
            discount = (new_list_price - price) / new_list_price * 100
            if (discount > 0 and new_list_price > 0) or (discount < 0 and new_list_price < 0):
                self.discount = discount
#
#
    #def _get_display_price(self, product):
    #    # TO DO: move me in master/saas-16 on sale.order
    #    # awa: don't know if it's still the case since we need the "product_no_variant_attribute_value_ids" field now
    #    # to be able to compute the full price
#
    #    # it is possible that a no_variant attribute is still in a variant if
    #    # the type of the attribute has been changed after creation.
    #    no_variant_attributes_price_extra = [
    #        ptav.price_extra for ptav in self.product_no_variant_attribute_value_ids.filtered(
    #            lambda ptav:
    #                ptav.price_extra and
    #                ptav not in product.product_template_attribute_value_ids
    #        )
    #    ]
    #    if no_variant_attributes_price_extra:
    #        product = product.with_context(
    #            no_variant_attributes_price_extra=tuple(no_variant_attributes_price_extra)
    #        )
#
    #    if self.pricelist_id.discount_policy == 'with_discount':
    #        return product.with_context(pricelist=self.pricelist_id.id).price
    #    product_context = dict(self.env.context, partner_id=self.order_id.partner_id.id, date=self.order_id.date_order, uom=self.product_uom.id)
#
    #    final_price, rule_id = self.pricelist_id.with_context(product_context).get_product_price_rule(product or self.product_id, self.product_uom_qty or 1.0, self.order_id.partner_id)
    #    base_price, currency = self.with_context(product_context)._get_real_price_currency(product, rule_id, self.product_uom_qty, self.product_uom, self.pricelist_id.id)
    #    if currency != self.pricelist_id.currency_id:
    #        base_price = currency._convert(
    #            base_price, self.pricelist_id.currency_id,
    #            self.order_id.company_id or self.env.company, self.order_id.date_order or fields.Date.today())
    #    # negative discounts (= surcharge) are included in the display price
    #    return max(base_price, final_price)