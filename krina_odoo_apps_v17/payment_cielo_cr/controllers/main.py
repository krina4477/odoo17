# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

import logging
import requests
import pprint
from odoo import _, http, fields
from odoo.http import request
import datetime
_logger = logging.getLogger(__name__)

class CieloController(http.Controller):

    @http.route('/payment/cielo/payment', type='json', auth='public', website=True)
    def payment_cielo_payment(self, reference, partner_id, opaque_data):
        tx = request.env['payment.transaction'].sudo().search([('reference', '=', reference)])
        tx.sudo().write({
            'cc_number': opaque_data.get('cardData').get('cardNumber')[-4:]
        })
        cc_brand = 'master'
        if opaque_data.get('cardData', False) and opaque_data.get('cardData').get('cardBrand', False):
            cc_brand = opaque_data.get('cardData').get('cardBrand')
            if opaque_data.get('cardData').get('cardBrand') == 'mastercard':
                cc_brand = 'master'
        SaveCard = 'true' if tx.tokenize else 'false'
        cielo_expiry = str(opaque_data.get('cardData').get('month')) + '/' + str(datetime.datetime.now().year)[:2] + str(opaque_data.get('cardData').get('year'))
        charge_params = {
            "MerchantOrderId": str(tx.id),
            "Customer": {
                "Name": tx.partner_id.name
            },
            "Payment": {
                "Type": "CreditCard",
                "Amount": tx.amount,
                "Currency": tx.currency_id.name,
                # "Country": tx.partner_country_id.code or '',
                "Installments": 1,
                "CreditCard": {
                    'CardNumber': opaque_data.get('cardData').get('cardNumber'),
                    "Holder": opaque_data.get('cardData').get('cardHolder'),
                    'ExpirationDate': cielo_expiry,
                    "SaveCard": SaveCard,
                    "Brand": cc_brand,
                }
            }
        }


        api_url_charge = 'https://%s/1/sales' % (tx.provider_id._get_cielo_api_url())
        r = requests.post(api_url_charge, json=charge_params, headers=tx.provider_id._get_cielo_api_headers())
        res = r.json()

        tx._handle_notification_data(
            'cielo', dict(res, merchantReference=reference),  # Match the transaction
        )
        
        _logger.info("make payment response:\n%s", pprint.pformat(res))
        feedback_data = {'reference': tx.reference, 'response': res}
        request.env['payment.transaction'].sudo()._handle_notification_data('cielo', feedback_data)
