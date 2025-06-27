# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _
import ast

class StockMove(models.Model):
    _inherit = "stock.move"

    def _action_done(self, cancel_backorder=False):
        moves_todo = super(StockMove, self)._action_done(cancel_backorder=cancel_backorder)
        for move in moves_todo:
            if move.state == 'done' and move.product_id.lightspeed_id:
                shop_id = self.env['lightspeed.shop.shop'].search([('warehouse_id','in',[move.location_dest_id.warehouse_id.id if move.location_dest_id.warehouse_id else 1]),
                                                                   ('shop_id', '=', move.product_id.shop_id.id)], limit=1)
                itemshop_dict = move.product_id.itemshop_dict
                sttr = ast.literal_eval(itemshop_dict)
                move.product_id.shop_id.with_context(itemshopid=int(sttr[0].get(shop_id.lightspeed_id))).lightspeed_update_product_stock(move.product_id)
        return moves_todo