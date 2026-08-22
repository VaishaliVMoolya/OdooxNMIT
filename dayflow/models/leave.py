# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HrLeave(models.Model):
    _inherit = 'hr.leave'

    dayflow_leave_type = fields.Selection([
        ('paid', 'Paid'),
        ('sick', 'Sick'),
        ('unpaid', 'Unpaid'),
    ], string='Dayflow Leave Type', default='paid', help='Leave category for Dayflow HRMS (Odoo holiday_status_id is primary ORM leave type)')

    dayflow_status = fields.Selection([
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string='Dayflow Status', default='pending', help='Review status for Dayflow HRMS leave workflow (Odoo state is primary ORM leave state)')

    remarks = fields.Text(string='Application Remarks')
    admin_comments = fields.Text(string='HR / Admin Comments')

    @api.constrains('request_date_from', 'request_date_to', 'date_from', 'date_to')
    def _check_leave_dates_validity(self):
        for record in self:
            start = record.request_date_from or (record.date_from.date() if record.date_from else False)
            end = record.request_date_to or (record.date_to.date() if record.date_to else False)
            if start and end and end < start:
                raise ValidationError(_('Leave end date cannot be earlier than start date.'))

