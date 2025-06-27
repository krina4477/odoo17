# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

from odoo import models, api, _, fields


class ResPartner(models.Model):
    _name = "res.partner"
    _inherit = ["res.partner","lightspeed.mixin"]

    lightspeed_type = fields.Selection([
                        ('customer','Customer'),
                        ('supplier','Supplier'),
                    ],default='customer',string='Lightspeed Type')



    @api.model
    def create(self, vals):
        res = super(ResPartner, self).create(vals)
        print("+====================", self._context.get('default_supplier_rank'))
        if self._context.get('default_supplier_rank') == 1 and res.shop_id:
            res.shop_id._create_vendor(vendor_id=res.id)
        elif res.shop_id:
            res.shop_id._create_customer(customer_id=res.id)

        return res


    def write(self,vals):
        res = super().write(vals)
        for rec in self:
            if rec.supplier_rank > 0 and rec.shop_id and rec.lightspeed_id:
                rec.shop_id._update_vendor(vendor_id=rec.id)
        return res
