# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _
from datetime import datetime, date
from odoo.exceptions import UserError, ValidationError


class ReportProductMultiBarcode(models.AbstractModel):
    _name = 'report.product_multi_barcode_cr.product_barcode_details'
    _description = "Product Barcode Values"

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = []
        for product_id in data['form']:
            docs.append(int(product_id))
        if data['model'] == 'generate.barcode.wizard':
            val = self.env['product.product'].browse(docs)
        else:
            val = self.env['product.template'].browse(docs)
        return {'doc_ids':data['ids'],
                'doc_model':data['model'],
                'docs':val,
                'length': data['form']
                }