# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
{
    'name' : "Hide Action Menus",
    'version' : "17.0.0.1",
    'category' : "Extra Tools",
    'author': 'Candidroot Solutions Pvt. Ltd.',
    'website': 'https://www.candidroot.com',
    'summary': 'Hide action menus',
    'description' : '''
             This module allows you to hide action menus for the users don't have rights. 
    ''',
    'depends' : ['base', 'web'],
    'data': [
             'security/security_group.xml',
             ],
    'assets': {
        'web.assets_backend': [
            'hide_action_menus_cr/static/src/js/action_menus.js',
            'hide_action_menus_cr/static/xml/base_extended.xml'
        ],
    },
    'images' : ['static/description/banner.png'],
    'price': 14.99,
    'currency': 'USD',
    'live_test_url': 'https://youtu.be/hcTFXQMGR_g',
    'installable': True,
    'auto_install': False,
    'application': False
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
