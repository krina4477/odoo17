# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

import logging

from odoo import _, api, models, fields
from odoo.exceptions import ValidationError

from odoo.addons.payment import utils as payment_utils
from .. import cardconnect

_logger = logging.getLogger(__name__)

class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    cct_txnid = fields.Char('Transaction ID')
    cct_txcurrency = fields.Char('Transaction Currency')

    def _send_payment_request(self):
        """ Override of payment to simulate a payment request.

        Note: self.ensure_one()

        :return: None
        """
        super()._send_payment_request()
        if self.code != 'cardconnect':
            return

        self._handle_notification_data('cardconnect', {'reference': self.reference})

    @api.model
    def _get_tx_from_notification_data(self, provider_code, notification_data):
        """ Override of payment to find the transaction based on cardconnect data.

        :param str provider_code: The code of the provider handling the transaction.
        :param dict notification_data: The cardconnect notification data
        :return: The transaction if found
        :rtype: recordset of `payment.transaction`
        :raise: ValidationError if the data match no transaction
        """
        tx = super()._get_tx_from_notification_data(provider_code, notification_data)
        if provider_code != 'cardconnect':
            return tx

        reference = notification_data.get('reference')
        tx = self.search([('reference', '=', reference), ('provider_code', '=', 'cardconnect')])
        if not tx:
            raise ValidationError(
                "Test: " + _("No transaction found matching reference %s.", reference)
            )
        return tx

    def _process_notification_data(self, notification_data):
        """ Override of payment to process the transaction based on cardconnect data.

        Note: self.ensure_one()

        :param dict notification_data: he notification data sent by the provider
        :return: None
        :raise: ValidationError if inconsistent data were received
        """
        super()._process_notification_data(notification_data)
        if self.provider_code != "cardconnect":
            return

        if notification_data.get('respcode') == '09':
            self.cardconnect_s2s_do_transaction(notification_data)
        if self.tokenize:
            token = self.env['payment.token'].create({
                'provider_id': self.provider_id.id,
                'name': payment_utils.build_token_name(payment_details_short=notification_data['cc_summary']),
                'partner_id': self.partner_id.id,
                'provider_ref': 'fake acquirer reference',
                'verified': True,
            })
            self.token_id = token.id


    def cardconnect_s2s_do_transaction(self, data):
        cardconnect.username = self.provider_id.cconnect_user
        cardconnect.password = self.provider_id.cconnect_pwd
        cardconnect.base_url = self.provider_id.cconnect_url
        cardconnect.debug = True
        result = cardconnect.Auth.create(
            merchid=self.provider_id.cconnect_merchant_account,
            profile=data.get('profileid') + '/' + data.get('acctid'),
            amount=self.amount,
            currency=self.currency_id.name,
        )
        return self._cardconnect_s2s_validate(result)

    def _cardconnect_s2s_validate(self, result):
        if result.get('respstat') == "A":
            self.write({
                'cct_txnid': result.get('retref'),
                'cct_txcurrency': self.currency_id.name,
                'provider_reference': result.get('retref'),
            })
            self._set_done()
            return True
        elif result.get('respstat') == "C":
            error = result.get('resptext')
            _logger.info(error)
            self.write({
                'provider_reference': result.get('retref'),
            })
            self._set_error(error)
            return False
        else:
            error = result.get('resptext')
            _logger.info(error)
            self.write({
                'provider_reference': result.get('retref'),
            })
            self._set_error(error)
            return False
