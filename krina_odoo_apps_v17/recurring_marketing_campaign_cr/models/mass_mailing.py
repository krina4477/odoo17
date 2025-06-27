# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
from datetime import datetime
from odoo import api, fields, models, tools, _, SUPERUSER_ID
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError


class MailingMailingScheduleDateInherit(models.TransientModel):
    _inherit = "mailing.mailing.schedule.date"
    
    enddate_time = fields.Datetime('End on',required=True)
    is_recurring = fields.Selection([
        ('daily','Daily'),
        ('week','Weekly'),
        ('monthly','Monthly'),
        ('yearly','Yearly'),
        ])
    
    @api.onchange('enddate_time')
    def _onchange_enddate_time(self):
        if self.enddate_time:
            if self.enddate_time < self.schedule_date:
                raise ValidationError(_('The start date must be anterior to the end date.'))
    
    def action_schedule_date(self):
        super(MailingMailingScheduleDateInherit,self).action_schedule_date()
        total_create_id = 0
        start_date = self.schedule_date
        end_date = self.enddate_time
        
        if self.is_recurring == 'daily':
            while start_date.date() < end_date.date():
                total_create_id += 1
                start_date += timedelta(days=1)
                res = self.mass_mailing_id.copy()
                res.write({'schedule_date': start_date, 'state': 'in_queue'})
                
                
        if self.is_recurring == 'week':
            while start_date.date() < end_date.date():
                start_date += timedelta(days=7)
                if start_date.date() <= end_date.date():
                    total_create_id += 1
                    res = self.mass_mailing_id.copy()
                    res.write({'schedule_date': start_date, 'state': 'in_queue'})
                
        if self.is_recurring == 'monthly':
            while start_date.date() < end_date.date():
                start_date += relativedelta(months=1)
                if start_date.date() <= end_date.date():
                    total_create_id += 1
                    res = self.mass_mailing_id.copy()
                    res.write({'schedule_date': start_date, 'state': 'in_queue'})
                
        if self.is_recurring == 'yearly':
            while start_date.date() < end_date.date():
                start_date += relativedelta(years=1)
                if start_date.date() <= end_date.date():
                    total_create_id += 1
                    res = self.mass_mailing_id.copy()
                    res.write({'schedule_date': start_date, 'state': 'in_queue'})                        

