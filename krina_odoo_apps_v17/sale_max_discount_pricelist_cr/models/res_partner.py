# -*- coding: utf-8 -*-

# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

from odoo import models,api,fields,_

class ResPartnerInherit(models.Model):
    
    _inherit = 'res.partner'

    pricelist_ids = fields.Many2many('product.pricelist',string='Customer Pricelists')
    
    