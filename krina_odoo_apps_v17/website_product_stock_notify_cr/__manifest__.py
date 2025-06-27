# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
{
    'name': 'Website product stock notify',
    'category': 'Ecommerce',
    'summary': 'Ecommerce - Product Stock Notification For Customers',
    'author': "Candidroot Solutions Pvt. Ltd.",
    'version': '17.0.0.1',
    'website': "https://www.candidroot.com/",
    'sequence': 3,
    'description': """This module helps to Send Email Notification to Customer when Product is available in Stock.""",
    'depends': ['website_sale', 'stock', 'website', 'website_sale_stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/notify_me_template.xml',
        'views/subscription_request.xml',
        'data/send_customer_notification_cron.xml',
        'data/notification_of_stock_available.xml',
    ],
    'images': ['static/description/banner.png'],
    'license': 'OPL-1',
    'installable': True,
    'live_test_url': 'https://youtu.be/4m-MSRbeGGU',
    'price': 29.99,
    'currency': 'USD',
    'auto_install': False,
    'application': True,
    'assets': {
        'web.assets_frontend_lazy': [
            'website_product_stock_notify_cr/static/src/js/product_availability.js',
            'website_product_stock_notify_cr/static/src/scss/notify_me.scss',
            'website_product_stock_notify_cr/static/src/xml/**/*',
        ],
    },
}
