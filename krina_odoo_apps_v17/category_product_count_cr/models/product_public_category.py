# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, tools, _


class ProductPublicCategory(models.Model):
    _inherit = 'product.public.category'

    product_count = fields.Integer('Product Count', compute='_get_product_count')

    def _get_product_count(self):
        for rec in self:
            if not rec.parent_id:
                product_count = self.env['product.template'].search_count([('public_categ_ids', '=', rec.id),
                                                                           ('is_published', '=', True)])
                sub_categ_rec = self.env['product.public.category'].search([('parent_id','=',rec.id)])
                if sub_categ_rec:
                    sub_product_count = self.env['product.template'].search_count([('public_categ_ids', 'in', sub_categ_rec.ids),
                                                                                   ('is_published', '=', True)])
                    rec.product_count = product_count + sub_product_count
                else:
                    rec.product_count = product_count
            else:
                product_count = self.env['product.template'].search_count([('public_categ_ids', '=', rec.id),
                                                                           ('is_published', '=', True)])
                rec.product_count = product_count
