# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

from odoo import models,api,fields,_


class LightspeedFailureLog(models.Model):
    _name = 'lightspeed.failure.log'

    record_name = fields.Char('Record name')
    import_obj = fields.Char('Import Object Name')
    failure_msg = fields.Char('Failure Message')
    response_json = fields.Text('Json Data')
    lightspeed_id = fields.Many2one('lightspeed.shop', 'Lightspeed Shop')
    is_send = fields.Boolean('Mail sent ??', default=False)


