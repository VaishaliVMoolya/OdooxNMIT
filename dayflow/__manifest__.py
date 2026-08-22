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
        'web',
        'auth_signup',
        'hr',
        'hr_attendance',
        'hr_holidays',
    ],
    'data': [
        'security/dayflow_security.xml',
        'security/ir.model.access.csv',
        'data/dayflow_sequence.xml',
        'data/leave_data.xml',
        'views/dashboard_views.xml',
        'views/auth_login_templates.xml',
        'views/account_provision_wizard_views.xml',
        'views/menu_views.xml',
        'views/employee_views.xml',
        'views/attendance_views.xml',
        'views/leave_views.xml',
        'views/payroll_views.xml',
        'views/document_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'dayflow/static/src/dashboard/dayflow_dashboard.scss',
            'dayflow/static/src/dashboard/dayflow_dashboard.xml',
            'dayflow/static/src/dashboard/dayflow_dashboard.js',
            'dayflow/static/src/scss/dayflow_auth.scss',
            'dayflow/static/src/js/dayflow_account_success.js',
            'dayflow/static/src/xml/dayflow_account_success.xml',
        ],
        'web.assets_frontend': [
            'dayflow/static/src/scss/dayflow_auth.scss',
        ],
        'web.assets_frontend_minimal': [
            'dayflow/static/src/js/dayflow_login.js',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
