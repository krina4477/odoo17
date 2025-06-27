# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
from odoo import models, fields


class ProductPackaging(models.Model):
    _inherit = 'product.packaging'

    deposit_type = fields.Selection(related="product_id.product_tmpl_id.deposit_type")
    deposit_product_id = fields.Many2one('product.product', copy=False)
