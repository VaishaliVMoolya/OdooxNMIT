import logging
from datetime import datetime, timedelta, time
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError

_logger = logging.getLogger(__name__)


class HrLeave(models.Model):
    _inherit = 'hr.leave'

    dayflow_leave_type = fields.Selection([
        ('paid', 'Paid Time Off'),
        ('sick', 'Sick Leave'),
        ('unpaid', 'Unpaid Leaves'),
    ], string='Dayflow Leave Type', default='paid',
       help='Category of time off: Paid Time Off, Sick Leave, or Unpaid Leaves')

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

    is_half_day = fields.Boolean(
        string='Half-Day Leave',
        default=False,
        help='Indicates if leave is for half-day (0.5 day deduction)'
    )
    half_day_period = fields.Selection([
        ('am', 'First Half (Morning)'),
        ('pm', 'Second Half (Afternoon)'),
    ], string='Half-Day Session', default='am',
       help='Session of the half-day leave')

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
                'state': 'confirm' if hasattr(record, 'state') else False,
            })
            record._send_dayflow_leave_notification('submitted')
        return True

    def action_dayflow_approve(self):
        """Admin / HR approves the time off request and creates attendance records with Leave status."""
        for record in self:
            if hasattr(self.env.user, 'has_group') and not self.env.user.has_group('dayflow.group_dayflow_admin') and not self.env.is_superuser():
                raise UserError(_("Only HR / Admin managers can approve time off requests."))

            record.write({
                'dayflow_status': 'approved',
                'approved_by_id': self.env.user.id,
                'state': 'validate' if hasattr(record, 'state') else False,
            })

            # Integrate with Attendance: generate/update attendance records with status = 'leave'
            record._integrate_leave_with_attendance()

            # Send approval email notification & in-app message to employee
            record._send_dayflow_leave_notification('approved')
        return True

    def action_dayflow_reject(self):
        """Admin / HR rejects the time off request."""
        for record in self:
            if hasattr(self.env.user, 'has_group') and not self.env.user.has_group('dayflow.group_dayflow_admin') and not self.env.is_superuser():
                raise UserError(_("Only HR / Admin managers can reject time off requests."))

            record.write({
                'dayflow_status': 'rejected',
                'approved_by_id': self.env.user.id,
                'state': 'refuse' if hasattr(record, 'state') else False,
            })

            # Send rejection email notification & in-app message to employee
            record._send_dayflow_leave_notification('rejected')
        return True

    def action_dayflow_reset_pending(self):
        """Reset Dayflow leave request back to pending."""
        for record in self:
            record.write({
                'dayflow_status': 'pending',
                'approved_by_id': False,
                'state': 'confirm' if hasattr(record, 'state') else False,
            })
        return True

    def _send_dayflow_leave_notification(self, event_type):
        """Send email alert and in-app chatter notification on leave events."""
        self.ensure_one()
        xmlid_map = {
            'submitted': 'dayflow.email_template_dayflow_leave_submitted',
            'approved': 'dayflow.email_template_dayflow_leave_approved',
            'rejected': 'dayflow.email_template_dayflow_leave_rejected',
        }
        xmlid = xmlid_map.get(event_type)
        if not xmlid:
            return

        try:
            template = self.env.ref(xmlid, raise_if_not_found=False)
            if template:
                template.send_mail(self.id, force_send=False, raise_exception=False)
                _logger.info("Dayflow leave notification '%s' queued for leave ID %s", event_type, self.id)
        except Exception as e:
            # Must not crash leave action if email delivery fails
            _logger.warning("Could not send Dayflow leave notification '%s' for leave ID %s: %s", event_type, self.id, e)

        # In-app chatter message if mail.thread is enabled
        try:
            if hasattr(self, 'message_post'):
                msg_map = {
                    'submitted': _("Time off application submitted for review."),
                    'approved': _("Time off request has been approved by HR."),
                    'rejected': _("Time off request has been rejected. Reason: %s") % (self.admin_comments or _("None")),
                }
                body = msg_map.get(event_type)
                if body:
                    self.message_post(body=body, subtype_xmlid='mail.mt_note')
        except Exception as e:
            _logger.debug("Chatter message post skipped: %s", e)


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
            if current_date.weekday() < 5:
                check_in_dt = datetime.combine(current_date, time(9, 0, 0))
                check_out_dt = datetime.combine(current_date, time(17, 0, 0))

                existing_attendance = attendance_obj.search([
                    ('employee_id', '=', self.employee_id.id),
                    ('check_in', '>=', datetime.combine(current_date, time(0, 0, 0))),
                    ('check_in', '<=', datetime.combine(current_date, time(23, 59, 59))),
                ], limit=1)

                leave_label = dict(self._fields['dayflow_leave_type'].selection).get(self.dayflow_leave_type, 'Leave')
                target_status = 'half_day' if self.is_half_day else 'leave'
                remark_text = _("Approved %s (%s - %s)") % (
                    leave_label,
                    _("Half-Day %s") % (self.half_day_period.upper() if self.half_day_period else 'AM') if self.is_half_day else _("Full Day"),
                    self.remarks or ''
                )

                if existing_attendance:
                    existing_attendance.write({
                        'dayflow_status': target_status,
                        'remarks': remark_text,
                    })
                else:
                    attendance_obj.create({
                        'employee_id': self.employee_id.id,
                        'check_in': check_in_dt,
                        'check_out': check_out_dt,
                        'dayflow_status': target_status,
                        'remarks': remark_text,
                    })

            current_date += timedelta(days=1)
