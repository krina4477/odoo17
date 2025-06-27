# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    finished_product_count = fields.Integer(
        '# Finished Product', compute='_compute_finished_product_count')

    @api.depends('bom_line_ids', 'bom_line_ids.product_qty', 'bom_line_ids.product_uom_id')
    def _compute_finished_product_count(self):
        for bom in self:
            finish_product_count = 0
            finish_product = []
            product_uom_dict = {}
            product_qty_dict = {}
            for bom_line in bom.bom_line_ids:
                if not product_qty_dict.get(bom_line.product_id, False):
                    product_qty_dict.update({bom_line.product_id: bom_line.product_qty})
                    product_uom_dict.update({bom_line.product_id: bom_line.product_uom_id})
                else:
                    if bom_line.product_uom_id != product_uom_dict[bom_line.product_id]:
                        update_finished_qty = product_uom_dict[bom_line.product_id]._compute_quantity(
                            bom_line.product_qty,
                            bom_line.product_uom_id)
                    else:
                        update_finished_qty = product_uom_dict[bom_line.product_id]._compute_quantity(
                            bom_line.product_qty,
                            bom_line.product_uom_id)
                    product_qty_dict[bom_line.product_id] and product_qty_dict.update({
                        bom_line.product_id: update_finished_qty+product_qty_dict[bom_line.product_id]})
            for key,val in product_qty_dict.items():
                computed_qty = key.uom_id._compute_quantity(key.qty_available, product_uom_dict[key])
                finished_qty = computed_qty / val
                finish_product.append(finished_qty)
            if finish_product:
                finish_product_count = min(finish_product)
            bom.finished_product_count = int(finish_product_count)
            print("\n # bom.finished_product_count::",bom.finished_product_count)

