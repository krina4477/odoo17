# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
{
    'name': 'Secure Multi Uninstall With Log',
    'category': 'Extra Tools',
    'summary': 'Secure Multi Uninstall with Log',
    'version': '17.0.0.1',
    'website': "https://www.candidroot.com/",
    'author': "Candidroot Solutions Pvt. Ltd.",
    'description': """This module will help you to uninstall multiple modules from app list, ask password before proceeding and it will also save the log who has uninstalled the modules.
        Features :
        
            1). It will ask for a password before proceeding to module uninstallation.
            2). User can select multiple modules from list to uninstall it
            3). Admin can see the log which user has uninstalled the modules 
    """,
    'sequence': 8,
    'depends': [
        'base',
    ],
    'data': [
        'security/allow_security.xml',
        'security/ir.model.access.csv',
        'views/log_action.xml',
        'views/kanban_view_button.xml',
        'wizard/unistall_wizard.xml',
        'views/multiple_uninstall.xml',
    ],

    'images' : ['static/description/banner.png'],
    'license': 'OPL-1',
    'installable': True,
    'live_test_url': 'https://youtu.be/IreHQycosAY',
    'price': 14.99,
    'currency': 'USD',
    'auto_install': False,
    'application': True,
}
