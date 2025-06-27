# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models

class PaymentAcquirerCielo(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(selection_add=[('cielo', "Cielo")], ondelete={'cielo': 'set default'})
    cielo_merchant_key = fields.Char(string="Cielo Merchant Key", required_if_provider='cielo', groups='base.group_user')
    cielo_merchant_id = fields.Char(string='Cielo Merchant Id', required_if_provider='cielo',groups='base.group_user')
    cielo_image_url = fields.Char("Checkout Image URL", groups='base.group_user')
    
    @api.model
    def _get_default_payment_method_id(self, code):
        self.ensure_one()
        if self.code != 'cielo':
            return super()._get_default_payment_method_id(code)
        return self.env.ref('payment_cielo_cr.payment_method_cielo').id

    @api.model
    def _get_cielo_api_url(self):
        """Get cielo API URLs used in all s2s communication
            Takes state in consideration.
        """
        if self.state == 'test':
            return 'apisandbox.cieloecommerce.cielo.com.br'
        if self.state == 'enabled':
            return 'api.cieloecommerce.cielo.com.br'

    def _get_cielo_api_headers(self):
        """Get cielo API headers used in all s2s communication
        Takes state in consideration. If state is production
        merchant_id and merchant_key need to be defined.
        """
        if self.state == 'test':
            CIELO_HEADERS = {
                'MerchantId': '',
                'MerchantKey': '',
                'Content-Type': 'application/json',
                }
        if self.state == 'enabled':
            CIELO_HEADERS = {
                'MerchantId': self.cielo_merchant_id,
                'MerchantKey': self.cielo_merchant_key,
                'Content-Type': 'application/json',
                }
        return CIELO_HEADERS
