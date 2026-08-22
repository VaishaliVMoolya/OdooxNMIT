# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, timedelta, time


class HrLeave(models.Model):
    _inherit = 'hr.leave'

    dayflow_leave_type = fields.Selection([
        ('paid', 'Paid Time Off'),
        ('sick', 'Sick Leave'),
        ('unpaid', 'Unpaid Leaves'),
    ], string='Dayflow Leave Type', default='paid',
       help='Category of time off: Paid Time Off (Annual/Casual), Sick Leave, or Unpaid Leaves')

    dayflow_status = fields.Selection([
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string='Dayflow Status', default='pending', tracking=True,
       help='Review status for Dayflow HRMS leave workflow (Pending, Approved, Rejected)')

    attachment_submitted = fields.Boolean(
        string='Medical Certificate / Document Attached',
        default=False,
        help='Indicates whether medical document/certificate is attached for Sick Leave'
    )

    remarks = fields.Text(string='Employee Remarks / Reason')
    admin_comments = fields.Text(string='HR / Admin Decision Comments')
    approved_by_id = fields.Many2one('res.users', string='Approved/Reviewed By', readonly=True)

    @api.constrains('request_date_from', 'request_date_to')
    def _check_dayflow_leave_dates(self):
        for record in self:
            if record.request_date_from and record.request_date_to:
                if record.request_date_to < record.request_date_from:
                    raise ValidationError(_("The End Date cannot be earlier than the Start Date."))

    def action_dayflow_submit(self):
        """Employee submits time off request for approval."""
        for record in self:
            record.write({
                'dayflow_status': 'pending',
                'state': 'confirm',
            })
        return True

    def action_dayflow_approve(self):
        """Admin / HR approves the time off request and creates attendance records with Leave status."""
        for record in self:
            if not self.env.user.has_group('dayflow.group_dayflow_admin') and not self.env.is_superuser():
                raise UserError(_("Only HR / Admin managers can approve time off requests."))

            record.write({
                'dayflow_status': 'approved',
                'approved_by_id': self.env.user.id,
                'state': 'validate',
            })

            # Integrate with Attendance: generate/update attendance records with status = 'leave'
            record._integrate_leave_with_attendance()
        return True

    def action_dayflow_reject(self):
        """Admin / HR rejects the time off request."""
        for record in self:
            if not self.env.user.has_group('dayflow.group_dayflow_admin') and not self.env.is_superuser():
                raise UserError(_("Only HR / Admin managers can reject time off requests."))

            record.write({
                'dayflow_status': 'rejected',
                'approved_by_id': self.env.user.id,
                'state': 'refuse',
            })
        return True

    def _integrate_leave_with_attendance(self):
        """Creates or updates hr.attendance records for approved leave dates."""
        self.ensure_one()
        if not self.employee_id:
            return

        start_date = self.request_date_from
        end_date = self.request_date_to or self.request_date_from

        if not start_date or not end_date:
            return

        current_date = start_date
        attendance_obj = self.env['hr.attendance']

        while current_date <= end_date:
            # Skip Saturday (5) and Sunday (6) for regular business days
            if current_date.weekday() < 5:
                # Target start and end of day timestamp
                check_in_dt = datetime.combine(current_date, time(9, 0, 0))
                check_out_dt = datetime.combine(current_date, time(17, 0, 0))

                # Check if an attendance record already exists for this employee and date
                existing_attendance = attendance_obj.search([
                    ('employee_id', '=', self.employee_id.id),
                    ('check_in', '>=', datetime.combine(current_date, time(0, 0, 0))),
                    ('check_in', '<=', datetime.combine(current_date, time(23, 59, 59))),
                ], limit=1)

                leave_label = dict(self._fields['dayflow_leave_type'].selection).get(self.dayflow_leave_type, 'Leave')

                if existing_attendance:
                    existing_attendance.write({
                        'dayflow_status': 'leave',
                        'remarks': _("Approved %s (%s)") % (leave_label, self.remarks or ''),
                    })
                else:
                    attendance_obj.create({
                        'employee_id': self.employee_id.id,
                        'check_in': check_in_dt,
                        'check_out': check_out_dt,
                        'dayflow_status': 'leave',
                        'remarks': _("Approved %s (%s)") % (leave_label, self.remarks or ''),
                    })

            current_date += timedelta(days=1)
