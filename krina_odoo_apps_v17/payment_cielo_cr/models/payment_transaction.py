# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
import logging
import requests
import pprint
from odoo.http import request
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)

class PaymentTransactionCielo(models.Model):
    _inherit = 'payment.transaction'

    cielo_s2s_capture_link = fields.Char(string="Capture Link",required=False,)
    cielo_s2s_void_link = fields.Char(string="Void Link", required=False,)
    cielo_s2s_check_link = fields.Char(string="Check Link",required=False,)
    cc_number = fields.Char(string="cc Number", required=False,)


    def _get_tx_from_notification_data(self, provider_code, notification_data):
        """ Override of payment to find the transaction based on Cielo data.

        :param str provider_code: The code of the provider that handled the transaction
        :param dict notification_data: The notification data sent by the provider
        :return: The transaction if found
        :rtype: recordset of `payment.transaction`
        :raise: ValidationError if inconsistent data were received
        :raise: ValidationError if the data match no transaction
        """
        tx = super()._get_tx_from_notification_data(provider_code, notification_data)
        if provider_code != 'cielo' or len(tx) == 1:
            return tx

        reference = notification_data.get('reference')

        tx = self.search([('reference', '=', reference), ('provider_code', '=', 'cielo')])
        if not tx:
            raise ValidationError(
                "Cielo: " + _("No transaction found matching reference %s.", reference)
            )

        return tx

    def _process_notification_data(self, data):
        super()._process_notification_data(data)
        self.ensure_one()
        if self.provider_code != 'cielo':
            return

        if self.state != 'draft':
            _logger.info('Cielo: trying to validate an already validated tx (ref %s)', self.reference)
            return True
        
        if self.token_id:
            data = data.get('response')

        if type(data) != list:
            status = data.get('Payment').get('Status')
            if status == 1:
                self.sudo().write({
                    'provider_reference': data.get('Payment').get('PaymentId'),
                })
                if self.tokenize and not self.token_id:
                    self._cielo_tokenize_from_notification_data(data)
                self._set_done()
                # store capture and void links for future manual operations
                for method in data.get('Payment').get('Links'):
                    if 'Rel' in method and 'Href' in method:
                        if method.get('Rel') == 'self':
                            self.sudo().write({
                                'cielo_s2s_check_link': method.get('Href'),
                            })
                        if method.get('Rel') == 'capture':
                            self.sudo().write({
                                'cielo_s2s_capture_link': method.get('Href'),
                            })
                        if method.get('Rel') == 'void':
                            self.sudo().write({
                                'cielo_s2s_void_link': method.get('Href'),
                            })
                # setting transaction to Cielo - must match Cielo
                return True
            else:
                error = data.get('Payment').get('ReturnMessage')
                PaymentAccountReference = data.get('Payment', {}).get('CreditCard', {}).get('PaymentAccountReference', {})
                PaymentId = data.get('Payment').get('PaymentId')
                _logger.info(error)
                self._set_error(_("Received data with status code \"%(status)s\" and error code \"%(error)s\"\n Payment Account Reference : \"%(PaymentAccountReference)s\"\n Payment ID : \"%(PaymentId)s\"", status=status, error=error,PaymentAccountReference=PaymentAccountReference,PaymentId=PaymentId))
                return False
        elif type(data) == list:
            error = data[0].get('Message')
            PaymentAccountReference = data.get('Payment', {}).get('CreditCard', {}).get('PaymentAccountReference',{})
            PaymentId = data.get('Payment').get('PaymentId')
            _logger.info(error)
            self._set_error(_("Received data with status code \"%(status)s\" and error code \"%(error)s\"\n Payment Account Reference : \"%(PaymentAccountReference)s\"\n Payment ID : \"%(PaymentId)s\"", status=status, error=error,PaymentAccountReference=PaymentAccountReference,PaymentId=PaymentId))
            return False
        else:
            self._set_canceled()

    def _cielo_tokenize_from_notification_data(self, data):
        self.ensure_one()
        res = {
            'provider_ref': self.reference,
            'payment_details': 'XXXXXXXXXXXX%s' % (self.cc_number),
            'provider_id': self.provider_id.id,
            'payment_method_id':self.payment_method_id.id,
            'card_brand': data.get('Payment').get('CreditCard').get('Brand'),
            'cielo_token': data.get('Payment').get('CreditCard').get('CardToken'),
            'partner_id': self.partner_id.id,
            'active': True,
        }
        token = self.env['payment.token'].sudo().create(res)
        self.sudo().write({
            'token_id': token.id,
        })
        _logger.info("created token with id %s for partner with id %s", token.id, self.partner_id.id)

    def _send_payment_request(self):
        super()._send_payment_request()
        if self.provider_code != 'cielo':
            return
        
        if not self.token_id:
            raise UserError(_("The transaction is not linked to a token."))
        # company = self.env.company
        # br_currency = self.env['res.currency'].sudo().search([('name', '=', 'BRL')], limit=1)
        # if not br_currency:
        #     unactive_br_currency = self.env['res.currency'].sudo().search([('name', '=', 'BRL'), ('active', '=', False)], limit=1)
        #     unactive_br_currency.active = True
        #     br_currency = self.env['res.currency'].sudo().search([('name', '=', 'BRL')], limit=1)
        # if self.currency_id and br_currency and self.currency_id != br_currency:
        #     balance = self.currency_id._convert(self.amount, br_currency, company, fields.Date.today())
        #     amount = balance
        # else:
        #     amount = self.amount
        charge_params = {
            "MerchantOrderId": str(self.id),
            "Customer": {
                "Name": self.partner_id.name
            },
            "Payment": {
                "Type": "CreditCard",
                "Amount": self.amount,
                "Installments": 1,
                "CreditCard": {
                    "CardToken": self.token_id.cielo_token,
                    "Brand": self.token_id.card_brand,
                }
            }
        }
        
        api_url_charge = 'https://%s/1/sales' % (self.provider_id._get_cielo_api_url())
        r = requests.post(api_url_charge, json=charge_params, headers=self.provider_id._get_cielo_api_headers())
        res = r.json()
        _logger.info("make payment response:\n%s", pprint.pformat(res))
        feedback_data = {'reference': self.reference, 'response': res}
        self._handle_notification_data('cielo', feedback_data)