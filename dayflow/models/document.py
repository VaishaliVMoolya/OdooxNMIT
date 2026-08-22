# -*- coding: utf-8 -*-
from odoo import models, fields


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
    ], string='Document Type', default='other')
    document_file = fields.Binary(string='Attachment / File', required=True)
    file_name = fields.Char(string='File Name')
    upload_date = fields.Date(string='Upload Date', default=fields.Date.context_today)
    notes = fields.Text(string='Notes')
