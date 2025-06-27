# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, fields, api

class ProductTemplateAttributeValue(models.Model):
    _inherit = 'product.template.attribute.value'

    @api.model
    def create(self, vals):
        if self._context.get('skip_log'):
            return super(ProductTemplateAttributeValue, self).create(vals)
        res = super(ProductTemplateAttributeValue, self).create(vals)
        if res.id:
            self.env['product.attribute.value.update'].broadcast_product_template_attribute_value(res)
        return res

    def write(self, vals):
        if self._context.get('skip_log'):
            return super(ProductTemplateAttributeValue, self).write(vals)

        if 'active' in vals and vals.get('active') == False:
            for rec in self:
                self.env['product.attribute.value.update'].sudo().create({'delete_ids': str(rec.id)})

        for rec in self:
            delete_ids = self.env['product.attribute.value.update'].sudo().search([('delete_ids', '=', str(rec.id))])
            if delete_ids:
                delete_ids.sudo().unlink()
            self.env['product.attribute.value.update'].broadcast_product_template_attribute_value(rec)

        res = super(ProductTemplateAttributeValue, self).write(vals)
        for rec in self:
            self.env['product.attribute.value.update'].broadcast_product_template_attribute_value(rec)
        return res

    def unlink(self):
        if self._context.get('skip_log'):
            return super(ProductTemplateAttributeValue, self).unlink()

        for rec in self:
            self.env['product.attribute.value.update'].sudo().create({'delete_ids': str(rec.id)})
        res = super(ProductTemplateAttributeValue, self).unlink()
        return res

class ProductAttributeValueUpdate(models.Model):
    _name = 'product.attribute.value.update'
    _description = 'Product Attribute Update'

    delete_ids = fields.Char("Delete Ids")

    def broadcast_product_template_attribute_value(self, attribute_value):
        if attribute_value.id:
            fields = ['attribute_id', 'name', 'product_attribute_value_id', 'write_date', 'id', 'display_name']
            data = attribute_value.read(fields)
            if data and len(data) > 0:
                pos_session = self.env['pos.session'].search([('state', 'in', ['opened', 'opening_control'])])
                if pos_session:
                    for each_session in pos_session:
                        self.env['bus.bus']._sendmany(
                            [[each_session.user_id.partner_id, 'product_attribute_update', data]]
                        )
