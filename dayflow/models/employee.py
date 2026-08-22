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

    def _dayflow_login_component(self, value, fallback):
        """Return a login-safe uppercase component without punctuation."""
        component = re.sub(r'[^A-Z0-9]+', '', (value or '').upper())
        return component or fallback

    def _generate_dayflow_login(self):
        """Generate COMPANY-NAME-YEAR-SERIAL using the configured ORM sequence."""
        self.ensure_one()

        company_component = self._dayflow_login_component(
            self.company_id.name, 'COMPANY'
        )
        name_component = self._dayflow_login_component(self.name, 'EMPLOYEE')
        joining_date = self.dayflow_joining_date or fields.Date.context_today(self)
        joining_year = fields.Date.to_date(joining_date).year
        serial = self.env['ir.sequence'].next_by_code('dayflow.employee.login')

        if not serial:
            raise UserError('The Dayflow Login ID sequence is not configured.')

        return '%s-%s-%s-%s' % (
            company_component, name_component, joining_year, serial
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

        # The sequence makes collisions unlikely, but checking protects against
        # a manually reset or altered sequence.
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
            'tag': 'dayflow.account_provision_success',
            'params': {
                'login': login,
                'temporary_password': initial_password,
            },
        }
