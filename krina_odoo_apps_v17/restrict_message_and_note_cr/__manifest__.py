# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

{
    'name': 'Restrict Message and Note',
    'version': '17.0.0.1',
    'sequence': 1,
    'category': 'Extra Tools',
    'summary': 'Restrict Message and Note In Chatter',
    'author': 'Candidroot Solutions Pvt. Ltd.',
    'website': 'https://www.candidroot.com',
    'description': "This module helps to set restriction on message and notes for followers in chatter.",
    'depends': ['web', 'mail'],
    'data': [
        'views/mail_message.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'restrict_message_and_note_cr/static/src/components/composer.js',
            'restrict_message_and_note_cr/static/src/components/composer.xml',
            'restrict_message_and_note_cr/static/src/discuss/discuss.scss',
            'restrict_message_and_note_cr/static/src/components/thread_service.js',
        ],
        
    },
    'demo': [],
    'images': ['static/description/banner.png'],
    'live_test_url': 'https://www.youtube.com/watch?v=a_hCAq3V9bA',
    'price': 19.99,
    'currency': 'USD',
    'auto_install': False,
    'application': False,
}
