# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _
from datetime import date


class RefusePoWizard(models.TransientModel):
    _name = "refuse.po.wizard"
    _description = "Refuse PO Wizard"

    reason = fields.Text(string="Reason")

    def refuse_order(self):
        active_id = self._context.get('active_id')
        purchase_rec = self.env['purchase.order'].browse(active_id)
        if purchase_rec:
            purchase_rec.write({'refuse_by_id': self.env.user.id,
                                'refuse_reason': self.reason or '',
                                'refuse_date': date.today(),
                                'state': 'refuse'})
            template = self.env.ref('po_three_level_approval_cr.po_refusal_template')
            val = { 'purchase_order': purchase_rec.name,
                    'manager': self.env.user.name,
                    'user': purchase_rec.user_id.name,
                    'reason': self.reason}
            template.with_context(val=val).send_mail(purchase_rec.id,email_values={ 'subject': 'Purchase Order : %s (Refused)'%(str(purchase_rec.name)),
                                                     'email_from': self.env.user.email,\
                                                     'email_to': purchase_rec.user_id.email,\
                                                     },force_send=True)
        return True
