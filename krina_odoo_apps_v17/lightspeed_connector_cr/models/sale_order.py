# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
from odoo import models, api, fields, _


class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = ['sale.order', 'lightspeed.mixin']

    lightspeed_state = fields.Boolean(srting='Completed')

    def _prepare_invoice(self):
        res = super(SaleOrder, self)._prepare_invoice()
        if self.lightspeed_id:
            res.update({
                'ref': self.name,
                'payment_reference': self.name,
                # 'lightspeed_id': self.lightspeed_id,
                # 'shop_id': self.shop_id.id,
            })
        return res

    def _cron_update_payment_status_lightspeed(self):
        shops = self.env['lightspeed.shop'].search([])
        for shop in shops:
            orders_result = shop.lightspeed_get_response_by_type('Sale', 'orders', params={})
            if orders_result:
                for order in orders_result:
                    if order['completed'] == 'true':
                        sale_order = self.env['sale.order'].search([('lightspeed_id', '=', order.get('saleID')),
                                                                    ('shop_id', '=', shop.id),
                                                                    ('state', '=', 'draft')], limit=1)
                        if sale_order:
                            if shop.do_complete:
                                sale_order.action_confirm()
                            if shop.invoice_complete:
                                if not sale_order.invoice_ids:
                                    sale_order._create_invoices()
                                if sale_order.invoice_ids:
                                    for invoice in sale_order.invoice_ids:
                                        invoice.action_post()
                            if shop.payment_complete:
                                self.env['account.payment.register'].with_context(active_model='account.move',
                                                                                  active_ids=sale_order.invoice_ids.ids).create(
                                    {
                                        'group_payment': True,
                                    })._create_payments()


class SaleOrderLine(models.Model):
    _name = 'sale.order.line'
    _inherit = ['sale.order.line', 'lightspeed.mixin']
