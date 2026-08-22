# -*- coding: utf-8 -*-
from odoo import models, fields


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    dayflow_status = fields.Selection([
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('half_day', 'Half-day'),
        ('leave', 'Leave'),
    ], string='Dayflow Status', default='present', help='Attendance status tracking for Dayflow HRMS')

    extra_hours = fields.Float(string='Extra Hours', default=0.0)
    remarks = fields.Text(string='Remarks')
