# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

import logging
from odoo import api, fields, models, _
import aftership
import pprint

_logger = logging.getLogger(__name__)

AFTERSHIP_DELIVERY_STATUS = {
    'Pending': 'pending',
    'InfoReceived': 'inforeceived',
    'InTransit': 'intransit',
    'OutForDelivery': 'outfordelivery',
    'AttemptFail': 'attemptfail',
    'Delivered': 'delivered',
    'Exception': 'exception',
    'Expired': 'expired'
}


class AftershipCourierList(models.Model):
    _name = 'aftership.courier.list'
    _inherit = ['mail.thread']
    _order = "active,name"
    _description = "Aftership Courier List"

    name = fields.Char('Courier Name', tracking=True)
    other_name = fields.Char('Courier Other Name', tracking=True)
    lang_id = fields.Many2one('res.lang', 'language', tracking=True)
    country_id = fields.Many2one('res.country', 'Country', tracking=True)
    phone = fields.Char('Phone', tracking=True)
    web_url = fields.Char('Web URL', tracking=True)
    slug_name = fields.Char('Slug Name', readonly=True)
    active = fields.Boolean("Active", default=True)

    @api.model
    def _cron_generate_courier_list(self):
        aftership_api_key = self.env['ir.config_parameter'].sudo().get_param('aftership_api_key')
        try:
            # api = aftership.APIv4(aftership_api_key)
            aftership.api_key = aftership_api_key
            couriers = aftership.courier.list_couriers()
            _logger.info(
                'Aftership: get data from aftership %s', pprint.pformat(couriers))
            if couriers:
                for courier in couriers['couriers']:
                    exe_courier_id = self.search([('slug_name', '=', courier['slug'])])
                    if not exe_courier_id:
                        lang_id = self.env['res.lang'].search(
                            [('active', 'in', (True, False)), ('iso_code', '=', courier['default_language'])], limit=1)
                        vals = {
                            'name': courier['name'],
                            'other_name': courier['other_name'],
                            'lang_id': lang_id.id,
                            'phone': courier['phone'],
                            'web_url': courier['web_url'],
                            'slug_name': courier['slug'],
                        }
                        if courier['service_from_country_iso3']:
                            country_id = self.env['res.country'].search(
                                [('code_alpha3', '=', courier['service_from_country_iso3'][0])], limit=1)
                            vals.update({'country_id': country_id.id})
                        self.create(vals)

        except aftership.exception.NotFound as error:
            _logger.error("Error while fetching the courier list %s", error)


class AftershipTracking(models.Model):
    _name = "aftership.tracking"
    _inherit = ['mail.thread']
    _description = "Aftership Tracking"

    name = fields.Char('Name')
    sale_id = fields.Many2one('sale.order', string="Sale Order")
    picking_id = fields.Many2one('stock.picking', string="Delivery Order")
    tracking_no = fields.Char("Tracking Number")
    partner_id = fields.Many2one("res.partner", 'Partner')
    courier_id = fields.Many2one('aftership.courier.list', 'Courier')
    state = fields.Selection([
        ('pending', 'Pending'),
        ('inforeceived', 'Info Received'),
        ('intransit', 'In Transit'),
        ('outfordelivery', 'Out For Delivery'),
        ('attemptfail', 'AttemptFail'),
        ('delivered', 'Delivered'),
        ('exception', 'Exception'),
        ('expired', 'Expired'),
        ('cancel', 'Canceled')], 'Status',
        copy=False, default='pending', index=True, tracking=True)
    state_pending = fields.Integer('Pending State')
    state_intransit = fields.Integer('In Transit State')
    state_outfordelivery = fields.Integer('Out For Delivery State')
    state_delivered = fields.Integer('Delivered State')

    def write(self, vals):
        vals.update(self._set_state_field(vals))
        return super(AftershipTracking, self).write(vals)

    def _set_state_field(self, vals):
        res = {}
        if 'state' in vals:
            if vals['state'] == 'pending':
                res['state_pending'] = 1
                res['state_intransit'] = 0
                res['state_outfordelivery'] = 0
                res['state_delivered'] = 0
            if vals['state'] == 'intransit':
                res['state_intransit'] = 2
                res['state_outfordelivery'] = 0
                res['state_delivered'] = 0
            if vals['state'] == 'outfordelivery':
                res['state_outfordelivery'] = 3
                res['state_delivered'] = 0
            if vals['state'] == 'delivered':
                res['state_delivered'] = 4
        return res

    @api.model
    def _cron_get_tracking_status(self):
        aftership_api_key = self.env['ir.config_parameter'].sudo().get_param('aftership_api_key')
        tracking_ids = self.search([('state', 'not in', ('delivered', 'cancel'))])
        _logger.info("Perform status fetch %s", tracking_ids)
        if tracking_ids:
            for tracking in tracking_ids:
                slug = tracking.courier_id.slug_name
                try:
                    aftership.api_key = aftership_api_key
                    res = aftership.tracking.get_tracking(slug=slug,
                                                             tracking_number=tracking.tracking_no,
                                                             fields=['title', 'checkpoints'])
                    _logger.info('Aftership: get data from aftership %s', pprint.pformat(res))
                    if res:
                        state = res['tracking']['tag']
                        tracking.state = AFTERSHIP_DELIVERY_STATUS[state]
                except aftership.exception.NotFound as error:
                    _logger.error("Error while fetching the courier list %s", error)
