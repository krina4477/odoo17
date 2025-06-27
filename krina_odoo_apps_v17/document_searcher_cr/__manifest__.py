# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

{
    "name": "Document Content Searcher",
    "version": "17.0.0.1",
    'author': 'Candidroot Solutions Pvt. Ltd.',
    'website': 'https://www.candidroot.com',
    'category': 'Tools',
    'description': """

This module allows to search from any of the uploaded document by its content.

""",
    "depends": ['base', 'documents', 'web'],
    'data': [],
    'external_dependencies': {
        'python': ['cv2','pytesseract','PyPDF2','xlrd','openpyxl','csv']
    },
    'assets': {
        'web.assets_backend': [
            '/document_searcher_cr/static/src/xml/search_box.xml',
            '/document_searcher_cr/static/src/js/search.js',
            '/document_searcher_cr/static/src/js/search_bar.js',
        ],

    },
    'images': ['static/description/banner.jpeg'],
    'live_test_url': 'https://youtu.be/_sddTj9LMZM',
    'price': 50,
    'currency': 'USD',
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}