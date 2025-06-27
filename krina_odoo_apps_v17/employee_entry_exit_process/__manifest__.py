# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
{
    'name': "Employee Entry Exit Process",
    'version': '17.0.0.1',
    'author': 'Candidroot Solutions Pvt. Ltd.',
    'category': 'Extra Tools"',
    'website': 'https://www.candidroot.com',
    'summary': 'Display total number of products according to their related categories in website.',
    'description': """This module helps to display total number of products
                      according to their related categories in website.""",
    'depends': ['base','hr','hr_holidays','hr_contract'],
    'data': [
        'security/ir.model.access.csv',
        'views/employee_details_views.xml',
        'views/employee_details_menu.xml',
        'views/employee_entry_exit_checklist_views.xml',
        'views/hr_employee_inherit_views.xml',
        'wizard/hr_leave_allocation_views.xml',
    ],
    'qweb': [],
    'license': 'OPL-1',
    'installable': True,
    'auto_install': False,
    'application': True,
}
