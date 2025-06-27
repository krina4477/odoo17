# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
import datetime
from odoo import fields, models, _
from odoo.exceptions import UserError,ValidationError

#CustomAccountMove
from collections import defaultdict
from odoo.exceptions import UserError, ValidationError, AccessError, RedirectWarning
from odoo.tools import (
    float_compare,
    format_date,
    formatLang,
    get_lang,
)




class StockPicking(models.Model):
    _inherit = "stock.picking"

    move_id = fields.Many2one('account.move', string="Credit Notes")


class ReturnPicking(models.TransientModel):
    _inherit = "stock.return.picking"

    journal_id = fields.Many2one('account.journal', string="Journal")

    def create_return_and_credit_note(self):
        context = self._context.copy()
        context.update({'sale': True})        
        if not self.journal_id:
            raise UserError('Please add journal for creating Credit Note!')

        # Search for reference whether it is sale order or purchase order
        reference_order = self.picking_id.sale_id or self.picking_id.purchase_id
        if reference_order and not reference_order.invoice_ids:
            raise UserError('For creating credit note or vendor credit note, order must have an invoice!')

        # Create returns and validate
        ret_pick = self.action_create_returns()
        return_picking_id = self.env['stock.picking'].browse(ret_pick['res_id'])
        return_picking_id.button_validate()

        return_products = return_picking_id.move_ids_without_package.mapped(
            'product_id').ids

        invoices = reference_order.invoice_ids.invoice_line_ids.filtered(
            lambda ml: ml.product_id.id in return_products).mapped('move_id')

        posted_invoices = invoices.filtered(lambda move: move.state == 'posted')
        if  not posted_invoices:
            raise UserError('Invoice must be posted before creating Credit Note!')

        # Generate credit note with the same product line only .
        if ret_pick['name'].startswith('Return') and posted_invoices:
            move_reversal = self.env['account.move.reversal'].with_context(active_model='account.move',
                                                                           active_ids=posted_invoices.ids).create({
                'date': datetime.datetime.today().strftime('%Y-%m-%d'),
                'journal_id': self.journal_id.id
            })

            move_reversal.reverse_moves()
            invoice_ref = reference_order.invoice_ids.sorted(key=lambda inv: inv.id, reverse=False)[-1]
        
            invoice_ref and invoice_ref.invoice_line_ids.with_context(check_move_validity=False).write({'quantity': 0})
            for move_line in self.product_return_moves:
                lines = invoice_ref.invoice_line_ids.filtered(
                    lambda line: line.product_id == move_line.product_id and line.quantity == 0)
                if lines and lines[0]:
                    lines[0].with_context(check_move_validity=False).write({'quantity': move_line.quantity})
            
                    
            invoice_ref.invoice_line_ids.with_context(test=True).filtered(lambda line: line.quantity == 0).with_context(
                check_move_validity=False).unlink()
            # invoice_ref.with_context(sale=True).action_post()
            invoice_ref.action_post()
            
            # If invoice/vendor bill is paid, credit note will be paid when click on Credte Credit note and Return.
            if posted_invoices.amount_residual == 0:
                self.env['account.payment.register'].with_context(active_model='account.move',
                                                                  active_ids=[invoice_ref.id]).create({
                    'payment_date': invoice_ref.date,
                })._create_payments()
        

