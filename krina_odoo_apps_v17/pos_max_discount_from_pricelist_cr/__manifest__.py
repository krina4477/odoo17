# -*- coding: utf-8 -*-index
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

{
    'name': "Best Offer Pricelist Auto Apply In POS",
    'category': 'Point of Sale',
    'summary': """Best Offer Pricelist Auto Apply In POS.""",
    'version': '17.0.0.1',
    'author': "Candidroot Solutions Pvt. Ltd.",
    'website': 'https://www.candidroot.com/',
    'sequence': 2,
    'description': """This module allows you to automatically apply maximum price-list in POS order line.""",
    'depends': ['point_of_sale','pos_self_order'],
    'data': [
        'views/pos_order_view.xml',
    ],
    'assets': {

        'point_of_sale._assets_pos': [
            'pos_max_discount_from_pricelist_cr/static/src/xml/OrderLine.xml',
            'pos_max_discount_from_pricelist_cr/static/src/js/pos_custom.js',
        ],

    },
    'images': ['static/description/banner.png'],
    'installable': True,
    'live_test_url': 'https://youtu.be/tpLf8qkirlk',
    'price': 14.99,
    'currency': 'USD',
    'auto_install': False,
    'license':'LGPL-3',
    'application': True,
}
