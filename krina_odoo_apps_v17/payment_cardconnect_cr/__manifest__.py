# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
{
    'name': "CardConnect Payment Acquirer",
    'version': '17.0.0.0.1',
    'summary': """
        Integrate Cardconnect Payment with Odoo. With this module, your customers can pay for their online orders with Cardconnect payment gateway on Odoo website.
    """,
    "license": "Other proprietary",
    'description': """
Description
-----------
    - CardConnect Payment Acquirer
    """,
    'author': "Candidroot Solutions Pvt. Ltd.",
    'website': "https://www.candidroot.com/",
    'category': 'Payment',
    'depends': ['payment', 'website_sale'],
    'data': [
        'views/payment_acquirer_view.xml',
        'views/payment_transaction_view.xml',
        'views/payment_views.xml',
        'data/payment_acquirer_data.xml',
    ],
    'demo': [
    ],
    'images': ['static/description/banner.jpg'],
    'qweb': [],
    'installable': True,
    'live_test_url': '',
    'auto_install': False,
    'application': False,
    'assets': {
        'web.assets_frontend': [
            'payment_cardconnect_cr/static/lib/jquery.payment/jquery.payment.js',
            'payment_cardconnect_cr/static/src/js/payment_form.js',
            'payment_cardconnect_cr/static/src/js/payment_portal.js',
        ],
    },
    'uninstall_hook': 'uninstall_hook',
}











