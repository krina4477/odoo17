# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

{
    'name': "Show All Records (using pager) In One  Click",
    'summary': """Show All Records (using pager) In One  Click""",
    'description': """Show All Records (using pager) In One  Click""",
    'author': 'Candidroot Solutions Pvt. Ltd.',
    'category': 'Extra Tools',
    'version': '17.0.0.1',
    'website': 'https://www.candidroot.com/',
    'depends': ['web'],

    'assets': {
        'web.assets_backend': [
            'show_all_records_pager_cr/static/src/js/list_controller_custom.js',
            'show_all_records_pager_cr/static/src/xml/*.xml',
        ],
    },
    'images': ['static/description/banner.png'],
    'demo': [],
    'price': 4.99,
    'currency': 'USD',
    'live_test_url': 'https://youtu.be/3kOnhFuY_LE',
    'installable': True,
    'auto_install': False,
    'application': False
}
