# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class DayflowDocument(models.Model):
    _name = 'dayflow.document'
    _description = 'Dayflow Employee Document'

    name = fields.Char(string='Document Name', required=True)
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True, ondelete='cascade')
    document_type = fields.Selection([
        ('id_proof', 'ID Proof'),
        ('contract', 'Contract'),
        ('certificate', 'Certificate'),
        ('other', 'Other'),
    ], string='Document Type', default='other', required=True)

    document_file = fields.Binary(string='Attachment / File', required=True)
    file_name = fields.Char(string='File Name')
    file_size = fields.Char(string='File Size', help='Size of uploaded file (e.g. 245 KB)')
    upload_date = fields.Date(string='Upload Date', default=fields.Date.context_today)
    issue_date = fields.Date(string='Issue Date', help='Date when document was issued')
    expiry_date = fields.Date(string='Expiry Date', help='Expiration date of contract or document')

    document_status = fields.Selection([
        ('draft', 'Pending Verification'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected / Action Required'),
        ('expired', 'Expired'),
    ], string='Status', default='draft', tracking=True)

    notes = fields.Text(string='Employee Remarks & Description')
    admin_comments = fields.Text(string='HR / Admin Review Comments')
    verified_by_id = fields.Many2one('res.users', string='Reviewed By', readonly=True)

    @api.constrains('issue_date', 'expiry_date')
    def _check_document_dates(self):
        for record in self:
            if record.issue_date and record.expiry_date:
                if record.expiry_date < record.issue_date:
                    raise ValidationError(_("Document Expiry Date cannot be earlier than Issue Date."))

    def action_verify_document(self):
        """Action for HR/Admin manager to approve and verify the uploaded document."""
        for record in self:
            if not self.env.user.has_group('dayflow.group_dayflow_admin') and not self.env.is_superuser():
                raise UserError(_("Only HR / Admin managers can verify employee documents."))

            record.write({
                'document_status': 'verified',
                'verified_by_id': self.env.user.id,
            })
        return True

    def action_reject_document(self):
        """Action for HR/Admin manager to reject or request revision for the document."""
        for record in self:
            if not self.env.user.has_group('dayflow.group_dayflow_admin') and not self.env.is_superuser():
                raise UserError(_("Only HR / Admin managers can review employee documents."))

            record.write({
                'document_status': 'rejected',
                'verified_by_id': self.env.user.id,
            })
        return True
