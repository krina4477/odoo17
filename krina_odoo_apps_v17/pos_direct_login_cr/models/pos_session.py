# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.http import request
class PosSession(models.Model):
    _inherit = 'pos.session'

    def get_permission_for_log_out(self,user_config_id=None):
        if user_config_id:
            Users = request.env['res.users']
            user_rec = Users.sudo().browse(request.uid)
            if user_rec:
                if user_rec.pos_config_id:
                    return True
                else:
                    return False
