# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'


    def _compute_sale_order_line_count(self):
        for partner in self:
            partner.sale_order_line_count = self.env['sale.order.line'].search_count(
                [('order_partner_id', '=', partner.id), ('qty_delivered', '>', 0)]
            )

    def _compute_purchase_order_line_count(self):
        for partner in self:
            partner.purchase_order_line_count = self.env['purchase.order.line'].search_count(
                [('partner_id', '=', partner.id), ('qty_received', '>', 0)]
            )

    sale_order_line_count = fields.Integer(compute='_compute_sale_order_line_count', string='Sale Order Count')
    purchase_order_line_count = fields.Integer(compute='_compute_purchase_order_line_count',
                                               string='Purchase Order Count')

    def action_view_sale_order_line(self):
        action = self.env['ir.actions.act_window']._for_xml_id(
            'product_deposit_management.act_res_partner_2_sale_order_lines')
        action['domain'] = [('order_partner_id.id', '=', self.id), ('qty_delivered', '>', 0)]
        return action

    def action_view_purchase_order_line(self):
        action = self.env['ir.actions.act_window']._for_xml_id(
            'product_deposit_management.act_res_partner_2_purchase_order_lines')
        action['domain'] = [('partner_id.id', '=', self.id), ('qty_received', '>', 0)]
        return action
