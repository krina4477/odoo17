# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _


class PurchaseSplitReceipt(models.TransientModel):
    _name = "purchase.split.receipt"
    _description = "Purchase Split Receipt"

    @api.model
    def default_get(self, fields):
        defaults = super(PurchaseSplitReceipt, self).default_get(fields)
        if self.env.context.get('active_id'):
            defaults['purchase_id'] = self.env.context.get('active_id')
        return defaults

    purchase_id = fields.Many2one('purchase.order', string='Purchase Order')
    purchase_line_ids = fields.Many2many("purchase.order.line", 
        string="Order lines to receive",
        domain="[('order_id', '=', purchase_id), ('receipt_order_done','=', False)]")

    def split_receipt(self):
        self.purchase_id.with_context({'receipt_line_ids':self.purchase_line_ids.ids,'split_receipt': True}).button_confirm()
        self.purchase_line_ids.write({'receipt_order_done': True})
        return True

