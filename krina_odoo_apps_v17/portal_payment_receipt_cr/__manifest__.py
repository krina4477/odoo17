# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
{
    'name': 'Portal Payment Receipt',
    'version': '17.0.0.1',
    'summary': 'Portal Payment Receipt',
    'description': """This module allows portal user to print payment receipt from my account""",
    'author': "Candidroot Solutions Pvt. Ltd.",
    'website': "https://candidroot.com/",
    'category': 'Accounting',
    'depends': ['account'],
    'images': ['static/description/banner.png'],
    'data': [
        'security/ir.model.access.csv',
        'views/portal_template.xml',
    ],
    'price': 9.99,
    'currency': 'USD',
    'live_test_url': 'https://youtu.be/X38yWrspK-4',
    'installable': True,
    'auto_install': False,
    'application': False,
}
