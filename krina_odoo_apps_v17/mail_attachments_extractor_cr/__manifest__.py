# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
{
    'name': 'Mail Attachments Extractor',
    'category': 'Extra Tool',
    'summary': 'Mail Attachments Extractor',
    'version': '17.0.0.1',
    'author': "Candidroot Solutions Pvt. Ltd.",
    'website': 'https://www.candidroot.com/',
    'sequence':3,
    'description': """Mail Attachments Extractor""",
    'depends': ['base','mail','google_gmail'],
    'demo': [],
    'data': [
            'security/ir.model.access.csv',
            'views/tag_view.xml',
            'views/fetch_mail_view.xml',
            'views/directory_view.xml',
            'views/all_files_view.xml',
            ],
    'qweb': [],
    'images' : ['static/description/banner.png'],
    'installable': True,
    'live_test_url':'https://youtu.be/c4GpkWpr8bM',
    'price': 9.99,
    'currency': 'USD',
    'auto_install': False,
    'application': True,
}
