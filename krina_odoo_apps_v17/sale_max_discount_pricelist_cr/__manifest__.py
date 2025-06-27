# -*- coding: utf-8 -*-

# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

{
    'name': 'Sale Max Discount Pricelist',
    'version': '17.0.0.1',
    'category': 'Sales',
    'description': '''
        This module helps you to apply maximum discount pricelist in Sales Order. 
    ''',
    'summary': 'Sale Max Discount Pricelist',
    'website': "https://www.candidroot.com/",
    'author': "Candidroot Solutions Pvt. Ltd.",
    'depends': [
        'sale',
    ],
    'data': [
        'security/custome_access.xml',
        'views/res_partner_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'images' : ['static/description/banner.png'],
    'live_test_url': 'https://youtu.be/2dRQIFvMHgY',
    'price': 19.99,
    'currency': 'USD',
 }