# -*- coding: utf-8 -*-
from odoo import models, fields, api


class DayflowPayroll(models.Model):
    _name = 'dayflow.payroll'
    _description = 'Dayflow Payroll Entry'

    name = fields.Char(string='Reference', required=True, default='New')
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True, ondelete='cascade')
    salary_structure = fields.Char(string='Salary Structure', default='Standard Base')
    base_salary = fields.Float(string='Base Salary', required=True, default=0.0)
    allowances = fields.Float(string='Allowances', default=0.0)
    deductions = fields.Float(string='Deductions', default=0.0)
    net_salary = fields.Float(string='Net Salary', compute='_compute_net_salary', store=True)
    payroll_status = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('paid', 'Paid'),
    ], string='Status', default='draft')
    pay_period = fields.Char(string='Pay Period', help='e.g., August 2026')
    notes = fields.Text(string='Notes')

    @api.depends('base_salary', 'allowances', 'deductions')
    def _compute_net_salary(self):
        for record in self:
            record.net_salary = record.base_salary + record.allowances - record.deductions

    def action_approve(self):
        """Approve payroll record (Admin/HR only)."""
        for record in self:
            record.payroll_status = 'approved'
        return True

    def action_pay(self):
        """Mark payroll record as paid (Admin/HR only)."""
        for record in self:
            record.payroll_status = 'paid'
        return True

    def action_draft(self):
        """Reset payroll record to draft (Admin/HR only)."""
        for record in self:
            record.payroll_status = 'draft'
        return True
