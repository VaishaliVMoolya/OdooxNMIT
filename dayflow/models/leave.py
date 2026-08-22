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

    def action_dayflow_approve(self):
        """Approve Dayflow leave request (Admin/HR only)."""
        for record in self:
            record.write({
                'dayflow_status': 'approved',
            })
            # Also attempt standard Odoo leave approval if applicable
            if hasattr(record, 'state') and record.state in ['draft', 'confirm']:
                try:
                    record.action_approve()
                except Exception:
                    pass
        return True

    def action_dayflow_reject(self):
        """Reject Dayflow leave request (Admin/HR only)."""
        for record in self:
            record.write({
                'dayflow_status': 'rejected',
            })
            # Also attempt standard Odoo leave refusal if applicable
            if hasattr(record, 'state') and record.state in ['draft', 'confirm']:
                try:
                    record.action_refuse()
                except Exception:
                    pass
        return True

    def action_dayflow_reset_pending(self):
        """Reset Dayflow leave request back to pending."""
        for record in self:
            record.write({
                'dayflow_status': 'pending',
            })
            if hasattr(record, 'state') and record.state in ['refuse', 'cancel']:
                try:
                    record.action_draft()
                except Exception:
                    pass
        return True
