# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
from odoo import fields, http, _
from odoo.http import request


class CreateCrmLead(http.Controller):

    @http.route('/create/crm/lead', type='json', auth="public", website=True, csrf=False)
    def create_crm_lead(self, name=None,email_name=None,product_name=None,\
                                partner_id=None,phone_no=None,question=None,details=None,**post):
        if name and email_name and product_name\
           and partner_id and phone_no and question and details:
            partner = request.env['res.partner'].sudo().browse(partner_id)
            if partner.id ==  request.env.ref('base.public_partner').id:
                user = request.env.ref('base.public_user')
                flag = False    
            else:
                user = request.env['res.users'].sudo().search([('partner_id','=',partner.id)])
                flag = True
            street = partner.street if flag == True else ''
            street2 = partner.street2 if flag == True else ''
            city = partner.city if flag == True else ''
            state_id = partner.state_id.id if flag == True else ''
            zip_val = partner.zip if flag == True else ''
            country_id = partner.country_id.id if flag == True else ''
            website = partner.website if flag == True else ''
            val = {
                    'name': question,
                    'partner_id': partner_id,
                    'partner_name': partner.name,
                    'user_id': user.id,
                    'contact_name': name,
                    'email_from': email_name,
                    'phone': phone_no,
                    'description': details,
                    'type': 'lead',
                    'street': street,
                    'street2': street2,
                    'city': city,
                    'state_id': state_id,
                    'zip': zip_val,
                    'country_id': country_id,
                    'website': website,

                }
            crm_lead_id = request.env['crm.lead'].sudo().create(val)
            if crm_lead_id:
                return {'result':True}
        else:
            return {'result':False}