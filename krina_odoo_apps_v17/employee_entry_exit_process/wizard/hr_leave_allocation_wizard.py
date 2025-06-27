from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta

class HrLeaveAllocationWizard(models.TransientModel):
    _name = 'hr.leave.allocation.wizard'
    _description = 'Leave Allocation Wizard'

    holiday_status_id = fields.Many2one("hr.leave.type", string="Time Off Type", required=True)
    date_from = fields.Date("Date From", required=True)
    date_to = fields.Date("Date To", required=True)
    no_of_days = fields.Float("Number Of Days", compute="_compute_no_of_days", store=True)
    related_employee_id = fields.Many2one('hr.employee', string="Related Employee", readonly=True)

    @api.depends('date_from', 'date_to')
    def _compute_no_of_days(self):
        for record in self:
            if record.date_from and record.date_to and record.date_from <= record.date_to:
                current_date = record.date_from
                count = 0
                while current_date <= record.date_to:
                    if current_date.weekday() not in [5, 6]:
                        count += 1
                    current_date += timedelta(days=1)
                record.no_of_days = count
            else:
                record.no_of_days = 0

    def action_confirm_leave(self):
        if not self.related_employee_id:
            raise UserError("No employees are linked to this leave allocation. Please check the employee details.")

        leave_ids = []
        for employee in self.related_employee_id:
            # Check for duplicate leave allocation
            existing_leave = self.env['hr.leave.allocation'].search([
                ('employee_id', '=', employee.id),
                ('holiday_status_id', '=', self.holiday_status_id.id),
                ('date_from', '=', self.date_from),
                ('date_to', '=', self.date_to)
            ], limit=1)

            if existing_leave:
                raise UserError(f"Leave allocation for {employee.name} with the same details already exists!")

            # Create new leave allocation
            leave = self.env['hr.leave.allocation'].create({
                'name': f"Leave for {employee.name}",
                'employee_id': employee.id,
                'employee_ids': [(6, 0, [employee.id])],
                'holiday_status_id': self.holiday_status_id.id,
                'date_from': self.date_from,
                'date_to': self.date_to,
                'number_of_days': self.no_of_days,
                'employee_details_id': self._context.get('active_id')
            })
            leave_ids.append(leave.id)

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'hr.leave.allocation',
            'domain': [('id', 'in', leave_ids)],
            'view_mode': 'tree,form',
            'target': 'current',
        }