# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    dayflow_status = fields.Selection([
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('half_day', 'Half-day'),
        ('leave', 'Leave'),
    ], string='Dayflow Status', default='present',
       compute='_compute_dayflow_status', store=True, readonly=False,
       help='Attendance status tracking for Dayflow HRMS (Present, Absent, Half-day, Leave)')

    extra_hours = fields.Float(
        string='Extra Hours',
        compute='_compute_hours_breakdown',
        store=True,
        default=0.0,
        help='Extra hours worked beyond standard 8 hours'
    )
    effective_hours = fields.Float(
        string='Effective Hours',
        compute='_compute_hours_breakdown',
        store=True,
        default=0.0,
        help='Effective worked hours'
    )
    remarks = fields.Text(string='Remarks')

    @api.depends('worked_hours', 'check_in', 'check_out')
    def _compute_hours_breakdown(self):
        for record in self:
            hours = record.worked_hours or 0.0
            record.effective_hours = round(hours, 2)
            if hours > 8.0:
                record.extra_hours = round(hours - 8.0, 2)
            else:
                record.extra_hours = 0.0

    @api.depends('worked_hours', 'check_in', 'check_out')
    def _compute_dayflow_status(self):
        for record in self:
            if record.dayflow_status == 'leave':
                continue
            if not record.check_in:
                record.dayflow_status = 'absent'
            elif not record.check_out:
                record.dayflow_status = 'present'
            else:
                if record.worked_hours >= 4.0:
                    record.dayflow_status = 'present'
                elif record.worked_hours > 0.0:
                    record.dayflow_status = 'half_day'
                else:
                    record.dayflow_status = 'absent'

    @api.constrains('check_in', 'check_out')
    def _check_validity_check_out(self):
        for record in self:
            if record.check_in and record.check_out and record.check_out < record.check_in:
                raise ValidationError(_('Check-out time cannot be earlier than Check-in time.'))

    @api.model
    def employee_check_in(self, employee_id=None):
        """Action for an employee to check in."""
        if not employee_id:
            employee = self.env.user.employee_id
        else:
            employee = self.env['hr.employee'].browse(employee_id)

        if not employee:
            raise UserError(_("No employee profile found linked to current user."))

        open_attendance = self.search([
            ('employee_id', '=', employee.id),
            ('check_out', '=', False),
        ], limit=1)

        if open_attendance:
            raise ValidationError(_("Employee %s is already checked in since %s.") % (
                employee.name, open_attendance.check_in.strftime('%Y-%m-%d %H:%M:%S')
            ))

        return self.create({
            'employee_id': employee.id,
            'check_in': fields.Datetime.now(),
            'dayflow_status': 'present',
        })

    @api.model
    def employee_check_out(self, employee_id=None):
        """Action for an employee to check out."""
        if not employee_id:
            employee = self.env.user.employee_id
        else:
            employee = self.env['hr.employee'].browse(employee_id)

        if not employee:
            raise UserError(_("No employee profile found linked to current user."))

        open_attendance = self.search([
            ('employee_id', '=', employee.id),
            ('check_out', '=', False),
        ], limit=1)

        if not open_attendance:
            raise ValidationError(_("No active check-in record found for employee %s.") % employee.name)

        open_attendance.write({
            'check_out': fields.Datetime.now(),
        })
        return open_attendance

    def action_check_in(self):
        """Form view button trigger for Check In."""
        return self.employee_check_in()

    def action_check_out(self):
        """Form view button trigger for Check Out."""
        return self.employee_check_out()
