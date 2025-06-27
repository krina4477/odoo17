# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
{
    'name' : "Create Sales order based on timesheet lines",
    'version' : "17.0.0.0",
    'category' : "Project",
    'author': 'Candidroot Solutions Pvt. Ltd.',
    'website': 'https://www.candidroot.com',
    'summary': 'Create Sales order based on timesheet lines',
    'description' : '''
           This module allows you to configure generate sales order in task stages.
           Add multiple product with quantity in timesheet lines in order to create sales order 
           for each product lines added in timesheet by doing sum for the same product
    ''',
    'depends' : ['project', 'sale_management', 'hr_timesheet', 'sale_timesheet'],
    'data': [
             'security/ir.model.access.csv',
                'views/product_qty_timesheet_view.xml',
                'views/project_views.xml',
             ],
    'qweb': [],
    'images' : ['static/description/banner.jpeg'],
    'price': 19.99,
    'currency': 'USD',
    'live_test_url': 'https://youtu.be/7dS4BVMyzxU',
    'installable': True,
    'auto_install': False,
    'application': False
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

