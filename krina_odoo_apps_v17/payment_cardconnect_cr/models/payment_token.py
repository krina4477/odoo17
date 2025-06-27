# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class PaymentToken(models.Model):
    _inherit = 'payment.token'

    acctid = fields.Char('CardConnect Account ID')
