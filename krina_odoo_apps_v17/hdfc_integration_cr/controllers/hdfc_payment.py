# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
import logging
from pay_ccavenue import CCAvenue
from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class PaymentHDFC(http.Controller):

    _webhook_url = '/payment/hdfc/webhook'

    @http.route(['/payment/hdfc/return', '/payment/hdfc/cancel'],
                type='http', auth='public',
                methods=['POST'], csrf=False, save_session=False)
    def _handle_notification_data(self, **post):
        if post:
            payment_provider = request.env['payment.provider'].sudo().search(
                [('code', '=', 'hdfc')])
            web_url = request.env[
                'ir.config_parameter'].sudo().get_param('web.base.url')
            
            ccavenue = CCAvenue(payment_provider.hdfc_working_key,
                            payment_provider.hdfc_access_code,
                            payment_provider.hdfc_merchant_key,
                            web_url + '/payment/hdfc/return',
                            web_url + '/payment/hdfc/cancel')
            decrypted_data = ccavenue.decrypt(post)
            tx_sudo = request.env[
                'payment.transaction'].sudo()._get_tx_from_notification_data(
                'hdfc', decrypted_data)
            tx_sudo._handle_notification_data('hdfc', decrypted_data)
        return request.redirect('/payment/status')
    

    @http.route(_webhook_url, type='http', auth='public', methods=['POST'], csrf=False)
    def hdfc_webhook(self, **data):
        _logger.info("notification received from HDFC with data:\n%s", pprint.pformat(data))
        try:
            decrypted_data = data
            tx_sudo = request.env['payment.transaction'].sudo()._get_tx_from_notification_data(
                'hdfc', decrypted_data
            )
            tx_sudo._handle_notification_data('hdfc', decrypted_data)
        except ValidationError:  # Acknowledge the notification to avoid getting spammed
            _logger.exception("unable to handle the notification data; skipping to acknowledge")

        return 'SUCCESS'