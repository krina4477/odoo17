# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
{
    'name': 'Secure Uninstall',
    'category': 'Uninstall',
    'summary': 'Secure Uninstall',
    'version': '17.0.0.1',
    'website': "https://www.candidroot.com/",
    'author': "Candidroot Solutions Pvt. Ltd.",
    'description': """Secure Uninstall will ask password before proceeding to module uninstallation.""",
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
    'live_test_url': 'https://youtu.be/cK55Ux6q5h0',
    'price': 9.99,
    'currency': 'USD',
    'auto_install': False,
    'application': True,

}
