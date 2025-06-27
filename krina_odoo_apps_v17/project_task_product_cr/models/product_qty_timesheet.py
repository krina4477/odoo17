# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

from odoo import fields, models, _


class ProductQtyTimesheet(models.Model):
    _name = 'product.qty.timesheet'
    _description = 'Product Qty Timesheet'

    product_id = fields.Many2one('product.product', string="Product", default=False, copy=False,)
    quantity = fields.Float('Quantity')
    timesheet_id = fields.Many2one('account.analytic.line', string="Timesheet")
