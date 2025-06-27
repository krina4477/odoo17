# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
{
    'name': "Account Partner Auto Reconcile(Community)",
    'category': 'Accounting/Accounting',
    'summary': """Account Partner Auto Reconcile for odoo community version.""",
    'version': '17.0.0.1',
    'author': "Candidroot Solutions Pvt. Ltd.",
    'website': 'https://www.candidroot.com/',
    'sequence': 2,
    'description': """This module allows you to automatically reconcile all the customer invoices and vendor bills with just one click.""",
    'depends': ['account'],
    'data': [
        'data/auto_reconcile_action.xml',
    ],
    'qweb': [],
    'images' : ['static/description/banner.jpeg'],
    'installable': True,
    'live_test_url': 'https://youtu.be/XTBuZzlva3I',
    'price': 24.99,
    'currency': 'USD',
    'auto_install': False,
    'application': False,
}
