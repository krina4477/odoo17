# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleMailConfirmation(WebsiteSale):

    @http.route('/shop/payment/validate', type='http', auth="public", website=True, sitemap=False)
    def shop_payment_validate(self, transaction_id=None, sale_order_id=None, **post):
        sale_order_id = request.session.get('sale_last_order_id')
        last_transaction_records = []
        if sale_order_id:
            order = request.env['sale.order'].sudo().browse(sale_order_id)
            transaction_record = request.env['payment.transaction'].search([])
            for rec in transaction_record:
                last_transaction_records.append(rec)
            reason_rec = request.env['payment.link.wizard'].sudo().with_context(
                {'active_id': int(order.id), 'active_model': 'sale.order'}).create(
                {'amount': order.amount_total, 'res_model': 'sale.order',
                 'res_id': int(order.id), 'currency_id': order.currency_id.id, 'partner_id': order.partner_id.id})
            if last_transaction_records[0].state != 'done':
                last_transaction_records[0].state = 'error'
                last_transaction_records[0].state_message = 'Your card was declined.'
                template_id = request.env.ref('payment_reminder_cr.payment_failed_template').id
                template = request.env['mail.template'].sudo().browse(template_id)
                template.with_context(link=reason_rec.link).send_mail(last_transaction_records[0].id, force_send=True)
        return request.redirect('/shop/confirmation')
