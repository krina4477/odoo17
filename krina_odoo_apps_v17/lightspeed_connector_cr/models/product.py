# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
from odoo import models, api, _, fields


class ProductTemplate(models.Model):
    _name = 'product.template'
    _inherit = ['product.template','lightspeed.mixin']

    brand_id = fields.Many2one('product.brand',string='Brand')
    shopwarehouse_id = fields.Many2many('lightspeed.shop.shop',string='Shop/Warehouse')
    itemshop_dict = fields.Char()
    # tag_ids = fields.Many2many('product.tag',string='Tags')
    # product_category_ids = fields.Many2many('product.category',string='Product Categories')


class ProductProduct(models.Model):
    _name = 'product.product'
    _inherit = ['product.product', 'lightspeed.mixin']

    lightspeed_template_id = fields.Char(string='Lightspeed Template Id')

    @api.model
    def create(self, vals):
        res = super(ProductProduct, self).create(vals)
        if res.shop_id:
            res.shop_id._create_product(product_id=res.id)
        if res.product_tmpl_id.shop_id:
            res.product_tmpl_id.shop_id._create_product(product_id=res.id)

        return res

    def write(self, vals):
        res = super().write(vals)
        if self.lightspeed_template_id and self.lightspeed_id:
            self.shop_id._update_lightspeed_price(product_id=self)
        return res


class ProductAttribute(models.Model):
    _name = "product.attribute"
    _inherit = ['product.attribute','lightspeed.mixin']


    @api.model
    def create(self, vals):
        res = super().create(vals)
        if res.shop_id:
            res.shop_id._create_product_attribute(attribute_id=res.id)
        return res


class ProductAttributeValue(models.Model):
    _name = "product.attribute.value"
    _inherit = ['product.attribute.value', 'lightspeed.mixin']


class AccountTax(models.Model):
    _name = 'account.tax'
    _inherit = ['account.tax','lightspeed.mixin']


    @api.model
    def create(self, vals):
        res = super().create(vals)
        if res.shop_id:
            res.shop_id._create_tax(tax_id=res.id)
        return res


