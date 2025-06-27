# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _
from datetime import date


class PurchaseOrderInherit(models.Model):
    _inherit = "purchase.order"

    state = fields.Selection([
        ('draft', 'RFQ'),
        ('sent', 'RFQ Sent'),
        ('to approve', 'To Approve'),
        ('finance_approval', 'Waiting Finance Approval'),
        ('director_approval', 'Waiting Director Approval'),
        ('purchase', 'Purchase Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
        ('refuse','Refuse')
    ], string='Status', readonly=True, index=True, copy=False, default='draft', tracking=True)
    approval_department_manager_id = fields.Many2one('res.users',string="Manager Approval",copy=False)
    approval_finance_manager_id = fields.Many2one('res.users',string="Finance Manager Approval ",copy=False)
    approval_director_manager_id = fields.Many2one('res.users',string="Director Approval",copy=False)
    manager_approval_date = fields.Date(string="Manager Approval Date",copy=False)
    finance_approval_date = fields.Date(string="Finance Manager Approval Date",copy=False)
    director_approval_date = fields.Date(string="Director Approval Date",copy=False)
    purchase_manager_id = fields.Many2one('res.users',string="Purchase Manager",copy=False)
    finance_manager_id = fields.Many2one('res.users',string="Finance Manager",copy=False)
    director_manager_id = fields.Many2one('res.users',string="Director Manager",copy=False)
    refuse_by_id = fields.Many2one('res.users',string="Refused By",copy=False)
    refuse_reason = fields.Text(string="Refuse Reason",copy=False)
    refuse_date = fields.Date(string="Refuse Date",copy=False)
    is_purchase_manager = fields.Boolean(string="Is Purchase",compute="_is_active_purchase")
    is_finance_manager = fields.Boolean(string="Is Finance",compute="_is_active_finance")
    is_director_manager = fields.Boolean(string="Is Director",compute="_is_active_director")

    @api.depends('company_id.three_level_approval','state')
    def _is_active_purchase(self):
        for rec in self:
            if rec.user_has_groups('purchase.group_purchase_manager')\
                and rec.company_id.three_level_approval and rec.state == 'to approve':
                rec.is_purchase_manager = True
            else:
                rec.is_purchase_manager = False

    @api.depends('company_id.three_level_approval','state','is_purchase_manager')
    def _is_active_finance(self):
        for rec in self:
            if rec.user_has_groups('po_three_level_approval_cr.group_finance_manager')\
                and rec.company_id.three_level_approval and rec.state == 'finance_approval':
                rec.is_finance_manager = True
                rec.is_purchase_manager = False
            else:
                rec.is_finance_manager = False

    @api.depends('company_id.three_level_approval','state','is_finance_manager')
    def _is_active_director(self):
        for rec in self:
            if rec.user_has_groups('po_three_level_approval_cr.group_director_manager')\
                and rec.company_id.three_level_approval and rec.state == 'director_approval':
                rec.is_director_manager = True
                rec.is_finance_manager = False
            else:
                rec.is_director_manager = False

    # From User To Purchase Manager
    def button_confirm(self):
        res = super(PurchaseOrderInherit,self).button_confirm()
        for rec in self:
            if not rec.order_line:
                return res
            elif rec.amount_total <= rec.company_id.manager_approve_limit:
                rec.write({ 'state':'to approve'})
                rec.picking_ids.sudo().unlink()
                template = self.env.ref('po_three_level_approval_cr.po_approval_template')
                managers = self.env['res.users'].search(
                        [('groups_id', '=', self.env.ref('purchase.group_purchase_manager').id)])
                for manager in managers:
                    val = { 'purchase_order': rec.name,
                            'manager': manager.name or '',
                            'user': rec.user_id.name}
                    template.with_context(val=val).send_mail(rec.id,email_values={ 'subject': 'Approval Purchase Order : %s (Waiting)'%(str(rec.name)),
                                                             'email_from': self.user_id.email,\
                                                             'email_to': manager.login or '',\
                                                             },force_send=True)
                # return res
            return res

    # From Manager To Finance Manager
    def button_approve(self, force=False):
        res = super(PurchaseOrderInherit,self).button_approve(force=force)
        for rec in self:

            if rec.company_id.three_level_approval == False or not rec.order_line:

                return res
            elif rec.amount_total <= rec.company_id.manager_approve_limit and self.env.user.has_group('purchase.group_purchase_manager'):
                rec.write({ 'approval_department_manager_id': self.env.user.id,
                            'manager_approval_date': date.today(),
                            'purchase_manager_id': self.env.user.id,
                            'state':'purchase'})
                rec._create_picking()
                return res
            elif rec.amount_total >= rec.company_id.manager_approve_limit and\
               rec.amount_total <= rec.company_id.finance_approve_limit:
                template = self.env.ref('po_three_level_approval_cr.po_approval_template')                
                managers = self.env['res.users'].search(
                        [('groups_id', 'in', self.env.ref('po_three_level_approval_cr.group_finance_manager').id)])
                for manager in managers:
                    val = { 'purchase_order': rec.name,
                            'manager': manager.name or '',
                            'user': self.env.user.name}
                    template.with_context(val=val).send_mail(rec.id,email_values={ 'subject': 'Approval Purchase Order : %s (Waiting)'%(str(rec.name)),
                                                             'email_from': self.purchase_manager_id.login,\
                                                             'email_to': manager.login or '',\
                                                             },force_send=True)
                rec.write({ 'approval_department_manager_id': self.env.user.id,
                            'manager_approval_date': date.today(),
                            'purchase_manager_id': self.env.user.id,
                            'state':'finance_approval'})
                rec.picking_ids.sudo().unlink()
                return res
            else:
                template = self.env.ref('po_three_level_approval_cr.po_approval_template')                
                managers = self.env['res.users'].search(
                        [('groups_id', 'in', self.env.ref('po_three_level_approval_cr.group_finance_manager').id)])
                for manager in managers:
                    val = { 'purchase_order': rec.name,
                            'manager': manager.name or '',
                            'user': self.env.user.name}
                    template.with_context(val=val).send_mail(rec.id,email_values={ 'subject': 'Approval Purchase Order : %s (Waiting)'%(str(rec.name)),
                                                             'email_from': self.purchase_manager_id.login,\
                                                             'email_to': manager.login or '',\
                                                             },force_send=True)
                
                if self.env.user.has_group('purchase.group_purchase_manager'):
                    rec.write({ 'approval_department_manager_id': self.env.user.id,
                                'manager_approval_date': date.today(),
                                'purchase_manager_id': self.env.user.id,
                                'state':'finance_approval'})
                    rec.picking_ids.sudo().unlink()
                # return res
            return res

    # Finance Manager To Director
    def finance_approve_order(self):
        for rec in self:
            if rec.amount_total > rec.company_id.finance_approve_limit:
                rec.write({ 'approval_finance_manager_id': self.env.user.id,
                            'finance_approval_date': date.today(),
                            'finance_manager_id': self.env.user.id,
                            'state':'director_approval'})
                template = self.env.ref('po_three_level_approval_cr.po_approval_template')
                managers = self.env['res.users'].search(
                        [('groups_id', 'in', self.env.ref('po_three_level_approval_cr.group_director_manager').id)])
                for manager in managers:
                    val = { 'purchase_order': rec.name,
                            'manager': manager.name or '',
                            'user': self.env.user.name}
                    template.with_context(val=val).send_mail(rec.id,email_values={ 'subject': 'Approval Purchase Order : %s (Waiting)'%(str(rec.name)),
                                                             'email_from': self.finance_manager_id.login,\
                                                             'email_to': manager.login or '',\
                                                             },force_send=True)
            else:
                rec.write({ 'approval_finance_manager_id': self.env.user.id,
                            'finance_approval_date': date.today(),
                            'finance_manager_id': self.env.user.id,
                            'state':'purchase'})
                rec._create_picking()
        return True

    # Director Manager Approval
    def director_approval(self):
        self.write({ 'approval_director_manager_id': self.env.user.id,
                     'director_approval_date': date.today(),
                     'director_manager_id': self.env.user.id,
                     'state':'purchase'})
        self._create_picking()
    
    # Refuse Order Wizard
    def button_refuse(self):
        wizard_form = self.env.ref('po_three_level_approval_cr.refuse_wizard_form_view')
        return {
            'name': _('Refuse Purchase Order'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'refuse.po.wizard',
            'views': [(wizard_form.id, 'form')],
            'view_id': wizard_form.id,
            'target': 'new',
        }
