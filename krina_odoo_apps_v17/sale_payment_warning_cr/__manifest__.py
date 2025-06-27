# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
{
    'name': 'Restrict Sales Order For Due Payment',
    'category': 'Website',
    'summary': "This module allows user to restrict the creation of Sales Order once the previous due is not clear based on Payment Terms",
    'version': '17.0.0.1',
    'author': "Candidroot Solutions Pvt. Ltd.",
    'website': 'https://www.candidroot.com/',
    'sequence': 3,
    'description': """This module allows user to restrict the creation of Sales Order once the previous due is not clear based on Payment Terms""",
    'depends': ['sale'],
    'demo': [],
    'data': [
            'views/res_config_settings_views.xml',
            'views/sale_order_view.xml',
            ],
    'qweb': [],
    'license': 'OPL-1',
    'installable': True,
    'images' : ['static/description/banner.png'],
    'live_test_url': 'https://youtu.be/ZGLMWoOhNFA',
    'price': 9.99,
    'currency': 'USD',
    'auto_install': False,
    'application': True,

}

