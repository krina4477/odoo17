# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
{
    "name": "Screen Recorder",
    "version": "17.0.1.0.0",
    "category": "Extra Tools",
    "summary": """Record your current screen with one click
        """,
    "description": "Record your current screen with one click",
    "author": "Candidroot Solutions Pvt. Ltd.",
    "website": "https://candidroot.com/",
    'images': ['static/description/banner.jpg'],
    "depends": ["base", "project", "crm"],
    "data": [
        "security/ir.model.access.csv",
        "security/res_groups.xml",
        "views/res_config_views.xml",
        "wizard/task_lead_name_view.xml"
    ],
    "assets": {
        "web.assets_backend": [
            "/screen_recorder_cr/static/src/js/screen_recorder.js",
            "/screen_recorder_cr/static/src/xml/screen_recorder.xml",
        ]
    },
    "license": "AGPL-3",
    "price": 10.00,
    "currency": 'USD',
    "installable": True,
    "auto_install": False,
    "application": True,
}
