# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
from odoo import api, exceptions, fields, models, _


class ProductProductInherit(models.Model):
	_inherit = 'product.product'

	set_min_qty = fields.Boolean("Set Minimum Qty", default=False, company_dependent=True)
	min_qty = fields.Integer("Minimum Qty", company_dependent=True)

	@api.onchange("set_min_qty")
	def _get_min_quantity(self):
		if self.set_min_qty:
			self.min_qty = self.env.company.min_quantity
		else:
			self.min_qty = 0

	def _cron_low_stock_quantity(self):
		records = self.env['product.product'].search([('set_min_qty', '=', True)])
		low_product_qty_list = []
		for rec in records:
			if rec.warehouse_id:
				warehouse_id = rec.warehouse_id
			else:
				warehouse_id = self.env['stock.warehouse'].search([('company_id', '=', self.env.company.id)],
																  limit=1)
			available_qty = int(rec.with_context(warehouse=warehouse_id.id).qty_available)
			if available_qty < rec.min_qty:
				low_product_qty_list.append({
					'product_name': rec.display_name,
					'on_hand_qty': available_qty,
					'min_qty': rec.min_qty,
				})
		users = self.env['res.users'].search([])
		user_set = []
		for user in users:
			if user.has_group('stock.group_stock_manager'):
				user_set.append(user.email_formatted)
		email_template = self.env.ref('stock_notification_cr.mail_template_stock_notification_cr')
		email_values = {
			'email_from': self.env.user.email_formatted,
			'email_to': ','.join(user for user in user_set),
		}
		email_template.with_context(low_product_qty_list=low_product_qty_list).send_mail(self.id, force_send=True,
																						 email_values=email_values)
