# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
{
    'name' : "Split Receipt on Purchase Order Confirm",
    'version' : "17.0.0.1",
    'category' : "Purchase",
    'author': 'Candidroot Solutions Pvt. Ltd.',
    'website': 'https://www.candidroot.com',
    'summary': 'Split receipt on purchase order confirm',
    'description' : '''
             This module allows to split receipt on purchase order confirm. 
    ''',
    'depends' : ['purchase_stock'],
    'data': [
            'security/ir.model.access.csv',
             'wizard/purchase_make_invoice_advance_views.xml',
             'views/purchase_order_view.xml',
             ],
    'images' : ['static/description/banner.png'],
    'price': 9.99,
    'currency': 'USD',
    'live_test_url':'https://youtu.be/YfiY5XOicaQ',
    'installable': True,
    'auto_install': False,
    'application': False
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: