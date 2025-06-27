# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

{
    "name": "Multi Company Select/Deselect All and search companies across the dropdown",
    "summary": "This module allows user to Select/Deselect All companies on single click."
               "User can also search companies across the dropdown",
    "version": "17.0.0.1",
    'author': 'Candidroot Solutions Pvt. Ltd.',
    'website': 'https://www.candidroot.com',
    "category": "MultiCompany",
    "depends": ["web"],
    "data": [],
    "demo": [],
    'assets': {
        'web.assets_backend': [
            'multicompany_dropdown_changes_cr/static/src/js/switch_company_menu.js',
            'multicompany_dropdown_changes_cr/static/src/xml/switch_company_menu.xml',
        ],
    },
    'images' : ['static/description/banner.jpeg'],
    "price": 35.99,
    "currency": "EUR",
    "live_test_url": 'https://youtu.be/KNPzRCYImRY',
    "license": "LGPL-3",
    "installable": True,
    "auto_install": False,
}
