from odoo import api, fields, models, tools, _


class EmployeeEntryChecklist(models.Model):
    _name = 'employee.entry.checklist'

    name = fields.Char(string="Checklist Item", required=True)
    description = fields.Text(string="Description")

class EmployeeExitChecklist(models.Model):
    _name = 'employee.exit.checklist'

    name = fields.Char("Name")
    description = fields.Text("Description")


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    checklist_ids = fields.Many2many(
        'employee.entry.checklist','check_hr_rel', 'hr_check_rel',
        string="Entry Checklist",
    )
    exit_checklist_ids = fields.Many2many(
        'employee.exit.checklist', 'exit_hr_rel', 'hr_exit_rel',
        string="Entry Checklist"
    )

    checklist_progress = fields.Float(
        string="Checklist Progress", compute="_compute_checklist_progress", store=True
    )

    exit_checklist_progress = fields.Float(
        string="Exit Checklist Progress", compute="_compute_exit_checklist_progress", store=True
    )
    employee_details_id = fields.Many2one('employee.details', string="Employee Details")

    @api.depends('checklist_ids')
    def _compute_checklist_progress(self):
        total_checklist_items = self.env['employee.entry.checklist'].search_count([])

        for employee in self:
            if total_checklist_items > 0:
                completed_items = len(employee.checklist_ids)
                employee.checklist_progress = (completed_items / total_checklist_items) * 100
            else:
                employee.checklist_progress = 0.0

    @api.depends('exit_checklist_ids')
    def _compute_exit_checklist_progress(self):
        total_checklist_items = self.env['employee.exit.checklist'].search_count([])

        for employee in self:
            if total_checklist_items > 0:
                completed_items = len(employee.exit_checklist_ids)
                employee.exit_checklist_progress = (completed_items / total_checklist_items) * 100
            else:
                employee.exit_checklist_progress = 0.0

class HrContract(models.Model):
    _inherit = 'hr.contract'

    employee_details_id = fields.Many2one('employee.details', string="Employee Details")


class HrLeave(models.Model):
    _inherit = 'hr.leave.allocation'

    employee_details_id = fields.Many2one('employee.details', string="Employee Details",related="employee_id.employee_details_id",store=True)

