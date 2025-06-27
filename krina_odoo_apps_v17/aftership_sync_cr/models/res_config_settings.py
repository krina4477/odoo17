# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models,_
from odoo.exceptions import UserError, RedirectWarning

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'


    aftership_api_key = fields.Char(string='AfterShip API Key')

    def get_courier_list(self):
        if self.aftership_api_key:
            self.env['aftership.courier.list']._cron_generate_courier_list()
        else:
            raise UserError(_("Please Add 'AfterShip API Key'"))

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        aftership_api_key = params.get_param('aftership_api_key', default=False)
        res.update(
            aftership_api_key=aftership_api_key,
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param("aftership_api_key", self.aftership_api_key)
