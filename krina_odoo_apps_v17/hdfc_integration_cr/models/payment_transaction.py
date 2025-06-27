# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
import logging
from pay_ccavenue import CCAvenue
from odoo import api, models, _
from odoo.exceptions import ValidationError
from odoo.addons.payment import utils as payment_utils

_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'
    _order = 'id desc'
    _rec_name = 'reference'

    @api.model_create_multi
    def create(self, values_list):
        for values in values_list:
            provider = self.env['payment.provider'].browse(values['provider_id'])

            if not values.get('reference'):
                values['reference'] = self._compute_reference(provider.code, **values)

            partner = self.env['res.partner'].browse(values['partner_id'])
        
            txs = super(PaymentTransaction,self).create(values)
            txs.partner_phone = partner.mobile
        return txs

    @api.model
    def _compute_reference(self, provider_code, prefix=None, separator='-',
                           **kwargs):
        if provider_code == 'hdfc':
            prefix = payment_utils.singularize_reference_prefix()
        return super()._compute_reference(provider_code, prefix=prefix,
                                          separator=separator, **kwargs)

    def _get_specific_rendering_values(self, processing_values):
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != 'hdfc':
            return res
        
        return self.execute_payment()

    def execute_payment(self):
        self.ensure_one()
        web_url = self.env['ir.config_parameter'].get_param('web.base.url')
        sale_order = self.env['sale.order'].search(
            [('id', '=', self.sale_order_ids.id)])
        
        form_data = {
            "order_id": self.reference,
            "currency": "INR",
            "amount": (self.amount - sale_order.amount_tax),
            "redirect_url": f"{web_url}/payment/hdfc/return",
            "cancel_url": f"{web_url}/payment/hdfc/cancel",
            "billing_name": self.partner_name,
            "billing_tel": self.partner_phone,
            "billing_address": self.partner_address,
            "billing_city": self.partner_city,
            "billing_state": self.partner_state_id.name,
            "billing_country": self.partner_country_id.name,
            "billing_zip": self.partner_zip,
            "billing_email": self.partner_email
        }


        if self.provider_id.state == "test":
            api_url = ("https://test.ccavenue.com/transaction/transaction.do?command=initiateTransaction")
        else:
            api_url = ("https://secure.ccavenue.com/transaction/transaction.do"
                        "?command=initiateTransaction")
        ccavenue = CCAvenue(self.provider_id.hdfc_working_key,
                            self.provider_id.hdfc_access_code,
                            self.provider_id.hdfc_merchant_key,
                            web_url + '/payment/hdfc/return',
                            web_url + '/payment/hdfc/cancel')
        encrypted_data = ccavenue.encrypt(form_data)
        response_content = {
            "encrypted_data": encrypted_data,
            "access_code": self.provider_id.hdfc_access_code,
            "api_url": api_url
        }
        return response_content

    def _get_tx_from_notification_data(self, provider_code, notification_data):
        tx = super()._get_tx_from_notification_data(provider_code,
                                                    notification_data)
        if provider_code != 'hdfc':
            return tx
        reference = notification_data.get('order_id', False)
        if not reference:
            raise ValidationError("HDFC: " + _("No reference found.", ))
        tx = self.search(
            [('reference', '=', reference), ('provider_code', '=', 'hdfc')])
        if not tx:
            raise ValidationError("HDFC: " + _("No transaction found "
                                                    "matching reference %s.",
                                                    reference))
        return tx

    def _handle_notification_data(self, provider_code, notification_data):
        tx = self._get_tx_from_notification_data(provider_code,
                                                notification_data)
        tx._process_notification_data(notification_data)
        tx._execute_callback()
        return tx

    def _process_notification_data(self, notification_data):

        super()._process_notification_data(notification_data)
        if self.provider_code != 'hdfc':
            return
        status = notification_data.get('order_status')
        if status == 'Success':
            self._set_done()
        elif status == 'Aborted':
            self._set_canceled(state_message="Error")
        elif status == "Failure":
            self._set_canceled(state_message="Error")
        else:
            _logger.warning("received unrecognized payment state %s for "
                            "transaction with reference %s",
                            status, self.reference)
            self._set_error("HDFC: " + _("Invalid payment status."))
