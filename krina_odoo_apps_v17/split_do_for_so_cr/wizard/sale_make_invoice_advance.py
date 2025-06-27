# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import time

from odoo import fields, models, api

class SaleSplitDO(models.TransientModel):
    _name = "sale.split.do"
    _description = "Sales Split Devivery Order"

    @api.model
    def default_get(self, fields):
        defaults = super(SaleSplitDO, self).default_get(fields)
        if self.env.context.get('active_id'):
            defaults['sale_id'] = self.env.context.get('active_id')
            # defaults['sale_line_ids'] = self.env['sale.order'].browse(self.env.context.get('active_id')).order_line
        return defaults

    @api.onchange('sale_id')
    def sale_id_onchange(self):
        return {'domain': {'sale_line_ids': [('order_id', '=', self.sale_id.id), ('delivery_order_done','=', False)]}}

    sale_id = fields.Many2one('sale.order', string='Sales Order')
    sale_line_ids = fields.Many2many("sale.order.line", 'split_id', 'line_id', string="Order lines to deliver")

    def split_delivery_order(self):
        self.sale_id.with_context({'do_line_ids':self.sale_line_ids.ids,'split_do': True}).action_confirm()
        self.sale_line_ids.write({'delivery_order_done': True})
        return True

