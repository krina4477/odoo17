# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _
from datetime import datetime, date
from odoo.exceptions import UserError, ValidationError

class CallPrice(models.Model):
    _name = "call.price"
    _description = 'Call For Price'
    _rec_name = "first_name"

    first_name = fields.Char(string="First Name")
    last_name = fields.Char(string="Last Name")
    email = fields.Char(string="Email")
    mobile = fields.Char(string="Contact No")
    quantity = fields.Integer(string="Quantity")
    message = fields.Text(string="Message")