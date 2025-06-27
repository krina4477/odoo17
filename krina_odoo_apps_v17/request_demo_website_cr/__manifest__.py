# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
{
    'name': 'Request Demo for Product',
    'category': 'Website',
    'summary': 'Request Demo for Product on Ecommerce / Shop Website Page.',
    'version': '17.0.0.1',
    'author': "Candidroot Solutions Pvt. Ltd.",
    'website': 'https://www.candidroot.com/',
    'sequence': 4,
    'description': """This module helps to Request Demo for Product on Ecommerce / Shop Website Page
                      from with and without login users.""",
    'depends': ['crm', 'website_sale'],
    'data': [
            'data/confirm_email_template.xml',
            'views/request_demo_view.xml',
            'views/thank_you_page.xml'
    ],
    'qweb': [],
    'images': ['static/description/banner.png'],
    'price': 19.99,
    'currency': 'USD',
    'installable': True,
    'live_test_url': 'https://youtu.be/gxTMYjTjJ2c',
    'auto_install': False,
    'application': True,
    'assets': {
    'web.assets_frontend': [
      'request_demo_website_cr/static/src/js/request_demo.js'
    ]
    },

}
