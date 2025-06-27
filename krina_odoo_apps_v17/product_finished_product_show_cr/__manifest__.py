# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
{
    'name': "Finish Product Count Show on BoM and on Product",
    'version' : "17.0.0.1",
    'category': 'MRP',
    'author': 'Candidroot Solutions Pvt. Ltd.',
    'website': 'https://www.candidroot.com',
    'summary': """Finish Product Count Show on BoM and on Product""",
    'description': """This module shows finished product counts in Bill of Material and Product based on available components.""",
    'depends': ['mrp'],
    'data': [
        'views/product_template_views.xml',
        'views/mrp_bom_view.xml',
             ],
    'qweb': [],
    'images' : ['static/description/banner.png'],
    'price': 9.99,
    'currency': 'USD',
    'live_test_url': 'https://youtu.be/KhUwSkpp6Ns',
    'installable': True,
    'auto_install': False,
    'application': False
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:



