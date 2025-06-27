# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request


class StockNotiFy(http.Controller):

    @http.route('/product_notify_me', type='http', auth='public', website=True)
    def sale_details(self, **post):
        user = request.env.user
        product = request.env['product.product'].sudo().search([('id', '=', post.get('product'))])
        subscription_details = request.env['subscription.requests'].sudo().create({
            'user_id': user.id,
            'customer_email': post.get('email') if post.get('email') else user.email,
            'product_id': product.product_tmpl_id.id,
            'customer_phone_no': user.partner_id.mobile,
            'Company': user.partner_id.company_id.name,
            'customer': user.partner_id.name
        })
        return request.render('website_product_stock_notify_cr.website_stock_notify_form')
