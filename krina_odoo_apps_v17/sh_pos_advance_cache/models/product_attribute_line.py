# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, fields, api

class ProductTemplateAttributeLine(models.Model):
    _inherit = 'product.template.attribute.line'

    @api.model
    def create(self, vals):
        if self._context.get('skip_log'):
            return super(ProductTemplateAttributeLine, self).create(vals)

        res = super(ProductTemplateAttributeLine, self).create(vals)
        if res.id:
            self.env['product.template.attribute.line.update'].broadcast_product_template_attribute_line(res)
        return res

    def write(self, vals):
        if self._context.get('skip_log'):
            return super(ProductTemplateAttributeLine, self).write(vals)
        if 'active' in vals and vals.get('active') == False:
            for rec in self:
                self.env['product.template.attribute.line.update'].sudo().create({'delete_ids': str(rec.id)})

        for rec in self:
            delete_ids = self.env['product.template.attribute.line.update'].sudo().search([('delete_ids', '=', str(rec.id))])
            if delete_ids:
                delete_ids.sudo().unlink()
            self.env['product.template.attribute.line.update'].broadcast_product_template_attribute_line(rec)

        res = super(ProductTemplateAttributeLine, self).write(vals)
        for rec in self:
            self.env['product.template.attribute.line.update'].broadcast_product_template_attribute_line(rec)
        return res

    def unlink(self):
        if self._context.get('skip_log'):
            return super(ProductTemplateAttributeLine, self).unlink()


        for rec in self:
            self.env['product.template.attribute.line.update'].sudo().create({'delete_ids': str(rec.id)})
        res = super(ProductTemplateAttributeLine, self).unlink()
        return res


class ProductAttributeUpdate(models.Model):
    _name = 'product.template.attribute.line.update'
    _description = 'Product Attribute Update'

    delete_ids = fields.Char("Delete Ids")

    def broadcast_product_template_attribute_line(self, attribute_line):

        if attribute_line.id:
            fields = ['product_template_value_ids', 'product_tmpl_id', 'value_ids', 'write_date','attribute_id','id']
            data = attribute_line.read(fields)
            if data and len(data) > 0:
                pos_session = self.env['pos.session'].search([('state', 'in', ['opened', 'opening_control'])])
                if pos_session:
                    for each_session in pos_session:
                        self.env['bus.bus']._sendmany(
                            [[each_session.user_id.partner_id, 'product_attribute_line_update', data]]
                        )
