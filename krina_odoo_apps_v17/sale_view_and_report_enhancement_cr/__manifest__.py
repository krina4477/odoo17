# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

{
    'name': "Sales Enhancement",
    'version': '17.0.0.1',
    'summary': """
        Sales Enhancement for Quotation/Order View and Report.
    """,
    'description': """

    Sales Enhancement
    =================
    Sales Enhancement
    
    Description
    -----------
        - This module contains adding product's category as a section in quotation and order report.
    """,

    'author': "Candidroot Solutions Pvt. Ltd.",
    'website': "https://www.candidroot.com/",
    'category': 'Sales/Sales',
    'depends': ['sale_management'],
    'data': [
            "views/sale_order_view.xml",
            "report/sale_report_templates.xml",
    ],
    'images':  ['static/description/banner.jpg'],
    'demo': [
    ],
    'price':10,
    'currency': 'USD',
    'live_test_url': 'https://youtu.be/RzI5Qk3AHMw',
    'installable': True,
    'auto_install': False,
    'application': False
}
