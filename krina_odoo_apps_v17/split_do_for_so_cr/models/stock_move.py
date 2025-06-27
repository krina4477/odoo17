# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

from itertools import groupby

from odoo import SUPERUSER_ID, _, api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    def _assign_picking(self):
        Picking = self.env['stock.picking']
        grouped_moves = groupby(sorted(self, key=lambda m: [f.id for f in m._key_assign_picking()]),
                                key=lambda m: [m._key_assign_picking()])
        for group, moves in grouped_moves:
            moves = self.env['stock.move'].concat(*list(moves))
            new_picking = False
            picking = moves[0]._search_picking_for_assignation()
            if picking and not self.env.context.get('split_do'):
                vals = {}
                if any(picking.partner_id.id != m.partner_id.id for m in moves):
                    vals['partner_id'] = False
                if any(picking.origin != m.origin for m in moves):
                    vals['origin'] = False
                if vals:
                    picking.write(vals)
            else:
                new_picking = True
                picking = Picking.create(moves._get_new_picking_values())

            moves.write({'picking_id': picking.id})
            moves._assign_picking_post_process(new=new_picking)
        return True