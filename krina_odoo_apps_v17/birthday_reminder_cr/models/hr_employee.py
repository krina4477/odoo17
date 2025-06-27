# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
from datetime import datetime
import logging
from odoo import SUPERUSER_ID
from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)

class HrEmployee(models.Model):
    _inherit = "hr.employee"

    @api.model
    def _cron_birthday_reminder(self):
        su_id = self.env['res.users'].browse(SUPERUSER_ID)
        if not self:
            employee_ids = self.env['hr.employee'].sudo().search([('birthday', '!=', False)])
        else:
            employee_ids = self
        for employee in employee_ids:
            if employee.birthday:
                bdate = datetime.strptime(str(employee.birthday), '%Y-%m-%d').date()
                today = datetime.now().date()
                if bdate.month == today.month:
                    if bdate.day == today.day:
                        message_body = ''
                        if not employee.parent_id:
                            _logger.info('Manager is missing for the employee!')
                        if not employee.parent_id.user_id:
                            _logger.info('User is missing for manager of the employee!')
                        if employee.parent_id:
                            message_body += _("Hi  %(manager)s ", manager=employee.parent_id.name)
                            message_body += _(" An employee  %(emp)s   from department %(dept)s has a birthday today. ",
                                             emp=employee.name, dept=employee.department_id.name)
                            message_body += _(" Please take this opportunity to reach out to %(emp)s and wish happy birthday!",
                                             emp=employee.name)
                        employee.message_notify(
                                subject=_("Birthday Reminder"),
                                body=message_body,
                                partner_ids=[employee.parent_id.user_id.partner_id.id],
                                email_layout_xmlid='mail.mail_notification_light',
                            )

        return True