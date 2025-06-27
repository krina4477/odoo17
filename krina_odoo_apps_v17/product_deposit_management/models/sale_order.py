# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api
from collections import defaultdict

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    sale_line_count = fields.Integer("Sale line count")

    # @api.onchange('order_line')
    # def _onchange_order_line(self):
    #     if self.sale_line_count - len(self.order_line) == 1:
    #         self.sale_line_count -= 1
    #         return {}
    #     values = []
    #     # find size attribute_id
    #     old_line = self.order_line.filtered(lambda sol: sol.product_id.deposit_type == False)
    #
    #     # iterate thru lines
    #     for order_line in self.order_line.filtered(
    #             lambda sol: sol.product_id.deposit_type == 'has_deposit'):
    #         # import pdb
    #         # pdb.set_trace()
    #         # add line selected by user
    #         new_line = order_line.copy_data()[0]
    #         values.append([0, 0, new_line])
    #         # new_line_values = new_line.copy()
    #         if order_line.product_packaging_id:
    #             if order_line.product_packaging_id.deposit_product_id:
    #                 crate_line_values = order_line.copy_data()[0]
    #                 crate_line_values.update({
    #                     'price_unit': order_line.product_packaging_id.product_id.lst_price,
    #                     'product_packaging_qty': False,
    #                     'product_packaging_id': False,
    #                     'product_uom_qty': order_line.product_packaging_qty,
    #                     'product_id': order_line.product_packaging_id.deposit_product_id.id,
    #                     'name': order_line.product_packaging_id.deposit_product_id.name,
    #                     'tax_id': [(6, 0, [])]
    #                 })
    #                 values.append([0, 0, crate_line_values])
    #
    #         if order_line.product_id.deposit_type == 'has_deposit' and order_line.product_id.deposit_product_id:
    #             new_line_values = new_line.copy()
    #             new_line_values.update({
    #                 'price_unit': order_line.product_id.deposit_product_id.lst_price,
    #                 'product_packaging_qty': False,
    #                 'product_packaging_id': False,
    #                 'product_id': order_line.product_id.deposit_product_id.id,
    #                 'name': order_line.product_id.deposit_product_id.name,
    #                 'tax_id': [(6, 0, [])]
    #             })
    #             values.append([0, 0, new_line_values])
    #         else:
    #             continue
    #     if values:
    #         self.update({'order_line': [(6, 0, [])]})
    #         self.update({'order_line': values, 'sale_line_count': len(values)})
    #         self.order_line += old_line
    #         for order_line in self.order_line:
    #             order_line._onchange_product_id_warning()

    @api.model_create_multi
    def create(self, vals_list):
        # Create sale orders
        sale_orders = super(SaleOrder, self).create(vals_list)

        for sale_order in sale_orders:
            # Trigger custom logic to process order lines
            sale_order._apply_order_line_sequence()

        return sale_orders

    def _apply_order_line_sequence(self):
        """Process order lines to set the sequence field and align with `_onchange_order_line` logic."""
        self.ensure_one()

        # Initialize lists to separate product lines and deposit product lines
        product_lines = []
        deposit_lines = []
        merged_dict = defaultdict(lambda: None)

        old_line = self.order_line.filtered(lambda sol: not sol.product_id.deposit_type)

        # Iterate through lines to separate products and deposit products
        for order_line in self.order_line.filtered(
                lambda sol: sol.product_id.deposit_type == 'has_deposit'):
            # Add product line
            product_lines.append([0, 0, order_line.copy_data()[0]])

            if order_line.product_packaging_id and order_line.product_packaging_id.deposit_product_id:
                crate_line_values = order_line.copy_data()[0]
                crate_line_values.update({
                    'price_unit': order_line.product_packaging_id.product_id.lst_price,
                    'product_packaging_qty': False,
                    'product_packaging_id': False,
                    'product_uom_qty': order_line.product_packaging_qty,
                    'product_id': order_line.product_packaging_id.deposit_product_id.id,
                    'name': order_line.product_packaging_id.deposit_product_id.name,
                    'tax_id': [(6, 0, [])]
                })
                deposit_lines.append([0, 0, crate_line_values])

            if order_line.product_id.deposit_product_id:
                deposit_line_values = order_line.copy_data()[0]
                deposit_line_values.update({
                    'price_unit': order_line.product_id.deposit_product_id.lst_price,
                    'product_packaging_qty': False,
                    'product_packaging_id': False,
                    'product_id': order_line.product_id.deposit_product_id.id,
                    'name': order_line.product_id.deposit_product_id.name,
                    'tax_id': [(6, 0, [])]
                })
                deposit_lines.append([0, 0, deposit_line_values])

        combined_lines = product_lines + deposit_lines
        for record in combined_lines:
            _, _, details = record
            product_id = details['product_id']
            if product_id in merged_dict:
                merged_dict[product_id]['product_uom_qty'] += details['product_uom_qty']
            else:
                merged_dict[product_id] = details.copy()

        merged_data = [[0, 0, details] for details in merged_dict.values()]

        # Update order lines with merged data and reattach old lines
        if merged_data:
            self.update({'order_line': [(6, 0, [])]})
            self.update({'order_line': merged_data})
            self.order_line += old_line

        # # Update the order lines
        # if combined_lines:
        #     self.update({'order_line': [(6, 0, [])]})
        #     self.update({'order_line': combined_lines})
        #     self.order_line += old_line  # Re-attach the old lines

        for index, line in enumerate(self.order_line, start=1):
            line.sequence = index

    @api.onchange('order_line')
    def _onchange_order_line(self):
        self._apply_order_line_sequence()
        return {}
