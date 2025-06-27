# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
{
    'name': "Update Records On Import",
    'summary': 'Update Records On Import',
    'description': '''Update Records On Import.''',
    'author': 'Candidroot',
    'category': "Tools",
    'version': "17.0.0.1",
    'depends': ['web'],
    'data': [],
    'assets': {
        'web.assets_backend': [
            'update_records_on_import/static/src/js/import_action.js',
            'update_records_on_import/static/src/js/update_field.js',
            'update_records_on_import/static/src/components/**/*',
        ],
    },
    'qweb':[],
    'installable': True,

}
