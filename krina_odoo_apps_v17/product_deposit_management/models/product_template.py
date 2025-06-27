# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    

    def _compute_sale_order_line_count(self):
        for product in self:
            product.sale_order_line_count = self.env['sale.order.line'].search_count(
                [('product_template_id', '=', product.id), ('qty_delivered', '>', 0)])

    def _compute_purchase_order_line_count(self):
        for product in self:
            product_template_id = self.env['product.product'].search([('product_tmpl_id', '=', product.id)])
            product.purchase_order_line_count = self.env['purchase.order.line'].search_count(
                [('product_id', 'in', product_template_id.ids), ('qty_received', '>', 0)])

    sale_order_line_count = fields.Integer(compute='_compute_sale_order_line_count', string='Sale Order Count')
    purchase_order_line_count = fields.Integer(compute='_compute_purchase_order_line_count',
                                               string='Purchase Order Count')
    deposit_type = fields.Selection(
        selection=[('has_deposit', 'Contains Deposit'), ('deposit_product', 'Deposit Product')])
    deposit_product_id = fields.Many2one('product.product', copy=False)

    @api.onchange('deposit_type')
    def _onchange_deposit_type(self):
        if self.deposit_type and self.deposit_type != 'has_deposit':
            self.deposit_product_id = False

    def action_view_sale_order_line(self):
        action = self.env['ir.actions.act_window']._for_xml_id(
            'product_deposit_management.act_product_template_2_sale_order_lines')
        action['domain'] = [('product_template_id.id', '=', self.id), ('qty_delivered', '>', 0)]
        return action

    def action_view_purchase_order_line(self):
        product_template_id = self.env['product.product'].search([('product_tmpl_id', '=', self.id)])
        action = self.env['ir.actions.act_window']._for_xml_id(
            'product_deposit_management.act_product_template_2_purchase_order_lines')
        action['domain'] = [('product_id', '=', product_template_id.id), ('qty_received', '>', 0)]
        return action


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def action_view_sale_order_line(self):
        action = self.env['ir.actions.act_window']._for_xml_id(
            'product_deposit_management.act_product_template_2_sale_order_lines')
        action['domain'] = [('product_id.id', '=', self.id), ('qty_delivered', '>', 0)]
        return action

    def action_view_purchase_order_line(self):
        action = self.env['ir.actions.act_window']._for_xml_id(
            'product_deposit_management.act_product_template_2_purchase_order_lines')
        action['domain'] = [('product_id', '=', self.id), ('qty_received', '>', 0)]
        return action
