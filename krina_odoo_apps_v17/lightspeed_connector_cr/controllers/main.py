# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
from odoo import http
from odoo.http import request,route


class WebsiteAccessTokenGet(http.Controller):

    @http.route(['/update/access_token/<int:shop_id>'], type='http', auth="public")
    def get_access_token_from_url(self, shop_id, **kw):
        shop_obj = request.env['lightspeed.shop'].browse(shop_id)
        shop_obj.sudo().write({'code': kw.get('code', False)})

    @http.route(['/update/access_token1'], type='http', auth="public")
    def get_access_token_from_url1(self, code, **kw):
        shop = request.env['lightspeed.shop'].search([])
        if shop:
            shop[0].code = code
        return code

