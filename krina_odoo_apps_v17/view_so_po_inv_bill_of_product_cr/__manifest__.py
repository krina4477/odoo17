# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.


{
    'name': 'So Po Bill Invoice of Product',
    'category': '',
    'summary': 'View So Po Bill Invoice of Product',
    'version': '17.0.0.1',
    'website': "https://www.candidroot.com/",
    'author': "Candidroot Solutions Pvt. Ltd.",
    'description': """This module helps to View Sale Order,Purchase Order,Bill,Invoice of Product.""",
    'sequence':8,
    'depends': [
        'sale_management','purchase','stock'
    ],
    'data': [
        'views/product_inherit.xml',
    ],
    'images' : ['static/description/banner.png'],
    'installable': True,
    'live_test_url': 'https://youtu.be/tJ8vsiAiJA8',
    'price': 9.99,
    'currency': 'USD',
    'auto_install': False,
    'application': True,

}
