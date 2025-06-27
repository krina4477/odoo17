# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'

    pricelist_id = fields.Many2one('product.pricelist', string='Pricelist')
    pricelist_label = fields.Char(related='pricelist_id.name', store=True)

    def _export_for_ui(self, orderline):
        result = super()._export_for_ui(orderline)
        result['pricelist_id'] = orderline.pricelist_id.id
        result['pricelist_label'] = orderline.pricelist_label
        return result


