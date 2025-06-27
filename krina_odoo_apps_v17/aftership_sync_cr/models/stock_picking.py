# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

import logging
import aftership
from odoo import fields, models, _
from odoo.exceptions import ValidationError
import time
_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    courier_id = fields.Many2one('aftership.courier.list', 'Courier', tracking=True)
    tracking_no = fields.Char("Tracking Number", tracking=True,readonly=True)
    aftership_tracking_id = fields.Many2one('aftership.tracking', 'Tracking ID', readonly=True)

    def action_view_tracking(self):
        view_id = self.env.ref('aftership_sync_cr.view_aftership_tracking_tree').id
        form_view_id = self.env.ref('aftership_sync_cr.view_aftership_tracking_form').id
        context = self._context.copy()
        return {
            'name': 'AfterShip Tracking',
            'view_type': 'form',
            'view_mode': 'tree',
            'res_model': 'aftership.tracking',
            'view_id': view_id,
            'views': [(view_id, 'tree'), (form_view_id, 'form')],
            'type': 'ir.actions.act_window',
            'domain': [('sale_id', '=', self.sale_id.id)],
            'target': 'current',
            'context': context,
        }

    def _action_done(self):
        res = super(StockPicking, self)._action_done()
        if self.state == 'done':
            if self.courier_id and self.sale_id:
                tracking_no = str(time.time()).replace('.','')
                self.tracking_no = tracking_no
                self.set_tracking_number_aftership()
        return res

    def set_tracking_number_aftership(self):
        for picking in self:
            aftership_api_key = self.env['ir.config_parameter'].sudo().get_param('aftership_api_key')
            custom_fields = {'amount': picking.sale_id.amount_total}
            # api = aftership.APIv4(aftership_api_key)
            aftership.api_key = aftership_api_key
            slug = picking.courier_id.slug_name
            number = picking.tracking_no
            partner_name = picking.partner_id.name
            title = "Sale Order - " + picking.sale_id.name
            language = self.env['res.lang'].search([('code', '=', picking.partner_id.lang)])
            try:
                aftership.tracking.create_tracking(tracking=dict(custom_fields=custom_fields,
                    slug=slug,
                    tracking_postal_code=picking.partner_id.zip,
                    tracking_ship_date=str(picking.scheduled_date.date()),
                    tracking_origin_country=picking.company_id.country_id.name,
                    tracking_destination_country=picking.partner_id.company_id.country_id.name,
                    tracking_state=picking.partner_id.state_id.name,
                    emails=picking.partner_id.email,
                    smses=picking.partner_id.mobile,
                    tracking_number=number,
                    order_id=picking.name,
                    customer_name=partner_name,
                    title=title,
                    language=language[0].iso_code,
                    ))
                tracking_vals = {
                    'name': picking.sale_id.name + ' - ' + picking.name,
                    'sale_id': picking.sale_id.id,
                    'picking_id': picking.id,
                    'partner_id': picking.partner_id.id,
                    'courier_id': picking.courier_id.id,
                    'tracking_no': number
                }
                tracking_id = self.env['aftership.tracking'].create(tracking_vals)
                picking.aftership_tracking_id = tracking_id.id
            except aftership.exception.NotFound as error:
                _logger.error("Error while creating tracking %s", error)
                raise ValidationError(_(
                    "Error while creating tracking %s" % (error)))
