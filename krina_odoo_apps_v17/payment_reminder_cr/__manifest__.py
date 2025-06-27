# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

{
    'name': 'Payment Reminder',
    'category': 'Reminder',
    'summary': 'Send Reminder to Customer When Transaction Fail From website',
    'author': "Candidroot Solutions Pvt. Ltd.",
    'version': '17.0.0.1',
    'website': "https://www.candidroot.com/",
    'description': """This module helps to Send Reminder to Customer When Payment Transaction Fail From website.""",
    'sequence': 5,
    'depends': ['website_sale'],
    'data': [
        'security/ir.model.access.csv',
        'data/payment_fail_template.xml'
    ],
    'images': ['static/description/banner.png'],
    'installable': True,
    'live_test_url': 'https://youtu.be/ntx8nIvFFms',
    'price': 9.99,
    'currency': 'USD',
    'auto_install': False,
    'application': True,
}
