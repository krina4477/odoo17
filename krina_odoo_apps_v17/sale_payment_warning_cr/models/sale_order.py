# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

from odoo import models, api,_
from odoo.exceptions import UserError, AccessError
from datetime import datetime, date, timedelta


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        base_warning = self.env["ir.config_parameter"].sudo().get_param(
            "sale_payment_warning_cr.add_warning_on_sale")
        if base_warning:
            for order in self:
                if order.payment_term_id:
                    for line in order.payment_term_id.line_ids:
                        # before_date = datetime.today() - timedelta(days=line.days)
                        before_date = datetime.today() - timedelta(days=1)
                        print("before_date::",before_date)

                        invoices = self.env['account.move'].search(
                            [('partner_id', '=', self.partner_id.id), ('invoice_date', '<=', before_date),
                             ('payment_state', '!=', 'paid'),('move_type','=','out_invoice')])
                        if invoices:
                            print("if --")
                            raise UserError(_("Partner not paid due payment!!"))
        return res
