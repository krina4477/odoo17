# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _
from datetime import datetime, date
from odoo.exceptions import UserError, ValidationError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def generate_barcode(self):
        action = self.env.ref('product_multi_barcode_cr.template_barcode_action').read()[0]
        active_ids = self.env.context.get('active_ids', [])
        product_rec = self.env['product.template'].browse(active_ids)
        val = []
        if product_rec:
            for rec in product_rec:
                val.append((0,0,{'product_template_id': rec.id,
                                 'quantity': 1}))
            action['context'] = {'default_product_ids': val}
        return action


class ProductProduct(models.Model):
    _inherit = "product.product"

    def generate_barcode(self):
        action = self.env.ref('product_multi_barcode_cr.generate_barcode_action').read()[0]
        active_ids = self.env.context.get('active_ids', [])
        product_rec = self.env['product.product'].browse(active_ids)
        val = []
        if product_rec:
            for rec in product_rec:
                val.append((0,0,{'product_id': rec.id,
                                 'quantity': 1}))
            action['context'] = {'default_product_ids': val}
        return action