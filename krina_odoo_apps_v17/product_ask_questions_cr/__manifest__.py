# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
{
    'name': 'Product Ask Questions',
    'category': 'Website',
    'summary': 'Ask Questions for a product from with and without login users.',
    'version': '17.0.0.2',
    'author': "Candidroot Solutions Pvt. Ltd.",
    'website': 'https://www.candidroot.com/',
    'sequence':4,
    'description': """This module helps to Ask Questions for a product
                      from with and without login users.""",
    'depends': ['base', 'crm', 'website', 'website_sale'],
    'data': [
            'views/product_ask_question_view.xml',
            ],
    'qweb': [],
    'images' : ['static/description/banner.png'],
    'license': 'OPL-1',
    'installable': True,
    'live_test_url': 'https://youtu.be/doK0oYh5R_s',
    'price': 9.99,
    'currency': 'USD',
    'auto_install': False,
    'application': True,
    'assets': {
        'web.assets_frontend_lazy': [
          'product_ask_questions_cr/static/src/js/ask_question_popup.js'
        ]
    }
}