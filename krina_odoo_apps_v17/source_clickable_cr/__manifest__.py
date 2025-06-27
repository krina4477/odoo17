# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
{
    'name': 'Source Document Clickable',
    'summary': 'Source Document Clickable',
    'version': '17.0.0.1',
    'sequence': 1,
    'author': 'Candidroot Solutions Pvt. Ltd.',
    'website': 'https://www.candidroot.com',
    'description': """
    This module will allow to make all source document(origin) field clickable. Easy for users to click and navigate the 
    origin document from Delivery Order, Incoming Picking, Purchase Order, Manufacturing Order.
    """,
    'category': 'Extra Tools',
    'depends': ['base', 'sale_management', 'mrp', 'account', 'stock', 'purchase'],
    'data': [
        'views/clickable_picking_view.xml',
        'views/clickable_invoice_view.xml',
    ],
    'demo': [],
    'images' : ['static/description/banner.jpeg'],
    'installable': True,
    'live_test_url': 'https://youtu.be/EctULhwe8Vo',
    'price': 9.99,
    'currency': 'USD',
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}

