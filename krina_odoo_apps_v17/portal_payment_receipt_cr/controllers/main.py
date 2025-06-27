# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
import logging
from odoo import http
from odoo.http import request
from odoo import SUPERUSER_ID
from odoo.tools.translate import _
from odoo.addons.portal.controllers import portal
from odoo.addons.portal.controllers.portal import pager as portal_pager
from collections import OrderedDict

_logger = logging.getLogger(__name__)


class CustomerPortal(portal.CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'payment_count' in counters:
            values['payment_count'] = request.env['account.payment'].sudo().search_count([('partner_id', '=', request.env.user.partner_id.id)])
        return values

    @http.route('/print/receipt/detail/<int:payment_id>', methods=['POST', 'GET'], csrf=False, type='http', auth="user",
                website=True)
    def detail_payment_receipt(self, payment_id, **kw):
        IrActionsReport = request.env['ir.actions.report'].sudo()
        html = IrActionsReport._render_qweb_html('account.action_report_payment_receipt', payment_id)[0]
        return request.make_response(html)

        # return request.render("portal_payment_receipt_cr.portal_payment_detail", values)

    @http.route('/print/receipt/<int:payment_id>', methods=['POST', 'GET'], csrf=False, type='http', auth="user", website=True)
    def print_payment_receipt(self,payment_id, **kw):
        if payment_id:
            pdf = request.env['ir.actions.report'].sudo()._render_qweb_pdf("account.action_report_payment_receipt", payment_id)[0]
            pdfhttpheaders = [('Content-Type', 'application/pdf'), ('Content-Length', len(pdf))]
            return request.make_response(pdf, headers=pdfhttpheaders)
        else:
            return request.redirect('/')

    @http.route(['/my/payment_receipt', '/my/payment_receipt/<int:page>'], type='http', auth="user", website=True)
    def my_payment(self, page=1, date_begin=None, date_end=None, sortby=None, filterby='all', search=None,
                            groupby='none', search_in='content', **kw):
        values = self._prepare_portal_layout_values()
        Payment = request.env['account.payment'].sudo()
        partner_id = request.env.user.partner_id

        domain = [('partner_id', '=', partner_id.id)]

        searchbar_sortings = {
            'date': {'label': _('Date'), 'order': 'date desc'},
            'name': {'label': _('Reference'), 'order': 'name desc'},
            'state': {'label': _('Status'), 'order': 'state'},
        }
        # default sort by order
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']
        searchbar_filters = {
            'all': {'label': _('All'), 'domain': [('partner_id', '=', partner_id.id)]}}
        # default filter by value
        if not filterby:
            filterby = 'all'
        domain += searchbar_filters[filterby]['domain']

        if date_begin and date_end:
            domain += [('date', '>', date_begin), ('date', '<=', date_end)]

        # count for pager
        payment_count = Payment.sudo().search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/payment_receipt",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=payment_count,
            page=page,
            step=self._items_per_page
        )
        # content according to pager and archive selected
        payments = Payment.sudo().search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_payment_history'] = payments.ids[:100]
        values.update({
            'date': date_begin,
            'payments': payments,
            'page_name': 'payment',
            'pager': pager,
            'default_url': '/my/payment_receipt',
            'searchbar_sortings': searchbar_sortings,
            'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
            'sortby': sortby,
            'filterby': filterby,
        })
        return request.render("portal_payment_receipt_cr.portal_payment_receipt", values)
