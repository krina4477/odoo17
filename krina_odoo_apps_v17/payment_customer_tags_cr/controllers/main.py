# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
import json
import logging
import pprint
import werkzeug
from unicodedata import normalize

from odoo import http
from odoo.addons.payment.controllers.portal import PaymentPortal
from odoo.http import request
from odoo.http import request
from odoo.osv import expression
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, consteq, ustr
from odoo.tools.float_utils import float_repr
from datetime import datetime, timedelta
from odoo.addons.sale.controllers.portal import CustomerPortal

_logger = logging.getLogger(__name__)
from odoo.addons.website_sale.controllers.main import WebsiteSale

class WebsiteSale(WebsiteSale):
    def _get_shop_payment_values(self, order, **kwargs):
        res = super(WebsiteSale, self)._get_shop_payment_values(order)
        domain = expression.AND([
            ['&', ('state', 'in', ['enabled', 'test']), ('company_id', '=', order.company_id.id)],
            ['&', ('state', 'in', ['enabled', 'test']), ('company_id', '=', order.company_id.id)],
            ['|', ('website_id', '=', False), ('website_id', '=', request.website.id)],
            ['|', ('country_ids', '=', False), ('country_ids', 'in', [order.partner_id.country_id.id])],
            ['|', ('tag_ids', '=', False), ('tag_ids', 'in', order.partner_id.category_id.ids)]
        ])
        acquirers = request.env['payment.provider'].search(domain)
        res['acquirers'] = [acq for acq in acquirers if (acq.payment_flow == 'form' and acq.view_template_id) or
                            (acq.payment_flow == 's2s' and acq.registration_view_template_id)]
        return res

class CustomerPortal(CustomerPortal):

    def _order_get_page_view_values(self, order, access_token, **kwargs):
        res = super(CustomerPortal, self)._order_get_page_view_values(order, access_token)
        if order.has_to_be_paid():
            domain = expression.AND([
                ['&', ('state', 'in', ['enabled', 'test']), ('company_id', '=', order.company_id.id)],
                ['|', ('country_ids', '=', False), ('country_ids', 'in', [order.partner_id.country_id.id])],
                ['|', ('tag_ids', '=', False), ('tag_ids', 'in', order.partner_id.category_id.ids)]
            ])
            acquirers = request.env['payment.provider'].sudo().search(domain)
            res['acquirers'] = acquirers.filtered(lambda acq: (acq.payment_flow == 'form' and acq.view_template_id) or (acq.payment_flow == 's2s' and acq.registration_view_template_id))
        return res


class PortalController(PaymentPortal):
    @http.route(['/website_payment/pay'], type='http', auth='public', website=True, sitemap=False)
    def pay(self, reference='', order_id=None, amount=False, currency_id=None, acquirer_id=None, partner_id=False,
            access_token=None, **kw):

        response = super(PortalController, self).pay(reference, order_id, amount, currency_id, acquirer_id, partner_id,
                                                     access_token)
        env = request.env
        user = env.user.sudo()
        reference = normalize('NFKD', reference).encode('ascii', 'ignore').decode('utf-8')
        if partner_id and not access_token:
            raise werkzeug.exceptions.NotFound
        if partner_id and access_token:
            token_ok = request.env['payment.link.wizard'].check_token(access_token, int(partner_id), float(amount),
                                                                      int(currency_id))
            if not token_ok:
                raise werkzeug.exceptions.NotFound

        invoice_id = kw.get('invoice_id')
        # Default values
        values = {
            'amount': 0.0,
            'currency': user.company_id.currency_id,
        }
        # Check sale order
        if order_id:
            try:
                order_id = int(order_id)
                if partner_id:
                    # `sudo` needed if the user is not connected.
                    # A public user woudn't be able to read the sale order.
                    # With `partner_id`, an access_token should be validated, preventing a data breach.
                    order = env['sale.order'].sudo().browse(order_id)
                else:
                    order = env['sale.order'].browse(order_id)
                values.update({
                    'currency': order.currency_id,
                    'amount': order.amount_total,
                    'order_id': order_id
                })
            except:
                order_id = None

        if invoice_id:
            try:
                values['invoice_id'] = int(invoice_id)
            except ValueError:
                invoice_id = None

        # Check currency
        if currency_id:
            try:
                currency_id = int(currency_id)
                values['currency'] = env['res.currency'].browse(currency_id)
            except:
                pass

        # Check amount
        if amount:
            try:
                amount = float(amount)
                values['amount'] = amount
            except:
                pass

        # Check reference
        reference_values = order_id and {'sale_order_ids': [(4, order_id)]} or {}
        values['reference'] = env['payment.transaction']._compute_reference(values=reference_values, prefix=reference)

        # Check acquirer
        acquirers = None
        if order_id and order:
            cid = order.company_id.id
        elif kw.get('company_id'):
            try:
                cid = int(kw.get('company_id'))
            except:
                cid = user.company_id.id
        else:
            cid = user.company_id.id

        # Check partner
        if not user._is_public():
            # NOTE: this means that if the partner was set in the GET param, it gets overwritten here
            # This is something we want, since security rules are based on the partner - assuming the
            # access_token checked out at the start, this should have no impact on the payment itself
            # existing besides making reconciliation possibly more difficult (if the payment partner is
            # not the same as the invoice partner, for example)
            partner_id = user.partner_id.id
        elif partner_id:
            partner_id = int(partner_id)

        values.update({
            'partner_id': partner_id,
            'bootstrap_formatting': True,
            'error_msg': kw.get('error_msg')
        })

        acquirer_domain = ['&', ('state', 'in', ['enabled', 'test']), ('company_id', '=', cid)]
        if partner_id:
            partner = request.env['res.partner'].browse([partner_id])
            acquirer_domain_cou = expression.AND([
                acquirer_domain,
                ['|', ('country_ids', '=', False), ('country_ids', 'in', [partner.sudo().country_id.id])]
            ])
            acquirer_domain = expression.AND([acquirer_domain_cou,
                                              ['|', ('tag_ids', '=', False),
                                               ('tag_ids', 'in', partner.sudo().category_id.ids)]
                                              ])
        if acquirer_id:
            acquirers = env['payment.provider'].browse(int(acquirer_id))
        if order_id:
            acquirers = env['payment.provider'].search(acquirer_domain)
        if not acquirers:
            acquirers = env['payment.provider'].search(acquirer_domain)

        response.qcontext['acquirers'] = self._get_acquirers_compatible_with_current_user(acquirers)
        if partner_id:
            values['pms'] = request.env['payment.token'].search([
                ('acquirer_id', 'in', acquirers.ids),
                ('partner_id', 'child_of', partner.commercial_partner_id.id)
            ])
        else:
            values['pms'] = []
        response.qcontext['acquirers'] = self._get_acquirers_compatible_with_current_user(acquirers)
        return response
