# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
{
    'name': "Sale Order Automation",
    'category': 'CRM',
    'summary': """Sales Order Automation for odoo community version and odoo enterptrise version.""",
    'version': '17.0.0.1',
    'author': "Candidroot Solutions Pvt. Ltd.",
    'website': 'https://www.candidroot.com/',
    'sequence': 2,
    'description': """This module allows you to create and validate picking, create invoices and register the payment on one click.""",
    'depends': ["base", "sale_stock", "account"],
    'data': [
        'views/res_users_view.xml',
    ],
    'qweb': [],
    'images' : ['static/description/banner.png'],
    'installable': True,
    'live_test_url': 'https://youtu.be/SIks1yfFhFc',
    'price': 19.99,
    'currency': 'USD',
    'auto_install': False,
    'application': False,
}
