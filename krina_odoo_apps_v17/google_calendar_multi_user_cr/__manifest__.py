# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
{
    'name': "Google Calendar Multi User",
    'summary': """
        The module adds the possibility to synchronize your google calendar based on user so only respective user can sync and see their google calendar records in Odoo.""",
    'description': """
        Google Calendar Multi User
    """,
    'version': '17.0.0.1',
    'author': "Candidroot Solutions Pvt. Ltd.",
    'website': "https://www.candidroot.com/",
    # any module necessary for this one to work correctly
    'depends': ['google_calendar'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/res_config_settings_views.xml',
        'views/res_users_views.xml',
    ],
    'qweb': [],
    'images': ['static/description/banner.png'],
    'license': 'OPL-1',
    'installable': True,
    'live_test_url': 'https://www.youtube.com/watch?v=95QhUq9LM_Y',
    'price': 49.99,
    'currency': 'USD',
    'auto_install': False,
    'application': True,
}
