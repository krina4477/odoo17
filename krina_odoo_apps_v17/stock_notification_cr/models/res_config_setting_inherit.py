# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

from odoo import api, exceptions, fields, models, _


class ResCompanyInherited(models.Model):
	_inherit = 'res.company'

	min_quantity = fields.Integer("Minimum Quantity")


class ResConfigSettings(models.TransientModel):
	_inherit = 'res.config.settings'

	min_quantity = fields.Integer("Minimum Quantity", related="company_id.min_quantity", readonly=False)
