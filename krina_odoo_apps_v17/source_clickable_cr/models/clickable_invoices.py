# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
from odoo import api, models, fields, _


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.model
    def create(self, vals):
        res = super(AccountMove, self).create(vals)
        origin_val = vals.get('invoice_origin')
        sale_order_id = self.env['sale.order'].search([('name', '=', origin_val)]).id
        if sale_order_id:
            res.invoice_origin = "%s,%s" % ('sale.order', sale_order_id)
        return res
