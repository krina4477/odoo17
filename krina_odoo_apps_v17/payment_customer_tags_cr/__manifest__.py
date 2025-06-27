# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
{
    'name': 'Payment Customer Tags',
    'version': '17.0.0.1',
    'summary': '',
    'description': """""",
    'author': "Candidroot Solutions Pvt. Ltd.",
    'website': "https://candidroot.com/",
    'category': 'Accounting',
    'depends': ['payment'],
    'images': ['static/description/banner.png'],
    'data': [
        'data/data.xml',
        'views/payment_views.xml',
    ],
    'price':24.99,
    'currency': 'USD',
    'live_test_url': 'https://youtu.be/U_eaIlECKeM',
    'post_init_hook': 'post_init',
    'uninstall_hook':'uninstall_hook',
    'installable': True,
    'auto_install': False,
    'application': False,
}
