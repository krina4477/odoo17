# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _


class SaleOrderLine(models.Model):
	_inherit = "sale.order.line"

	delivery_order_done = fields.Boolean('DO done', default=False, copy=False)


class SaleOrder(models.Model):
	_inherit = "sale.order"

	def _can_be_confirmed(self):
		self.ensure_one()
		return self.state in {'draft', 'sent', 'sale'}
	@api.depends('order_line.delivery_order_done')
	def compute_delivery_order_complete(self):
		for order in self:
			order.update({
				'delivery_order_complete': False if any(sol.delivery_order_done == False for sol in order.order_line) else True,
			})

	delivery_order_complete = fields.Boolean('DO complete', default=False, copy=False, compute=compute_delivery_order_complete)

	def _action_confirm(self):
		if self.env.context.get('do_line_ids'):
			self.order_line.filtered(lambda l: l.id in self.env.context.get('do_line_ids'))._action_launch_stock_rule()
		else:
			self.order_line._action_launch_stock_rule()
		for order in self:
			if any(expense_policy not in [False, 'no'] for expense_policy in order.order_line.mapped('product_id.expense_policy')):
				if not order.analytic_account_id:
					order._create_analytic_account()
		return True

	def action_draft(self):
		orders = self.filtered(lambda s: s.state in ['cancel', 'sent'])
		for oline in orders.order_line:
			oline.write({'delivery_order_done': False})
		return orders.write({
			'state': 'draft',
			'signature': False,
			'signed_by': False,
			'signed_on': False,
			'delivery_order_complete': False,
		})

