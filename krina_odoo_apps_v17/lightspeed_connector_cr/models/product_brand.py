# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
from odoo import models, api, _, fields


class ProductBrand(models.Model):
    _name = 'product.brand'
    _inherit = 'lightspeed.mixin'

    name = fields.Char(string='Name')
    image = fields.Binary(string='Image')
    description = fields.Html(string='Content')
    is_visible = fields.Boolean(string='Is Visible in Lightspeed?')
