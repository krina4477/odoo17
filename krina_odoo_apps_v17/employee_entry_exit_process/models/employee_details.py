from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError


class EmployeeDetails(models.Model):
    _name = 'employee.details'

    name = fields.Char("Name")
    email = fields.Char('Email')
    job_position = fields.Many2one("hr.job", string="Job Position", required=True)
    manager_id = fields.Many2one('hr.employee', string="Manager", required=True)
    phone = fields.Char(string="Phone", required=True)
    date_of_birth = fields.Date(string="Date of Birth", required=True)
    address = fields.Text(string="Address", required=True)
    joining_date = fields.Date('Joining Date')
    salary_amount = fields.Integer('Salary Amount')

    employee_ids = fields.One2many('hr.employee', 'employee_details_id', string="Employees")
    contract_ids = fields.One2many('hr.contract', 'employee_details_id', string="Contracts")
    leave_ids = fields.One2many('hr.leave.allocation', 'employee_details_id', string="Leaves")

    employee_count = fields.Integer(compute="_compute_employee_count", string="Employees")
    contract_count = fields.Integer(compute="_compute_contract_count", string="Contracts")
    leave_count = fields.Integer(compute="_compute_leave_count", string="Leaves")

    def action_create_employee(self):
        employees = self.env['hr.employee']  # Empty recordset to store created employees
        for record in self:
            # Check if an employee already exists with the same details
            existing_employee = self.env['hr.employee'].search([
                ('work_email', '=', record.email),
                ('active', '=', True),
                ('birthday', '=', record.date_of_birth),
            ], limit=1)

            if existing_employee:
                raise ValidationError(f"An employee with email {record.email} and same details already exists.")

            # Create a new employee if no match is found
            hr_employee = self.env['hr.employee'].create({
                'name': record.name,
                'work_email': record.email,
                'job_id': record.job_position.id,
                'parent_id': record.manager_id.id,
                'private_phone': record.phone,
                'birthday': record.date_of_birth,
                'private_street': record.address,
                'employee_details_id': record.id,
            })
            employees += hr_employee

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'hr.employee',
            'res_id': employees[0].id if len(employees) == 1 else False,
            'domain': [('id', 'in', employees.ids)] if len(employees) > 1 else [],
            'view_mode': 'form' if len(employees) == 1 else 'tree,form',
            'target': 'current',
        }

    def action_create_portal_user(self):
        for record in self:
            employee = self.env['hr.employee'].search([('work_email', '=', record.email)], limit=1)

            if not employee:
                raise ValidationError(
                    _("No employee found with this email: %s. Please create an employee first.") % record.email)

            action = employee.action_create_user()
            action['context'] = dict(action.get('context', {}),
                                     default_groups_id=[(6, 0, [self.env.ref('base.group_portal').id])])

            return action

    # def action_create_contract(self):
    #     """Call the existing `action_open_contract` method from `hr.employee`"""
    #     self.ensure_one()
    #     employee = self.env['hr.employee'].search([('work_email', '=', self.email)], limit=1)
    #     if not employee:
    #         raise ValidationError(_("No employee found with this email. Please create an employee first."))
    #
    #     return employee.action_open_contract()

    def action_create_contract(self):
        contracts = self.env['hr.contract']

        for record in self:
            employee = self.env['hr.employee'].search([('employee_details_id', '=', record.id)], limit=1)

            if not employee:
                raise ValidationError(
                    _("No employee found for this record: %s. Please create an employee first.") % record.name)

            existing_contract = self.env['hr.contract'].search([
                ('employee_id', '=', employee.id),
                ('state', 'not in', ['close', 'cancel'])
            ], limit=1)

            if existing_contract:
                raise ValidationError(
                    _("An active contract already exists for this employee: %s.") % employee.name)


            contract = self.env['hr.contract'].create({
                'name': f"{employee.name} Contract",
                'employee_id': employee.id,
                'employee_details_id': record.id,
                'wage': record.salary_amount or 0,
                'date_start': record.joining_date or fields.Date.today(),
            })

            contracts += contract

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'hr.contract',
            'domain': [('id', 'in', contracts.ids)],
            'view_mode': 'tree,form',
            'target': 'current',
        }

    # def action_open_leave_wizard(self):
    #     """Opens the leave allocation wizard for the selected employee."""
    #     employee = self.env['hr.employee'].search([('name', '=', self.name)], limit=1)
    #     return {
    #         'name': "Allocate Leave",
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'hr.leave.allocation.wizard',
    #         'view_mode': 'form',
    #         'target': 'new',
    #         'context': {
    #             'default_related_employee_id': employee.id if employee else False,
    #         }
    #     }

    def action_open_leave_wizard(self):
        self.ensure_one()
        employees = self.env['hr.employee'].search([
            '|',
            ('employee_details_id', '=', self.id),
            ('name', '=', self.name),
            ('active', '=', True)
        ])

        if not employees:
            raise ValidationError("No employee found for this record. Please create an employee first.")

        actions = []
        for employee in employees:
            action = {
                'name': "Allocate Leave",
                'type': 'ir.actions.act_window',
                'res_model': 'hr.leave.allocation.wizard',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'default_related_employee_id': employee.id
                }
            }
            actions.append(action)

        return actions if len(actions) > 1 else actions[0]

    @api.depends('email')
    def _compute_employee_count(self):
        for record in self:
            record.employee_count = self.env['hr.employee'].search_count([('work_email', '=', record.email)])

    @api.depends('contract_ids')
    def _compute_contract_count(self):
        for record in self:
            record.contract_count = len(record.contract_ids)

    @api.depends('leave_ids')
    def _compute_leave_count(self):
        for record in self:
            record.leave_count = len(record.leave_ids)

    def action_open_employees(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Employees',
            'res_model': 'hr.employee',
            'domain': [('work_email', '=', self.email)],
            'view_mode': 'tree,form',
            'target': 'current',
        }

    def action_open_contracts(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Contracts',
            'res_model': 'hr.contract',
            'domain': [('employee_id.employee_details_id', '=', self.id)],
            'view_mode': 'tree,form',
            'target': 'current',
        }

    def action_open_leaves(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Leaves',
            'res_model': 'hr.leave.allocation',
            'domain': [('employee_details_id', '=', self.id)],
            'view_mode': 'tree,form',
            'target': 'current',
        }
