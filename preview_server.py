# -*- coding: utf-8 -*-
"""
Dayflow HRMS - Fully Functional Live UI Preview Server
Renders an interactive, dynamic Dayflow HRMS interface covering:
- Attendance Tracking & Live Ticker
- Time Off / Leave Requests & HR Approvals
- Employee Profile Directory & Account Provisioning (Person 2)
- Employee Verification Documents Upload & Library (Person 2)
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import webbrowser

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dayflow HRMS — Live UI Preview</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-primary: #12131a;
            --bg-secondary: #1a1c26;
            --bg-card: #222533;
            --bg-input: #2d3142;
            --accent-purple: #714B67;
            --accent-purple-hover: #86597a;
            --accent-blue: #3b82f6;
            --accent-green: #10b981;
            --accent-yellow: #f59e0b;
            --accent-red: #ef4444;
            --text-primary: #f3f4f6;
            --text-secondary: #9ca3af;
            --border-color: #374151;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        body {
            background-color: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }

        .navbar {
            background-color: var(--bg-secondary);
            border-bottom: 1px solid var(--border-color);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0.75rem 1.5rem;
            position: sticky;
            top: 0;
            z-index: 50;
        }

        .navbar-brand {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            font-size: 1.25rem;
            font-weight: 700;
            color: #fff;
            text-decoration: none;
        }

        .navbar-logo {
            background: linear-gradient(135deg, var(--accent-purple), #9333ea);
            color: white;
            padding: 0.35rem 0.65rem;
            border-radius: 6px;
            font-weight: 800;
            font-size: 0.95rem;
            letter-spacing: 0.5px;
        }

        .navbar-nav {
            display: flex;
            list-style: none;
            gap: 0.5rem;
        }

        .nav-item {
            padding: 0.5rem 1rem;
            border-radius: 6px;
            color: var(--text-secondary);
            cursor: pointer;
            font-weight: 500;
            font-size: 0.9rem;
            transition: all 0.2s;
        }

        .nav-item:hover {
            color: var(--text-primary);
            background-color: rgba(255, 255, 255, 0.05);
        }

        .nav-item.active {
            color: #fff;
            background-color: var(--accent-purple);
        }

        .nav-right {
            display: flex;
            align-items: center;
            gap: 1rem;
        }

        .role-badge {
            background-color: var(--bg-input);
            border: 1px solid var(--border-color);
            padding: 0.35rem 0.75rem;
            border-radius: 20px;
            font-size: 0.8rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .role-badge select {
            background: transparent;
            border: none;
            color: var(--text-primary);
            font-size: 0.8rem;
            font-weight: 600;
            outline: none;
            cursor: pointer;
        }

        .container {
            max-width: 1280px;
            margin: 0 auto;
            padding: 1.5rem;
            width: 100%;
            flex: 1;
        }

        .page-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
        }

        .page-title {
            font-size: 1.5rem;
            font-weight: 700;
        }

        .page-subtitle {
            font-size: 0.875rem;
            color: var(--text-secondary);
            margin-top: 0.25rem;
        }

        .btn {
            padding: 0.5rem 1.25rem;
            border-radius: 6px;
            border: none;
            font-weight: 600;
            font-size: 0.875rem;
            cursor: pointer;
            transition: all 0.2s;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
        }

        .btn:disabled {
            opacity: 0.4;
            cursor: not-allowed;
        }

        .btn-primary {
            background-color: var(--accent-purple);
            color: white;
        }

        .btn-primary:hover:not(:disabled) {
            background-color: var(--accent-purple-hover);
        }

        .btn-success {
            background-color: var(--accent-green);
            color: white;
        }

        .btn-success:hover:not(:disabled) {
            filter: brightness(1.1);
        }

        .btn-danger {
            background-color: var(--accent-red);
            color: white;
        }

        .btn-danger:hover:not(:disabled) {
            filter: brightness(1.1);
        }

        .btn-secondary {
            background-color: var(--bg-input);
            color: var(--text-primary);
            border: 1px solid var(--border-color);
        }

        .btn-secondary:hover:not(:disabled) {
            background-color: var(--border-color);
        }

        .card {
            background-color: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
        }

        .action-banner {
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: linear-gradient(135deg, rgba(113, 75, 103, 0.15), rgba(34, 37, 51, 0.9));
            border: 1px solid rgba(113, 75, 103, 0.4);
            border-radius: 10px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
        }

        .banner-metrics {
            display: flex;
            gap: 2.5rem;
            align-items: center;
        }

        .metric-group {
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
        }

        .metric-label {
            font-size: 0.75rem;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-weight: 600;
        }

        .metric-value {
            font-size: 1.35rem;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .status-dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
        }

        .status-dot.green { background-color: var(--accent-green); box-shadow: 0 0 10px var(--accent-green); }
        .status-dot.red { background-color: var(--accent-red); }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 1rem;
            margin-bottom: 1.5rem;
        }

        .stat-card {
            background-color: var(--bg-card);
            border: 1px solid var(--border-color);
            padding: 1.25rem;
            border-radius: 8px;
        }

        .stat-card .val {
            font-size: 1.6rem;
            font-weight: 700;
            margin-top: 0.35rem;
        }

        .employee-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 1.25rem;
            margin-top: 1rem;
        }

        .employee-card {
            background-color: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 1.25rem;
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
            position: relative;
        }

        .emp-header {
            display: flex;
            align-items: center;
            gap: 1rem;
        }

        .emp-avatar {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background: linear-gradient(135deg, var(--accent-purple), var(--accent-blue));
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 1.1rem;
            color: white;
        }

        .emp-info h4 { font-size: 1.05rem; font-weight: 700; }
        .emp-info p { font-size: 0.8rem; color: var(--text-secondary); }

        .emp-meta {
            font-size: 0.8rem;
            color: var(--text-secondary);
            display: flex;
            flex-direction: column;
            gap: 0.3rem;
            border-top: 1px solid var(--border-color);
            padding-top: 0.75rem;
        }

        .table-responsive {
            width: 100%;
            overflow-x: auto;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            font-size: 0.9rem;
        }

        th {
            background-color: var(--bg-card);
            color: var(--text-secondary);
            padding: 0.75rem 1rem;
            font-weight: 600;
            border-bottom: 1px solid var(--border-color);
            text-transform: uppercase;
            font-size: 0.75rem;
            letter-spacing: 0.5px;
        }

        td {
            padding: 0.85rem 1rem;
            border-bottom: 1px solid rgba(55, 65, 81, 0.5);
        }

        tr:hover td {
            background-color: rgba(255, 255, 255, 0.02);
        }

        .badge {
            display: inline-flex;
            align-items: center;
            padding: 0.25rem 0.6rem;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 600;
        }

        .badge-present { background-color: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); }
        .badge-halfday { background-color: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3); }
        .badge-absent { background-color: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); }
        .badge-leave { background-color: rgba(59, 130, 246, 0.15); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.3); }
        .badge-pending { background-color: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3); }
        .badge-role { background-color: rgba(113, 75, 103, 0.3); color: #e9d5ff; border: 1px solid rgba(113, 75, 103, 0.5); }

        .form-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
            gap: 1.25rem;
            margin-bottom: 1.25rem;
        }

        .form-group {
            display: flex;
            flex-direction: column;
            gap: 0.4rem;
        }

        .form-group label {
            font-size: 0.85rem;
            font-weight: 600;
            color: var(--text-secondary);
        }

        .form-control {
            background-color: var(--bg-input);
            border: 1px solid var(--border-color);
            color: var(--text-primary);
            padding: 0.65rem 0.85rem;
            border-radius: 6px;
            font-size: 0.9rem;
            outline: none;
        }

        .form-control:focus {
            border-color: var(--accent-purple);
        }

        .tab-content { display: none; }
        .tab-content.active { display: block; }
    </style>
</head>
<body>

    <!-- Navbar -->
    <nav class="navbar">
        <a href="#" class="navbar-brand">
            <span class="navbar-logo">DF</span> Dayflow HRMS
        </a>
        <ul class="navbar-nav">
            <li class="nav-item" id="nav-employees" onclick="switchTab('employees')">Employees</li>
            <li class="nav-item active" id="nav-attendance" onclick="switchTab('attendance')">Attendance</li>
            <li class="nav-item" id="nav-leave" onclick="switchTab('leave')">Time Off</li>
            <li class="nav-item" id="nav-payroll" onclick="switchTab('payroll')">Payroll</li>
            <li class="nav-item" id="nav-documents" onclick="switchTab('documents')">Documents</li>
        </ul>
        <div class="nav-right">
            <div class="role-badge">
                Role: 
                <select id="user-role-select" onchange="onRoleChange(this.value)">
                    <option value="employee">Employee (John Doe)</option>
                    <option value="admin">HR / Admin Manager</option>
                </select>
            </div>
        </div>
    </nav>

    <div class="container">

        <!-- ATTENDANCE TAB -->
        <div id="tab-attendance" class="tab-content active">
            <div class="page-header">
                <div>
                    <h1 class="page-title">Attendance Tracking</h1>
                    <p class="page-subtitle">Real-time check-in/out, worked hours calculation, and status logging</p>
                </div>
                <div style="display: flex; gap: 0.5rem;">
                    <button class="btn btn-secondary" onclick="resetAttendanceData()">Reset Data</button>
                </div>
            </div>

            <!-- Attendance Banner -->
            <div class="action-banner">
                <div class="banner-metrics">
                    <div class="metric-group">
                        <span class="metric-label">Today's Status</span>
                        <div class="metric-value">
                            <span id="banner-status-dot" class="status-dot red"></span>
                            <span id="banner-status-text">Not Checked In</span>
                        </div>
                    </div>
                    <div class="metric-group">
                        <span class="metric-label">Check In Time</span>
                        <span class="metric-value" id="banner-checkin-time">--:--</span>
                    </div>
                    <div class="metric-group">
                        <span class="metric-label">Working Hours</span>
                        <span class="metric-value" id="banner-worked-hours" style="color: var(--accent-purple-hover);">0h 00m</span>
                    </div>
                </div>
                <div class="banner-actions">
                    <button id="btn-check-in" class="btn btn-success" onclick="handleCheckIn()">Check In</button>
                    <button id="btn-check-out" class="btn btn-danger" onclick="handleCheckOut()" disabled>Check Out</button>
                </div>
            </div>

            <div class="card">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 1rem;">
                    <h3 style="font-size: 1.1rem;">Attendance Logs & Worked Hours</h3>
                    <span id="record-rule-tag" style="font-size: 0.8rem; color: var(--text-secondary);">Showing personal attendance logs (Record Rule Protected)</span>
                </div>
                <div class="table-responsive">
                    <table>
                        <thead>
                            <tr>
                                <th>Date</th>
                                <th>Employee</th>
                                <th>Check In</th>
                                <th>Check Out</th>
                                <th>Status</th>
                                <th>Worked Hours</th>
                                <th>Effective Hours</th>
                                <th>Extra Hours</th>
                            </tr>
                        </thead>
                        <tbody id="attendance-table-body"></tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- TIME OFF / LEAVE TAB -->
        <div id="tab-leave" class="tab-content">
            <div class="page-header">
                <div>
                    <h1 class="page-title">Time Off & Leave Management</h1>
                    <p class="page-subtitle">Apply for leave, review allocations, and manage approvals</p>
                </div>
            </div>

            <div class="stats-grid">
                <div class="stat-card">
                    <div class="metric-label">Paid Time Off</div>
                    <div class="val" style="color: #34d399;">12 Days</div>
                </div>
                <div class="stat-card">
                    <div class="metric-label">Sick Leave</div>
                    <div class="val" style="color: #fbbf24;">8 Days</div>
                </div>
                <div class="stat-card">
                    <div class="metric-label">Unpaid Leave</div>
                    <div class="val" style="color: #60a5fa;">Unlimited</div>
                </div>
            </div>

            <!-- Apply Leave Form -->
            <div class="card" id="apply-leave-card">
                <h3 style="font-size: 1.1rem; margin-bottom: 1.25rem;">Apply for Time Off</h3>
                <form onsubmit="handleLeaveSubmit(event)">
                    <div class="form-grid">
                        <div class="form-group">
                            <label>Leave Type</label>
                            <select id="leave-type" class="form-control" required>
                                <option value="paid">Paid Time Off</option>
                                <option value="sick">Sick Leave</option>
                                <option value="unpaid">Unpaid Leaves</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Start Date</label>
                            <input type="date" id="leave-start-date" class="form-control" required>
                        </div>
                        <div class="form-group">
                            <label>End Date</label>
                            <input type="date" id="leave-end-date" class="form-control" required>
                        </div>
                    </div>
                    <div class="form-group" style="margin-bottom: 1.25rem;">
                        <label>Reason / Remarks</label>
                        <textarea id="leave-remarks" class="form-control" rows="2" placeholder="State reason for leave application..." required></textarea>
                    </div>
                    <button type="submit" class="btn btn-primary">Submit Leave Application</button>
                </form>
            </div>

            <!-- Leave Applications Table -->
            <div class="card">
                <h3 style="font-size: 1.1rem; margin-bottom: 1rem;">Leave Applications & Approval Workflow</h3>
                <div class="table-responsive">
                    <table>
                        <thead>
                            <tr>
                                <th>Employee</th>
                                <th>Leave Type</th>
                                <th>Start Date</th>
                                <th>End Date</th>
                                <th>Days</th>
                                <th>Reason</th>
                                <th>Status</th>
                                <th>HR Comments / Actions</th>
                            </tr>
                        </thead>
                        <tbody id="leave-table-body"></tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- EMPLOYEES TAB (Person 2) -->
        <div id="tab-employees" class="tab-content">
            <div class="page-header">
                <div>
                    <h1 class="page-title">Employee Profiles & Directory</h1>
                    <p class="page-subtitle">Manage organization member profiles, roles, joining dates, and account provisioning</p>
                </div>
                <button class="btn btn-primary" onclick="toggleAddEmpForm()">+ Add Employee</button>
            </div>

            <!-- Add Employee Form -->
            <div class="card" id="add-emp-card" style="display: none;">
                <h3 style="font-size: 1.1rem; margin-bottom: 1.25rem;">Create New Employee Profile</h3>
                <form onsubmit="handleAddEmployee(event)">
                    <div class="form-grid">
                        <div class="form-group">
                            <label>Full Name</label>
                            <input type="text" id="emp-name" class="form-control" placeholder="e.g. Alice Johnson" required>
                        </div>
                        <div class="form-group">
                            <label>Work Email</label>
                            <input type="email" id="emp-email" class="form-control" placeholder="alice@company.com" required>
                        </div>
                        <div class="form-group">
                            <label>Job Title</label>
                            <input type="text" id="emp-job" class="form-control" placeholder="e.g. Software Engineer" required>
                        </div>
                        <div class="form-group">
                            <label>Department</label>
                            <input type="text" id="emp-dept" class="form-control" placeholder="e.g. Engineering" required>
                        </div>
                        <div class="form-group">
                            <label>Dayflow Role</label>
                            <select id="emp-role" class="form-control" required>
                                <option value="Employee">Employee</option>
                                <option value="Admin / HR">Admin / HR</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Joining Date</label>
                            <input type="date" id="emp-joining" class="form-control" required>
                        </div>
                    </div>
                    <button type="submit" class="btn btn-success">Save Employee Profile</button>
                </form>
            </div>

            <div class="employee-grid" id="employee-grid"></div>
        </div>

        <!-- DOCUMENTS TAB (Person 2) -->
        <div id="tab-documents" class="tab-content">
            <div class="page-header">
                <div>
                    <h1 class="page-title">Employee Verification Documents</h1>
                    <p class="page-subtitle">Upload, classify, and verify contracts, ID proofs, and certificates</p>
                </div>
            </div>

            <div class="card">
                <h3 style="font-size: 1.1rem; margin-bottom: 1.25rem;">Upload Employee Document</h3>
                <form onsubmit="handleDocUpload(event)">
                    <div class="form-grid">
                        <div class="form-group">
                            <label>Document Title</label>
                            <input type="text" id="doc-title" class="form-control" placeholder="e.g. Passport ID Copy" required>
                        </div>
                        <div class="form-group">
                            <label>Employee</label>
                            <select id="doc-employee" class="form-control" required>
                                <option value="John Doe">John Doe</option>
                                <option value="Jane Smith">Jane Smith</option>
                                <option value="Robert Taylor">Robert Taylor</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Document Category</label>
                            <select id="doc-type" class="form-control" required>
                                <option value="id_proof">ID Proof</option>
                                <option value="contract">Contract</option>
                                <option value="certificate">Certificate</option>
                                <option value="other">Other</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Attachment File Name</label>
                            <input type="text" id="doc-filename" class="form-control" placeholder="e.g. passport_scan.pdf" required>
                        </div>
                    </div>
                    <button type="submit" class="btn btn-primary">Upload Verification Document</button>
                </form>
            </div>

            <div class="card">
                <h3 style="font-size: 1.1rem; margin-bottom: 1rem;">Document Attachment Library</h3>
                <div class="table-responsive">
                    <table>
                        <thead>
                            <tr>
                                <th>Document Title</th>
                                <th>Employee</th>
                                <th>Classification</th>
                                <th>File Name</th>
                                <th>Upload Date</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody id="document-table-body"></tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- PAYROLL PLACEHOLDER (Person 4) -->
        <div id="tab-payroll" class="tab-content">
            <div class="card">
                <h2>Payroll & Salary Management</h2>
                <p style="color:var(--text-secondary); margin-top:0.5rem;">Managed by Person 4 (Base salary, allowances, deductions, net salary).</p>
            </div>
        </div>

    </div>

    <script>
        const DEFAULT_ATTENDANCE = [
            { id: 1, date: '2026-08-21', employee: 'John Doe', checkIn: '09:00 AM', checkOut: '05:30 PM', status: 'present', workedHours: 8.5, effectiveHours: 8.5, extraHours: 0.5 },
            { id: 2, date: '2026-08-20', employee: 'John Doe', checkIn: '08:50 AM', checkOut: '06:10 PM', status: 'present', workedHours: 9.3, effectiveHours: 9.3, extraHours: 1.3 },
            { id: 3, date: '2026-08-19', employee: 'John Doe', checkIn: '09:15 AM', checkOut: '01:00 PM', status: 'half_day', workedHours: 3.75, effectiveHours: 3.75, extraHours: 0.0 },
            { id: 4, date: '2026-08-21', employee: 'Jane Smith', checkIn: '08:55 AM', checkOut: '05:00 PM', status: 'present', workedHours: 8.08, effectiveHours: 8.08, extraHours: 0.08 }
        ];

        const DEFAULT_LEAVE = [
            { id: 101, employee: 'John Doe', type: 'sick', startDate: '2026-08-25', endDate: '2026-08-26', days: 2, remarks: 'Fever and rest recommended', status: 'pending', adminComments: '' },
            { id: 102, employee: 'Jane Smith', type: 'paid', startDate: '2026-08-28', endDate: '2026-08-30', days: 3, remarks: 'Family vacation', status: 'approved', adminComments: 'Approved by HR' }
        ];

        const DEFAULT_EMPLOYEES = [
            { id: 1, name: 'John Doe', email: 'john.doe@company.com', job: 'Senior Software Engineer', dept: 'Engineering', role: 'Employee', joining: '2024-03-15', loginId: 'DAYFLOW-JOHN-2024-00001', provisioned: true },
            { id: 2, name: 'Jane Smith', email: 'jane.smith@company.com', job: 'HR Specialist', dept: 'Human Resources', role: 'Admin / HR', joining: '2023-01-10', loginId: 'DAYFLOW-JANE-2023-00002', provisioned: true },
            { id: 3, name: 'Robert Taylor', email: 'robert.t@company.com', job: 'Product Manager', dept: 'Product', role: 'Employee', joining: '2025-06-01', loginId: '', provisioned: false }
        ];

        const DEFAULT_DOCUMENTS = [
            { id: 1, title: 'Passport Verification ID', employee: 'John Doe', type: 'id_proof', filename: 'john_passport.pdf', date: '2026-08-10' },
            { id: 2, title: 'Employment Contract 2026', employee: 'Jane Smith', type: 'contract', filename: 'jane_contract_2026.pdf', date: '2026-08-01' }
        ];

        let state = {
            role: 'employee',
            currentEmployee: 'John Doe',
            isCheckedIn: false,
            activeCheckInTime: null,
            checkInTimestamp: null,
            tickerInterval: null,
            attendances: JSON.parse(localStorage.getItem('df_attendances')) || DEFAULT_ATTENDANCE,
            leaves: JSON.parse(localStorage.getItem('df_leaves')) || DEFAULT_LEAVE,
            employees: JSON.parse(localStorage.getItem('df_employees')) || DEFAULT_EMPLOYEES,
            documents: JSON.parse(localStorage.getItem('df_documents')) || DEFAULT_DOCUMENTS
        };

        function saveState() {
            localStorage.setItem('df_attendances', JSON.stringify(state.attendances));
            localStorage.setItem('df_leaves', JSON.stringify(state.leaves));
            localStorage.setItem('df_employees', JSON.stringify(state.employees));
            localStorage.setItem('df_documents', JSON.stringify(state.documents));
        }

        function resetAttendanceData() {
            localStorage.clear();
            state.attendances = JSON.parse(JSON.stringify(DEFAULT_ATTENDANCE));
            state.leaves = JSON.parse(JSON.stringify(DEFAULT_LEAVE));
            state.employees = JSON.parse(JSON.stringify(DEFAULT_EMPLOYEES));
            state.documents = JSON.parse(JSON.stringify(DEFAULT_DOCUMENTS));
            state.isCheckedIn = false;
            if (state.tickerInterval) clearInterval(state.tickerInterval);
            renderAll();
        }

        function formatTime(date) {
            return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true });
        }

        function formatDate(date) {
            return date.toISOString().split('T')[0];
        }

        function switchTab(tabId) {
            document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));

            const targetNav = document.getElementById('nav-' + tabId);
            if (targetNav) targetNav.classList.add('active');
            const targetTab = document.getElementById('tab-' + tabId);
            if (targetTab) targetTab.classList.add('active');
        }

        function onRoleChange(role) {
            state.role = role;
            renderAll();
        }

        function handleCheckIn() {
            if (state.isCheckedIn) return;
            const now = new Date();
            state.isCheckedIn = true;
            state.activeCheckInTime = formatTime(now);
            state.checkInTimestamp = now.getTime();

            state.tickerInterval = setInterval(updateLiveTicker, 1000);

            const newRecord = {
                id: Date.now(),
                date: formatDate(now),
                employee: state.currentEmployee,
                checkIn: state.activeCheckInTime,
                checkOut: '--',
                status: 'present',
                workedHours: 0.0,
                effectiveHours: 0.0,
                extraHours: 0.0,
                isActive: true
            };

            state.attendances.unshift(newRecord);
            saveState();
            renderAttendance();
        }

        function updateLiveTicker() {
            if (!state.isCheckedIn || !state.checkInTimestamp) return;

            const diffMs = Date.now() - state.checkInTimestamp;
            const diffSec = Math.floor(diffMs / 1000);
            const hrs = Math.floor(diffSec / 3600);
            const mins = Math.floor((diffSec % 3600) / 60);
            const secs = diffSec % 60;

            document.getElementById('banner-worked-hours').innerText = `${hrs}h ${mins.toString().padStart(2, '0')}m ${secs.toString().padStart(2, '0')}s`;

            const activeRec = state.attendances.find(a => a.isActive);
            if (activeRec) {
                const workedHrs = parseFloat((diffSec / 3600).toFixed(2));
                activeRec.workedHours = workedHrs;
                activeRec.effectiveHours = workedHrs;
                activeRec.extraHours = workedHrs > 8.0 ? parseFloat((workedHrs - 8.0).toFixed(2)) : 0.0;
                renderAttendanceTable();
            }
        }

        function handleCheckOut() {
            if (!state.isCheckedIn) return;

            const now = new Date();
            const checkOutStr = formatTime(now);

            if (state.tickerInterval) clearInterval(state.tickerInterval);

            const activeRec = state.attendances.find(a => a.isActive);
            if (activeRec) {
                activeRec.checkOut = checkOutStr;
                activeRec.isActive = false;
                const diffMs = state.checkInTimestamp ? (now.getTime() - state.checkInTimestamp) : 0;
                const diffSec = Math.floor(diffMs / 1000);
                const workedHrs = parseFloat((diffSec / 3600).toFixed(2));

                activeRec.workedHours = workedHrs > 0 ? workedHrs : 0.1;
                activeRec.effectiveHours = activeRec.workedHours;
                activeRec.extraHours = activeRec.workedHours > 8.0 ? parseFloat((activeRec.workedHours - 8.0).toFixed(2)) : 0.0;
                activeRec.status = 'present';
            }

            state.isCheckedIn = false;
            state.activeCheckInTime = null;
            state.checkInTimestamp = null;

            saveState();
            renderAttendance();
        }

        function handleLeaveSubmit(e) {
            e.preventDefault();
            const type = document.getElementById('leave-type').value;
            const startDate = document.getElementById('leave-start-date').value;
            const endDate = document.getElementById('leave-end-date').value;
            const remarks = document.getElementById('leave-remarks').value;

            const start = new Date(startDate);
            const end = new Date(endDate);
            if (end < start) {
                alert('End Date cannot be earlier than Start Date.');
                return;
            }

            const days = Math.ceil((end - start) / (1000 * 60 * 60 * 24)) + 1;

            state.leaves.unshift({
                id: Date.now(),
                employee: state.currentEmployee,
                type: type,
                startDate: startDate,
                endDate: endDate,
                days: days,
                remarks: remarks,
                status: 'pending',
                adminComments: ''
            });

            saveState();
            renderLeaves();
            e.target.reset();
            alert('Leave application submitted!');
        }

        function handleApproveLeave(leaveId) {
            const commentsInput = document.getElementById('hr-comments-' + leaveId);
            const comments = commentsInput ? commentsInput.value : 'Approved by HR';

            const leave = state.leaves.find(l => l.id === leaveId);
            if (leave) {
                leave.status = 'approved';
                leave.adminComments = comments;

                let current = new Date(leave.startDate);
                const end = new Date(leave.endDate);

                while (current <= end) {
                    if (current.getDay() !== 0 && current.getDay() !== 6) {
                        const dStr = formatDate(current);
                        const existingAtt = state.attendances.find(a => a.date === dStr && a.employee === leave.employee);
                        if (existingAtt) {
                            existingAtt.status = 'leave';
                            existingAtt.remarks = `Approved ${leave.type} Leave`;
                        } else {
                            state.attendances.unshift({
                                id: Date.now() + Math.random(),
                                date: dStr,
                                employee: leave.employee,
                                checkIn: '09:00 AM',
                                checkOut: '05:00 PM',
                                status: 'leave',
                                workedHours: 8.0,
                                effectiveHours: 8.0,
                                extraHours: 0.0
                            });
                        }
                    }
                    current.setDate(current.getDate() + 1);
                }

                saveState();
                renderAll();
                alert('Leave request approved!');
            }
        }

        function handleRejectLeave(leaveId) {
            const commentsInput = document.getElementById('hr-comments-' + leaveId);
            const comments = commentsInput ? commentsInput.value : 'Rejected by HR';
            const leave = state.leaves.find(l => l.id === leaveId);
            if (leave) {
                leave.status = 'rejected';
                leave.adminComments = comments;
                saveState();
                renderLeaves();
                alert('Leave request rejected.');
            }
        }

        function toggleAddEmpForm() {
            const card = document.getElementById('add-emp-card');
            card.style.display = card.style.display === 'none' ? 'block' : 'none';
        }

        function handleAddEmployee(e) {
            e.preventDefault();
            const name = document.getElementById('emp-name').value;
            const email = document.getElementById('emp-email').value;
            const job = document.getElementById('emp-job').value;
            const dept = document.getElementById('emp-dept').value;
            const role = document.getElementById('emp-role').value;
            const joining = document.getElementById('emp-joining').value;

            state.employees.unshift({
                id: Date.now(),
                name: name,
                email: email,
                job: job,
                dept: dept,
                role: role,
                joining: joining,
                loginId: '',
                provisioned: false
            });

            saveState();
            renderEmployees();
            e.target.reset();
            toggleAddEmpForm();
            alert('Employee profile created successfully!');
        }

        function handleProvisionAccount(empId) {
            const emp = state.employees.find(e => e.id === empId);
            if (emp) {
                const year = emp.joining ? emp.joining.split('-')[0] : '2026';
                const nameComp = emp.name.replace(/[^A-Z0-9]/gi, '').toUpperCase();
                const loginId = `DAYFLOW-${nameComp}-${year}-000${Math.floor(Math.random() * 90 + 10)}`;

                emp.provisioned = true;
                emp.loginId = loginId;

                saveState();
                renderEmployees();
                alert(`Account Provisioned Successfully!\n\nLogin ID: ${loginId}\nInitial Password: ${Math.random().toString(36).substring(2, 10)}`);
            }
        }

        function handleDocUpload(e) {
            e.preventDefault();
            const title = document.getElementById('doc-title').value;
            const employee = document.getElementById('doc-employee').value;
            const type = document.getElementById('doc-type').value;
            const filename = document.getElementById('doc-filename').value;

            state.documents.unshift({
                id: Date.now(),
                title: title,
                employee: employee,
                type: type,
                filename: filename,
                date: formatDate(new Date())
            });

            saveState();
            renderDocuments();
            e.target.reset();
            alert('Employee verification document uploaded successfully!');
        }

        function renderAttendanceBanner() {
            const statusDot = document.getElementById('banner-status-dot');
            const statusText = document.getElementById('banner-status-text');
            const checkInTime = document.getElementById('banner-checkin-time');
            const workedHours = document.getElementById('banner-worked-hours');
            const btnIn = document.getElementById('btn-check-in');
            const btnOut = document.getElementById('btn-check-out');

            if (state.isCheckedIn) {
                statusDot.className = 'status-dot green';
                statusText.innerText = 'Present (Checked In)';
                checkInTime.innerText = state.activeCheckInTime || '--:--';
                btnIn.disabled = true;
                btnOut.disabled = false;
            } else {
                statusDot.className = 'status-dot red';
                statusText.innerText = 'Not Checked In';
                checkInTime.innerText = '--:--';
                workedHours.innerText = '0h 00m';
                btnIn.disabled = false;
                btnOut.disabled = true;
            }
        }

        function renderAttendanceTable() {
            const tbody = document.getElementById('attendance-table-body');
            const tag = document.getElementById('record-rule-tag');

            let filtered = state.attendances;
            if (state.role === 'employee') {
                filtered = state.attendances.filter(a => a.employee === state.currentEmployee);
                tag.innerText = 'Showing personal attendance logs (Record Rule Protected)';
            } else {
                tag.innerText = 'Showing all organization attendance logs (HR / Admin Access)';
            }

            tbody.innerHTML = filtered.map(a => {
                const badgeClass = a.status === 'present' ? 'badge-present' :
                                   a.status === 'half_day' ? 'badge-halfday' :
                                   a.status === 'leave' ? 'badge-leave' : 'badge-absent';
                return `
                    <tr>
                        <td><strong>${a.date}</strong></td>
                        <td>${a.employee}</td>
                        <td>${a.checkIn}</td>
                        <td>${a.checkOut}</td>
                        <td><span class="badge ${badgeClass}">${a.status.toUpperCase().replace('_', ' ')}</span></td>
                        <td>${a.workedHours}h</td>
                        <td>${a.effectiveHours}h</td>
                        <td style="color: ${a.extraHours > 0 ? 'var(--accent-green)' : 'inherit'}; font-weight: ${a.extraHours > 0 ? '700' : 'normal'};">${a.extraHours}h</td>
                    </tr>
                `;
            }).join('');
        }

        function renderLeaves() {
            const tbody = document.getElementById('leave-table-body');
            let filtered = state.leaves;
            if (state.role === 'employee') {
                filtered = state.leaves.filter(l => l.employee === state.currentEmployee);
            }

            tbody.innerHTML = filtered.map(l => {
                const badgeClass = l.status === 'approved' ? 'badge-present' :
                                   l.status === 'rejected' ? 'badge-absent' : 'badge-pending';
                const typeLabel = l.type === 'paid' ? 'Paid Time Off' : l.type === 'sick' ? 'Sick Leave' : 'Unpaid Leave';

                let actionCol = '';
                if (state.role === 'admin' && l.status === 'pending') {
                    actionCol = `
                        <div style="display:flex; flex-direction:column; gap:0.4rem;">
                            <input type="text" id="hr-comments-${l.id}" class="form-control" style="font-size:0.75rem; padding:0.3rem;" placeholder="HR comment...">
                            <div style="display:flex; gap:0.4rem;">
                                <button class="btn btn-success" style="padding:0.25rem 0.5rem; font-size:0.75rem;" onclick="handleApproveLeave(${l.id})">Approve</button>
                                <button class="btn btn-danger" style="padding:0.25rem 0.5rem; font-size:0.75rem;" onclick="handleRejectLeave(${l.id})">Reject</button>
                            </div>
                        </div>
                    `;
                } else {
                    actionCol = `<span style="font-size:0.8rem; color:var(--text-secondary);">${l.adminComments || 'No HR comments'}</span>`;
                }

                return `
                    <tr>
                        <td><strong>${l.employee}</strong></td>
                        <td>${typeLabel}</td>
                        <td>${l.startDate}</td>
                        <td>${l.endDate}</td>
                        <td>${l.days} day(s)</td>
                        <td>${l.remarks}</td>
                        <td><span class="badge ${badgeClass}">${l.status.toUpperCase()}</span></td>
                        <td>${actionCol}</td>
                    </tr>
                `;
            }).join('');
        }

        function renderEmployees() {
            const grid = document.getElementById('employee-grid');
            grid.innerHTML = state.employees.map(e => `
                <div class="employee-card">
                    <div class="emp-header">
                        <div class="emp-avatar">${e.name.split(' ').map(n=>n[0]).join('')}</div>
                        <div class="emp-info">
                            <h4>${e.name}</h4>
                            <p>${e.job}</p>
                        </div>
                    </div>
                    <div class="emp-meta">
                        <div><strong>Dept:</strong> ${e.dept}</div>
                        <div><strong>Email:</strong> ${e.email}</div>
                        <div><strong>Joined:</strong> ${e.joining}</div>
                        <div style="margin-top:0.3rem;">
                            <span class="badge badge-role">${e.role}</span>
                        </div>
                        ${e.provisioned ? `
                            <div style="margin-top:0.5rem; font-size:0.75rem; color:#34d399;">
                                🔒 Account Provisioned<br><code style="color:var(--text-primary);">${e.loginId}</code>
                            </div>
                        ` : `
                            <button class="btn btn-secondary" style="margin-top:0.5rem; font-size:0.75rem; padding:0.3rem 0.6rem;" onclick="handleProvisionAccount(${e.id})">
                                Provision User Account
                            </button>
                        `}
                    </div>
                </div>
            `).join('');
        }

        function renderDocuments() {
            const tbody = document.getElementById('document-table-body');
            tbody.innerHTML = state.documents.map(d => `
                <tr>
                    <td><strong>${d.title}</strong></td>
                    <td>${d.employee}</td>
                    <td><span class="badge badge-role">${d.type.toUpperCase().replace('_', ' ')}</span></td>
                    <td><code>${d.filename}</code></td>
                    <td>${d.date}</td>
                    <td><span class="badge badge-present">VERIFIED</span></td>
                </tr>
            `).join('');
        }

        function renderAll() {
            renderAttendanceBanner();
            renderAttendanceTable();
            renderLeaves();
            renderEmployees();
            renderDocuments();
        }

        window.addEventListener('DOMContentLoaded', () => {
            renderAll();
        });
    </script>
</body>
</html>
"""

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(HTML_CONTENT.encode('utf-8'))

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print("==================================================")
    print(" Dayflow HRMS - Interactive Live UI Preview Server")
    print(" Running at: http://localhost:%d" % port)
    print(" Press Ctrl+C to stop the server.")
    print("==================================================")
    webbrowser.open("http://localhost:%d" % port)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping preview server...")
        httpd.server_close()

if __name__ == '__main__':
    run_server()
