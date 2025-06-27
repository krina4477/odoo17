# Part of Softhealer Technologies.
{
    "name": "Point Of Sale Advance Cache",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Point Of Sale",
    "license": "OPL-1",
    "summary": "POS Cache Management Update Product Real Time Product Update Customer Real Time Update Customer Load Fast POS Loading Update Contacts On Refresh Update Contact On Refresh Update Products On Refresh Update Product On Refresh POS Quick Load Odoo",
    "description": """This module helps to load partners and products in real-time or on refresh. Real-time data load that helps to boost the speed of pos.""",
    "version": "16.0.23",
    "depends": ["point_of_sale","sh_pos_all_in_one_retail",'hemfa_pos_attributes_values_viewer'],
    "application": True,
    "data": [
        'security/ir.model.access.csv',
        'data/ir_cron.xml',
        'views/pos_config_view.xml',
        'views/pos_config_cache_data_view.xml',
        'views/pos_config_cache_model_data_views.xml'
    ],
     'assets': {
        'point_of_sale.assets': [
            'sh_pos_advance_cache/static/src/js/indexDB.js',
            'sh_pos_advance_cache/static/src/js/cache_customer.js',
            'sh_pos_advance_cache/static/src/js/cache_product.js',
            'sh_pos_advance_cache/static/src/js/cache_product_attribute_value.js',
            'sh_pos_advance_cache/static/src/js/cache_product_attribute_line.js',
            'sh_pos_advance_cache/static/src/js/cache_res_country.js',
            'sh_pos_advance_cache/static/src/js/cache_state.js',
            'sh_pos_advance_cache/static/src/js/cache_pre_define_note.js',
            'sh_pos_advance_cache/static/src/js/cache_uom.js',
            'sh_pos_advance_cache/static/src/js/close_popup.js',
            'sh_pos_advance_cache/static/src/js/chrome.js',
        ],
       
    },
    'post_init_hook': 'create_config_cache_data',
    "auto_install": False,
    "installable": True,
    'images': ['static/description/background.png', ],
    "price": 70,
    "currency": "EUR"
}
