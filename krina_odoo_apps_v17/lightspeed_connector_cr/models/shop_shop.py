# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
from odoo import models, fields


class LightSpeedShopShop(models.Model):
    _name = "lightspeed.shop.shop"
    _description = "Shops"
    _inherit = ['lightspeed.mixin']

    lightspeed_warehouse_id = fields.Char('Lightspeed Shop')
    name = fields.Char('Shop Name')
    active = fields.Boolean(default=True)
    warehouse_id = fields.Many2one('stock.warehouse', string="Warehouse")


class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    shop_id = fields.Many2one('lightspeed.shop.shop', 'Connected Lightspeed Shop')
