# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

from odoo import fields, models, _


class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    create_auto_quote = fields.Boolean(string="Create Automatic Quotation?", default=False, copy=False)
    product_id = fields.Many2one('product.product', string="Service Product", default=False, copy=False,
                                 domain=[('detailed_type','=','service')], required=True)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    related_task_id = fields.Many2one('project.task', copy=False, string="Related Task", readonly=False)

    def action_view_related_task(self):
        action_window = {
            "type": "ir.actions.act_window",
            "res_model": "project.task",
            "name": _("Project Tasks"),
            "res_id": self.related_task_id.id,
            "views": [[False, "form"]],
            "context": {"create": False, "show_sale": True},
        }
        return action_window


class ProjectTask(models.Model):
    _inherit = 'project.task'

    create_auto_quote = fields.Boolean(string="Create Automatic Quotation?",
                                       related='stage_id.create_auto_quote',
                                       default=False, copy=False)
    saleorder_id = fields.Many2one('sale.order', copy=False, string="Sale Order", readonly=False)

    def write(self, vals):
        res = super().write(vals)
        if vals and vals.get('stage_id',False) and self.stage_id.create_auto_quote:
            self.write({'create_auto_quote': self.stage_id.create_auto_quote})
        return res

    def action_created_so(self):
        action_window = {
            "type": "ir.actions.act_window",
            "res_model": "sale.order",
            "name": _("Sales Order"),
            "res_id": self.saleorder_id.id,
            "views": [[False, "form"]],
            "context": {"create": False, "show_sale": True},
        }
        return action_window

    def generate_quote(self):
        service_type = self.env.ref('sale_timesheet.time_product_product_template')
        sale_order_vals = {
            'partner_id': self.partner_id.id,
            'related_task_id': self.id,
        }
        order_line_dict = []
        line_dict = {}
        service_product_id = self.stage_id.product_id.id
        for line in self.timesheet_ids:
            for p_line in line.product_qty_ids:
                if not p_line.product_id.id in line_dict:
                    line_dict[p_line.product_id.id] = p_line.quantity
                else:
                    line_dict[p_line.product_id.id] = line_dict[p_line.product_id.id] + p_line.quantity
            if line.unit_amount:
                order_line_dict.append(
                    (0, 0, {'product_id': service_product_id, 'name': line.name, 'product_uom_qty': line.unit_amount}))
        order_line_dict += [(0, 0, {'product_id': ol, 'product_uom_qty': line_dict[ol]}) for ol in line_dict]
        sale_order_vals['order_line'] = order_line_dict
        so_id = self.env['sale.order'].create(sale_order_vals)
        self.write({'saleorder_id': so_id.id})
        return so_id


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    product_qty_ids = fields.One2many('product.qty.timesheet', 'timesheet_id', 'Product Qty Timesheet')