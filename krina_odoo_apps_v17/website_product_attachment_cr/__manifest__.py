# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
{
    'name': 'Attachments On Website Shop',
    'category': 'Website',
    'summary': 'Attachments On Website Shop',
    'version': '17.0.0.1',
    'author': "Candidroot Solutions Pvt. Ltd.",
    'website': 'https://www.candidroot.com/',
    'sequence':3,
    'description': """This module helps to Attachments On Website Shop.""",
    'depends': ['base', 'account', 'website','website_sale'],
    'demo': [],
    'data': [
            'views/product.xml',
            'views/website_product_view.xml',
            ],
    'qweb': [],
    'images' : ['static/description/banner.png'],
    'license': 'OPL-1',
    'installable': True,
    'live_test_url': 'https://youtu.be/8VmW16FPcrI',
    'price': 9.99,
    'currency': 'USD',
    'auto_install': False,
    'application': True,
}
