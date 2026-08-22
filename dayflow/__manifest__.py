# -*- coding: utf-8 -*-
{
    'name': 'Dayflow',
    'summary': 'Human Resource Management System (HRMS) - Odoo × NMIT Hackathon',
    'description': """
Dayflow HRMS Module
===================
Streamlined Human Resource Management System supporting:
- Authentication & Role-based Access Control (Employee vs Admin/HR)
- Employee Profile & Document Management
- Attendance Check-in / Check-out & Tracking
- Leave Application & Approval Workflow
- Payroll & Salary Structure Management
    """,
    'author': 'Odoo × NMIT Hackathon Team',
    'category': 'Human Resources',
    'version': '1.0.0',
    'depends': [
        'base',
        'hr',
        'hr_attendance',
        'hr_holidays',
    ],
    'data': [
        'security/dayflow_security.xml',
        'security/ir.model.access.csv',
        'data/dayflow_sequence.xml',
        'views/menu_views.xml',
        'views/employee_views.xml',
        'views/attendance_views.xml',
        'views/leave_views.xml',
        'views/payroll_views.xml',
        'views/document_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
