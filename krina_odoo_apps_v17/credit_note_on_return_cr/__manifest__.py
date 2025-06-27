# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
{
    'name' : "Credit Note on Return Delivery Order",
    'version' : "17.0.0.1",
    'category' : "Accounting",
    'author': 'Candidroot Solutions Pvt. Ltd.',
    'website': 'https://www.candidroot.com',
    'summary': 'Credit Note on Return Delivery Order',
    'description' : '''
             This module allows you to generate credit note on delivery order return. 
    ''',
    'depends' : ['sale_management', 'account', 'stock'],
    'data': [
             'views/stock_picking_view.xml',
             ],
    'images' : ['static/description/banner.png'],
    'price': 9.99,
    'currency': 'USD',
    'live_test_url': 'https://youtu.be/SjJryD_ZUjw',
    'installable': True,
    'auto_install': False,
    'application': False
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
