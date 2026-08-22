# -*- coding: utf-8 -*-
from odoo import models, fields, api


class DayflowPayroll(models.Model):
    _name = 'dayflow.payroll'
    _description = 'Dayflow Payroll Entry'

    name = fields.Char(string='Reference', required=True, default='New')
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True, ondelete='cascade')
    salary_structure = fields.Char(string='Salary Structure', default='Standard Base')
    
    # Wireframes 3 & 4 Salary Computation Fields
    monthly_wage = fields.Float(string='Monthly Wage', default=50000.0, required=True)
    yearly_wage = fields.Float(string='Yearly Wage', compute='_compute_salary_breakdown', store=True)
    
    base_salary = fields.Float(string='Basic Salary (50%)', compute='_compute_salary_breakdown', store=True)
    hra = fields.Float(string='House Rent Allowance (HRA 50% of Basic)', compute='_compute_salary_breakdown', store=True)
    standard_allowance = fields.Float(string='Standard Allowance (16.67%)', compute='_compute_salary_breakdown', store=True)
    performance_bonus = fields.Float(string='Performance Bonus (8.33%)', compute='_compute_salary_breakdown', store=True)
    lta = fields.Float(string='Leave Travel Allowance (LTA 8.33%)', compute='_compute_salary_breakdown', store=True)
    fixed_allowance = fields.Float(string='Fixed Allowance (Remainder)', compute='_compute_salary_breakdown', store=True)
    
    allowances = fields.Float(string='Total Allowances', compute='_compute_salary_breakdown', store=True)
    
    pf_deduction = fields.Float(string='PF Contribution (12% of Basic)', compute='_compute_salary_breakdown', store=True)
    prof_tax = fields.Float(string='Professional Tax', default=200.0)
    deductions = fields.Float(string='Total Deductions', compute='_compute_salary_breakdown', store=True)
    
    net_salary = fields.Float(string='Net Salary', compute='_compute_salary_breakdown', store=True)
    payroll_status = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('paid', 'Paid'),
    ], string='Status', default='draft')
    pay_period = fields.Char(string='Pay Period', help='e.g., August 2026')
    notes = fields.Text(string='Notes')

    @api.depends('monthly_wage', 'prof_tax')
    def _compute_salary_breakdown(self):
        for record in self:
            wage = record.monthly_wage or 0.0
            record.yearly_wage = wage * 12.0
            
            # Wireframe 4 Formula Rules
            basic = round(wage * 0.50, 2)
            hra_val = round(basic * 0.50, 2)
            std_val = round(wage * (16.67 / 100.0), 2)
            bonus_val = round(wage * (8.33 / 100.0), 2)
            lta_val = round(wage * (8.33 / 100.0), 2)
            
            allocated = basic + hra_val + std_val + bonus_val + lta_val
            fixed_val = max(0.0, round(wage - allocated, 2))
            
            tot_allowances = round(hra_val + std_val + bonus_val + lta_val + fixed_val, 2)
            pf_val = round(basic * 0.12, 2)
            ptax_val = record.prof_tax or 200.0
            tot_deductions = round(pf_val + ptax_val, 2)
            
            record.base_salary = basic
            record.hra = hra_val
            record.standard_allowance = std_val
            record.performance_bonus = bonus_val
            record.lta = lta_val
            record.fixed_allowance = fixed_val
            record.allowances = tot_allowances
            record.pf_deduction = pf_val
            record.deductions = tot_deductions
            record.net_salary = round(basic + tot_allowances - tot_deductions, 2)

    def action_approve(self):
        for record in self:
            record.payroll_status = 'approved'
        return True

    def action_pay(self):
        for record in self:
            record.payroll_status = 'paid'
        return True

    def action_draft(self):
        for record in self:
            record.payroll_status = 'draft'
        return True
