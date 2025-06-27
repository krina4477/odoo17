# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
{
    'name': "One2Many Duplicate Records",
    'summary': """One2Many Duplicate Records""",
    'description': """This module helps you to duplicate records in One2many line for Quotation, Sale Order, Invoice etc.""",
    'author': 'Candidroot Solutions Pvt. Ltd',
    'category': 'Extra Tools',
    'version': '17.0.0.1',
    'depends': ['web'],
    'data': [],
    'assets': {
        'web.assets_backend':[
            'web_one2many_duplicate_cr/static/src/xml/list_render.xml',
            'web_one2many_duplicate_cr/static/src/js/list_editable_renderer.js',
            'web_one2many_duplicate_cr/static/src/css/list_editable_renderer.css'
        ]
    },
    'images': ['static/description/banner.png'],
    'license': 'OPL-1',
    'installable': True,
    'live_test_url': 'https://youtu.be/IjSy-wrtpN0',
    'price': 24.99,
    'currency': 'USD',
    'auto_install': False,
    'application': True,
    'website':'https://www.candidroot.com/'
}
# See LICENSE file for full copyright and licensing details.

