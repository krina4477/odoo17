# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

import logging
import requests
import datetime
from odoo import api, fields, models
_logger = logging.getLogger(__name__)

class PaymentTokenCielo(models.Model):
    _inherit = 'payment.token'

    card_number = fields.Char(string="Number", required=False,)
    card_holder = fields.Char(string="Holder", required=False,)
    card_exp = fields.Char(string="Expiration date", required=False,)
    card_cvc = fields.Char(string="cvc", required=False,)
    card_brand = fields.Char(string="Brand", required=False,)
    cielo_token = fields.Char(string="Cielo Token", required=False,)


    def _build_display_name(self, *args, should_pad=True, **kwargs):
        """ Override of `payment` to build the display name without padding.

        Note: self.ensure_one()

        :param list args: The arguments passed by QWeb when calling this method.
        :param bool should_pad: Whether the token should be padded or not.
        :param dict kwargs: Optional data.
        :return: The cielo token name.
        :rtype: str
        """
        if self.provider_code != 'cielo':
            return super()._build_display_name(*args, should_pad=should_pad, **kwargs)
        return super()._build_display_name(*args, should_pad=False, **kwargs)