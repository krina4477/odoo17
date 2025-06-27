# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api
from collections import defaultdict


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    purchase_line_count = fields.Integer("Purchase line count")

    # @api.onchange('order_line')
    # def _onchange_order_line(self):
    #     ''' generated automated lines for deposit products on onchange instead of create/write, so user can see on
    #     selection of product.'''
    #     if self.purchase_line_count - len(self.order_line) == 1:
    #         self.purchase_line_count -= 1
    #         return {}
    #     values = []
    #
    #     # find lines for non-related product (deposit type not configured)
    #     old_line = self.order_line.filtered(lambda pol: pol.product_id.deposit_type == False)
    #
    #     # iterate thru lines
    #     for order_line in self.order_line.filtered(
    #             lambda pol: pol.product_id.deposit_type == 'has_deposit'):
    #         # add line for bottle product deposit
    #         new_line = order_line.copy_data({'price_unit': order_line.product_id.lst_price})[0]
    #         values.append([0, 0, new_line])
    #         new_line_values = new_line.copy()
    #         # add line for crate product deposit if packaging is defined
    #         if order_line.product_packaging_id:
    #             if order_line.product_packaging_id.deposit_product_id:
    #                 crate_line_values = order_line.copy_data()[0]
    #                 crate_line_values.update({
    #                     'price_unit': order_line.product_packaging_id.deposit_product_id.lst_price,
    #                     'product_packaging_qty': False,
    #                     'product_packaging_id': False,
    #                     'product_qty': order_line.product_packaging_qty,
    #                     'product_id': order_line.product_packaging_id.deposit_product_id.id,
    #                     'name': order_line.product_packaging_id.deposit_product_id.name,
    #                     'taxes_id': [(6, 0, [])]
    #                 })
    #                 values.append([0, 0, crate_line_values])
    #
    #         if order_line.product_id.deposit_type == 'has_deposit' and order_line.product_id.deposit_product_id:
    #             new_line_values = new_line.copy()
    #             new_line_values.update({
    #                 'price_unit': order_line.product_id.deposit_product_id.lst_price,
    #                 'product_packaging_qty': False,
    #                 'product_packaging_id': False,
    #                 'product_qty': order_line.product_qty,
    #                 'product_id': order_line.product_id.deposit_product_id.id or False,
    #                 'name': order_line.product_id.deposit_product_id.name,
    #                 'taxes_id': [(6, 0, [])]
    #             })
    #             values.append([0, 0, new_line_values])
    #         else:
    #             continue
    #
    #     if values:
    #         self.update({'order_line': [(6, 0, [])]})
    #         self.update({'order_line': values, 'purchase_line_count': len(values)})
    #         self.order_line += old_line
    #         # for order in self.order_line:
    #         #     order._product_id_change()

    @api.model_create_multi
    def create(self, vals_list):
        # Create purchase orders
        purchase_orders = super(PurchaseOrder, self).create(vals_list)

        for purchase_order in purchase_orders:
            # Trigger custom logic to process order lines
            purchase_order._apply_order_line_sequence()

        return purchase_orders

    def _apply_order_line_sequence(self):
        """Process order lines to set the sequence field and align with `_onchange_order_line` logic."""
        self.ensure_one()

        # Initialize lists to separate product lines and deposit product lines
        product_lines = []
        deposit_lines = []

        old_line = self.order_line.filtered(lambda pol: not pol.product_id.deposit_type)

        # Iterate through lines to separate products and deposit products
        for order_line in self.order_line.filtered(
                lambda pol: pol.product_id.deposit_type == 'has_deposit'):
            # Add product line
            product_lines.append([0, 0, order_line.copy_data()[0]])

            if order_line.product_packaging_id and order_line.product_packaging_id.deposit_product_id:
                crate_line_values = order_line.copy_data()[0]
                crate_line_values.update({
                    'price_unit': order_line.product_packaging_id.deposit_product_id.lst_price,
                    'product_packaging_qty': False,
                    'product_packaging_id': False,
                    'product_qty': order_line.product_packaging_qty,
                    'product_id': order_line.product_packaging_id.deposit_product_id.id,
                    'name': order_line.product_packaging_id.deposit_product_id.name,
                    'taxes_id': [(6, 0, [])]
                })
                deposit_lines.append([0, 0, crate_line_values])

            if order_line.product_id.deposit_product_id:
                deposit_line_values = order_line.copy_data()[0]
                deposit_line_values.update({
                    'price_unit': order_line.product_id.deposit_product_id.lst_price,
                    'product_packaging_qty': False,
                    'product_packaging_id': False,
                    'product_qty': order_line.product_qty,
                    'product_id': order_line.product_id.deposit_product_id.id,
                    'name': order_line.product_id.deposit_product_id.name,
                    'taxes_id': [(6, 0, [])]
                })
                deposit_lines.append([0, 0, deposit_line_values])

        combined_lines = product_lines + deposit_lines
        merged_dict = defaultdict(lambda: None)

        for record in combined_lines:
            _, _, details = record
            product_id = details['product_id']
            if product_id in merged_dict:
                merged_dict[product_id]['product_qty'] += details['product_qty']
            else:
                merged_dict[product_id] = details.copy()

        merged_data = [[0, 0, details] for details in merged_dict.values()]

        # Update the order lines
        if merged_data:
            self.update({'order_line': [(6, 0, [])]})
            self.update({'order_line': merged_data})
            self.order_line += old_line

        for index, line in enumerate(self.order_line, start=1):
            line.sequence = index

    @api.onchange('order_line')
    def _onchange_order_line(self):
        self._apply_order_line_sequence()
        return {}