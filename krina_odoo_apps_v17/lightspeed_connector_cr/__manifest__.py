# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
{
    'name': "LightSpeed Retail APIs (R Series) Integration With Odoo  ",
    'summary': """LightSpeed Retail APIs (R Series) Integration With Odoo  """,
    'description': """
            User will be able to import shops, customers/suppliers, products, tags, categories, taxes,
            attributes and Sales orders by doing the Lightspeed instance configuration.
    """,
    'author': 'Candidroot Solutions Pvt. Ltd.',
    'website': 'https://www.candidroot.com',
    'category': 'Integration',
    'version': '17.0.0.1',
    'category': "Extra Tools",
    'depends': ['sale_management', 'sale', 'product', 'account','stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/lightspeed_shop_views.xml',
        'views/product_brand_views.xml',
        'views/product_tag_views.xml',
        'views/product_product_views.xml',
        'views/product_category_views.xml',
        'views/record_log_view.xml',
        'views/res_partner.xml'
    ],
    'assets': {},
    'images': ['static/description/banner.jpg'],
    'qweb' : [
    ],
    'price': 249.99,
    'currency': 'USD',
    'live_test_url': 'https://youtu.be/LaUWTcn8bAA',
    'installable': True,
    'auto_install': False,
    'application': False
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
