# -*- coding: utf-8 -*-
"""
Dayflow HRMS — Live Interactive Dashboard Preview Server
Odoo x NMIT Hackathon
"""
import os
import json
import webbrowser
from flask import Flask, render_template_string, jsonify, request

app = Flask(__name__)

# Initial In-Memory Database State (mirroring Dayflow Odoo Models)
DATA = {
    "employees": [
        {"id": 1, "name": "Suhas Sharma", "barcode": "EMP-0001", "department": "Engineering", "designation": "Senior Python Developer", "work_email": "suhas.sharma@dayflow.org", "work_phone": "+91 98765 43210", "dayflow_role": "hr", "status": "Present"},
        {"id": 2, "name": "Rahul Kumar", "barcode": "EMP-0002", "department": "Product", "designation": "Product Manager", "work_email": "rahul.kumar@dayflow.org", "work_phone": "+91 98765 43211", "dayflow_role": "employee", "status": "Present"},
        {"id": 3, "name": "Anu Shetty", "barcode": "EMP-0003", "department": "Human Resources", "designation": "HR Specialist", "work_email": "anu.shetty@dayflow.org", "work_phone": "+91 98765 43212", "dayflow_role": "hr", "status": "On Leave"},
        {"id": 4, "name": "Pooja Hegde", "barcode": "EMP-0004", "department": "Design", "designation": "UI/UX Lead", "work_email": "pooja.hegde@dayflow.org", "work_phone": "+91 98765 43213", "dayflow_role": "employee", "status": "Present"},
        {"id": 5, "name": "Vikram Adiga", "barcode": "EMP-0005", "department": "Engineering", "designation": "DevOps Engineer", "work_email": "vikram.adiga@dayflow.org", "work_phone": "+91 98765 43214", "dayflow_role": "employee", "status": "Not Checked In"},
        {"id": 6, "name": "Divya Rao", "barcode": "EMP-0006", "department": "Finance", "designation": "Payroll Analyst", "work_email": "divya.rao@dayflow.org", "work_phone": "+91 98765 43215", "dayflow_role": "employee", "status": "Present"},
    ],
    "attendance": [
        {"id": 1, "employee_id": 1, "employee_name": "Suhas Sharma", "department": "Engineering", "check_in": "09:02", "check_out": "17:30", "status": "Present", "dayflow_status": "present", "worked_hours": 8.47, "extra_hours": 0.47},
        {"id": 2, "employee_id": 2, "employee_name": "Rahul Kumar", "department": "Product", "check_in": "09:15", "check_out": "—", "status": "Present", "dayflow_status": "present", "worked_hours": 5.20, "extra_hours": 0.0},
        {"id": 3, "employee_id": 4, "employee_name": "Pooja Hegde", "department": "Design", "check_in": "09:30", "check_out": "—", "status": "Present", "dayflow_status": "present", "worked_hours": 4.95, "extra_hours": 0.0},
        {"id": 4, "employee_id": 6, "employee_name": "Divya Rao", "department": "Finance", "check_in": "08:55", "check_out": "17:05", "status": "Present", "dayflow_status": "present", "worked_hours": 8.17, "extra_hours": 0.17},
        {"id": 5, "employee_id": 3, "employee_name": "Anu Shetty", "department": "Human Resources", "check_in": "—", "check_out": "—", "status": "On Leave", "dayflow_status": "leave", "worked_hours": 0.0, "extra_hours": 0.0},
    ],
    "leaves": [
        {"id": 1, "employee_id": 1, "employee_name": "Suhas Sharma", "department": "Engineering", "leave_type": "Paid", "date_from": "2026-08-25", "date_to": "2026-08-27", "number_of_days": 3.0, "remarks": "Attending Odoo Developer Conference", "dayflow_status": "pending", "admin_comments": ""},
        {"id": 2, "employee_id": 2, "employee_name": "Rahul Kumar", "department": "Product", "leave_type": "Sick", "date_from": "2026-08-26", "date_to": "2026-08-26", "number_of_days": 1.0, "remarks": "Doctor appointment & rest", "dayflow_status": "pending", "admin_comments": ""},
        {"id": 3, "employee_id": 3, "employee_name": "Anu Shetty", "department": "Human Resources", "leave_type": "Paid", "date_from": "2026-08-22", "date_to": "2026-08-22", "number_of_days": 1.0, "remarks": "Family occasion", "dayflow_status": "approved", "admin_comments": "Approved by HR Admin."},
        {"id": 4, "employee_id": 5, "employee_name": "Vikram Adiga", "department": "Engineering", "leave_type": "Unpaid", "date_from": "2026-08-10", "date_to": "2026-08-12", "number_of_days": 3.0, "remarks": "Personal travel", "dayflow_status": "approved", "admin_comments": "Approved."},
    ],
    "payrolls": [
        {"id": 1, "name": "PAY/2026/001", "employee_id": 1, "employee_name": "Suhas Sharma", "department": "Engineering", "salary_structure": "Senior Technical", "pay_period": "August 2026", "base_salary": 65000.0, "allowances": 12000.0, "deductions": 4500.0, "net_salary": 72500.0, "payroll_status": "approved"},
        {"id": 2, "name": "PAY/2026/002", "employee_id": 2, "employee_name": "Rahul Kumar", "department": "Product", "salary_structure": "Product Lead", "pay_period": "August 2026", "base_salary": 58000.0, "allowances": 9000.0, "deductions": 3800.0, "net_salary": 63200.0, "payroll_status": "draft"},
        {"id": 3, "name": "PAY/2026/003", "employee_id": 3, "employee_name": "Anu Shetty", "department": "Human Resources", "salary_structure": "Standard Base", "pay_period": "August 2026", "base_salary": 45000.0, "allowances": 6500.0, "deductions": 2500.0, "net_salary": 49000.0, "payroll_status": "approved"},
        {"id": 4, "name": "PAY/2026/004", "employee_id": 4, "employee_name": "Pooja Hegde", "department": "Design", "salary_structure": "Creative Lead", "pay_period": "August 2026", "base_salary": 52000.0, "allowances": 8000.0, "deductions": 3200.0, "net_salary": 56800.0, "payroll_status": "paid"},
        {"id": 5, "name": "PAY/2026/005", "employee_id": 5, "employee_name": "Vikram Adiga", "department": "Engineering", "salary_structure": "Standard Base", "pay_period": "August 2026", "base_salary": 48000.0, "allowances": 7000.0, "deductions": 3000.0, "net_salary": 52000.0, "payroll_status": "draft"},
        {"id": 6, "name": "PAY/2026/006", "employee_id": 6, "employee_name": "Divya Rao", "department": "Finance", "salary_structure": "Standard Base", "pay_period": "August 2026", "base_salary": 42000.0, "allowances": 5000.0, "deductions": 2200.0, "net_salary": 44800.0, "payroll_status": "paid"},
    ],
    "documents": [
        {"id": 1, "name": "Aadhaar Card", "employee_name": "Suhas Sharma", "document_type": "ID Proof", "file_name": "suhas_aadhaar.pdf", "upload_date": "2026-08-01"},
        {"id": 2, "name": "Employment Contract", "employee_name": "Rahul Kumar", "document_type": "Contract", "file_name": "rahul_contract_signed.pdf", "upload_date": "2026-08-05"},
        {"id": 3, "name": "Degree Certificate", "employee_name": "Anu Shetty", "document_type": "Certificate", "file_name": "anu_degree_nmit.pdf", "upload_date": "2026-08-10"},
    ]
}

