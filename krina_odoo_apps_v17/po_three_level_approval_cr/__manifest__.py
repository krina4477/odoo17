# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.=
{
    'name': 'PO Three Level Approval',
    'category': 'Purchases',
    'summary': 'Approve purchase orders, according to manager approval limit',
    'version': '17.0.0.2',
    'author': "Candidroot Solutions Pvt. Ltd.",
    'website': 'https://www.candidroot.com/',
    'sequence': 2,
    'description': """This module helps to approve purchase orders,
                      according to manager approval limit.""",
    'depends': ['base', 'purchase', 'account','purchase_stock'],
    'demo': [],
    'data': [
            'security/manager_security.xml',
            'security/ir.model.access.csv',
            'data/mail_template_data.xml',
            'wizard/refuse_po_wizard_view.xml',
            'views/purchase.xml',
            'views/company.xml',
            ],
    'qweb': [],
    'images' : ['static/description/banner.png'],
    'license': 'OPL-1',
    'installable': True,
    'live_test_url': 'https://youtu.be/Mh3gkaCMRjE',
    'price': 55.99,
    'currency': 'USD',
    'auto_install': False,
    'application': True,
    
}
