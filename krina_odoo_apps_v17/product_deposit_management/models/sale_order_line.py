# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
from odoo import models, api, _, fields


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    sequence = fields.Integer(string="Sequence", default=0)


    def view_related_transfer_sales(self):
        picking_id = self.env['stock.move'].search([('sale_line_id', 'in', [self.id])]).picking_id
        view_id = self.env.ref('stock.vpicktree').id
        if len(picking_id) == 1:
            return {
                'type': 'ir.actions.act_window',
                'view_id': self.env.ref('stock.view_picking_form').id,
                'view_mode': 'form',
                'name': _("Linked deliveries"),
                'res_model': 'stock.picking',
                'res_id': picking_id.id,
            }
        else:
            return {
                'type': 'ir.actions.act_window',
                'view_id': view_id,
                'view_mode': 'list',
                'views': [(view_id, 'list'), (self.env.ref('stock.view_picking_form').id, 'form')],
                'name': _("Linked deliveries"),
                'res_model': 'stock.picking',
                'domain': [('id', 'in', picking_id.ids)],
            }
