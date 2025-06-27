# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, SUPERUSER_ID, _


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    receipt_order_done = fields.Boolean('Receipt done', default=False, copy=False)


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.depends('order_line.receipt_order_done')
    def compute_receipt_order_complete(self):
        for order in self:
            order.update({
                'receipt_order_complete': False if any(pol.receipt_order_done == False for pol in order.order_line) else True,
            })

    receipt_order_complete = fields.Boolean('Receipt complete', default=False, copy=False, compute=compute_receipt_order_complete)

    def button_confirm(self):
        for order in self:
            if order.state not in ['draft', 'sent'] and not self.env.context.get('split_receipt'):
                continue
            order._add_supplier_to_product()
            # Deal with double validation process
            if order._approval_allowed():
                order.button_approve()
            else:
                order.write({'state': 'to approve'})
            if order.partner_id not in order.message_partner_ids:
                order.message_subscribe([order.partner_id.id])
        return True

    def _create_picking(self):
        StockPicking = self.env['stock.picking']
        for order in self.filtered(lambda po: po.state in ('purchase', 'done')):
            if any(product.type in ['product', 'consu'] for product in order.order_line.product_id):
                order = order.with_company(order.company_id)
                pickings = order.picking_ids.filtered(lambda x: x.state not in ('done', 'cancel'))
                if not pickings:
                    res = order._prepare_picking()
                    picking = StockPicking.with_user(SUPERUSER_ID).create(res)
                else:
                    if self.env.context.get('split_receipt'):
                        res = order._prepare_picking()
                        picking = StockPicking.with_user(SUPERUSER_ID).create(res)
                    else:
                        picking = pickings[0]
                if self.env.context.get('receipt_line_ids'):
                    moves = order.order_line.filtered(
                        lambda l: l.id in self.env.context.get('receipt_line_ids'))._create_stock_moves(picking)
                else:
                    moves = order.order_line._create_stock_moves(picking)
                moves = moves.filtered(lambda x: x.state not in ('done', 'cancel'))._action_confirm()
                seq = 0
                for move in sorted(moves, key=lambda move: move.date):
                    seq += 5
                    move.sequence = seq
                moves._action_assign()
                picking.message_post_with_source('mail.message_origin_link',
                                               render_values={'self': picking, 'origin': order},
                                               subtype_xmlid='mail.mt_note')
        return True

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
