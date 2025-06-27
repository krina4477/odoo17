# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models,_
import warnings
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

def assert_log_admin_access(method):
    def check_and_log(method, self, *args, **kwargs):
        user = self.env.user
        origin = request.httprequest.remote_addr if request else 'n/a'
        log_data = (method.__name__, self.sudo().mapped('name'), user.login, user.id, origin)
        if not self.env.is_admin():
            _logger.warning('DENY access to module.%s on %s to user %s ID #%s via %s', *log_data)
            raise AccessDenied()
        _logger.info('ALLOW access to module.%s on %s to user %s #%s via %s', *log_data)
        return method(self, *args, **kwargs)
    return decorator(check_and_log, method)

class ModuleINherit(models.Model):
    _inherit = "ir.module.module"

    @assert_log_admin_access
    def button_install(self):
        res=super(ModuleINherit,self).button_install()
        user_id = self.env.user
        for module in self:
            action_log_create = self.env['action.log'].create({
                'date':date.today(),
                'module_name':module.name,
                'user_name':user_id.id,
                'status':'install'
            })
        return res

    def button_immediate_upgrade(self):
        """
        Upgrade the selected module(s) immediately and fully,
        return the next res.config action to execute
        """
        user_id = self.env.user
        action_log_create = self.env['action.log'].create({
                'date':date.today(),
                'module_name':self.name,
                'user_name':user_id.id,
                'status':'upgrade'
            })
        return self._button_immediate_function(type(self).button_upgrade)
 

    @api.model
    def action_uninstall_inherit(self):
        module_ids = self.env['ir.module.module'].browse(self._context.get('active_ids'))
        if module_ids and self.user_has_groups('secure_uninstall_cr.group_allow_to_uninstall_module'):
            view = self.env.ref('secure_uninstall_cr.view_module_uninstall_duplicate')
            wiz = self.env['module.uninstall.duplicate'].create({'module_ids': [(6,0,module_ids.ids)]})
            return {
                'name': _('Please login to Uninstall module'),
                'type': 'ir.actions.act_window',
                'res_model': 'module.uninstall.duplicate',
                'views': [(view.id, 'form')],
                'target': 'new',
                'res_id': wiz.id,
            }

class ActionLog(models.Model):
    _name = 'action.log'
    _description = "Action Log"
    _rec_name = 'module_name'

    date = fields.Date("Date")
    module_name = fields.Char("Module Name")
    status = fields.Selection([('install', 'Install'), ('uninstall', 'Uninstall'),('upgrade','Upgrade')],"Status")
    user_name = fields.Many2one('res.users', "User Name")