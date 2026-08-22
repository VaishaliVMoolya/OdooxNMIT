# -*- coding: utf-8 -*-
import re
import secrets

from odoo import fields, models
from odoo.exceptions import AccessError, UserError


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    dayflow_role = fields.Selection([
        ('employee', 'Employee'),
        ('hr', 'Admin / HR'),
    ], string='Dayflow Role', default='employee', help='Role access within Dayflow HRMS')

    dayflow_joining_date = fields.Date(
        string='Dayflow Joining Date',
        default=fields.Date.context_today,
        copy=False,
        help='Used as the joining-year component of the Dayflow Login ID.',
    )

    document_ids = fields.One2many(
        'dayflow.document', 'employee_id', string='Documents'
    )
    payroll_ids = fields.One2many(
        'dayflow.payroll', 'employee_id', string='Payroll Records'
    )
    notes = fields.Text(string='Dayflow Notes')

    # Private Information
    pan_no = fields.Char(string='PAN Number', help='Permanent Account Number')
    aadhar_no = fields.Char(string='Aadhaar Number', help='12-digit Aadhaar UID')
    passport_no = fields.Char(string='Passport Number')
    bank_name = fields.Char(string='Bank Name', default='HDFC Bank')
    bank_account_no = fields.Char(string='Bank Account Number')
    ifsc_code = fields.Char(string='IFSC Code')
    emergency_contact_name = fields.Char(string='Emergency Contact Name')
    emergency_contact_phone = fields.Char(string='Emergency Contact Phone')
    emergency_contact_relation = fields.Char(string='Relationship')
    personal_email = fields.Char(string='Personal Email')
    personal_phone = fields.Char(string='Personal Mobile')

    # Salary & Compensation Structure
    monthly_wage = fields.Float(string='Monthly Base Wage', default=50000.0)
    salary_structure = fields.Char(string='Salary Structure', default='Standard Base')
    basic_salary = fields.Float(string='Basic Salary (50%)', compute='_compute_salary_breakdown', store=True)
    hra_allowance = fields.Float(string='HRA (50% of Basic)', compute='_compute_salary_breakdown', store=True)
    standard_allowance = fields.Float(string='Standard Allowance', compute='_compute_salary_breakdown', store=True)
    performance_bonus = fields.Float(string='Performance Bonus', compute='_compute_salary_breakdown', store=True)
    lta_allowance = fields.Float(string='LTA', compute='_compute_salary_breakdown', store=True)
    pf_deduction = fields.Float(string='PF Deduction (12% of Basic)', compute='_compute_salary_breakdown', store=True)
    pt_deduction = fields.Float(string='Professional Tax', default=200.0)
    net_take_home = fields.Float(string='Net Monthly Salary', compute='_compute_salary_breakdown', store=True)

    def _compute_salary_breakdown(self):
        for rec in self:
            wage = rec.monthly_wage or 0.0
            basic = round(wage * 0.50, 2)
            hra = round(basic * 0.50, 2)
            std_allow = round(wage * 0.1667, 2)
            bonus = round(wage * 0.0833, 2)
            lta = round(wage * 0.0833, 2)
            pf = round(basic * 0.12, 2)
            pt = rec.pt_deduction or 200.0

            rec.basic_salary = basic
            rec.hra_allowance = hra
            rec.standard_allowance = std_allow
            rec.performance_bonus = bonus
            rec.lta_allowance = lta
            rec.pf_deduction = pf

            total_allowances = hra + std_allow + bonus + lta
            total_deductions = pf + pt
            rec.net_take_home = round(basic + total_allowances - total_deductions, 2)

    def _dayflow_login_component(self, value, fallback):
        """Return a login-safe uppercase component without punctuation."""
        component = re.sub(r'[^A-Z0-9]+', '', (value or '').upper())
        return component or fallback

    def _generate_dayflow_login(self):
        """Generate Login ID following Wireframe 1 formula:
        [OI][First 2 letters of first & last name][Year of joining][Serial]
        Example: OIJODO20260001
        """
        self.ensure_one()

        company_prefix = "OI"
        name_parts = (self.name or "John Doe").strip().split()
        if len(name_parts) >= 2:
            name_code = (name_parts[0][:2] + name_parts[-1][:2]).upper()
        else:
            name_code = (self.name[:4] if len(self.name or '') >= 4 else 'EMPLOYEE').upper()

        joining_date = self.dayflow_joining_date or fields.Date.context_today(self)
        joining_year = fields.Date.to_date(joining_date).year
        raw_serial = self.env['ir.sequence'].next_by_code('dayflow.employee.login') or '0001'
        serial = str(raw_serial).zfill(4)

        return '%s%s%s%s' % (
            company_prefix, name_code, joining_year, serial
        )

    def action_provision_dayflow_user(self):
        """Create and link the employee's native Odoo user account.

        The generated password is returned only in this one-time client
        notification; it is never persisted on a Dayflow model.
        """
        self.ensure_one()

        if not self.env.user.has_group('dayflow.group_dayflow_admin'):
            raise AccessError('Only Dayflow HR/Admin users can provision accounts.')

        self.check_access_rights('write')
        self.check_access_rule('write')

        if self.user_id:
            raise UserError('This employee already has an Odoo user account.')

        group_xmlid = (
            'dayflow.group_dayflow_admin'
            if self.dayflow_role == 'hr'
            else 'dayflow.group_dayflow_employee'
        )
        group = self.env.ref(group_xmlid)
        user_model = self.env['res.users'].sudo().with_context(active_test=False)

        login = self._generate_dayflow_login()
        if user_model.search_count([('login', '=ilike', login)]):
            raise UserError('The generated Login ID already exists. Please retry.')

        initial_password = secrets.token_urlsafe(24)
        user_values = {
            'name': self.name,
            'login': login,
            'password': initial_password,
            'company_id': self.company_id.id,
            'company_ids': [(6, 0, [self.company_id.id])],
            'groups_id': [(6, 0, [group.id])],
        }
        user = user_model.with_context(no_reset_password=True).create(user_values)
        self.write({'user_id': user.id})

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Dayflow account provisioned',
                'message': (
                    'Login ID: %s\nInitial password: %s\n'
                    'Share this password securely and ask the employee to change it.'
                ) % (login, initial_password),
                'type': 'success',
                'sticky': True,
            },
        }
