# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
{
    'name': "Hide Delete From Actions",
    'version': "17.0.0.1",
    'category': "Extra Tools",
    'author': 'Candidroot Solutions Pvt. Ltd.',
    'website': 'https://www.candidroot.com',
    'summary': 'Hide Delete From Actions',
    'description': '''
             This module allows you to hide delete action for the users who don't have rights. 
    ''',
    'depends': ['base', 'web'],
    'data': [
             'security/security_group.xml',
             ],
    'assets': {
        'web.assets_backend': [
            'hide_delete_action_item_cr/static/src/js/action_menus.js',
        ],
    },
    'images': ['static/description/banner.png'],
    'price': 5.99,
    'currency': 'USD',
    'live_test_url': 'https://youtu.be/LPqeTmYdgN0',
    'installable': True,
    'auto_install': False,
    'application': False
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
