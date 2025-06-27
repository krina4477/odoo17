# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models

class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(selection_add=[('hdfc', "HDFC")], ondelete={'hdfc': 'set default'})
    hdfc_merchant_key = fields.Char(string="HDFC Merchant Key", groups='base.group_user')
    hdfc_access_code  = fields.Char(string='HDFC Access Code',groups='base.group_user')
    hdfc_working_key = fields.Char(string='HDFC Working Key',groups='base.group_user')

    @api.model
    def _get_payment_method_information(self):
        res = super()._get_payment_method_information()
        res['hdfc'] = {'mode': 'unique', 'domain': [('type', '=', 'bank')]}
        return res
    
    