# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from odoo import _, http
from odoo.http import request

_logger = logging.getLogger(__name__)


class CardconnectController(http.Controller):

    @http.route(['/payment/cardconnect/s2s/create_json_3ds'], type='json', auth='public', csrf=False)
    def cardconnect_s2s_create_json_3ds(self, verify_validity=False, **kwargs):
        if not kwargs.get('partner_id'):
            kwargs = dict(kwargs, partner_id=request.env.user.partner_id.id)
        response = False
        error = None
        try:
            response = request.env['payment.provider'].browse(int(kwargs.get('provider_id'))).cardconnect_payment_process(kwargs)
        except Exception as e:
            error = str(e)
        if not response:
            res = {
                'result': False,
                'error': error,
            }
            return res
        request.env['payment.transaction'].sudo()._handle_notification_data('cardconnect', response)
