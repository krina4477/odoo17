# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
from odoo import fields, api, models


class ShowDuplicateValue(models.Model):
    _name = 'show.duplicate.value'

    model_id = fields.Many2one('ir.model', string='Model')
    field_ids = fields.Many2many('ir.model.fields', string='Fields')
