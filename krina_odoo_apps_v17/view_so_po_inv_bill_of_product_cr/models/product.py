# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

from odoo import models, _, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    sale_order_count = fields.Char('so_count', compute='count_sale_order')
    order_id = fields.Many2one('sale.order')
    purchase_order_count = fields.Char('Po_count', compute='count_purchase_order')
    puchase_id = fields.Many2one('purchase.order')
    vendor_bills_count = fields.Char('Vendor Bill Count', compute='count_bills')
    invoice_id = fields.Many2one('account.move')
    invoice_count = fields.Char('Invoice Count', compute='count_invoices')

    def action_view_saleorder(self):
        self.ensure_one()
        tree_id = self.env.ref('sale.view_order_tree').id
        form_id = self.env.ref('sale.view_order_form').id

        return {'type': 'ir.actions.act_window',
                'name': _('Sale Order'),
                'res_model': 'sale.order',
                'view_mode': 'tree,form',
                'views': [(tree_id, 'tree'), (form_id, 'form')],
                'domain': [('order_line.product_id.name', 'ilike', self.display_name),('state','in',['sale','done','cancel'])]
                }

    def action_view_purchaseorder(self):
        self.ensure_one()
        tree_id = self.env.ref('purchase.purchase_order_tree').id
        form_id = self.env.ref('purchase.purchase_order_form').id

        return {'type': 'ir.actions.act_window',
                'name': _('Purchase Order'),
                'res_model': 'purchase.order',
                'view_mode': 'tree,form',
                'views': [(tree_id, 'tree'), (form_id, 'form')],
                'domain': [('order_line.product_id.name', 'ilike', self.display_name),('state','in',['purchase','done','cancel'])]
                }

    def action_view_invoices(self):
        self.ensure_one()
        tree_id = self.env.ref('account.view_invoice_tree').id
        form_id = self.env.ref('account.view_move_form').id

        return {'type': 'ir.actions.act_window',
                'name': _('Customer Invoices'),
                'res_model': 'account.move',
                'view_mode': 'tree,form',
                'views': [(tree_id, 'tree'), (form_id, 'form')],
                'domain': [('invoice_line_ids.product_id.name', '=', self.name), ('move_type', '=', 'out_invoice'),('state','in',['posted','cancel'])]
                }

    def action_view_bills(self):
        self.ensure_one()
        tree_id = self.env.ref('account.view_invoice_tree').id
        form_id = self.env.ref('account.view_move_form').id

        return {'type': 'ir.actions.act_window',
                'name': _('Customer Bills'),
                'res_model': 'account.move',
                'view_mode': 'tree,form',
                'views': [(tree_id, 'tree'), (form_id, 'form')],
                'domain': [('invoice_line_ids.product_id.name', '=', self.name), ('move_type', '=', 'in_invoice'),('state','in',['posted','cancel'])]
                }

    @api.depends('order_id')
    def count_sale_order(self):
        orders = self.env['sale.order'].search_count([('order_line.product_id.name', 'ilike', self.display_name),('state','in',['sale','done','cancel'])])
        for record in self:
            record.sale_order_count = orders

    @api.depends('puchase_id')
    def count_purchase_order(self):
        orders = self.env['purchase.order'].search_count([('order_line.product_id.name', 'ilike', self.display_name),('state','in',['purchase','done','cancel'])])
        for record in self:
            record.purchase_order_count = orders

    @api.depends('invoice_id')
    def count_invoices(self):
        orders = self.env['account.move'].search_count(
            [('invoice_line_ids.product_id.name', '=', self.name), ('move_type', '=', 'out_invoice'),('state','in',['posted','cancel'])])
        for record in self:
            record.invoice_count = orders

    @api.depends('invoice_id')
    def count_bills(self):
        orders = self.env['account.move'].search_count(
            [('invoice_line_ids.product_id.name', '=', self.name), ('move_type', '=', 'in_invoice'),('state','in',['posted','cancel'])])
        for record in self:
            record.vendor_bills_count = orders
