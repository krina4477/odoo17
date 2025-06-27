# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    sale_ir_sequence_id = fields.Many2one("ir.sequence", "Sale Receipt Number", config_parameter='sale_ir_sequence_id')
    is_sale_ir_sequence = fields.Boolean('Custom Sale Sequence', config_parameter='is_sale_ir_sequence')

