# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
{
    'name' : "Split Delivery Order on Sales Order Confirm",
    'version' : "17.0.0.1",
    'category' : "Sales",
    'author': 'Candidroot Solutions Pvt. Ltd.',
    'website': 'https://www.candidroot.com',
    'summary': 'Split Delivery Order on Sales Order confirm',
    'description' : '''
             This module allows to split delivery order on sales order confirm. 
    ''',
    'depends' : ['sale_management', 'stock'],
    'data': [
             'security/ir.model.access.csv',
             'wizard/sale_make_invoice_advance_views.xml',
             'views/sale_order_view.xml',
             ],
    'images' : ['static/description/banner.png'],
    'price': 9.99,
    'currency': 'USD',
    'live_test_url': 'https://youtu.be/TJLCPgtj108',
    'installable': True,
    'auto_install': False,
    'application': False
}
