# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

import logging

from odoo.addons.payment.models.payment_provider import ValidationError
from odoo import api, fields, models, _
from .. import cardconnect

_logger = logging.getLogger(__name__)


class PaymentAcquirer(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(selection_add=[('cardconnect', 'Card Connect')], ondelete={'cardconnect': 'set default'})
    cconnect_merchant_account = fields.Char('Merchant Account', required_if_provider='cardconnect',
                                            groups='base.group_user')
    cconnect_url = fields.Char('CardConnect URL', required_if_provider='cardconnect', groups='base.group_user')
    cconnect_user = fields.Char("Card Connect User", required_if_provider='cardconnect', groups='base.group_user')
    cconnect_pwd = fields.Char("Card Connect Password", required_if_provider='cardconnect', groups='base.group_user')

    def _get_default_payment_method_id(self,code):
        self.ensure_one()
        if self.code != 'cardconnect':
            return super(PaymentAcquirer,self)._get_default_payment_method_id(code)
        return self.env.ref('payment_cardconnect_cr.payment_method_cardconnect').id

    def cardconnect_s2s_form_validate(self, data):
        error = dict()
        mandatory_fields = ["cc_number", "cc_cvc", "cc_holder_name", "cc_expiry", "cc_brand"]
        for field_name in mandatory_fields:
            if not data.get(field_name):
                error[field_name] = 'missing'
        return False if error else True

    def cardconnect_s2s_form_process(self, data):
        acquirer_id = self.env['payment.provider'].sudo().browse(int(data.get('provider_id')))
        partner = self.env.user.partner_id
        cardconnect.username = acquirer_id.cconnect_user
        cardconnect.password = acquirer_id.cconnect_pwd
        cardconnect.base_url = acquirer_id.cconnect_url
        cardconnect.debug = True
        result = cardconnect.Profile.create(
            merchid=acquirer_id.cconnect_merchant_account,
            account=data.get('cc_number'),
            name=data.get('cc_holder_name'),
            expiry=data.get('cc_expiry'),
        )
        if result and result.get('respcode') == '09':
            result.update({'reference': data.get('reference')})
            return result
        else:
            ValidationError('api response not found')

    def cardconnect_payment_process(self, data):
        if not self.cardconnect_s2s_form_validate(data):
            return False
        if not data.get('partner_id'):
            raise ValueError(_('Missing partner reference when trying to create a new payment token'))
        return self.cardconnect_s2s_form_process(data)
