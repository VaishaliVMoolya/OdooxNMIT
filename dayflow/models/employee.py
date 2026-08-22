# -*- coding: utf-8 -*-
from odoo import models, fields


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    dayflow_role = fields.Selection([
        ('employee', 'Employee'),
        ('hr', 'Admin / HR'),
    ], string='Dayflow Role', default='employee', help='Role access within Dayflow HRMS')

    document_ids = fields.One2many(
        'dayflow.document', 'employee_id', string='Documents'
    )
    payroll_ids = fields.One2many(
        'dayflow.payroll', 'employee_id', string='Payroll Records'
    )
    notes = fields.Text(string='Dayflow Notes')
