# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
{
    'name': 'Cielo Payment Acquirer',
    'version': '17.0.0.1',
    'summary': 'Payment Acquirer: Cielo Integration With Odoo',
    'description': """CandidRoot Solutions with a feature that introduce new 'Payment Acquirer' method named 'Cielo'. you can configure 'Cielo Merchant Id' key and 'Cielo Merchant Key' key. it is one of the payment acquirer like Stripe, PayUmoney, Paypal etc.""",
    'author': "Candidroot Solutions Pvt. Ltd.",
    'website': "https://candidroot.com/",
    'category': 'Accounting',
    'depends': ['payment', 'account'],
    'images': ['static/description/payment_cielo_cr.png'],
    'data': [
        'views/payment_views.xml',
        'views/payment_cielo_templates.xml',
        'data/payment_acquirer_data.xml',
    ],
    'price': 44.99,
    'currency': 'USD',
    'live_test_url': 'https://youtu.be/29qjCPp0Z-U',
    'installable': True,
    'auto_install': False,
    'application': False,
    'uninstall_hook': 'uninstall_hook',
    'assets': {
            'web.assets_frontend': [
                'payment_cielo_cr/static/src/js/payment_portal.js',
                'payment_cielo_cr/static/src/js/payment_form.js',
            ],
        },
}
