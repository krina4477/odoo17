# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
from . import models


def post_init(env):
    env['payment.provider'].search([]).write({
        'tag_ids': env.ref('payment_customer_tags_cr.res_partner_category_all', False)
    })

def uninstall_hook(env):
    payment_ids = env['payment.provider'].search([('tag_ids', 'in', env.ref('payment_customer_tags_cr.res_partner_category_all', False).id)])
    payment_ids.write({'tag_ids': (2, env.ref('payment_customer_tags_cr.res_partner_category_all', False).id)})
    partner_ids = env['res.partner'].search(
        [('category_id', 'in', env.ref('payment_customer_tags_cr.res_partner_category_all', False).id)])
    partner_ids.write({'category_id': (2, env.ref('payment_customer_tags_cr.res_partner_category_all', False).id)})

