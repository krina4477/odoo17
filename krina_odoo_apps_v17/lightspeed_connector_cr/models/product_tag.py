# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
from odoo import models, api, _, fields


class ProductTag(models.Model):
    _name = 'product.tag'
    _inherit = ['product.tag', 'lightspeed.mixin']

    name = fields.Char(string='Name')
    # is_visible = fields.Boolean(string='Is Visible in Lightspeed?')

    @api.model
    def create(self, vals):
        res = super(ProductTag, self).create(vals)
        if res.shop_id:
            res.shop_id._create_product_tag(tag_id=res.id)
        return res


    def write(self,vals):
        res = super().write(vals)
        for rec in self:
            if rec.shop_id:
                rec.shop_id._update_product_tag(tag_id=rec.id)
        return res
