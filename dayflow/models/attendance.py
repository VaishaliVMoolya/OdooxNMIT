# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


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

    @api.constrains('check_in', 'check_out')
    def _check_validity_check_out(self):
        for record in self:
            if record.check_in and record.check_out and record.check_out < record.check_in:
                raise ValidationError(_('Check-out time cannot be earlier than Check-in time.'))

