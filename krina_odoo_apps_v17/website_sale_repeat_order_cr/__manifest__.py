# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

{
    'name': 'Website Sale Repeat Order',
    'category': 'Website',
    'summary': 'Repeat Website Sale Order And Buy A Product',
    'version': '17.0.0.1',
    'author': "Candidroot Solutions Pvt. Ltd.",
    'website': 'https://www.candidroot.com/',
    'sequence': 3,
    'description': """This module helps to repeat website sale order, 
                      and add a product in your cart on buy it again button.""",
    'depends': ['sale_management',
                'website',
                'website_sale'],
    'demo': [],
    'data': [
            'views/website_sale_view.xml',
            ],
    'qweb': [],
    'images': ['static/description/banner.png'],
    'license': 'OPL-1',
    'installable': True,
    'live_test_url': 'https://youtu.be/-WWpeyhwOF0',
    'price': 9.99,
    'currency': 'USD',
    'auto_install': False,
    'application': True,
    'assets': {
    'web.assets_frontend': [
       'website_sale_repeat_order_cr/static/src/js/buy_it_again.js',
       'website_sale_repeat_order_cr/static/src/scss/button_style.scss',
    ]
    }

}

