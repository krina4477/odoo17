# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class MailMessage(models.Model):
    _inherit = 'mail.message'

    follower_ids = fields.Many2many('mail.followers',string='Followers')

