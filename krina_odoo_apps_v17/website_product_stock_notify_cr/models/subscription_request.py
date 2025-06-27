# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class SubscriptionRequests(models.Model):
    _name = 'subscription.requests'
    _description = 'Subscription Requests'
    _rec_name = 'product_id'

    customer = fields.Char('Customer')
    product_id = fields.Many2one('product.template', 'Product')
    user_id = fields.Many2one('res.users', 'User')
    customer_email = fields.Char('Customer Email')
    customer_phone_no = fields.Char('Customer Contact No.')
    Company = fields.Char('Company')
    state = fields.Selection([('draft', 'Draft'), ('notified', 'Notified'), ('cancel', 'Cancel')], string='Status',
                             readonly=True, copy=False, default='draft')

    def notify_button(self):
        subscription_rec = self.env['subscription.requests'].search(
            [('state', '=', 'draft'), ('product_id.qty_available', '>', 0)])
        for rec in subscription_rec:
            if rec:
                template_id = self.env.ref('website_product_stock_notify_cr.notification_stock_available_template').id
                template = self.env['mail.template'].sudo().browse(template_id)
                template.send_mail(rec.id, force_send=True)
                rec.state = 'notified'

    def notify_cancel_button(self):
        self.state = 'cancel'
