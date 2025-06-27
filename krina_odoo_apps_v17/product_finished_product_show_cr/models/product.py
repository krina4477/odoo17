# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    finished_product_count = fields.Integer(
        '# Finished Product', compute='_compute_finished_product_count',
        help="Finished Product Count based on the components available")

    @api.depends('bom_ids', 'bom_ids.bom_line_ids', 'bom_ids.bom_line_ids.product_qty', 'bom_ids.bom_line_ids.product_uom_id')
    def _compute_finished_product_count(self):
        for template in self:
            template_bom = template.bom_ids[0] if len(template.bom_ids)>1 else template.bom_ids
            finished_product_count = 0
            for bom in template_bom:
                finished_product_count = int(bom.finished_product_count)
            template.finished_product_count = finished_product_count


class ProductProduct(models.Model):
    _inherit = 'product.product'

    finished_product_count = fields.Integer(
        '# Finished Product', compute='_compute_finished_product_count',
        help="Finished Product Count based on the components available")

    @api.depends('bom_ids', 'bom_ids.bom_line_ids', 'bom_ids.bom_line_ids.product_qty', 'bom_ids.bom_line_ids.product_uom_id')
    def _compute_finished_product_count(self):
        for template in self:
            template_bom = template.bom_ids[0] if len(template.bom_ids)>1 else template.bom_ids
            finished_product_count = 0
            for bom in template_bom:
                finished_product_count = int(bom.finished_product_count)
            template.finished_product_count = finished_product_count

