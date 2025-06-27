# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
{
    'name': "Form View Line Edit Using Up/Down Arrow Key",
    'summary': """
        This module will use for Edit form view lines of Sales and Invoice Using Up/Down Arrow key Navigation.
        """,
    'description': """
        Form View Line Edit Using Up/Down Arrow Key
    """,
    'version': '17.0.0.1',
    'author': "Candidroot Solutions Pvt. Ltd.",
    'website': "https://www.candidroot.com/",
    'depends': ['web'],
    'data': [
    ],
    'qweb': [],
    'images': ['static/description/banner.png'],
    'license': 'OPL-1',
    'installable': True,
    'live_test_url': 'https://youtu.be/9UuCbCYcg1I',
    'price': 19.99,
    'currency': 'USD',
    'auto_install': False,
    'application': True,
    'assets': {
        'web.assets_backend': [
            'listview_up_down_nevigation_cr/static/src/js/list_editable_renderer.js',
            ]
    }
}
