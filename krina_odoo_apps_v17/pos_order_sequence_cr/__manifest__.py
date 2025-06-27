# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
{
    'name': 'POS Order Sequence',
    'category': 'Point Of Sale',
    'summary': """This module helps to allow to add Auto Sequence in Receipt Number""",
    'version': '17.0.0.1',
    'author': "CandidRoot Solutions Pvt. Ltd.",
    'website': 'https://www.candidroot.com/',
    'sequence': 2,
    'description': """This module helps to allow to add Auto Sequence in Receipt Number""",
    'depends': ['point_of_sale'],
    'data': [
             'views/pos_config.xml',
             ],
    'images': ['static/description/banner.png'],
    'installable': True,
    'live_test_url': 'https://youtu.be/RcWf3E03CkA',
    'price': 39.99,
    'currency': 'USD',
    'auto_install': False,
    'application': True,
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_order_sequence_cr/static/src/js/screen_extend.js',
        ],
    }
}
