# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2023-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author:Anjhana A K(<https://www.cybrosys.com>)
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
    'name': "POS Multipal Currency",
    'version': '17.0.1.0.0',
    'category': 'Point of Sale',
    'summary': 'Multipal Currency in PoS',
    'description': """ """,
    'author': " ",
    'company': '',
    'maintainer': '',
    'website': '',
    'depends': ['pos_payment_in_multi_currency'],
    'data': [
        # 'views/pos_order_views.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'cr_multi_currency/static/src/xml/multi_currency_template.xml',
            'cr_multi_currency/static/src/js/MultiCurrencyPopup.js',
            'cr_multi_currency/static/src/js/main.js',
            'cr_multi_currency/static/src/xml/cr_multi_currency_template.xml',
            'cr_multi_currency/static/src/xml/pos_items_count.xml',
            'cr_multi_currency/static/src/js/MultiCurrencyPopup_exchange.js',
            'cr_multi_currency/static/src/js/order_summary.js',
            'cr_multi_currency/static/src/css/pos.css',
        ]
    },
    'images': ['static/description/banner.jpg'],
    'license': 'AGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}
