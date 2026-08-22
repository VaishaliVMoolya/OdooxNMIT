# -*- coding: utf-8 -*-
from odoo import fields, models
from odoo.exceptions import AccessError


class DayflowAccountProvisionWizard(models.TransientModel):
    _name = 'dayflow.account.provision.wizard'
    _description = 'Dayflow Employee Account Provisioning'

    company_id = fields.Many2one(
        'res.company',
        string='Company Name',
        required=True,
        default=lambda self: self.env.company,
    )
    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)
    work_email = fields.Char(string='Email')
    work_phone = fields.Char(string='Phone')
    joining_date = fields.Date(
        string='Joining Date',
        required=True,
        default=fields.Date.context_today,
    )
    dayflow_role = fields.Selection([
        ('employee', 'Employee'),
        ('hr', 'Admin / HR'),
    ], string='Role', required=True, default='employee')

    def action_create_account(self):
        """Create the employee, then delegate all credential work to Phase 1."""
        self.ensure_one()
        if not self.env.user.has_group('dayflow.group_dayflow_admin'):
            raise AccessError('Only Dayflow HR/Admin users can create employee accounts.')

        employee = self.env['hr.employee'].create({
            'name': '%s %s' % (self.first_name.strip(), self.last_name.strip()),
            'company_id': self.company_id.id,
            'work_email': self.work_email,
            'work_phone': self.work_phone,
            'dayflow_joining_date': self.joining_date,
            'dayflow_role': self.dayflow_role,
        })
        return employee.action_provision_dayflow_user()
