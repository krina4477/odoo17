# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
from odoo import fields, http, _
from odoo.http import request

class CartUpdateInherit(http.Controller):
    
    @http.route('/buy/product/again', type='json', auth="public", website=True, csrf=False)
    def buy_product_again(self, product_id=None, add_qty=None, set_qty=0, **kw):
        sale_order = request.website.sale_get_order(force_create=True)

        new_add_qty = add_qty.split();
        sale_order._cart_update(
            product_id=int(product_id),
            add_qty=int(float(new_add_qty[0])), 
            set_qty=set_qty)

        return {'result': True}

    @http.route('/copy/order', type='json', auth="public", website=True, csrf=False)
    def copy_order(self, data=None, set_qty=0, **kw):
        sale_order = request.website.sale_get_order(force_create=True)
        if data:
            for i in data:
                sale_order._cart_update(
                    product_id=i.get('id'),
                    add_qty=i.get('qty'),
                    set_qty=set_qty)
        return {'result': True}

    @http.route('/copy/order/from/tree', type='json', auth="public", website=True, csrf=False)
    def copy_order_from_tree(self, order_id=None, **kw):
        sale_order = request.website.sale_get_order(force_create=True)
        sale_rec = request.env['sale.order'].browse(order_id)
        if sale_rec:
            for line in sale_rec.order_line:
                sale_order._cart_update(
                    product_id=int(line.product_id.id),
                    add_qty=int(line.product_uom_qty),
                    set_qty=0)
        return {'result': True}
