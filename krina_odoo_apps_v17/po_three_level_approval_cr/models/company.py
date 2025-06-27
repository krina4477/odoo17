# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _


class ResCompany(models.Model):
    _inherit = "res.company"

    three_level_approval = fields.Boolean(string="Three Level Approval",copy=False)
    approval_template_id = fields.Many2one('mail.template',string="Approval Email Template",copy=False)
    refuse_template_id = fields.Many2one('mail.template',string="Refuse Email Template",copy=False)
    manager_approve_limit = fields.Monetary(string="Manager Approve Limit",copy=False)
    finance_approve_limit = fields.Monetary(string="Finance Manager Approve Limit",copy=False)
    director_approve_limit = fields.Monetary(string="Director Approve Limit",copy=False)

    def write(self, values):
        for rec in self:
            if values.get('three_level_approval') or values.get('manager_approve_limit'):
                values.update({'po_double_validation':'two_step',
                               'po_double_validation_amount': rec.manager_approve_limit})
            elif values.get('three_level_approval') == False:
                    values.update({'po_double_validation':'one_step',
                                   'po_double_validation_amount': rec.manager_approve_limit})
        return super(ResCompany, self).write(values)
