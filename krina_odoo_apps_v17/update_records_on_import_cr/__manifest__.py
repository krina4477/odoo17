# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
{
    'name': "Update Records On Import",
    'version': "17.0.0.2",
    'category': "Extra Tools",
    'author': 'Candidroot Solutions Pvt. Ltd.',
    'website': 'https://www.candidroot.com',
    'summary': 'Update Records On Import',
    'description': '''
             This module allows to Update Records On Import. 
    ''',
    'depends': ['web'],
    'data': [
    ],
    'assets': {
        'web.assets_backend': [
            'update_records_on_import_cr/static/src/js/import_action.js',
            'update_records_on_import_cr/static/src/js/update_field.js',
            'update_records_on_import_cr/static/src/components/**/*',
        ],
    },
    'images': ['static/description/banner.png'],
    'price': 49.99,
    'currency': 'USD',
    'live_test_url': 'https://youtu.be/29TejaM_riw',
    'installable': True,
    'auto_install': False,
    'application': False
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
