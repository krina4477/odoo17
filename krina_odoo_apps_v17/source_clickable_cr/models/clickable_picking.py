# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
from odoo import api, models, fields, _


class Picking(models.Model):
    _inherit = "stock.picking"
    _description = "Transfer"

    @api.model
    def create(self, vals):
        res = super(Picking, self).create(vals)
        if 'origin' in vals and res:
            origin_val = vals.get('origin')

            sale_id = self.env['sale.order'].search([('name', '=', origin_val)]).id
            if sale_id:
                res.origin = "%s,%s" % ('sale.order', sale_id)


            purchase_id = self.env['purchase.order'].search([('name', '=', origin_val)]).id
            if purchase_id:
                res.origin = "%s,%s" % ('purchase.order', purchase_id)


            manufacturing_id = self.env['mrp.production'].search([('name', '=', origin_val)]).id
            if manufacturing_id:
                res.origin = "%s,%s" % ('mrp.production', manufacturing_id)
        return res


# =================SO To PO=====================


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.model
    def create(self, vals):
        res = super(PurchaseOrder, self).create(vals)
        if 'origin' in vals:
            origin_val = vals.get('origin')
            sale_id = self.env['sale.order'].search([('name', '=', origin_val)]).id
            res['origin'] = "%s,%s" % ('sale.order', sale_id)
        return res


    def write(self, vals):
        if 'origin' in vals:
            origin_val = vals.get('origin')
            sale_names = origin_val.split(',')
            name = str(sale_names[-1])
            ogn = name.strip()
            sale_id = self.env['sale.order'].search([('name', '=', ogn)]).id
            vals['origin'] = "%s,%s" % ('sale.order', sale_id)
        return  super(PurchaseOrder, self).write(vals)


# ============================SO to MO===========================


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    @api.model
    def create(self, vals):
        res = super(MrpProduction, self).create(vals)
        if 'origin' in vals and res:
            origin_val = vals.get('origin')
            sale_id = self.env['sale.order'].search([('name', '=', origin_val)]).id
            if sale_id:
                res.origin = "%s,%s" % ('sale.order', sale_id)
        return res


