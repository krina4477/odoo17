# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

{
    'name': 'Show Duplicate Value List',
    'version': '17.0.0.1',
    'summary': 'This module can help to filter out the same value of record in list view',
    'description': """This module can help to filter out the same value of record in list view""",
    'author': "Candidroot Solutions Pvt. Ltd.",
    'website': "https://candidroot.com/",
    'category': '',
    'depends': ['web'],
    'images': ['static/description/banner.png'],
    'data': [
        'security/ir.model.access.csv',
        'views/show_duplicate_value.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'show_duplicate_value_list_cr/static/src/js/dublicate_values.js',
            'show_duplicate_value_list_cr/static/src/js/list_renderer.js',
        ],
    },
    'price': 24.99,
    'currency': 'USD',
    'live_test_url': 'https://youtu.be/oDjfoR0JYBU',
    'installable': True,
    'auto_install': False,
    'application': False,
}
