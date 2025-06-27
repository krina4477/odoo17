# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models,_
from odoo.exceptions import ValidationError
import passlib.context
from datetime import date
import logging
from odoo.http import request
from decorator import decorator


_logger = logging.getLogger(__name__)


DEFAULT_CRYPT_CONTEXT = passlib.context.CryptContext(
	['pbkdf2_sha512', 'plaintext'],
	deprecated=['plaintext'],
)

class BaseModuleUninstallDuplicate(models.TransientModel):
	_name = "module.uninstall.duplicate"
	_description = "Base Module Uninstall Duplicate"

	email = fields.Char('Email')
	password = fields.Char('Password')
	module_id = fields.Many2one(
		'ir.module.module', string="Module",
		domain=[('state', 'in', ['installed', 'to upgrade', 'to install'])],
		ondelete='cascade', readonly=True,
	)

	module_ids = fields.Many2many('ir.module.module', string="Module")

	def action_uninstall(self):
		user_id = self.env.user

		self.env.cr.execute(
			"SELECT COALESCE(password, '') FROM res_users WHERE id=%s",
			[self.env.user.id])
		[hashed] = self.env.cr.fetchone()
		valid, pw = DEFAULT_CRYPT_CONTEXT.verify_and_update(self.password, hashed)
		
		if self.email == user_id.login and valid:
			uninstall_list = []
			if self.module_ids:
				for module in self.module_ids:
					action_log_create = self.env['action.log'].create({
						'date':date.today(),
						'module_name':module.name,
						'user_name':user_id.id,
						'status':'uninstall'
						})
				return self.module_ids.button_immediate_uninstall()
			else:
				action_log_create = self.env['action.log'].create({
				'date':date.today(),
				'module_name':self.module_id.name,
				'user_name':user_id.id,
				'status':'uninstall'
				})

				return self.module_id.button_immediate_uninstall()
		else:
			raise ValidationError(_('Wrong login/password'))


class BaseModuleUninstall(models.TransientModel):
	_inherit = "base.module.uninstall"

	def action_uninstall(self):
		modules = self.mapped('module_id')
		if self.user_has_groups('secure_multi_uninstall_cr.group_allow_to_uninstall_module'):
			view = self.env.ref('secure_multi_uninstall_cr.view_module_uninstall_duplicate')
			wiz = self.env['module.uninstall.duplicate'].create({'module_id': modules.id})
			val = {
				'name': _('Please login to Uninstall module'),
				'type': 'ir.actions.act_window',
				'view_type': 'form',
				'view_mode': 'form',
				'res_model': 'module.uninstall.duplicate',
				'views': [(view.id, 'form')],
				'view_id': view.id,
				'target': 'new',
				'res_id': wiz.id,
			}
			return val
		else:
			raise ValidationError(_('You are not allowed to Uninstall Module, Please contact Administrator'))
