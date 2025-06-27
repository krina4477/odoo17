# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
{
    "name": "Payment Provider: HDFC",
    "version": "17.0.0.1",
    "summary": "Payment Provider: HDFC Integration With Odoo",
    "description": """CandidRoot Solutions with a feature that introduce new "Payment Acquirer" method named "HDFC". you can configure "HDFC Merchant Code and "HDFC Access Key and HDFC Working Key". it is one of the payment acquirer like Stripe, PayUmoney, Paypal etc.""",
    "author": "Candidroot Solutions Pvt. Ltd.",
    "website": "https://candidroot.com/",
    "category": "Accounting/Payment Providers",
    "depends": ["payment", "account", "website_sale"],
    "images": ['static/description/banner.png'],
    "data": [
        "views/payment_provider_views.xml",
        "views/hdfc_templates.xml",
        "data/payment_provider_data.xml",
    ],
    "installable": True,
    "auto_install": False,
    "application": True,
    "price": 59.99,
    "currency": "USD",
    "post_init_hook": "post_init_hook",
    "uninstall_hook": "uninstall_hook",
}
