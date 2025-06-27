# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

from odoo import models,api,fields,_
import json

class AccountMove(models.Model):
    _inherit = "account.move"

    invoice_outstanding_credits_debits_widget_custom = fields.Text(

        compute='_compute_payments_widget_to_reconcile_info_1',
    )
    def _compute_payments_widget_to_reconcile_info_1(self):
        for move in self:
            move.invoice_outstanding_credits_debits_widget_custom = json.dumps(False)
            move.invoice_has_outstanding = False

            if move.state != 'posted' \
                    or move.payment_state not in ('not_paid', 'partial') \
                    or not move.is_invoice(include_receipts=True):
                continue

            pay_term_lines = move.line_ids \
                .filtered(lambda line: line.account_id.account_type in ('asset_receivable', 'liability_payable'))
            domain = [
                ('account_id', 'in', pay_term_lines.account_id.ids),
                ('parent_state', '=', 'posted'),
                ('partner_id', '=', move.commercial_partner_id.id),
                ('reconciled', '=', False),
                '|', ('amount_residual', '!=', 0.0), ('amount_residual_currency', '!=', 0.0),
            ]
            payments_widget_vals = {'outstanding': True, 'content': [], 'move_id': move.id}

            if move.is_inbound():
                domain.append(('balance', '<', 0.0))
                payments_widget_vals['title'] = _('Outstanding credits')
            else:
                domain.append(('balance', '>', 0.0))
                payments_widget_vals['title'] = _('Outstanding debits')

            for line in self.env['account.move.line'].search(domain):
                if line.currency_id == move.currency_id:
                    # Same foreign currency.
                    amount = abs(line.amount_residual_currency)
                else:
                    # Different foreign currencies.
                    amount = move.company_currency_id._convert(
                        abs(line.amount_residual),
                        move.currency_id,
                        move.company_id,
                        line.date,
                    )

                if move.currency_id.is_zero(amount):
                    continue

                payments_widget_vals['content'].append({
                    'journal_name': line.ref or line.move_id.name,
                    'amount': amount,
                    'currency': move.currency_id.symbol,
                    'id': line.id,
                    'move_id': line.move_id.id,
                    'position': move.currency_id.position,
                    'digits': [69, move.currency_id.decimal_places],
                    'date': fields.Date.to_string(line.date),
                    'account_payment_id': line.payment_id.id,
                })

            if not payments_widget_vals['content']:
                continue

            move.invoice_outstanding_credits_debits_widget_custom = json.dumps(payments_widget_vals)
            move.invoice_has_outstanding = True

    def auto_rencile(self):
        move_ids_list = self.filtered(lambda move: move.state == 'posted')
        for move_id in move_ids_list:
            if not move_id._compute_has_reconciled_entries():
                out_cr_dr = json.loads(move_id.invoice_outstanding_credits_debits_widget_custom)
                if out_cr_dr:
                    for outstand_id in out_cr_dr.get('content'):
                        payment_id = self.env['account.move'].browse(outstand_id['move_id'])
                        pline_id = False
                        if payment_id.move_type == 'entry' and move_id.move_type == 'out_invoice':
                            pline_id = payment_id.line_ids.filtered(lambda line: line.credit > 0 and not line.reconciled)
                        elif payment_id.move_type == 'entry' and move_id.move_type == 'out_refund':
                            pline_id = payment_id.line_ids.filtered(lambda line: line.debit > 0 and not line.reconciled)

                        elif payment_id.move_type == 'entry' and move_id.move_type == 'in_invoice':
                            pline_id = payment_id.line_ids.filtered(lambda line: line.debit > 0 and not line.reconciled)
                        elif payment_id.move_type == 'entry' and move_id.move_type == 'in_refund':
                            pline_id = payment_id.line_ids.filtered(lambda line: line.credit > 0 and not line.reconciled)
                        pline_id and move_id.js_assign_outstanding_line(pline_id.id)

        return True