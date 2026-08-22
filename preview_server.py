# -*- coding: utf-8 -*-
"""
Dayflow HRMS - Ultra-Clean, Decluttered Live UI Preview Server
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import webbrowser

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dayflow HRMS — Workspace</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-body: #0f1117;
            --bg-surface: #181b24;
            --bg-card: #202433;
            --bg-input: #292d3e;
            --accent-purple: #714b67;
            --accent-purple-hover: #885b7c;
            --accent-green: #10b981;
            --accent-amber: #f59e0b;
            --accent-red: #ef4444;
            --accent-blue: #3b82f6;
            --text-main: #f3f4f6;
            --text-muted: #9ca3af;
            --border-line: #2d3345;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
        }

        body {
            background-color: var(--bg-body);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }

        /* Top Navbar */
        .navbar {
            background-color: var(--bg-surface);
            border-bottom: 1px solid var(--border-line);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0.75rem 1.75rem;
            position: sticky;
            top: 0;
            z-index: 50;
        }

        .brand {
            display: flex;
            align-items: center;
            gap: 0.6rem;
            font-weight: 700;
            font-size: 1.15rem;
            color: #fff;
            text-decoration: none;
        }

        .brand-badge {
            background: linear-gradient(135deg, var(--accent-purple), #8b5cf6);
            color: #fff;
            padding: 0.25rem 0.55rem;
            border-radius: 6px;
            font-size: 0.85rem;
            font-weight: 800;
        }

        .nav-links {
            display: flex;
            gap: 0.35rem;
            list-style: none;
        }

        .nav-tab {
            padding: 0.45rem 0.9rem;
            border-radius: 6px;
            color: var(--text-muted);
            font-size: 0.875rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.15s ease;
        }

        .nav-tab:hover {
            color: var(--text-main);
            background-color: rgba(255, 255, 255, 0.04);
        }

        .nav-tab.active {
            color: #fff;
            background-color: var(--accent-purple);
        }

        .user-pill {
            background-color: var(--bg-input);
            border: 1px solid var(--border-line);
            padding: 0.3rem 0.75rem;
            border-radius: 20px;
            font-size: 0.8rem;
            color: var(--text-muted);
            display: flex;
            align-items: center;
            gap: 0.4rem;
        }

        .user-pill select {
            background: transparent;
            border: none;
            color: var(--text-main);
            font-weight: 600;
            font-size: 0.8rem;
            outline: none;
            cursor: pointer;
        }

        /* Container & Layout */
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 1.5rem;
            width: 100%;
            flex: 1;
        }

        .header-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.25rem;
        }

        .header-title {
            font-size: 1.35rem;
            font-weight: 700;
        }

        .card {
            background-color: var(--bg-surface);
            border: 1px solid var(--border-line);
            border-radius: 10px;
            padding: 1.25rem 1.5rem;
            margin-bottom: 1.25rem;
        }

        /* Buttons */
        .btn {
            padding: 0.45rem 1.1rem;
            border-radius: 6px;
            border: none;
            font-weight: 600;
            font-size: 0.85rem;
            cursor: pointer;
            transition: all 0.15s ease;
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
        }

        .btn:disabled {
            opacity: 0.4;
            cursor: not-allowed;
        }

        .btn-primary { background-color: var(--accent-purple); color: #fff; }
        .btn-primary:hover:not(:disabled) { background-color: var(--accent-purple-hover); }

        .btn-success { background-color: var(--accent-green); color: #fff; }
        .btn-success:hover:not(:disabled) { filter: brightness(1.1); }

        .btn-danger { background-color: var(--accent-red); color: #fff; }
        .btn-danger:hover:not(:disabled) { filter: brightness(1.1); }

        .btn-secondary {
            background-color: var(--bg-input);
            color: var(--text-main);
            border: 1px solid var(--border-line);
        }
        .btn-secondary:hover:not(:disabled) { background-color: var(--border-line); }

        /* Action Banner */
        .banner {
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: linear-gradient(135deg, rgba(113, 75, 103, 0.18), rgba(24, 27, 36, 0.95));
            border: 1px solid rgba(113, 75, 103, 0.35);
            border-radius: 10px;
            padding: 1.25rem 1.5rem;
            margin-bottom: 1.25rem;
        }

        .banner-metrics {
            display: flex;
            gap: 2.5rem;
            align-items: center;
        }

        .metric {
            display: flex;
            flex-direction: column;
            gap: 0.2rem;
        }

        .metric-label {
            font-size: 0.72rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-weight: 600;
        }

        .metric-val {
            font-size: 1.25rem;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 0.4rem;
        }

        .dot { width: 9px; height: 9px; border-radius: 50%; }
        .dot.green { background-color: var(--accent-green); box-shadow: 0 0 8px var(--accent-green); }
        .dot.red { background-color: var(--accent-red); }

        /* Metrics Grid */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-bottom: 1.25rem;
        }

        .stat-box {
            background-color: var(--bg-card);
            border: 1px solid var(--border-line);
            padding: 1rem 1.25rem;
            border-radius: 8px;
        }

        .stat-box .num {
            font-size: 1.5rem;
            font-weight: 700;
            margin-top: 0.25rem;
        }

        /* Employee Grid */
        .emp-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 1rem;
        }

        .emp-card {
            background-color: var(--bg-card);
            border: 1px solid var(--border-line);
            border-radius: 8px;
            padding: 1.1rem;
            display: flex;
            flex-direction: column;
            gap: 0.6rem;
        }

        .emp-head {
            display: flex;
            align-items: center;
            gap: 0.85rem;
        }

        .avatar {
            width: 44px;
            height: 44px;
            border-radius: 50%;
            background: linear-gradient(135deg, var(--accent-purple), var(--accent-blue));
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            color: #fff;
            font-size: 1rem;
        }

        .emp-name { font-size: 1rem; font-weight: 700; }
        .emp-job { font-size: 0.78rem; color: var(--text-muted); }

        /* Tables */
        .table-wrap {
            width: 100%;
            overflow-x: auto;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            font-size: 0.875rem;
        }

        th {
            background-color: var(--bg-card);
            color: var(--text-muted);
            padding: 0.65rem 0.9rem;
            font-weight: 600;
            border-bottom: 1px solid var(--border-line);
            font-size: 0.72rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        td {
            padding: 0.75rem 0.9rem;
            border-bottom: 1px solid rgba(45, 51, 69, 0.6);
        }

        tr:hover td {
            background-color: rgba(255, 255, 255, 0.015);
        }

        /* Badges */
        .badge {
            display: inline-flex;
            align-items: center;
            padding: 0.2rem 0.55rem;
            border-radius: 12px;
            font-size: 0.73rem;
            font-weight: 600;
        }

        .badge-green { background-color: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); }
        .badge-amber { background-color: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3); }
        .badge-red { background-color: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); }
        .badge-purple { background-color: rgba(113, 75, 103, 0.3); color: #e9d5ff; border: 1px solid rgba(113, 75, 103, 0.5); }

        /* Forms */
        .form-row {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 1rem;
            margin-bottom: 1rem;
        }

        .field {
            display: flex;
            flex-direction: column;
            gap: 0.35rem;
        }

        .field label {
            font-size: 0.8rem;
            font-weight: 600;
            color: var(--text-muted);
        }

        .input {
            background-color: var(--bg-input);
            border: 1px solid var(--border-line);
            color: var(--text-main);
            padding: 0.55rem 0.75rem;
            border-radius: 6px;
            font-size: 0.875rem;
            outline: none;
        }

        .input:focus { border-color: var(--accent-purple); }

        /* Filter Pills */
        .filter-group {
            display: flex;
            gap: 0.4rem;
            flex-wrap: wrap;
        }

        .pill-btn {
            padding: 0.3rem 0.75rem;
            border-radius: 20px;
            font-size: 0.78rem;
            font-weight: 600;
            background-color: var(--bg-card);
            color: var(--text-muted);
            border: 1px solid var(--border-line);
            cursor: pointer;
            transition: all 0.15s ease;
        }

        .pill-btn.active {
            background-color: var(--accent-purple);
            color: #fff;
            border-color: var(--accent-purple);
        }

        /* Modal */
        .modal {
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background-color: rgba(0, 0, 0, 0.8);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 100;
        }

        .modal-card {
            background-color: var(--bg-surface);
            border: 1px solid var(--border-line);
            border-radius: 10px;
            max-width: 650px;
            width: 90%;
            padding: 1.25rem;
            max-height: 85vh;
            overflow-y: auto;
        }

        .tab-panel { display: none; }
        .tab-panel.active { display: block; }
    </style>
</head>
<body>

    <!-- Top Navbar -->
    <nav class="navbar">
        <a href="#" class="brand">
            <span class="brand-badge">DF</span> Dayflow HRMS
        </a>
        <ul class="nav-links">
            <li class="nav-tab active" id="tab-btn-attendance" onclick="openTab('attendance')">Attendance</li>
            <li class="nav-tab" id="tab-btn-leave" onclick="openTab('leave')">Time Off</li>
            <li class="nav-tab" id="tab-btn-employees" onclick="openTab('employees')">Employees</li>
            <li class="nav-tab" id="tab-btn-documents" onclick="openTab('documents')">Documents</li>
            <li class="nav-tab" id="tab-btn-payroll" onclick="openTab('payroll')">Payroll</li>
        </ul>
        <div class="user-pill">
            <span>Signed in as:</span>
            <select id="user-role-select" onchange="onRoleChange(this.value)">
                <option value="employee">Employee (John Doe)</option>
                <option value="admin">HR Manager (Admin)</option>
            </select>
        </div>
    </nav>

    <div class="container">

        <!-- ATTENDANCE TAB -->
        <div id="panel-attendance" class="tab-panel active">
            <div class="header-row">
                <div>
                    <h1 class="header-title">Attendance Tracking</h1>
                </div>
                <button class="btn btn-secondary" onclick="resetData()">Reset Data</button>
            </div>

            <div class="banner">
                <div class="banner-metrics">
                    <div class="metric">
                        <span class="metric-label">Status</span>
                        <div class="metric-val">
                            <span id="dot-status" class="dot red"></span>
                            <span id="txt-status">Not Checked In</span>
                        </div>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Check-In</span>
                        <span class="metric-val" id="txt-checkin-time">--:--</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Working Hours</span>
                        <span class="metric-val" id="txt-worked-hours" style="color: var(--accent-purple-hover);">0h 00m</span>
                    </div>
                </div>
                <div>
                    <button id="btn-in" class="btn btn-success" onclick="handleCheckIn()">Check In</button>
                    <button id="btn-out" class="btn btn-danger" onclick="handleCheckOut()" disabled>Check Out</button>
                </div>
            </div>

            <div class="card">
                <div class="table-wrap">
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
                        <tbody id="tbl-attendance"></tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- TIME OFF / LEAVE TAB -->
        <div id="panel-leave" class="tab-panel">
            <div class="header-row">
                <h1 class="header-title">Time Off & Leave Management</h1>
            </div>

            <div class="stats-grid">
                <div class="stat-box">
                    <div class="metric-label">Paid Time Off</div>
                    <div class="num" style="color: #34d399;">12 Days</div>
                </div>
                <div class="stat-box">
                    <div class="metric-label">Sick Leave</div>
                    <div class="num" style="color: #fbbf24;">8 Days</div>
                </div>
                <div class="stat-box">
                    <div class="metric-label">Unpaid Leave</div>
                    <div class="num" style="color: #60a5fa;">Unlimited</div>
                </div>
            </div>

            <div class="card">
                <h3 style="font-size: 1.05rem; margin-bottom: 1rem;">Apply for Time Off</h3>
                <form onsubmit="handleLeaveSubmit(event)">
                    <div class="form-row">
                        <div class="field">
                            <label>Leave Type</label>
                            <select id="leave-type" class="input" required>
                                <option value="paid">Paid Time Off</option>
                                <option value="sick">Sick Leave</option>
                                <option value="unpaid">Unpaid Leave</option>
                            </select>
                        </div>
                        <div class="field">
                            <label>Start Date</label>
                            <input type="date" id="leave-start" class="input" required>
                        </div>
                        <div class="field">
                            <label>End Date</label>
                            <input type="date" id="leave-end" class="input" required>
                        </div>
                    </div>
                    <div class="field" style="margin-bottom: 1rem;">
                        <label>Reason / Remarks</label>
                        <textarea id="leave-reason" class="input" rows="2" placeholder="State reason..." required></textarea>
                    </div>
                    <button type="submit" class="btn btn-primary">Submit Application</button>
                </form>
            </div>

            <div class="card">
                <div class="table-wrap">
                    <table>
                        <thead>
                            <tr>
                                <th>Employee</th>
                                <th>Type</th>
                                <th>Start Date</th>
                                <th>End Date</th>
                                <th>Days</th>
                                <th>Reason</th>
                                <th>Status</th>
                                <th>HR Decision</th>
                            </tr>
                        </thead>
                        <tbody id="tbl-leave"></tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- EMPLOYEES TAB -->
        <div id="panel-employees" class="tab-panel">
            <div class="header-row">
                <h1 class="header-title">Employee Directory</h1>
                <button class="btn btn-primary" onclick="toggleEmpForm()">+ Add Employee</button>
            </div>

            <div class="card" id="form-emp-card" style="display: none;">
                <h3 style="font-size: 1.05rem; margin-bottom: 1rem;">Create Employee Profile</h3>
                <form onsubmit="handleAddEmp(event)">
                    <div class="form-row">
                        <div class="field">
                            <label>Full Name</label>
                            <input type="text" id="emp-name" class="input" placeholder="Alice Johnson" required>
                        </div>
                        <div class="field">
                            <label>Work Email</label>
                            <input type="email" id="emp-email" class="input" placeholder="alice@company.com" required>
                        </div>
                        <div class="field">
                            <label>Job Title</label>
                            <input type="text" id="emp-job" class="input" placeholder="Software Engineer" required>
                        </div>
                        <div class="field">
                            <label>Department</label>
                            <input type="text" id="emp-dept" class="input" placeholder="Engineering" required>
                        </div>
                        <div class="field">
                            <label>Role</label>
                            <select id="emp-role" class="input" required>
                                <option value="Employee">Employee</option>
                                <option value="Admin / HR">Admin / HR</option>
                            </select>
                        </div>
                        <div class="field">
                            <label>Joining Date</label>
                            <input type="date" id="emp-joining" class="input" required>
                        </div>
                    </div>
                    <button type="submit" class="btn btn-success">Save Profile</button>
                </form>
            </div>

            <div class="emp-grid" id="grid-employees"></div>
        </div>

        <!-- DOCUMENTS TAB -->
        <div id="panel-documents" class="tab-panel">
            <div class="header-row">
                <h1 class="header-title">Employee Documents</h1>
            </div>

            <div class="stats-grid">
                <div class="stat-box">
                    <div class="metric-label">ID Proofs</div>
                    <div class="num" style="color: #60a5fa;" id="stat-id">0</div>
                </div>
                <div class="stat-box">
                    <div class="metric-label">Contracts</div>
                    <div class="num" style="color: #34d399;" id="stat-contract">0</div>
                </div>
                <div class="stat-box">
                    <div class="metric-label">Certificates</div>
                    <div class="num" style="color: #fbbf24;" id="stat-cert">0</div>
                </div>
                <div class="stat-box">
                    <div class="metric-label">Verified Documents</div>
                    <div class="num" style="color: var(--accent-purple-hover);" id="stat-verified">0</div>
                </div>
            </div>

            <div class="card">
                <h3 style="font-size: 1.05rem; margin-bottom: 1rem;">Upload Document</h3>
                <form onsubmit="handleDocUpload(event)">
                    <div class="form-row">
                        <div class="field">
                            <label>Document Title</label>
                            <input type="text" id="doc-title" class="input" placeholder="Passport Verification Copy" required>
                        </div>
                        <div class="field">
                            <label>Employee</label>
                            <select id="doc-employee" class="input" required>
                                <option value="John Doe">John Doe</option>
                                <option value="Jane Smith">Jane Smith</option>
                                <option value="Robert Taylor">Robert Taylor</option>
                            </select>
                        </div>
                        <div class="field">
                            <label>Category</label>
                            <select id="doc-type" class="input" required>
                                <option value="id_proof">ID Proof</option>
                                <option value="contract">Contract</option>
                                <option value="certificate">Certificate</option>
                                <option value="other">Other</option>
                            </select>
                        </div>
                        <div class="field">
                            <label>Select File (PDF, Image, Doc)</label>
                            <input type="file" id="real-file-input" class="input" accept="image/*,.pdf,.doc,.docx,.txt" required>
                        </div>
                    </div>
                    <button type="submit" class="btn btn-primary">Upload & Attach File</button>
                </form>
            </div>

            <div class="card">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 0.9rem;">
                    <h3 style="font-size: 1.05rem;">Document Library</h3>
                    <div class="filter-group">
                        <button class="pill-btn active" id="f-all" onclick="filterDoc('all')">All</button>
                        <button class="pill-btn" id="f-id_proof" onclick="filterDoc('id_proof')">ID Proofs</button>
                        <button class="pill-btn" id="f-contract" onclick="filterDoc('contract')">Contracts</button>
                        <button class="pill-btn" id="f-certificate" onclick="filterDoc('certificate')">Certificates</button>
                        <button class="pill-btn" id="f-verified" onclick="filterDoc('verified')">Verified</button>
                    </div>
                </div>
                <div class="table-wrap">
                    <table>
                        <thead>
                            <tr>
                                <th>Title</th>
                                <th>Employee</th>
                                <th>Category</th>
                                <th>File Info</th>
                                <th>Uploaded</th>
                                <th>Status</th>
                                <th>Action</th>
                                <th>HR Review</th>
                            </tr>
                        </thead>
                        <tbody id="tbl-documents"></tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- PAYROLL TAB -->
        <div id="panel-payroll" class="tab-panel">
            <div class="card">
                <h2 style="font-size: 1.1rem;">Payroll & Salary Management</h2>
                <p style="color:var(--text-muted); margin-top:0.35rem; font-size:0.875rem;">Managed by Person 4 (Payroll computation, base salary, allowances, net salary).</p>
            </div>
        </div>

    </div>

    <!-- Modal -->
    <div id="file-modal" class="modal" style="display: none;">
        <div class="modal-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <h3 id="modal-title" style="font-size: 1.1rem;">Document Preview</h3>
                <button class="btn btn-secondary" onclick="closeModal()">✕</button>
            </div>
            <div id="modal-content" style="min-height: 220px; display: flex; align-items: center; justify-content: center; background-color: var(--bg-body); border-radius: 6px; padding: 1rem; border: 1px solid var(--border-line);">
            </div>
            <div style="display: flex; justify-content: flex-end; margin-top: 1rem;">
                <a id="modal-download" href="#" download class="btn btn-primary">💾 Download File</a>
            </div>
        </div>
    </div>

    <script>
        const DEFAULT_ATTENDANCE = [
            { id: 1, date: '2026-08-21', employee: 'John Doe', checkIn: '09:00 AM', checkOut: '05:30 PM', status: 'present', workedHours: 8.5, effectiveHours: 8.5, extraHours: 0.5 },
            { id: 2, date: '2026-08-20', employee: 'John Doe', checkIn: '08:50 AM', checkOut: '06:10 PM', status: 'present', workedHours: 9.3, effectiveHours: 9.3, extraHours: 1.3 },
            { id: 3, date: '2026-08-19', employee: 'John Doe', checkIn: '09:15 AM', checkOut: '01:00 PM', status: 'half_day', workedHours: 3.75, effectiveHours: 3.75, extraHours: 0.0 }
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
            { id: 1, title: 'Passport Verification ID', employee: 'John Doe', type: 'id_proof', filename: 'john_passport.pdf', size: '1.2 MB', date: '2026-08-10', status: 'verified', adminComments: 'Verified by HR', fileData: '' },
            { id: 2, title: 'Employment Contract 2026', employee: 'Jane Smith', type: 'contract', filename: 'jane_contract_2026.pdf', size: '450 KB', date: '2026-08-01', status: 'verified', adminComments: 'Signed contract on file', fileData: '' }
        ];

        let state = {
            role: 'employee',
            currentEmployee: 'John Doe',
            isCheckedIn: false,
            activeCheckInTime: null,
            checkInTimestamp: null,
            tickerInterval: null,
            currentDocFilter: 'all',
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

        function resetData() {
            localStorage.clear();
            state.attendances = JSON.parse(JSON.stringify(DEFAULT_ATTENDANCE));
            state.leaves = JSON.parse(JSON.stringify(DEFAULT_LEAVE));
            state.employees = JSON.parse(JSON.stringify(DEFAULT_EMPLOYEES));
            state.documents = JSON.parse(JSON.stringify(DEFAULT_DOCUMENTS));
            state.isCheckedIn = false;
            if (state.tickerInterval) clearInterval(state.tickerInterval);
            renderAll();
        }

        function formatTime(d) {
            return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true });
        }

        function formatDate(d) {
            return d.toISOString().split('T')[0];
        }

        function formatFileSize(bytes) {
            if (!bytes) return '0 B';
            const k = 1024;
            const sizes = ['B', 'KB', 'MB'];
            const i = Math.floor(Math.log(bytes) / Math.log(k));
            return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
        }

        function openTab(tabId) {
            document.querySelectorAll('.nav-tab').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.tab-panel').forEach(el => el.classList.remove('active'));

            const btn = document.getElementById('tab-btn-' + tabId);
            if (btn) btn.classList.add('active');
            const panel = document.getElementById('panel-' + tabId);
            if (panel) panel.classList.add('active');
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

            const newRec = {
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

            state.attendances.unshift(newRec);
            saveState();
            renderAttendance();
        }

        function updateLiveTicker() {
            if (!state.isCheckedIn || !state.checkInTimestamp) return;

            const diffSec = Math.floor((Date.now() - state.checkInTimestamp) / 1000);
            const hrs = Math.floor(diffSec / 3600);
            const mins = Math.floor((diffSec % 3600) / 60);
            const secs = diffSec % 60;

            document.getElementById('txt-worked-hours').innerText = `${hrs}h ${mins.toString().padStart(2, '0')}m ${secs.toString().padStart(2, '0')}s`;

            const activeRec = state.attendances.find(a => a.isActive);
            if (activeRec) {
                const workedHrs = parseFloat((diffSec / 3600).toFixed(2));
                activeRec.workedHours = workedHrs;
                activeRec.effectiveHours = workedHrs;
                activeRec.extraHours = workedHrs > 8.0 ? parseFloat((workedHrs - 8.0).toFixed(2)) : 0.0;
                renderAttendanceTbl();
            }
        }

        function handleCheckOut() {
            if (!state.isCheckedIn) return;
            const now = new Date();
            if (state.tickerInterval) clearInterval(state.tickerInterval);

            const activeRec = state.attendances.find(a => a.isActive);
            if (activeRec) {
                activeRec.checkOut = formatTime(now);
                activeRec.isActive = false;
                const diffSec = Math.floor((now.getTime() - state.checkInTimestamp) / 1000);
                const workedHrs = parseFloat((diffSec / 3600).toFixed(2));
                activeRec.workedHours = workedHrs > 0 ? workedHrs : 0.1;
                activeRec.effectiveHours = activeRec.workedHours;
                activeRec.extraHours = activeRec.workedHours > 8.0 ? parseFloat((activeRec.workedHours - 8.0).toFixed(2)) : 0.0;
                activeRec.status = 'present';
            }

            state.isCheckedIn = false;
            saveState();
            renderAttendance();
        }

        function handleLeaveSubmit(e) {
            e.preventDefault();
            const type = document.getElementById('leave-type').value;
            const start = document.getElementById('leave-start').value;
            const end = document.getElementById('leave-end').value;
            const reason = document.getElementById('leave-reason').value;

            const days = Math.ceil((new Date(end) - new Date(start)) / (1000 * 60 * 60 * 24)) + 1;

            state.leaves.unshift({
                id: Date.now(),
                employee: state.currentEmployee,
                type: type,
                startDate: start,
                endDate: end,
                days: days,
                remarks: reason,
                status: 'pending',
                adminComments: ''
            });

            saveState();
            renderLeaves();
            e.target.reset();
        }

        function handleApproveLeave(id) {
            const comment = document.getElementById('hr-leave-comment-' + id)?.value || 'Approved by HR';
            const leave = state.leaves.find(l => l.id === id);
            if (leave) {
                leave.status = 'approved';
                leave.adminComments = comment;
                saveState();
                renderAll();
            }
        }

        function handleRejectLeave(id) {
            const comment = document.getElementById('hr-leave-comment-' + id)?.value || 'Rejected by HR';
            const leave = state.leaves.find(l => l.id === id);
            if (leave) {
                leave.status = 'rejected';
                leave.adminComments = comment;
                saveState();
                renderLeaves();
            }
        }

        function toggleEmpForm() {
            const card = document.getElementById('form-emp-card');
            card.style.display = card.style.display === 'none' ? 'block' : 'none';
        }

        function handleAddEmp(e) {
            e.preventDefault();
            state.employees.unshift({
                id: Date.now(),
                name: document.getElementById('emp-name').value,
                email: document.getElementById('emp-email').value,
                job: document.getElementById('emp-job').value,
                dept: document.getElementById('emp-dept').value,
                role: document.getElementById('emp-role').value,
                joining: document.getElementById('emp-joining').value,
                loginId: '',
                provisioned: false
            });

            saveState();
            renderEmployees();
            e.target.reset();
            toggleEmpForm();
        }

        function handleProvision(id) {
            const emp = state.employees.find(e => e.id === id);
            if (emp) {
                const year = emp.joining ? emp.joining.split('-')[0] : '2026';
                emp.provisioned = true;
                emp.loginId = `DAYFLOW-${emp.name.replace(/[^A-Z]/gi, '').toUpperCase()}-${year}-000${Math.floor(Math.random() * 90 + 10)}`;
                saveState();
                renderEmployees();
            }
        }

        function filterDoc(cat) {
            state.currentDocFilter = cat;
            document.querySelectorAll('.pill-btn').forEach(b => b.classList.remove('active'));
            const b = document.getElementById('f-' + cat);
            if (b) b.classList.add('active');
            renderDocuments();
        }

        function handleDocUpload(e) {
            e.preventDefault();
            const fileInput = document.getElementById('real-file-input');
            if (!fileInput.files || fileInput.files.length === 0) return;

            const file = fileInput.files[0];
            const reader = new FileReader();

            reader.onload = function(evt) {
                state.documents.unshift({
                    id: Date.now(),
                    title: document.getElementById('doc-title').value,
                    employee: document.getElementById('doc-employee').value,
                    type: document.getElementById('doc-type').value,
                    filename: file.name,
                    size: formatFileSize(file.size),
                    date: formatDate(new Date()),
                    status: 'draft',
                    adminComments: '',
                    fileData: evt.target.result
                });

                saveState();
                renderDocuments();
                e.target.reset();
            };

            reader.readAsDataURL(file);
        }

        function handleVerifyDoc(id) {
            const comment = document.getElementById('doc-comment-' + id)?.value || 'Verified by HR';
            const doc = state.documents.find(d => d.id === id);
            if (doc) {
                doc.status = 'verified';
                doc.adminComments = comment;
                saveState();
                renderDocuments();
            }
        }

        function handleRejectDoc(id) {
            const comment = document.getElementById('doc-comment-' + id)?.value || 'Rejected by HR';
            const doc = state.documents.find(d => d.id === id);
            if (doc) {
                doc.status = 'rejected';
                doc.adminComments = comment;
                saveState();
                renderDocuments();
            }
        }

        function previewFile(id) {
            const doc = state.documents.find(d => d.id === id);
            if (!doc) return;

            document.getElementById('modal-title').innerText = `${doc.title} (${doc.filename})`;
            const container = document.getElementById('modal-content');
            const link = document.getElementById('modal-download');

            link.download = doc.filename;
            link.href = doc.fileData || '#';

            if (doc.fileData && doc.fileData.startsWith('data:image')) {
                container.innerHTML = `<img src="${doc.fileData}" style="max-width:100%; max-height:360px; border-radius:6px;">`;
            } else if (doc.fileData && doc.fileData.startsWith('data:application/pdf')) {
                container.innerHTML = `<embed src="${doc.fileData}" type="application/pdf" width="100%" height="360px" />`;
            } else {
                container.innerHTML = `<div style="text-align:center; color:var(--text-muted);"><div style="font-size:2.5rem;">📄</div><p style="margin-top:0.5rem; color:#fff;">${doc.filename}</p></div>`;
            }

            document.getElementById('file-modal').style.display = 'flex';
        }

        function closeModal() {
            document.getElementById('file-modal').style.display = 'none';
        }

        function renderAttendance() {
            const dot = document.getElementById('dot-status');
            const txt = document.getElementById('txt-status');
            const checkIn = document.getElementById('txt-checkin-time');
            const btnIn = document.getElementById('btn-in');
            const btnOut = document.getElementById('btn-out');

            if (state.isCheckedIn) {
                dot.className = 'dot green';
                txt.innerText = 'Present';
                checkIn.innerText = state.activeCheckInTime || '--:--';
                btnIn.disabled = true;
                btnOut.disabled = false;
            } else {
                dot.className = 'dot red';
                txt.innerText = 'Not Checked In';
                checkIn.innerText = '--:--';
                document.getElementById('txt-worked-hours').innerText = '0h 00m';
                btnIn.disabled = false;
                btnOut.disabled = true;
            }
            renderAttendanceTbl();
        }

        function renderAttendanceTbl() {
            const tbody = document.getElementById('tbl-attendance');
            let data = state.role === 'employee' ? state.attendances.filter(a => a.employee === state.currentEmployee) : state.attendances;

            tbody.innerHTML = data.map(a => `
                <tr>
                    <td><strong>${a.date}</strong></td>
                    <td>${a.employee}</td>
                    <td>${a.checkIn}</td>
                    <td>${a.checkOut}</td>
                    <td><span class="badge ${a.status==='present'?'badge-green':a.status==='half_day'?'badge-amber':'badge-red'}">${a.status.toUpperCase()}</span></td>
                    <td>${a.workedHours}h</td>
                    <td>${a.effectiveHours}h</td>
                    <td style="color:${a.extraHours>0?'var(--accent-green)':'inherit'}">${a.extraHours}h</td>
                </tr>
            `).join('');
        }

        function renderLeaves() {
            const tbody = document.getElementById('tbl-leave');
            let data = state.role === 'employee' ? state.leaves.filter(l => l.employee === state.currentEmployee) : state.leaves;

            tbody.innerHTML = data.map(l => {
                const badge = l.status === 'approved' ? 'badge-green' : l.status === 'rejected' ? 'badge-red' : 'badge-amber';
                let action = '';

                if (state.role === 'admin' && l.status === 'pending') {
                    action = `
                        <div style="display:flex; gap:0.3rem;">
                            <input type="text" id="hr-leave-comment-${l.id}" class="input" style="font-size:0.75rem; padding:0.25rem 0.5rem;" placeholder="Comment...">
                            <button class="btn btn-success" style="padding:0.2rem 0.5rem; font-size:0.75rem;" onclick="handleApproveLeave(${l.id})">Approve</button>
                            <button class="btn btn-danger" style="padding:0.2rem 0.5rem; font-size:0.75rem;" onclick="handleRejectLeave(${l.id})">Reject</button>
                        </div>
                    `;
                } else {
                    action = `<span style="font-size:0.8rem; color:var(--text-muted);">${l.adminComments || '--'}</span>`;
                }

                return `
                    <tr>
                        <td><strong>${l.employee}</strong></td>
                        <td>${l.type.toUpperCase()}</td>
                        <td>${l.startDate}</td>
                        <td>${l.endDate}</td>
                        <td>${l.days}d</td>
                        <td>${l.remarks}</td>
                        <td><span class="badge ${badge}">${l.status.toUpperCase()}</span></td>
                        <td>${action}</td>
                    </tr>
                `;
            }).join('');
        }

        function renderEmployees() {
            const grid = document.getElementById('grid-employees');
            grid.innerHTML = state.employees.map(e => `
                <div class="emp-card">
                    <div class="emp-head">
                        <div class="avatar">${e.name.split(' ').map(n=>n[0]).join('')}</div>
                        <div>
                            <div class="emp-name">${e.name}</div>
                            <div class="emp-job">${e.job} • ${e.dept}</div>
                        </div>
                    </div>
                    <div style="font-size:0.8rem; color:var(--text-muted); display:flex; flex-direction:column; gap:0.25rem;">
                        <div>Email: ${e.email}</div>
                        <div>Role: <span class="badge badge-purple">${e.role}</span></div>
                        ${e.provisioned ? `<div style="color:#34d399; font-size:0.75rem; margin-top:0.25rem;">🔒 Account: <code>${e.loginId}</code></div>` :
                        `<button class="btn btn-secondary" style="font-size:0.75rem; padding:0.25rem 0.5rem; margin-top:0.35rem;" onclick="handleProvision(${e.id})">Provision Account</button>`}
                    </div>
                </div>
            `).join('');
        }

        function renderDocuments() {
            document.getElementById('stat-id').innerText = state.documents.filter(d => d.type === 'id_proof').length;
            document.getElementById('stat-contract').innerText = state.documents.filter(d => d.type === 'contract').length;
            document.getElementById('stat-cert').innerText = state.documents.filter(d => d.type === 'certificate').length;
            document.getElementById('stat-verified').innerText = state.documents.filter(d => d.status === 'verified').length;

            const tbody = document.getElementById('tbl-documents');
            let data = state.documents;
            if (state.role === 'employee') data = data.filter(d => d.employee === state.currentEmployee);

            if (state.currentDocFilter !== 'all') {
                data = state.currentDocFilter === 'verified' ? data.filter(d => d.status === 'verified') : data.filter(d => d.type === state.currentDocFilter);
            }

            tbody.innerHTML = data.map(d => {
                const badge = d.status === 'verified' ? 'badge-green' : d.status === 'rejected' ? 'badge-red' : 'badge-amber';
                let hrAction = '';

                if (state.role === 'admin' && d.status === 'draft') {
                    hrAction = `
                        <div style="display:flex; gap:0.3rem;">
                            <input type="text" id="doc-comment-${d.id}" class="input" style="font-size:0.75rem; padding:0.25rem 0.5rem;" placeholder="Comment...">
                            <button class="btn btn-success" style="padding:0.2rem 0.5rem; font-size:0.75rem;" onclick="handleVerifyDoc(${d.id})">Approve</button>
                            <button class="btn btn-danger" style="padding:0.2rem 0.5rem; font-size:0.75rem;" onclick="handleRejectDoc(${d.id})">Reject</button>
                        </div>
                    `;
                } else {
                    hrAction = `<span style="font-size:0.8rem; color:var(--text-muted);">${d.adminComments || '--'}</span>`;
                }

                return `
                    <tr>
                        <td><strong>${d.title}</strong></td>
                        <td>${d.employee}</td>
                        <td><span class="badge badge-purple">${d.type.toUpperCase().replace('_', ' ')}</span></td>
                        <td><code>${d.filename}</code> <span style="font-size:0.75rem; color:var(--text-muted);">(${d.size})</span></td>
                        <td>${d.date}</td>
                        <td><span class="badge ${badge}">${d.status.toUpperCase()}</span></td>
                        <td><button class="btn btn-secondary" style="padding:0.2rem 0.5rem; font-size:0.75rem;" onclick="previewFile(${d.id})">👁️ View</button></td>
                        <td>${hrAction}</td>
                    </tr>
                `;
            }).join('');
        }

        function renderAll() {
            renderAttendance();
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
    print(" Dayflow HRMS - Decluttered Live Preview Server")
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
