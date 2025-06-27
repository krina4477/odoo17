# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = "product.template"

    attachment_ids = fields.Many2many('ir.attachment',string="Attachment")

    @api.onchange('attachment_ids')
    def _onchange_attachment_ids(self):
        for rec in self:
            if rec.attachment_ids.ids:
                attchment_rec = self.env['ir.attachment'].browse(rec.attachment_ids.ids)
                for line in attchment_rec:
                    if not line.res_id:
                        if rec.default_code:
                            name = '['+rec.default_code+'] '+rec.name
                        else:
                            name = rec.name
                        line.sudo().write({ 'res_id': self._origin.id,
                                            'product_name': rec.name,
                                            'res_name': name})


class IrAttachment(models.Model):
    _inherit = "ir.attachment"

    product_name = fields.Char(string="Product Name")

    @api.model
    def default_get(self,values):
        res = super(IrAttachment,self).default_get(values)
        res.update({'res_model':'product.template',
                    'public': True})
        return res

    @api.model
    def create(self,values):
        res = super(IrAttachment,self).create(values)
        if res.res_model == 'product.template' and res.res_id and res.res_name:
            product_rec = self.env['product.template'].browse(int(res.res_id))
            res.product_name = product_rec.name
        return res