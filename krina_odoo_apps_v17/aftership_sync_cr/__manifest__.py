# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

{
    'name': "Aftership Integration with Odoo",
    'version': '17.0.0.0.1',
    'summary': """
        Aftership Integration with Odoo
    """,
    'description': """

Aftership Integration with Odoo
===============================
Aftership Integration with Odoo

Description
-----------
    - This module will allow user to create shipment record in aftership while validating delivery order.

    """,

    'author': "Candidroot Solutions Pvt. Ltd.",
    'website': "https://candidroot.com/",
    'category': 'Payment',
    'depends': ['base','base_setup', 'sale_stock', 'sale_management'],
    "external_dependencies": {"python": ['aftership'], "bin": []},
    'data': [
            'security/ir.model.access.csv',
            'data/aftership_data.xml',
            'views/country_view.xml',
            'views/res_config_settings_views.xml',
            'views/aftership_config_view.xml',
            'views/stock_picking_view.xml',
            'views/sale_order_view.xml',
    ],
    'images':  ['static/description/aftership_integration.jpg'],
    'license': 'OPL-1',
    'demo': [
    ],
    'price':99.99,
    'currency': 'EUR',
    'live_test_url': 'https://www.youtube.com/watch?v=Fw0Lyj01kwA&feature=youtu.be',
    'installable': True,
    'auto_install': False,
    'application': False
}
# Help For Api Tracking https://developers.aftership.com/reference/trackings
