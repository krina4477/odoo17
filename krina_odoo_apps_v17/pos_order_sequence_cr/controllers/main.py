# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
from odoo import conf, http, _
from odoo.http import content_disposition, Controller, request, route

class NewSeq(Controller):


        @http.route(['/new_seq'], type='json')
        def new_seq(self, **kw):
            kw = kw.get('kwargs')
            sale_sequence_id = request.env['ir.config_parameter'].sudo().get_param('sale_ir_sequence_id')
            sale_ir_sequence = request.env['ir.config_parameter'].sudo().get_param('is_sale_ir_sequence')
            if sale_sequence_id and sale_ir_sequence:
                seq_id = request.env['ir.sequence'].browse([int(sale_sequence_id)])
                pos_id = request.env['pos.order'].sudo().search([('pos_reference', '=', kw.get('old_name'))])
                pos_id.pos_reference = seq_id.next_by_id()
                return pos_id.pos_reference
            else:
                return kw.get('old_name')
