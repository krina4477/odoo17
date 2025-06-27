# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
{
    "name": "Recurring Marketing Campaign",
    "summary": "Recurring Marketing Campaign",
    "version": "17.0.0.1",
    "category": "Marketing",
    "description": """
        This module will help you to set recurring Email marketing campaign with default setting like Daily, Weekly, Monthly or Yearly along with set end date of Marketing Campaign recurrance.
    """,
    "author": "Candidroot Solutions Pvt. Ltd.",
    'website': "https://www.candidroot.com/",
    "depends": [
        'mass_mailing'
    ],
    "data": [
        'views/mass_mailing.xml',
    ],
    "installable": True,
    'application': True,
    'images' : ['static/description/banner.png'],
    'live_test_url': 'https://www.youtube.com/watch?v=tjbkzBTkfgk',
    'price': 15.99,
    'currency': 'USD',
}
