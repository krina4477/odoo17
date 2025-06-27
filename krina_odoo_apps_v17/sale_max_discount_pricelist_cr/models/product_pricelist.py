# -*- coding: utf-8 -*-

# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

from itertools import chain

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_repr
from odoo.tools.misc import get_lang

class ProductPricelistInherit(models.Model):
    
    _inherit = 'product.pricelist'

    def _compute_price_rule(self, products, quantity, uom=None, date=False, **kwargs):
        print("---product.pricelist----")
        self.ensure_one()
        if not products:
            return {}
        if not date:
            date = fields.Datetime.now()
        rules = self._get_applicable_rules(products, date, **kwargs)

        results = {}
        for product in products:
            suitable_rule = self.env['product.pricelist.item']

            product_uom = product.uom_id
            target_uom = uom or product_uom  # If no uom is specified, fall back on the product uom
            if target_uom != product_uom:
                print("---product.pricelist if---")
                qty_in_product_uom = target_uom._compute_quantity(quantity, product_uom, raise_if_failure=False)
            else:
                print("---product.pricelist else---")
                qty_in_product_uom = quantity

            for rule in rules:
                if rule._is_applicable_for(product, qty_in_product_uom):
                    suitable_rule = rule
                    break

            kwargs['pricelist'] = self
            price = suitable_rule._compute_price(product, quantity, target_uom, date=date, currency=self.currency_id)
            print("---product.pricelist price---",price)
            results[product.id] = (price, suitable_rule.id)

        return results