def get_kpis():
    total_emp = len(DATA["employees"])
    present_today = len([a for a in DATA["attendance"] if a["dayflow_status"] == "present"])
    on_leave = len([l for l in DATA["leaves"] if l["dayflow_status"] == "approved" and l["date_from"] <= "2026-08-22" <= l["date_to"]])
    pending_leaves = len([l for l in DATA["leaves"] if l["dayflow_status"] == "pending"])
    total_payroll = sum(p["net_salary"] for p in DATA["payrolls"])
    return {
        "total_employees": total_emp,
        "present_today": present_today,
        "on_leave_today": on_leave,
        "pending_leave_requests": pending_leaves,
        "total_payroll": f"{total_payroll:,.2f}"
    }

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dayflow HRMS — Odoo x NMIT Admin Dashboard</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    <style>
        body { background-color: #f1f5f9; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; color: #1e293b; }
        .odoo-topbar { background-color: #714B67; color: #ffffff; padding: 0.5rem 1.5rem; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .odoo-brand { font-size: 1.15rem; font-weight: 700; display: flex; align-items: center; gap: 0.5rem; }
        .odoo-nav { display: flex; gap: 1.25rem; align-items: center; }
        .odoo-nav-link { color: rgba(255,255,255,0.85); font-weight: 500; font-size: 0.88rem; text-decoration: none; padding: 0.25rem 0.6rem; border-radius: 4px; cursor: pointer; }
        .odoo-nav-link:hover, .odoo-nav-link.active { color: #ffffff; background: rgba(255,255,255,0.2); text-decoration: none; }
        .dashboard-container { max-width: 1380px; margin: 1.5rem auto; padding: 0 1rem; }
        .dashboard-header { background: #ffffff; border-radius: 12px; padding: 1.25rem 1.75rem; display: flex; justify-content: space-between; align-items: center; border: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(0,0,0,0.05); margin-bottom: 1.5rem; }
        .brand-badge { width: 48px; height: 48px; border-radius: 10px; background: linear-gradient(135deg, #714B67, #00A09D); display: flex; align-items: center; justify-content: center; color: #ffffff; font-size: 1.5rem; }
        .kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1.25rem; margin-bottom: 1.5rem; }
        .kpi-card { background: #ffffff; border-radius: 12px; padding: 1.25rem 1.5rem; display: flex; align-items: center; cursor: pointer; border: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(0,0,0,0.05); transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1); }
        .kpi-card:hover { transform: translateY(-3px); box-shadow: 0 10px 15px -3px rgba(0,0,0,0.08); }
        .kpi-icon-box { width: 52px; height: 52px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 1.4rem; margin-right: 1.25rem; }
        .kpi-blue { border-left: 4px solid #3b82f6; } .kpi-blue .kpi-icon-box { background: #eff6ff; color: #2563eb; }
        .kpi-green { border-left: 4px solid #10b981; } .kpi-green .kpi-icon-box { background: #ecfdf5; color: #059669; }
        .kpi-amber { border-left: 4px solid #f59e0b; } .kpi-amber .kpi-icon-box { background: #fffbeb; color: #d97706; }
        .kpi-red { border-left: 4px solid #ef4444; } .kpi-red .kpi-icon-box { background: #fef2f2; color: #dc2626; }
        .kpi-label { font-size: 0.8rem; font-weight: 600; text-transform: uppercase; color: #64748b; margin-bottom: 2px; }
        .kpi-value { font-size: 1.85rem; font-weight: 700; color: #0f172a; line-height: 1.1; }
        .kpi-sub { font-size: 0.75rem; font-weight: 600; color: #64748b; margin-top: 4px; }
        .section-card { background: #ffffff; border-radius: 12px; border: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(0,0,0,0.04); margin-bottom: 1.5rem; overflow: hidden; }
        .section-header { padding: 1rem 1.5rem; border-bottom: 1px solid #f1f5f9; display: flex; justify-content: space-between; align-items: center; }
        .section-title { font-size: 1.05rem; font-weight: 700; margin: 0; color: #1e293b; }
        .custom-table th { font-size: 0.775rem; font-weight: 600; text-transform: uppercase; color: #64748b; background: #f8fafc; border-top: none; border-bottom: 1px solid #e2e8f0; padding: 0.75rem 1rem; }
        .custom-table td { padding: 0.85rem 1rem; vertical-align: middle; border-bottom: 1px solid #f1f5f9; }
        .custom-table tr:hover { background-color: #f8fafc; }
        .btn-action { padding: 0.25rem 0.6rem; font-size: 0.75rem; font-weight: 600; border-radius: 6px; }
    </style>
</head>
<body>
    <div class="odoo-topbar">
        <div class="odoo-brand">
            <i class="fa fa-cubes"></i> <span>Odoo 17 — Dayflow HRMS</span>
        </div>
        <div class="odoo-nav">
            <a class="odoo-nav-link active" onclick="switchTab('dashboard')"><i class="fa fa-dashboard"></i> Dashboard</a>
            <a class="odoo-nav-link" onclick="switchTab('employees')"><i class="fa fa-users"></i> Employees</a>
            <a class="odoo-nav-link" onclick="switchTab('attendance')"><i class="fa fa-clock-o"></i> Attendance</a>
            <a class="odoo-nav-link" onclick="switchTab('leaves')"><i class="fa fa-calendar-minus-o"></i> Leave Requests</a>
            <a class="odoo-nav-link" onclick="switchTab('payroll')"><i class="fa fa-money"></i> Payroll</a>
            <a class="odoo-nav-link" onclick="switchTab('documents')"><i class="fa fa-folder-open-o"></i> Documents</a>
        </div>
        <div>
            <span class="badge badge-light p-2"><i class="fa fa-user-circle"></i> Admin / HR User</span>
        </div>
    </div>

    <div class="dashboard-container">
        <div class="dashboard-header">
            <div class="d-flex align-items-center">
                <div class="brand-badge mr-3">
                    <i class="fa fa-cubes"></i>
                </div>
                <div>
                    <h2 class="mb-0 font-weight-bold" style="font-size: 1.45rem; color: #0f172a;">Dayflow HRMS Management Console</h2>
                    <p class="text-muted mb-0 small">Odoo x NMIT Hackathon — Human Resource Management System</p>
                </div>
            </div>
            <div>
                <button class="btn btn-outline-info btn-sm rounded-pill mr-2" onclick="editPayroll(1)">
                    <i class="fa fa-credit-card mr-1"></i> Update Salary
                </button>
                <button class="btn btn-light btn-sm rounded-circle" onclick="location.reload()" title="Refresh live data">
                    <i class="fa fa-refresh"></i>
                </button>
            </div>
        </div>

        <div id="alert-box"></div>

        <!-- Hero KPI Cards -->
        <div class="kpi-grid">
            <div class="kpi-card kpi-blue" onclick="switchTab('employees')">
                <div class="kpi-icon-box"><i class="fa fa-users"></i></div>
                <div>
                    <div class="kpi-label">Total Employees</div>
                    <div class="kpi-value" id="kpi-total-emp">{{ kpis.total_employees }}</div>
                    <div class="kpi-sub text-primary">View Directory <i class="fa fa-arrow-right"></i></div>
                </div>
            </div>

            <div class="kpi-card kpi-green" onclick="switchTab('attendance')">
                <div class="kpi-icon-box"><i class="fa fa-check-circle"></i></div>
                <div>
                    <div class="kpi-label">Present Today</div>
                    <div class="kpi-value" id="kpi-present">{{ kpis.present_today }}</div>
                    <div class="kpi-sub text-success">View Attendance <i class="fa fa-arrow-right"></i></div>
                </div>
            </div>

            <div class="kpi-card kpi-amber" onclick="switchTab('leaves')">
                <div class="kpi-icon-box"><i class="fa fa-calendar-minus-o"></i></div>
                <div>
                    <div class="kpi-label">On Leave Today</div>
                    <div class="kpi-value" id="kpi-on-leave">{{ kpis.on_leave_today }}</div>
                    <div class="kpi-sub text-warning">View Time Off <i class="fa fa-arrow-right"></i></div>
                </div>
            </div>

            <div class="kpi-card kpi-red" onclick="switchTab('leaves')">
                <div class="kpi-icon-box"><i class="fa fa-hourglass-half"></i></div>
                <div>
                    <div class="kpi-label">Pending Requests</div>
                    <div class="kpi-value" id="kpi-pending">{{ kpis.pending_leave_requests }}</div>
                    <div class="kpi-sub text-danger">Review Requests <i class="fa fa-arrow-right"></i></div>
                </div>
            </div>
        </div>

        <!-- Section 1: Pending Leave Requests -->
        <div class="section-card shadow-sm" id="section-leaves">
            <div class="section-header">
                <div class="d-flex align-items-center">
                    <i class="fa fa-hourglass-half text-danger mr-2 fa-lg"></i>
                    <div>
                        <h4 class="section-title">Pending Leave Requests (Decision Hub)</h4>
                        <span class="text-muted small">Approve, reject, or add admin comments to employee leave applications</span>
                    </div>
                </div>
                <span class="badge badge-danger badge-pill" id="badge-pending-count">{{ pending_leaves|length }} Pending</span>
            </div>
            <div class="table-responsive">
                <table class="table custom-table mb-0">
                    <thead>
                        <tr>
                            <th>Employee</th>
                            <th>Department</th>
                            <th>Leave Type</th>
                            <th>Duration</th>
                            <th>Reason / Remarks</th>
                            <th class="text-right">Actions</th>
                        </tr>
                    </thead>
                    <tbody id="pending-leaves-tbody">
                        {% for leave in pending_leaves %}
                        <tr id="leave-row-{{ leave.id }}">
                            <td><strong>{{ leave.employee_name }}</strong></td>
                            <td><span class="text-muted">{{ leave.department }}</span></td>
                            <td><span class="badge badge-info badge-pill">{{ leave.leave_type }}</span></td>
                            <td><span class="small font-weight-bold">{{ leave.date_from }} → {{ leave.date_to }}</span> ({{ leave.number_of_days }} d)</td>
                            <td><span class="text-muted small">{{ leave.remarks }}</span></td>
                            <td class="text-right">
                                <button class="btn btn-success btn-xs btn-action mr-1" onclick="decisionLeave({{ leave.id }}, 'approved')">
                                    <i class="fa fa-check"></i> Approve
                                </button>
                                <button class="btn btn-danger btn-xs btn-action mr-1" onclick="decisionLeave({{ leave.id }}, 'rejected')">
                                    <i class="fa fa-times"></i> Reject
                                </button>
                                <button class="btn btn-outline-secondary btn-xs btn-action" onclick="reviewLeave({{ leave.id }})">
                                    <i class="fa fa-commenting-o"></i> Comment
                                </button>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>

        <!-- 2 Column Section: Today's Attendance & Employee Directory -->
        <div class="row">
            <div class="col-lg-6 mb-4">
                <div class="section-card shadow-sm h-100" id="section-attendance">
                    <div class="section-header">
                        <div class="d-flex align-items-center">
                            <i class="fa fa-calendar-check-o text-success mr-2 fa-lg"></i>
                            <div>
                                <h4 class="section-title">Today's Attendance Overview</h4>
                                <span class="text-muted small">Daily check-in & check-out logs</span>
                            </div>
                        </div>
                    </div>
                    <div class="table-responsive">
                        <table class="table custom-table mb-0">
                            <thead>
                                <tr>
                                    <th>Employee</th>
                                    <th>Check In</th>
                                    <th>Check Out</th>
                                    <th>Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for att in attendances %}
                                <tr>
                                    <td>
                                        <strong>{{ att.employee_name }}</strong>
                                        <div class="small text-muted">{{ att.department }}</div>
                                    </td>
                                    <td><span class="badge badge-light">{{ att.check_in }}</span></td>
                                    <td><span class="badge badge-light">{{ att.check_out }}</span></td>
                                    <td>
                                        {% if att.dayflow_status == 'present' %}
                                        <span class="badge badge-success badge-pill">Present</span>
                                        {% elif att.dayflow_status == 'leave' %}
                                        <span class="badge badge-warning badge-pill">On Leave</span>
                                        {% else %}
                                        <span class="badge badge-secondary badge-pill">{{ att.status }}</span>
                                        {% endif %}
                                    </td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <div class="col-lg-6 mb-4">
                <div class="section-card shadow-sm h-100" id="section-employees">
                    <div class="section-header">
                        <div class="d-flex align-items-center">
                            <i class="fa fa-id-badge text-primary mr-2 fa-lg"></i>
                            <div>
                                <h4 class="section-title">Employee Overview</h4>
                                <span class="text-muted small">Search and select organization members</span>
                            </div>
                        </div>
                    </div>
                    <div class="p-3 border-bottom bg-light">
                        <input type="text" class="form-control form-control-sm" id="empSearch" placeholder="Search employees by name, department, designation..." onkeyup="filterEmployees()">
                    </div>
                    <div class="table-responsive" style="max-height: 340px; overflow-y: auto;">
                        <table class="table custom-table mb-0">
                            <thead>
                                <tr>
                                    <th>Employee</th>
                                    <th>Designation</th>
                                    <th>Role</th>
                                    <th>Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for emp in employees %}
                                <tr class="emp-row">
                                    <td>
                                        <strong>{{ emp.name }}</strong>
                                        <div class="small text-muted">{{ emp.work_email }}</div>
                                    </td>
                                    <td>
                                        <span class="text-dark small font-weight-bold">{{ emp.designation }}</span>
                                        <div class="small text-muted">{{ emp.department }}</div>
                                    </td>
                                    <td>
                                        {% if emp.dayflow_role == 'hr' %}
                                        <span class="badge badge-dark badge-pill">Admin / HR</span>
                                        {% else %}
                                        <span class="badge badge-secondary badge-pill">Employee</span>
                                        {% endif %}
                                    </td>
                                    <td>
                                        {% if emp.status == 'Present' %}
                                        <span class="badge badge-success badge-pill">Present</span>
                                        {% elif emp.status == 'On Leave' %}
                                        <span class="badge badge-warning badge-pill">On Leave</span>
                                        {% else %}
                                        <span class="badge badge-light badge-pill">Not In</span>
                                        {% endif %}
                                    </td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>

        <!-- Section 3: Payroll & Salary Structures -->
        <div class="section-card shadow-sm mb-4" id="section-payroll">
            <div class="section-header">
                <div class="d-flex align-items-center">
                    <i class="fa fa-money text-primary mr-2 fa-lg"></i>
                    <div>
                        <h4 class="section-title">Payroll & Salary Structure Overview</h4>
                        <span class="text-muted small">Update and manage employee base salary, allowances, and deductions</span>
                    </div>
                </div>
                <span class="font-weight-bold text-dark small">Total Net Payroll: ₹<span id="total-payroll-val">{{ kpis.total_payroll }}</span></span>
            </div>
            <div class="table-responsive">
                <table class="table custom-table mb-0">
                    <thead>
                        <tr>
                            <th>Reference</th>
                            <th>Employee</th>
                            <th>Structure</th>
                            <th>Period</th>
                            <th class="text-right">Base Salary</th>
                            <th class="text-right">Allowances</th>
                            <th class="text-right">Deductions</th>
                            <th class="text-right">Net Salary</th>
                            <th class="text-center">Status</th>
                            <th class="text-right">Action</th>
                        </tr>
                    </thead>
                    <tbody id="payroll-tbody">
                        {% for pay in payrolls %}
                        <tr id="payroll-row-{{ pay.id }}">
                            <td><strong class="text-primary">{{ pay.name }}</strong></td>
                            <td>
                                <strong>{{ pay.employee_name }}</strong>
                                <div class="small text-muted">{{ pay.department }}</div>
                            </td>
                            <td><span class="small text-muted">{{ pay.salary_structure }}</span></td>
                            <td><span class="badge badge-light">{{ pay.pay_period }}</span></td>
                            <td class="text-right">₹{{ "{:,.2f}".format(pay.base_salary) }}</td>
                            <td class="text-right text-success">+ ₹{{ "{:,.2f}".format(pay.allowances) }}</td>
                            <td class="text-right text-danger">- ₹{{ "{:,.2f}".format(pay.deductions) }}</td>
                            <td class="text-right font-weight-bold text-dark">₹{{ "{:,.2f}".format(pay.net_salary) }}</td>
                            <td class="text-center">
                                {% if pay.payroll_status == 'draft' %}
                                <span class="badge badge-info badge-pill">Draft</span>
                                {% elif pay.payroll_status == 'approved' %}
                                <span class="badge badge-warning badge-pill">Approved</span>
                                {% elif pay.payroll_status == 'paid' %}
                                <span class="badge badge-success badge-pill">Paid</span>
                                {% endif %}
                            </td>
                            <td class="text-right">
                                <button class="btn btn-outline-primary btn-xs btn-action" onclick="editPayroll({{ pay.id }})">
                                    <i class="fa fa-pencil"></i> Edit Salary
                                </button>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- Edit Salary Modal -->
    <div class="modal fade" id="salaryModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title font-weight-bold"><i class="fa fa-credit-card text-primary mr-2"></i>Edit Employee Salary Structure</h5>
                    <button type="button" class="close" data-dismiss="modal">&times;</button>
                </div>
                <div class="modal-body">
                    <input type="hidden" id="edit-pay-id">
                    <div class="form-group">
                        <label class="font-weight-bold">Employee</label>
                        <input type="text" class="form-control" id="edit-pay-emp" readonly>
                    </div>
                    <div class="form-group">
                        <label class="font-weight-bold">Base Salary (₹)</label>
                        <input type="number" class="form-control" id="edit-pay-base" oninput="calcNetSalary()">
                    </div>
                    <div class="form-group">
                        <label class="font-weight-bold">Allowances (₹)</label>
                        <input type="number" class="form-control" id="edit-pay-allow" oninput="calcNetSalary()">
                    </div>
                    <div class="form-group">
                        <label class="font-weight-bold">Deductions (₹)</label>
                        <input type="number" class="form-control" id="edit-pay-deduct" oninput="calcNetSalary()">
                    </div>
                    <div class="alert alert-info">
                        <strong>Calculated Net Salary:</strong> ₹<span id="edit-pay-net" class="font-weight-bold">0.00</span>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary btn-sm" data-dismiss="modal">Cancel</button>
                    <button type="button" class="btn btn-primary btn-sm" onclick="savePayroll()">Save Changes</button>
                </div>
            </div>
        </div>
    </div>

    <!-- Review Leave Modal -->
    <div class="modal fade" id="leaveModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title font-weight-bold"><i class="fa fa-commenting-o text-danger mr-2"></i>Review Leave Request</h5>
                    <button type="button" class="close" data-dismiss="modal">&times;</button>
                </div>
                <div class="modal-body">
                    <input type="hidden" id="review-leave-id">
                    <div class="form-group">
                        <label class="font-weight-bold">Employee</label>
                        <input type="text" class="form-control" id="review-leave-emp" readonly>
                    </div>
                    <div class="form-group">
                        <label class="font-weight-bold">Reason / Remarks</label>
                        <textarea class="form-control" id="review-leave-remarks" readonly rows="2"></textarea>
                    </div>
                    <div class="form-group">
                        <label class="font-weight-bold">HR / Admin Decision Comments</label>
                        <textarea class="form-control" id="review-leave-comments" rows="3" placeholder="Add decision comments or conditions..."></textarea>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-danger btn-sm" onclick="submitLeaveDecision('rejected')">Reject with Comments</button>
                    <button type="button" class="btn btn-success btn-sm" onclick="submitLeaveDecision('approved')">Approve with Comments</button>
                </div>
            </div>
        </div>
    </div>

    <script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        function showAlert(message, type='success') {
            const html = `<div class="alert alert-${type} alert-dismissible fade show" role="alert">
                <strong>Dayflow:</strong> ${message}
                <button type="button" class="close" data-dismiss="alert">&times;</button>
            </div>`;
            document.getElementById('alert-box').innerHTML = html;
        }

        function filterEmployees() {
            const query = document.getElementById('empSearch').value.toLowerCase();
            const rows = document.querySelectorAll('.emp-row');
            rows.forEach(r => {
                const text = r.innerText.toLowerCase();
                r.style.display = text.includes(query) ? '' : 'none';
            });
        }

        function switchTab(tab) {
            if (tab === 'employees') {
                document.getElementById('section-employees').scrollIntoView({behavior: 'smooth'});
            } else if (tab === 'leaves') {
                document.getElementById('section-leaves').scrollIntoView({behavior: 'smooth'});
            } else if (tab === 'attendance') {
                document.getElementById('section-attendance').scrollIntoView({behavior: 'smooth'});
            } else if (tab === 'payroll') {
                document.getElementById('section-payroll').scrollIntoView({behavior: 'smooth'});
            } else {
                window.scrollTo({top: 0, behavior: 'smooth'});
            }
        }

        function decisionLeave(id, decision) {
            fetch('/api/leave/decision', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({id: id, decision: decision})
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    showAlert(data.message, decision === 'approved' ? 'success' : 'warning');
                    const row = document.getElementById('leave-row-' + id);
                    if (row) row.remove();
                    updateKpis();
                }
            });
        }

        function reviewLeave(id) {
            fetch('/api/leave/' + id)
            .then(res => res.json())
            .then(data => {
                document.getElementById('review-leave-id').value = data.id;
                document.getElementById('review-leave-emp').value = data.employee_name;
                document.getElementById('review-leave-remarks').value = data.remarks;
                document.getElementById('review-leave-comments').value = data.admin_comments || '';
                $('#leaveModal').modal('show');
            });
        }

        function submitLeaveDecision(decision) {
            const id = document.getElementById('review-leave-id').value;
            const comments = document.getElementById('review-leave-comments').value;
            fetch('/api/leave/decision', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({id: parseInt(id), decision: decision, comments: comments})
            })
            .then(res => res.json())
            .then(data => {
                $('#leaveModal').modal('hide');
                showAlert(data.message, decision === 'approved' ? 'success' : 'warning');
                const row = document.getElementById('leave-row-' + id);
                if (row) row.remove();
                updateKpis();
            });
        }

        function editPayroll(id) {
            fetch('/api/payroll/' + id)
            .then(res => res.json())
            .then(data => {
                document.getElementById('edit-pay-id').value = data.id;
                document.getElementById('edit-pay-emp').value = data.employee_name + ' (' + data.department + ')';
                document.getElementById('edit-pay-base').value = data.base_salary;
                document.getElementById('edit-pay-allow').value = data.allowances;
                document.getElementById('edit-pay-deduct').value = data.deductions;
                calcNetSalary();
                $('#salaryModal').modal('show');
            });
        }

        function calcNetSalary() {
            const base = parseFloat(document.getElementById('edit-pay-base').value) || 0;
            const allow = parseFloat(document.getElementById('edit-pay-allow').value) || 0;
            const deduct = parseFloat(document.getElementById('edit-pay-deduct').value) || 0;
            const net = base + allow - deduct;
            document.getElementById('edit-pay-net').innerText = net.toLocaleString('en-IN', {minimumFractionDigits: 2});
        }

        function savePayroll() {
            const id = document.getElementById('edit-pay-id').value;
            const base = parseFloat(document.getElementById('edit-pay-base').value) || 0;
            const allow = parseFloat(document.getElementById('edit-pay-allow').value) || 0;
            const deduct = parseFloat(document.getElementById('edit-pay-deduct').value) || 0;
            fetch('/api/payroll/update', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({id: parseInt(id), base_salary: base, allowances: allow, deductions: deduct})
            })
            .then(res => res.json())
            .then(data => {
                $('#salaryModal').modal('hide');
                showAlert(data.message, 'success');
                location.reload();
            });
        }

        function updateKpis() {
            fetch('/api/kpi')
            .then(res => res.json())
            .then(k => {
                document.getElementById('kpi-total-emp').innerText = k.total_employees;
                document.getElementById('kpi-present').innerText = k.present_today;
                document.getElementById('kpi-on-leave').innerText = k.on_leave_today;
                document.getElementById('kpi-pending').innerText = k.pending_leave_requests;
                document.getElementById('badge-pending-count').innerText = k.pending_leave_requests + ' Pending';
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def dashboard():
    kpis = get_kpis()
    pending_leaves = [l for l in DATA["leaves"] if l["dayflow_status"] == "pending"]
    return render_template_string(
        HTML_TEMPLATE,
        kpis=kpis,
        pending_leaves=pending_leaves,
        attendances=DATA["attendance"],
        employees=DATA["employees"],
        payrolls=DATA["payrolls"],
        documents=DATA["documents"]
    )

@app.route('/api/kpi')
def api_kpi():
    return jsonify(get_kpis())

@app.route('/api/leave/<int:leave_id>')
def api_get_leave(leave_id):
    leave = next((l for l in DATA["leaves"] if l["id"] == leave_id), None)
    if leave:
        return jsonify(leave)
    return jsonify({"error": "Not found"}), 404

@app.route('/api/leave/decision', methods=['POST'])
def api_leave_decision():
    req = request.get_json()
    leave_id = req.get('id')
    decision = req.get('decision')
    comments = req.get('comments', '')
    leave = next((l for l in DATA["leaves"] if l["id"] == leave_id), None)
    if leave:
        leave['dayflow_status'] = decision
        if comments:
            leave['admin_comments'] = comments
        return jsonify({"success": True, "message": f"Leave request for {leave['employee_name']} has been {decision}."})
    return jsonify({"success": False, "message": "Leave request not found."}), 404

@app.route('/api/payroll/<int:payroll_id>')
def api_get_payroll(payroll_id):
    pay = next((p for p in DATA["payrolls"] if p["id"] == payroll_id), None)
    if pay:
        return jsonify(pay)
    return jsonify({"error": "Not found"}), 404

@app.route('/api/payroll/update', methods=['POST'])
def api_payroll_update():
    req = request.get_json()
    pay_id = req.get('id')
    base = float(req.get('base_salary', 0.0))
    allow = float(req.get('allowances', 0.0))
    deduct = float(req.get('deductions', 0.0))
    pay = next((p for p in DATA["payrolls"] if p["id"] == pay_id), None)
    if pay:
        pay['base_salary'] = base
        pay['allowances'] = allow
        pay['deductions'] = deduct
        pay['net_salary'] = base + allow - deduct
        return jsonify({"success": True, "message": f"Salary structure for {pay['employee_name']} updated to Net: ₹{pay['net_salary']:,.2f}."})
    return jsonify({"success": False, "message": "Payroll record not found."}), 404

if __name__ == '__main__':
    print("=" * 60)
    print("  DAYFLOW HRMS — LIVE DEMO PREVIEW SERVER")
    print("  Running on: http://localhost:8069")
    print("=" * 60)
    app.run(host='0.0.0.0', port=8069, debug=False)
