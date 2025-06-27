# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2024-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Cybrosys Techno Solutions(<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
{
    'name': "POS Scrap Order Cr",
    'version': '17.0.0.1',
    'category': 'Point of Sale',
    'summary': "This module will update pos scrap orders.",
    'description': """The POS user can make orders as Dine-in or Take
                    away and it will create separate token for Take away orders.""",
    'author': 'Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'website': 'https://www.cybrosys.com',
    'depends': ['point_of_sale', 'stock_barcode','bus','web'],
    'data': [
        'security/ir.model.access.csv',
        'views/pos_order_views.xml',
        'views/pos_scrap_history_views.xml',
        'wizard/pos_scrap_wizard_views.xml'
    ],
    'assets': {
            'point_of_sale._assets_pos': [
                'pos_scrap_order_cr/static/src/js/pos_scrap.js',
            ],
            'web.assets_backend':[
                'pos_scrap_order_cr/static/src/xml/pos_order_line_inherit.xml',
            ],
        },
    'images': ['static/description/banner.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
