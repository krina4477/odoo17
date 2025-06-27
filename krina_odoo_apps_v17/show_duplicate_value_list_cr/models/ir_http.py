# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
from odoo import models
from odoo.http import request

class IrHttpCr(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self):
        """ """
        info = super().session_info()
        vals = {}
        for sdv in request.env['show.duplicate.value'].sudo().search([]):
            field_list = []
            for field_id in sdv.field_ids:
                field_list.append(field_id.name)
            vals.update({sdv.model_id.model: field_list})
        info["show_duplicate_value_list"] = vals
        return info
