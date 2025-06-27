# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
{
    'name': 'Kanban View Selector',
    'version': '17.0.0.1',
    'category': 'Extra Tools',
    'website': "https://www.candidroot.com/",
    'author': "Candidroot Solutions Pvt. Ltd.",
    'summary': 'Kanban View Selector',
    'description': """ User can select multiple records in Kanban view, Bulk print of quotation, Archive, Unarchive, Duplicate and Delete the records in Kanban view. """,
    'depends': ['web'],
    "installable": True,
    'application': True,
    'images' : ['static/description/banner.png'],
    'license': 'OPL-1',
    'live_test_url': 'https://youtu.be/Ea5GgtmUPOI',
    'price': 24.99,
    'currency': 'USD',
    'assets': {
        'web.assets_frontend': [
            '/kanban_view_selector_cr/static/src/css/kanban_box_style.scss',
        ],
        'web.assets_backend': [
            '/kanban_view_selector_cr/static/src/js/kanban_controller.js',
            '/kanban_view_selector_cr/static/src/js/kanban_renderer.js',
            '/kanban_view_selector_cr/static/src/xml/select_checkbox.xml',
            '/kanban_view_selector_cr/static/src/css/kanban_box_style.scss',
        ],
    }
}
