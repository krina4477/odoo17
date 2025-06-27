# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
{
	'name': 'Stock Notification',
	'version': '17.0.0.1',
	'summary': 'Product Low Stock Notification and Auto Reminder',
	'author': 'Candidroot Solution',
	'description': """
			This module allows user to set minimum quantity of the product.
			Once product quantity is less than the desired quantity inventory manager will receive the 
			email notification for the lower quantity product on daily basis.
    """,
	'website': 'www.candidroot.com',
	'depends': ['base', 'stock', 'mail', 'product'],
	'data': [
		'data/mail_template.xml',
		'data/ir_crone_low_qty_mail.xml',
		'views/res_config_settings_views_inherited.xml',
		'views/product_template_inherit_view.xml',
	],
	'demo': [
	],
	'images': ['static/description/banner.png'],
	'installable': True,
	'price': 9.99,
	'currency': 'USD',
	'live_test_url': 'https://youtu.be/fVGaFdV96gw',
	'application': True,
	'auto_install': False,
	'license': 'LGPL-3',
}