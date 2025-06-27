# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _
from itertools import groupby
from odoo.osv.expression import OR

class PosSession(models.Model):
    _inherit = 'pos.session'
    
    def _loader_params_product_product(self):
        result = super()._loader_params_product_product()
        result['search_params']['fields'].append('combo_products')
        result['search_params']['fields'].append('is_combo_deal')        
        return result
    

    def _get_attributes_by_ptal_id(self):
        res = super()._get_attributes_by_ptal_id()

        product_attributes = self.env['product.attribute'].search_fetch(
            [('create_variant', '=', 'no_variant')],
            ['name', 'display_type'],
        )
        product_template_attribute_values = self.env['product.template.attribute.value'].search_fetch(
            [('attribute_id', 'in', product_attributes.ids)],
            ['attribute_id', 'attribute_line_id', 'product_attribute_value_id', 'price_extra'],
        )
        product_template_attribute_values.product_attribute_value_id.fetch(['name', 'is_custom', 'html_color', 'image'])

        key1 = lambda ptav: (ptav.attribute_line_id.id, ptav.attribute_id.id)
        key2 = lambda ptav: (ptav.attribute_line_id.id, ptav.attribute_id)
        res = {}
        for key, group in groupby(sorted(product_template_attribute_values, key=key1), key=key2):
            attribute_line_id, attribute = key
            values = [{**ptav.product_attribute_value_id.read(['name', 'is_custom', 'html_color', 'image'])[0],
                       'price_extra': ptav.price_extra,
                       # id of a value should be from the "product.template.attribute.value" record
                       'id': ptav.id,
                       } for ptav in list(group)]

            res[attribute_line_id] = {
                'id': attribute_line_id,
                "not_mandatory" :  attribute.not_mandatory,
                'name': attribute.name,
                'display_type': attribute.display_type,
                'values': values,
                'sequence': attribute.sequence,
            }

        return res  
    
class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    not_mandatory = fields.Boolean(string="Is Optional",default=False)


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_combo_deal = fields.Boolean(string="Is Combo Deal",default=False)
    combo_deals_id = fields.Many2one('combo.deals',string="Combo Deals")
    combo_products = fields.Char(string="Combo Products",compute="fetch_combo_products",store=True)

    @api.depends('combo_deals_id','combo_deals_id.combo_line_ids','combo_deals_id.combo_line_ids.product_id')
    def fetch_combo_products(self):
        for rec in self:
            if rec.combo_deals_id:
                combo_line_products = rec.combo_deals_id.mapped('combo_line_ids.product_id.name')
                combo_line_products = str(combo_line_products).replace('[', '"').replace(']', '"')
                combo_line_products = combo_line_products.replace("'", "").replace('"', '')
                rec.combo_products = combo_line_products
            else:
                rec.combo_products = ''

class PosConfig(models.Model):
    _inherit = 'pos.config'
    def _get_available_product_domain(self):
        domain = super()._get_available_product_domain()
        return OR([domain, [('is_combo_deal', '=', True)]])