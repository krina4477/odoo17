# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _
from datetime import datetime, date
from odoo.exceptions import UserError, ValidationError


class GenerateBarcodeWizard(models.TransientModel):
    _name = "generate.barcode.wizard"
    _description = "Product Variant Wizard"

    product_ids = fields.One2many('product.details.wizard','generate_barcode_id',string="Barcode For Following")

    def generate_barcode(self):
        val = {}
        for rec in self.product_ids:
            val.update({rec.product_id.id: int(rec.quantity)})
        data = {'ids': self.ids,
                'model': self._name,
                'form': val,
                }
        return self.env.ref('product_multi_barcode_cr.product_barcode').report_action(self, data=data)

class ProductDetailsWizard(models.TransientModel):
    _name = "product.details.wizard"
    _description = "Product Variant One2many"

    product_id = fields.Many2one('product.product',string="Name")
    quantity = fields.Integer(string="Quantity")
    generate_barcode_id = fields.Many2one('generate.barcode.wizard',string="Barcode ID")