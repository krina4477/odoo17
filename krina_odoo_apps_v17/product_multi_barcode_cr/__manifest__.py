# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
{
    'name': 'Product Report with Multi Barcode',
    'category': 'Product',
    'summary': 'Generate Multiple Products Barcode Report Based on Given Quantity',
    'version': '17.0.0.1',
    'author': "Candidroot Solutions Pvt. Ltd.",
    'website': 'https://www.candidroot.com/',
    'sequence': 3,
    'description': """This module helps to print barcode report of
                      product according to given number of quantity.""",
    'license': "LGPL-3",
    'depends': ['base', 'sale_management', 'stock', 'purchase'],
    'demo': [],
    'data': [
        'security/ir.model.access.csv',
        'data/barcode_generate_data.xml',
        'report/product_barcode_template.xml',
        'report/product_barcode.xml',
        'wizard/template_barcode_view.xml',
        'wizard/generate_barcode_view.xml',
    ],
    'qweb': [],
    'installable': True,
    'live_test_url': 'https://youtu.be/LEaq1-NInOk',
    'price': 9.99,
    'currency': 'USD',
    'images': ['static/description/banner.png'],
    'auto_install': False,
    'application': True,    
    'license': 'OPL-1',    
}
