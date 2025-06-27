# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
{
    'name' : "Send Employee Birthday Reminder to Manager",
    'version' : "17.0.0.1",
    'category' : "Extra Tools",
    'author': 'Candidroot Solutions Pvt. Ltd.',
    'website': 'https://www.candidroot.com',
    'summary': 'Send Birthday Reminder of Employee to manager',
    'description' : '''
             Module to send an Email reminder to employee manager on Birthday.
             Birthday Reminder email to manager. 
    ''',
    'depends' : ['hr'],
    'data': [
             'views/birthday_reminder_cron.xml',
             'views/birthday_reminder_action_data.xml'
             ],
    'images' : ['static/description/Banner.png'],
    'price': 9.99,
    'currency': 'USD',
    'live_test_url': 'https://youtu.be/4m_MByRANF4',
    'installable': True,
    'auto_install': False,
    'application': False,
    'license':'LGPL-3'

}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
