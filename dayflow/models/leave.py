# -*- coding: utf-8 -*-
from odoo import models, fields


class HrLeave(models.Model):
    _inherit = 'hr.leave'

    dayflow_leave_type = fields.Selection([
        ('paid', 'Paid'),
        ('sick', 'Sick'),
        ('unpaid', 'Unpaid'),
    ], string='Dayflow Leave Type', default='paid', help='Leave category for Dayflow HRMS')

    dayflow_status = fields.Selection([
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string='Dayflow Status', default='pending', help='Review status for Dayflow HRMS leave workflow')

    remarks = fields.Text(string='Application Remarks')
    admin_comments = fields.Text(string='HR / Admin Comments')
