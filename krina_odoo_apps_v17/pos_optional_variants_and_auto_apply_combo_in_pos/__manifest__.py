# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
{
    'name': 'Product Optional Variants And Auto Apply Combo In POS',
    'category': 'Point Of Sale',
    'summary': """Allow to add only selected product variant
                  inside pos and merege products if there is any
                  combo deals available.""",
    'version': '17.0.0.1',
    'author': "Candidroot Solutions Pvt. Ltd.",
    'website': 'https://www.candidroot.com/',
    'sequence': 2,
    'description': """This module helps to allow to add only selected
                      product variant inside pos and merege products 
                      if there is any combo deals available.""",
    'depends': ['base',
                'web',
                'product',
                'sale_management',
                'point_of_sale'],
    'data': [
             'security/ir.model.access.csv',
             'views/pos_order_view.xml',
             'views/product_view.xml',
             'views/combo_deals_view.xml',
             ],
    'images': ['static/description/banner.png'],
    'license': 'OPL-1',
    'installable': True,
    'live_test_url': 'https://youtu.be/ZUpCEgFH5dk',
    'price': 24.99,
    'currency': 'USD',
    'auto_install': False,
    'application': True,



    'assets': {
        'point_of_sale._assets_pos': [
            'pos_optional_variants_and_auto_apply_combo_in_pos/static/src/js/models.js',
            'pos_optional_variants_and_auto_apply_combo_in_pos/static/src/js/combo.js',
            'pos_optional_variants_and_auto_apply_combo_in_pos/static/src/js/RadioProductAttribute.js',
            'pos_optional_variants_and_auto_apply_combo_in_pos/static/src/xml/Orderline.xml',
            'pos_optional_variants_and_auto_apply_combo_in_pos/static/src/xml/ProductConfiguratorPopup.xml',
            'pos_optional_variants_and_auto_apply_combo_in_pos/static/src/xml/ProductList.xml',
            
        ],
    },
}
