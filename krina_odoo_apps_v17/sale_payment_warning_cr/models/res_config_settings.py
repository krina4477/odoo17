# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
from odoo import models, api, fields, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    add_warning_on_sale = fields.Boolean(string='Sale Payment Warning',config_parameter='sale_payment_warning_cr.add_warning_on_sale')
