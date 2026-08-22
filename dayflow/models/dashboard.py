# -*- coding: utf-8 -*-
from datetime import datetime, time

from odoo import api, fields, models


class DayflowDashboard(models.Model):
    _name = 'dayflow.dashboard'
    _description = 'Dayflow HRMS Admin Dashboard'

    total_employees = fields.Integer(string='Total Employees', compute='_compute_dashboard_data')
    present_today = fields.Integer(string='Present Today', compute='_compute_dashboard_data')
    on_leave_today = fields.Integer(string='On Leave Today', compute='_compute_dashboard_data')
    pending_leave_requests = fields.Integer(string='Pending Leave Requests', compute='_compute_dashboard_data')
    total_payroll = fields.Float(string='Total Net Payroll', compute='_compute_dashboard_data')

    employee_ids = fields.Many2many(
        'hr.employee', compute='_compute_dashboard_data', string='Employees'
    )
    attendance_ids = fields.Many2many(
        'hr.attendance', compute='_compute_dashboard_data', string="Today's Attendance"
    )
    pending_leave_ids = fields.Many2many(
        'hr.leave', compute='_compute_dashboard_data', string='Pending Leave Requests'
    )
    payroll_ids = fields.Many2many(
        'dayflow.payroll', compute='_compute_dashboard_data', string='Payroll Overview'
    )

    @api.depends()
    def _compute_dashboard_data(self):
        today = fields.Date.context_today(self)
        day_start = datetime.combine(today, time.min)
        day_end = datetime.combine(today, time.max)

        employees = self.env['hr.employee'].search([])
        attendance_today = self.env['hr.attendance'].search([
            ('check_in', '>=', fields.Datetime.to_string(day_start)),
            ('check_in', '<=', fields.Datetime.to_string(day_end)),
        ], order='check_in desc')
        pending_leave = self.env['hr.leave'].search([
            ('dayflow_status', '=', 'pending'),
        ], order='request_date_from asc')
        leave_today = self.env['hr.leave'].search([
            ('request_date_from', '<=', today),
            ('request_date_to', '>=', today),
            '|',
            ('state', 'in', ('validate', 'validate1')),
            ('dayflow_status', '=', 'approved'),
        ])
        payroll = self.env['dayflow.payroll'].search([], order='employee_id, name')

        # Present employees: either marked present or checked in today without check out
        present_employees = attendance_today.filtered(
            lambda r: r.dayflow_status in ('present', 'half_day') or not r.check_out
        ).mapped('employee_id')

        total_net_payroll = sum(payroll.mapped('net_salary'))

        for dashboard in self:
            dashboard.total_employees = len(employees)
            dashboard.present_today = len(present_employees)
            dashboard.on_leave_today = len(set(leave_today.mapped('employee_id.id')))
            dashboard.pending_leave_requests = len(pending_leave)
            dashboard.total_payroll = total_net_payroll
            dashboard.employee_ids = employees
            dashboard.attendance_ids = attendance_today
            dashboard.pending_leave_ids = pending_leave
            dashboard.payroll_ids = payroll

    @api.model
    def get_dashboard_data(self):
        """Returns live dashboard metrics and data payload for the OWL dashboard client action."""
        today = fields.Date.context_today(self)
        day_start = datetime.combine(today, time.min)
        day_end = datetime.combine(today, time.max)

        # 1. Employees
        employees = self.env['hr.employee'].search([], order='name asc')
        total_employees = len(employees)

        # 2. Today's Attendance
        attendances_today = self.env['hr.attendance'].search([
            ('check_in', '>=', fields.Datetime.to_string(day_start)),
            ('check_in', '<=', fields.Datetime.to_string(day_end)),
        ], order='check_in desc')
        present_employee_ids = attendances_today.filtered(
            lambda r: r.dayflow_status in ('present', 'half_day') or not r.check_out
        ).mapped('employee_id.id')
        present_today_count = len(set(present_employee_ids))

        # 3. On Leave Today
        leaves_today = self.env['hr.leave'].search([
            ('request_date_from', '<=', today),
            ('request_date_to', '>=', today),
            '|',
            ('state', 'in', ('validate', 'validate1')),
            ('dayflow_status', '=', 'approved'),
        ])
        on_leave_employee_ids = set(leaves_today.mapped('employee_id.id'))
        on_leave_today_count = len(on_leave_employee_ids)

        # 4. Pending Leave Requests
        pending_leaves_records = self.env['hr.leave'].search([
            ('dayflow_status', '=', 'pending'),
        ], order='request_date_from asc')
        pending_leaves_count = len(pending_leaves_records)

        # 5. Payroll
        payrolls = self.env['dayflow.payroll'].search([], order='employee_id, name')
        total_payroll_sum = sum(payrolls.mapped('net_salary'))

        # Prepare formatted pending leaves list
        pending_leaves_list = []
        for leave in pending_leaves_records:
            pending_leaves_list.append({
                'id': leave.id,
                'employee_id': leave.employee_id.id,
                'employee_name': leave.employee_id.name or 'Unknown',
                'department': leave.employee_id.department_id.name or 'General',
                'leave_type': leave.dayflow_leave_type.capitalize() if leave.dayflow_leave_type else 'Paid',
                'date_from': str(leave.request_date_from or ''),
                'date_to': str(leave.request_date_to or ''),
                'number_of_days': leave.number_of_days or 1.0,
                'remarks': leave.remarks or leave.name or '—',
                'dayflow_status': leave.dayflow_status or 'pending',
            })

        # Prepare formatted today's attendance list
        attendance_list = []
        for att in attendances_today:
            check_in_str = att.check_in.strftime('%H:%M') if att.check_in else '—'
            check_out_str = att.check_out.strftime('%H:%M') if att.check_out else '—'
            status_label = (
                'Present' if att.dayflow_status == 'present'
                else ('Absent' if att.dayflow_status == 'absent'
                      else ('Half-day' if att.dayflow_status == 'half_day'
                            else ('Leave' if att.dayflow_status == 'leave'
                                  else 'Present')))
            )
            attendance_list.append({
                'id': att.id,
                'employee_id': att.employee_id.id,
                'employee_name': att.employee_id.name or 'Unknown',
                'department': att.employee_id.department_id.name or 'General',
                'check_in': check_in_str,
                'check_out': check_out_str,
                'status': status_label,
                'dayflow_status': att.dayflow_status or 'present',
                'worked_hours': round(att.worked_hours, 2) if att.worked_hours else 0.0,
                'extra_hours': round(att.extra_hours, 2) if att.extra_hours else 0.0,
            })

        # Prepare formatted employee directory list
        employee_list = []
        for emp in employees:
            if emp.id in present_employee_ids:
                status_text = 'Present'
                status_class = 'badge-success'
            elif emp.id in on_leave_employee_ids:
                status_text = 'On Leave'
                status_class = 'badge-warning'
            else:
                status_text = 'Not Checked In'
                status_class = 'badge-secondary'

            employee_list.append({
                'id': emp.id,
                'name': emp.name,
                'barcode': emp.barcode or f'EMP-{emp.id:04d}',
                'department': emp.department_id.name if emp.department_id else 'General',
                'designation': emp.job_title or (emp.job_id.name if emp.job_id else 'Staff'),
                'work_email': emp.work_email or '—',
                'work_phone': emp.work_phone or emp.phone or '—',
                'dayflow_role': 'Admin / HR' if emp.dayflow_role == 'hr' else 'Employee',
                'status': status_text,
                'status_class': status_class,
            })

        # Prepare formatted payroll list
        payroll_list = []
        for pay in payrolls:
            payroll_list.append({
                'id': pay.id,
                'name': pay.name,
                'employee_id': pay.employee_id.id,
                'employee_name': pay.employee_id.name or 'Unknown',
                'department': pay.employee_id.department_id.name if pay.employee_id.department_id else 'General',
                'salary_structure': pay.salary_structure or 'Standard Base',
                'pay_period': pay.pay_period or '—',
                'base_salary': f"{pay.base_salary:,.2f}",
                'allowances': f"{pay.allowances:,.2f}",
                'deductions': f"{pay.deductions:,.2f}",
                'net_salary': f"{pay.net_salary:,.2f}",
                'payroll_status': pay.payroll_status or 'draft',
            })

        return {
            'kpi': {
                'total_employees': total_employees,
                'present_today': present_today_count,
                'on_leave_today': on_leave_today_count,
                'pending_leave_requests': pending_leaves_count,
                'total_payroll': f"{total_payroll_sum:,.2f}",
            },
            'pending_leaves': pending_leaves_list,
            'attendance': attendance_list,
            'employees': employee_list,
            'payroll': payroll_list,
        }

    @api.model
    def action_quick_approve_leave(self, leave_id):
        """Quick approve a leave request from the dashboard."""
        leave = self.env['hr.leave'].browse(leave_id)
        if leave.exists():
            leave.action_dayflow_approve()
            return {'success': True, 'message': 'Leave request approved successfully.'}
        return {'success': False, 'message': 'Leave request not found.'}

    @api.model
    def action_quick_reject_leave(self, leave_id, admin_comments=''):
        """Quick reject a leave request from the dashboard."""
        leave = self.env['hr.leave'].browse(leave_id)
        if leave.exists():
            if admin_comments:
                leave.admin_comments = admin_comments
            leave.action_dayflow_reject()
            return {'success': True, 'message': 'Leave request rejected.'}
        return {'success': False, 'message': 'Leave request not found.'}

    def _open_action(self, xml_id, domain=None, context=None):
        self.ensure_one()
        action = self.env.ref(xml_id).read()[0]
        if domain is not None:
            action['domain'] = domain
        if context is not None:
            action['context'] = context
        return action

    def action_open_employees(self):
        return self._open_action('dayflow.action_dayflow_employee')

    def action_open_attendance(self):
        return self._open_action('dayflow.action_dayflow_attendance')

    def action_open_leave_requests(self):
        return self._open_action('dayflow.action_dayflow_leave')

    def action_open_pending_leaves(self):
        return self._open_action(
            'dayflow.action_dayflow_leave',
            [('dayflow_status', '=', 'pending')],
        )

    def action_open_payroll(self):
        return self._open_action('dayflow.action_dayflow_payroll')

    def action_open_documents(self):
        return self._open_action('dayflow.action_dayflow_document')