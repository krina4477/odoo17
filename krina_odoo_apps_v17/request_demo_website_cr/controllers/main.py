# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
from odoo import fields, http, _
from odoo.http import request



class CreateDemoRequest(http.Controller):

    @http.route('/thankyou_page', type='json', auth="public", website=True, csrf=False)
    def demo_response_thank_you(self, name=None, email_name=None, product_name=None, details=None):
        if name and email_name and product_name and details:
            val = {
                'name': 'Request Demo For %s' % (product_name),
                'contact_name': name,
                'email_from': email_name,
                'description': details,
                'type': 'lead'
            }
            crm_lead_id = request.env['crm.lead'].sudo().create(val)
            partner_id = request.env.ref('base.public_partner').id
            if crm_lead_id and request.env.user.id != partner_id:
                mail_values = {
                    'email_to': crm_lead_id.email_from,
                    'state': 'outgoing',
                    'message_type': 'email',
                }
                template_id = request.env.ref(
                    'request_demo_website_cr.confirmation_email_template')
                template_id.send_mail(
                    crm_lead_id.id, email_values=mail_values, force_send=True)
            return {'result': True}

        else:
            return {'result': False}
