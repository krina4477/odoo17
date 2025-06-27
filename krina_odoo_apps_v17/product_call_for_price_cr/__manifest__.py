# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
{
    'name': 'Call For Price',
    'category': 'Website',
    'summary': 'Call For Price',
    'version': '17.0.0.1',
    'author': "Candidroot Solutions Pvt. Ltd.",
    'website': 'https://www.candidroot.com/',
    'sequence':3,
    'description': """This module helps to call price of
                      a particular product for both customer and guest.""",
    'depends': ['base', 'sale_management', 'website','website_sale','stock'],
    'demo': [],
    'data': [
            'security/ir.model.access.csv',
            'data/call_price_data.xml',
            'views/call_price.xml',
            'views/boolean.xml',
            'views/website_product_view.xml',
            ],
    'qweb': [],
    'assets': {
        'web.assets_frontend_lazy': [
            'product_call_for_price_cr/static/src/js/call_price_popup.js',
        ]
    },
    'license': 'LGPL-3',
    'images' : ['static/description/banner.png'],
    'installable': True,
    'live_test_url': 'https://youtu.be/9q8bfPKZ_Ic',
    'price': 25.99,
    'currency': 'USD',
    'auto_install': False,
    'application': True,
}
