# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
from odoo import models, fields


class TaskLeadName(models.TransientModel):

    _name = "wizard.task.lead.name"
    _description = "Wizard for task/lead"

    name = fields.Char(string="Name")

    def action_task_lead_name(self):
        result = self.env['ir.config_parameter'].sudo().get_param('screen_recorder_cr.record_for')
        project_id = self.env['ir.config_parameter'].sudo().get_param('screen_recorder_cr.project_id')
        url = self._context.get('url').replace("data:video/webm;codecs=vp9,opus;base64,", "")
        file_name = self.name + '.mp4'
        if result == 'task':
            task_id = self.env['project.task'].create({
                'name': self.name,
                'project_id': int(project_id),
            })
            self.env['ir.attachment'].create({
                'datas': url,
                'name': file_name,
                'res_id': task_id.id,
                'res_model': 'project.task'
            })
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'project.task',
                'res_id': task_id.id,
                'view_mode': 'form',
            }
        else:
            lead_id = self.env['crm.lead'].create({
                'name': self.name,
            })
            self.env['ir.attachment'].create({
                'datas': url,
                'name': file_name,
                'res_id': lead_id.id,
                'res_model': 'crm.lead'
            })
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'crm.lead',
                'res_id': lead_id.id,
                'view_mode': 'form',
            }