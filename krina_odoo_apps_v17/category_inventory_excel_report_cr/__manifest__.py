# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

{
    'name': 'Category Inventory Excel Report',
    'category': 'Inventory',
    'summary': 'Category Wise Inventory Report',
    'version': '17.0.0.1',
    'author': "Candidroot Solutions Pvt. Ltd.",
    'website': 'https://www.candidroot.com/',
    'description': """This module will print Excel report of Inventory, 
        Using that report you can print category wise excel report.""",
    'depends': ['base', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/stock_quant.xml',
        'wizard/inventory_excel_report.xml',
    ],
    'qweb': [],
    'images': ['static/description/banner.png'],
    'installable': True,
    # 'live_test_url': 'https://youtu.be/9q8bfPKZ_Ic',
    'price': 4.99,
    'currency': 'USD',
    'auto_install': False,
    'application': True,
}
