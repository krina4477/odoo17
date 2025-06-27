# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.import datetime
from odoo import fields, models,api, _
from odoo.exceptions import UserError
import datetime


class StockPicking(models.Model):
    _inherit = "stock.picking"

    move_id = fields.Many2one('account.move', string="Credit Notes")


class ReturnPicking(models.TransientModel):
    _inherit = "stock.return.picking"

    journal_id = fields.Many2one('account.journal', string="Journal")

    def create_return_and_credit_note(self):
        if not self.journal_id:
            raise UserError('Please add journal for creating Credit Note!')
            # Search for reference whether it is sale order or purchase order
        reference_order = self.picking_id.sale_id or self.picking_id.purchase_id
        if reference_order and not reference_order.invoice_ids:
            raise UserError('For creating credit note or vendor credit note, order must have an invoice!')

        ret_pick = self.create_returns()
        
        return_picking_id = self.env['stock.picking'].browse(ret_pick['res_id'])
        move_line_ids = return_picking_id.move_line_ids
        
        product_quantity = []
        for line in move_line_ids:
            quantity = line.quantity
            product_quantity.append(quantity)
            
        return_picking_id._compute_show_check_availability()
        return_picking_id.button_validate()
        
        return_products = return_picking_id.move_ids_without_package.mapped(
        'product_id').ids
        
        return_quantity_dict = {}
        for ret_line in return_picking_id.move_ids_without_package:
            if ret_line.product_id not in return_quantity_dict:
                return_quantity_dict[ret_line.product_id.id] = ret_line.quantity
            else:
                return_quantity_dict[ret_line.product_id.id] += ret_line.quantity
        
        invoices = reference_order.invoice_ids.invoice_line_ids.filtered(
            lambda ml: ml.product_id.id in return_products).mapped('move_id')
        
        posted_invoices = invoices.filtered(lambda move: move.state == 'posted')
        
        if not posted_invoices:
            raise UserError('Invoice must be posted before creating Credit Note!')
        
        if ret_pick['name'].startswith('Return') and posted_invoices:
            move_reversal = self.env['account.move.reversal'].with_context(active_model='account.move',
                                                                           product_id=return_products,
                                                                           active_ids=posted_invoices.ids
                                                                           ,return_quantity_context=return_quantity_dict).create({
                'date': datetime.datetime.today().strftime('%Y-%m-%d'),
                'reason': 'refund',
                'journal_id': self.journal_id.id
            })

            reversal = move_reversal.reverse_moves()
            if reversal.get('res_id'):
                reverse_move = self.env['account.move'].browse(reversal['res_id'])
                reverse_move.action_post()



class AccountMove(models.Model):
    _inherit = 'account.move'
    
    @api.model
    def create(self, vals_list):
        return_quantity_dict = self._context.get('return_quantity_context')
        if vals_list.get('line_ids'):
            if self._context.get('product_id', False):
                for record in vals_list.get('line_ids'):
                    if record[2].get('product_id', False):
                        if record[2].get('product_id') in return_quantity_dict:
                            record[2].update({'quantity': return_quantity_dict[int(record[2].get('product_id'))]})
                    if not record[2].get('product_id') in self._context.get('product_id'):
                        vals_list.get('line_ids').remove(record)

        return super().create(vals_list)