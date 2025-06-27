# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
import logging
import psycopg2
import threading

from odoo import api, fields, models, modules, tools, _

from odoo.exceptions import AccessDenied, UserError

_logger = logging.getLogger(__name__)

ACTION_DICTS = {
    'view_mode': 'form',
    'res_model': 'base.module.upgrade',
    'target': 'new',
    'type': 'ir.actions.act_window',
}


class ModuleUninstall(models.Model):
    _inherit = "ir.module.module"
    _description = "module uninstall upgrade"

    def _button_immediates_function(self, function):
        if not self.env.registry.ready or self.env.registry._init:
            raise UserError(
                _('The method _button_immediate_install cannot be called on init or non loaded registries. Please use button_install instead.'))

        if getattr(threading.current_thread(), 'testing', False):
            raise RuntimeError(
                "Module operations inside tests are not transactional and thus forbidden.\n"
                "If you really need to perform module operations to test a specific behavior, it "
                "is best to write it as a standalone script, and ask the runbot/metastorm team "
                "for help."
            )
        try:
            self._cr.execute("SELECT * FROM ir_cron FOR UPDATE NOWAIT")
        except psycopg2.OperationalError:
            raise UserError(_("Odoo is currently processing a scheduled action.\n"
                              "Module operations are not possible at this time, "
                              "please try again later or contact your system administrator."))
        function(self)

        self._cr.commit()
        registry = modules.registry.Registry.new(self._cr.dbname, update_module=True)
        self._cr.commit()
        self._cr.reset()
        assert self.env.registry is registry

        config = self.env['ir.module.module'].next() or {}
        if config.get('type') not in ('ir.actions.act_window_close',):
            return config

        menu = self.env['ir.ui.menu'].search([('parent_id', '=', False)])[:1]
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
            'params': {'menu_id': menu.id},
        }

    # ______________________ Uninstall module code_____________________________

    def immediate_uninstall_button(self):

        _logger.info('User #%d triggered module uninstallation', self.env.uid)
        return self._button_immediates_function(type(self).button_uninstalls)

    def button_uninstalls(self):
        if 'base' in self.mapped('name'):
            raise UserError(_("The `base` module cannot be uninstalled"))

        deps = self.downstream_dependencies()
        (self + deps).write({'state': 'to remove'})
        return dict(ACTION_DICTS, name=_('Uninstall'))

    def multi_module_uninstall(self):
        modules = self
        return modules.immediate_uninstall_button()

    # ______________________ Upgrade module code_____________________________

    def button_upgrade(self):
        if not self:
            return
        Dependency = self.env['ir.module.module.dependency']
        self.update_list()

        todo = list(self)
        if 'base' in self.mapped('name'):
            # If an installed module is only present in the dependency graph through
            # a new, uninstalled dependency, it will not have been selected yet.
            # An update of 'base' should also update these modules, and as a consequence,
            # install the new dependency.
            todo.extend(self.search([
                ('state', '=', 'installed'),
                ('name', '!=', 'studio_customization'),
                ('id', 'not in', self.ids),
            ]))
        i = 0
        while i < len(todo):
            module = todo[i]
            i += 1
            if module.state not in ('installed', 'to upgrade'):
                raise UserError(_("Can not upgrade module '%s'. It is not installed.") % (module.name,))
            if self.get_module_info(module.name).get("installable", True):
                self.check_external_dependencies(module.name, 'to upgrade')
            for dep in Dependency.search([('name', '=', module.name)]):
                if (
                        dep.module_id.state == 'installed'
                        and dep.module_id not in todo
                        and dep.module_id.name != 'studio_customization'
                ):
                    todo.append(dep.module_id)

        self.browse(module.id for module in todo).write({'state': 'to upgrade'})

        to_install = []
        for module in todo:
            if not self.get_module_info(module.name).get("installable", True):
                continue
            for dep in module.dependencies_id:
                if dep.state == 'unknown':
                    raise UserError(
                        _('You try to upgrade the module %s that depends on the module: %s.\nBut this module is not available in your system.') % (
                            module.name, dep.name,))
                if dep.state == 'uninstalled':
                    to_install += self.search([('name', '=', dep.name)]).ids

        self.browse(to_install).button_install()
        return dict(ACTION_DICTS, name=_('Apply Schedule Upgrade'))

    def multi_module_upgrade(self):
        return self._button_immediates_function(type(self).button_upgrade)
