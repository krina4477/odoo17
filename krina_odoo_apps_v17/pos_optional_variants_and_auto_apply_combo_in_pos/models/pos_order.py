# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _


class PosOrder(models.Model):
    _inherit = "pos.order"

    combo_deals_id = fields.Many2one('combo.deals',string="Combo Deal")

    @api.model
    def _process_order(self, order, draft, existing_order):
        res = super(PosOrder,self)._process_order(order, draft, existing_order)
        order = order['data']
        order = order['lines'][0][2]
        pos_order = self.env['pos.order'].browse(res)
        deal_id = order.get('combo_deals_id', False)
        if deal_id and pos_order:
            combo_product = self.env['product.product'].browse(deal_id[0])
            pos_order.write({'combo_deals_id':combo_product.combo_deals_id.id})
        return res