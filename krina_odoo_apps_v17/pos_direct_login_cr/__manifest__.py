# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
{
    'name': 'POS Direct Login',
    'category': 'Point Of Sale',
    'summary': 'Direct POS Login without using backend',
    'version': '17.0.0.1',
    'author': "Candidroot Solutions Pvt. Ltd.",
    'website': 'https://www.candidroot.com/',
    'sequence': 2,
    'description': """This module helps to login POS without using backend,
                      and on pos close button, page redirect to user login page.""",
    'depends': ['base',
                'point_of_sale',
                'stock',
                'account',
                'web'],
    'data': [
             'views/pos_config_view.xml',
             ],
    'qweb': [],
    'images': ['static/description/banner.png'],
    'license': 'OPL-1',
    'installable': True,
    'live_test_url': 'https://youtu.be/81zSGmH9KVI',
    'price': 59.99,
    'currency': 'USD',
    'auto_install': False,
    'application': True,
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_direct_login_cr/static/src/js/session_log_out.js',
        ],
    },
}

