# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _
from datetime import datetime, date
from odoo.exceptions import UserError, ValidationError


class TemplateBarcodeWizard(models.TransientModel):
    _name = "template.barcode.wizard"
    _description = "Product Template Wizard"

    product_ids = fields.One2many('template.details.wizard','barcode_id',string="Barcode For Following")

    def generate_barcode(self):
        val = {}
        for rec in self.product_ids:
            val.update({rec.product_template_id.id: int(rec.quantity)})
        data = {'ids': self.ids,
                'model': self._name,
                'form': val,
                }
        return self.env.ref('product_multi_barcode_cr.product_barcode').report_action(self, data=data)


class TemplateDetailsWizard(models.TransientModel):
    _name = "template.details.wizard"
    _description = "Product Template One2many"

    product_template_id = fields.Many2one('product.template',string="Name")
    quantity = fields.Integer(string="Quantity")
    barcode_id = fields.Many2one('template.barcode.wizard',string="Barcode ID")