class CustomAccountMove(models.Model):
    _inherit = 'account.move'


    def _post(self, soft=True):
        """Post/Validate the documents.

        Posting the documents will give it a number, and check that the document is
        complete (some fields might not be required if not posted but are required
        otherwise).
        If the journal is locked with a hash table, it will be impossible to change
        some fields afterwards.

        :param soft (bool): if True, future documents are not immediately posted,
            but are set to be auto posted automatically at the set accounting date.
            Nothing will be performed on those documents before the accounting date.
        :return Model<account.move>: the documents that have been posted
        """
        if not self.env.su and not self.env.user.has_group('account.group_account_invoice'):
            raise AccessError(_("You don't have the access rights to post an invoice."))

        for invoice in self.filtered(lambda move: move.is_invoice(include_receipts=True)):
            if invoice.quick_edit_mode and invoice.quick_edit_total_amount and invoice.quick_edit_total_amount != invoice.amount_total:
                raise UserError(_(
                    "The current total is %s but the expected total is %s. In order to post the invoice/bill, "
                    "you can adjust its lines or the expected Total (tax inc.).",
                    formatLang(self.env, invoice.amount_total, currency_obj=invoice.currency_id),
                    formatLang(self.env, invoice.quick_edit_total_amount, currency_obj=invoice.currency_id),
                ))
            if invoice.partner_bank_id and not invoice.partner_bank_id.active:
                raise UserError(_(
                    "The recipient bank account linked to this invoice is archived.\n"
                    "So you cannot confirm the invoice."
                ))
            if float_compare(invoice.amount_total, 0.0, precision_rounding=invoice.currency_id.rounding) < 0:
                raise UserError(_(
                    "You cannot validate an invoice with a negative total amount. "
                    "You should create a credit note instead. "
                    "Use the action menu to transform it into a credit note or refund."
                ))

            if not invoice.partner_id:
                if invoice.is_sale_document():
                    raise UserError(_("The field 'Customer' is required, please complete it to validate the Customer Invoice."))
                elif invoice.is_purchase_document():
                    raise UserError(_("The field 'Vendor' is required, please complete it to validate the Vendor Bill."))

            # Handle case when the invoice_date is not set. In that case, the invoice_date is set at today and then,
            # lines are recomputed accordingly.
            if not invoice.invoice_date:
                if invoice.is_sale_document(include_receipts=True):
                    invoice.invoice_date = fields.Date.context_today(self)
                elif invoice.is_purchase_document(include_receipts=True):
                    raise UserError(_("The Bill/Refund date is required to validate this document."))

        for move in self:
            # if not self._context.get('sale'):
            if move.state in ['posted', 'cancel']:
                raise UserError('The entry %s (id %s) must be in draft.', move.name, move.id)
            if not move.line_ids.filtered(lambda line: line.display_type not in ('line_section', 'line_note')):
                raise UserError(_('You need to add a line before posting.'))
            if not soft and move.auto_post != 'no' and move.date > fields.Date.context_today(self):
                date_msg = move.date.strftime(get_lang(self.env).date_format)
                raise UserError(_("This move is configured to be auto-posted on %s", date_msg))
            if not move.journal_id.active:
                raise UserError(_(
                    "You cannot post an entry in an archived journal (%(journal)s)",
                    journal=move.journal_id.display_name,
                ))
            if move.display_inactive_currency_warning:
                raise UserError(_(
                    "You cannot validate a document with an inactive currency: %s",
                    move.currency_id.name
                ))

            if move.line_ids.account_id.filtered(lambda account: account.deprecated) and not self._context.get('skip_account_deprecation_check'):
                raise UserError(_("A line of this move is using a deprecated account, you cannot post it."))

        if soft:
            future_moves = self.filtered(lambda move: move.date > fields.Date.context_today(self))
            for move in future_moves:
                if move.auto_post == 'no':
                    move.auto_post = 'at_date'
                msg = _('This move will be posted at the accounting date: %(date)s', date=format_date(self.env, move.date))
                move.message_post(body=msg)
            to_post = self - future_moves
        else:
            to_post = self

        for move in to_post:
            affects_tax_report = move._affect_tax_report()
            lock_dates = move._get_violated_lock_dates(move.date, affects_tax_report)
            if lock_dates:
                move.date = move._get_accounting_date(move.invoice_date or move.date, affects_tax_report)

        # Create the analytic lines in batch is faster as it leads to less cache invalidation.
        to_post.line_ids._create_analytic_lines()

        # Trigger copying for recurring invoices
        to_post.filtered(lambda m: m.auto_post not in ('no', 'at_date'))._copy_recurring_entries()

        for invoice in to_post:
            # Fix inconsistencies that may occure if the OCR has been editing the invoice at the same time of a user. We force the
            # partner on the lines to be the same as the one on the move, because that's the only one the user can see/edit.
            wrong_lines = invoice.is_invoice() and invoice.line_ids.filtered(lambda aml:
                aml.partner_id != invoice.commercial_partner_id
                and aml.display_type not in ('line_note', 'line_section')
            )
            if wrong_lines:
                wrong_lines.write({'partner_id': invoice.commercial_partner_id.id})

        # reconcile if state is in draft and move has reversal_entry_id set
        draft_reverse_moves = to_post.filtered(lambda move: move.reversed_entry_id and move.reversed_entry_id.state == 'posted')

        to_post.write({
            'state': 'posted',
            'posted_before': True,
        })

        draft_reverse_moves.reversed_entry_id._reconcile_reversed_moves(draft_reverse_moves, self._context.get('move_reverse_cancel', False))
        to_post.line_ids._reconcile_marked()

        for invoice in to_post:
            invoice.message_subscribe([
                p.id
                for p in [invoice.partner_id]
                if p not in invoice.sudo().message_partner_ids
            ])

            if (
                invoice.is_sale_document()
                and invoice.journal_id.activity_type_id
                and (invoice.journal_id.sale_activity_user_id or invoice.invoice_user_id).id not in (self.env.ref('base.user_root').id, False)
            ):
                invoice.activity_schedule(
                    date_deadline=min((date for date in invoice.line_ids.mapped('date_maturity') if date), default=invoice.date),
                    activity_type_id=invoice.journal_id.activity_type_id.id,
                    summary=invoice.journal_id.sale_activity_note,
                    user_id=invoice.journal_id.sale_activity_user_id.id or invoice.invoice_user_id.id,
                )

        customer_count, supplier_count = defaultdict(int), defaultdict(int)
        for invoice in to_post:
            if invoice.is_sale_document():
                customer_count[invoice.partner_id] += 1
            elif invoice.is_purchase_document():
                supplier_count[invoice.partner_id] += 1
            elif invoice.move_type == 'entry':
                sale_amls = invoice.line_ids.filtered(lambda line: line.partner_id and line.account_id.account_type == 'asset_receivable')
                for partner in sale_amls.mapped('partner_id'):
                    customer_count[partner] += 1
                purchase_amls = invoice.line_ids.filtered(lambda line: line.partner_id and line.account_id.account_type == 'liability_payable')
                for partner in purchase_amls.mapped('partner_id'):
                    supplier_count[partner] += 1
        for partner, count in customer_count.items():
            (partner | partner.commercial_partner_id)._increase_rank('customer_rank', count)
        for partner, count in supplier_count.items():
            (partner | partner.commercial_partner_id)._increase_rank('supplier_rank', count)

        # Trigger action for paid invoices if amount is zero
        to_post.filtered(
            lambda m: m.is_invoice(include_receipts=True) and m.currency_id.is_zero(m.amount_total)
        )._invoice_paid_hook()

        return to_post

