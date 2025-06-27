# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
from odoo import models, fields


class RecordConfigSettings(models.TransientModel):

    _inherit = "res.config.settings"

    record_for = fields.Selection([('lead', 'CRM Lead'),
                                   ('task', 'Project Task')], string="Recording For", default="lead", config_parameter="screen_recorder_cr.record_for")
    project_id = fields.Many2one("project.project", string="Project", config_parameter="screen_recorder_cr.project_id")