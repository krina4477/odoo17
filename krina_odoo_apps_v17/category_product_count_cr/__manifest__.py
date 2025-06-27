# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
{
    'name': "Category Wise Product Count",
    'version': '17.0.0.1',
    'author': 'Candidroot Solutions Pvt. Ltd.',
    'category': 'Website',
    'website': 'https://www.candidroot.com',
    'summary': 'Display total number of products according to their related categories in website.',
    'description': """This module helps to display total number of products
                      according to their related categories in website.""",
    'depends': ['base','website_sale','web'],
    'data': [
        'views/product_public_category_view.xml',
        'views/templates.xml',
    ],
    'qweb': [],
    'images' : ['static/description/banner.png'],
    'license': 'OPL-1',
    'installable': True,
    'live_test_url': 'https://youtu.be/fwJ4FI82GAM',
    'auto_install': False,
    'currency': 'USD',
    'price': 9.99,
    'application': True,
    'assets': {
        'web.assets_frontend': [
            'category_product_count_cr/static/src/scss/product_count.scss',
            ]
    }
}
