# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api


class LightspeedMixin(models.Model):
    _name = 'lightspeed.mixin'
    _description = 'Lightspeed Mixin'

    lightspeed_id = fields.Char(string='Lightspeed Id')
    shop_id = fields.Many2one('lightspeed.shop',string='Shop')