# -*- coding: utf-8 -*-
"""
Dayflow HRMS - Unified Live UI Preview Server
Odoo x NMIT Hackathon
All-in-One Dashboard, Employees, Attendance, Time Off, Documents, and Payroll Console
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import webbrowser

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dayflow HRMS — Workspace & Management Console</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
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
            max-width: 1240px;
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

        .header-sub {
            font-size: 0.85rem;
            color: var(--text-muted);
            margin-top: 0.2rem;
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

        /* Hero KPI Grid */
        .kpi-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
            gap: 1rem;
            margin-bottom: 1.25rem;
        }

        .kpi-card {
            background-color: var(--bg-surface);
            border: 1px solid var(--border-line);
            border-radius: 10px;
            padding: 1.15rem 1.35rem;
            display: flex;
            align-items: center;
            gap: 1rem;
            cursor: pointer;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .kpi-card:hover {
            transform: translateY(-2px);
            border-color: var(--accent-purple);
            box-shadow: 0 8px 16px rgba(0,0,0,0.25);
        }

        .kpi-icon-box {
            width: 46px;
            height: 46px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.35rem;
        }

        .kpi-blue { border-left: 4px solid var(--accent-blue); }
        .kpi-blue .kpi-icon-box { background: rgba(59, 130, 246, 0.15); color: #60a5fa; }

        .kpi-green { border-left: 4px solid var(--accent-green); }
        .kpi-green .kpi-icon-box { background: rgba(16, 185, 129, 0.15); color: #34d399; }

        .kpi-amber { border-left: 4px solid var(--accent-amber); }
        .kpi-amber .kpi-icon-box { background: rgba(245, 158, 11, 0.15); color: #fbbf24; }

        .kpi-red { border-left: 4px solid var(--accent-red); }
        .kpi-red .kpi-icon-box { background: rgba(239, 68, 68, 0.15); color: #f87171; }

        .kpi-label { font-size: 0.72rem; font-weight: 600; text-transform: uppercase; color: var(--text-muted); }
        .kpi-val { font-size: 1.6rem; font-weight: 800; color: #fff; line-height: 1.1; margin-top: 2px; }
        .kpi-sub { font-size: 0.72rem; font-weight: 600; color: var(--text-muted); margin-top: 3px; }

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

        /* 2-Column Grid Layout */
        .two-col-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1.25rem;
            margin-bottom: 1.25rem;
        }

        @media (max-width: 900px) {
            .two-col-grid { grid-template-columns: 1fr; }
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
        .badge-blue { background-color: rgba(59, 130, 246, 0.15); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.3); }

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
            <li class="nav-tab active" id="tab-btn-dashboard" onclick="openTab('dashboard')">Dashboard</li>
            <li class="nav-tab" id="tab-btn-attendance" onclick="openTab('attendance')">Attendance</li>
            <li class="nav-tab" id="tab-btn-leave" onclick="openTab('leave')">Time Off</li>
            <li class="nav-tab" id="tab-btn-employees" onclick="openTab('employees')">Employees</li>
            <li class="nav-tab" id="tab-btn-documents" onclick="openTab('documents')">Documents</li>
            <li class="nav-tab" id="tab-btn-payroll" onclick="openTab('payroll')">Payroll</li>
        </ul>
        <div class="user-pill">
            <span>Signed in as:</span>
            <select id="user-role-select" onchange="onRoleChange(this.value)">
                <option value="admin">HR Manager (Admin)</option>
                <option value="employee">Employee (John Doe)</option>
            </select>
        </div>
    </nav>

    <div class="container">

        <!-- DASHBOARD TAB (Person 4: Admin/HR Management Console) -->
        <div id="panel-dashboard" class="tab-panel active">
            <div class="header-row">
                <div>
                    <h1 class="header-title">Dayflow HRMS Management Console</h1>
                    <p class="header-sub">Live organizational metrics, pending approvals, and executive summary</p>
                </div>
                <div style="display:flex; gap:0.5rem;">
                    <button class="btn btn-primary" onclick="openTab('payroll')">💰 Salary Overview</button>
                    <button class="btn btn-secondary" onclick="resetData()">↺ Refresh</button>
                </div>
            </div>

            <!-- Hero KPI Cards -->
            <div class="kpi-grid">
                <div class="kpi-card kpi-blue" onclick="openTab('employees')">
                    <div class="kpi-icon-box">👥</div>
                    <div>
                        <div class="kpi-label">Total Employees</div>
                        <div class="kpi-val" id="dash-kpi-employees">0</div>
                        <div class="kpi-sub" style="color: #60a5fa;">View Directory →</div>
                    </div>
                </div>

                <div class="kpi-card kpi-green" onclick="openTab('attendance')">
                    <div class="kpi-icon-box">✓</div>
                    <div>
                        <div class="kpi-label">Present Today</div>
                        <div class="kpi-val" id="dash-kpi-present">0</div>
                        <div class="kpi-sub" style="color: #34d399;">View Attendance →</div>
                    </div>
                </div>

                <div class="kpi-card kpi-amber" onclick="openTab('leave')">
                    <div class="kpi-icon-box">📅</div>
                    <div>
                        <div class="kpi-label">On Leave Today</div>
                        <div class="kpi-val" id="dash-kpi-on-leave">0</div>
                        <div class="kpi-sub" style="color: #fbbf24;">View Time Off →</div>
                    </div>
                </div>

                <div class="kpi-card kpi-red" onclick="openTab('leave')">
                    <div class="kpi-icon-box">⏳</div>
                    <div>
                        <div class="kpi-label">Pending Requests</div>
                        <div class="kpi-val" id="dash-kpi-pending">0</div>
                        <div class="kpi-sub" style="color: #f87171;">Review Hub →</div>
                    </div>
                </div>
            </div>

            <!-- Section: Pending Leave Requests (Decision Hub) -->
            <div class="card">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 1rem;">
                    <div>
                        <h3 style="font-size: 1.05rem;">Pending Leave Requests (Decision Hub)</h3>
                        <p style="font-size: 0.78rem; color: var(--text-muted); margin-top: 2px;">Review and take immediate action on employee time off applications</p>
                    </div>
                    <span class="badge badge-amber" id="dash-badge-pending-count">0 Pending</span>
                </div>
                <div class="table-wrap">
                    <table>
                        <thead>
                            <tr>
                                <th>Employee</th>
                                <th>Category</th>
                                <th>Duration</th>
                                <th>Reason / Remarks</th>
                                <th style="text-align: right;">Action</th>
                            </tr>
                        </thead>
                        <tbody id="dash-tbl-pending-leaves"></tbody>
                    </table>
                </div>
            </div>

            <!-- 2-Column: Today's Attendance Summary & Employee Overview -->
            <div class="two-col-grid">
                <div class="card">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 0.9rem;">
                        <h3 style="font-size: 1.05rem;">Today's Attendance Overview</h3>
                        <span class="badge badge-green" id="dash-badge-present-count">0 Active</span>
                    </div>
                    <div class="table-wrap" style="max-height: 300px;">
                        <table>
                            <thead>
                                <tr>
                                    <th>Employee</th>
                                    <th>Check In</th>
                                    <th>Check Out</th>
                                    <th>Status</th>
                                </tr>
                            </thead>
                            <tbody id="dash-tbl-today-attendance"></tbody>
                        </table>
                    </div>
                </div>

                <div class="card">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 0.9rem;">
                        <h3 style="font-size: 1.05rem;">Employee Directory</h3>
                        <span class="badge badge-purple" id="dash-badge-total-emp">0 Total</span>
                    </div>
                    <div style="margin-bottom: 0.75rem;">
                        <input type="text" class="input" style="width: 100%; font-size: 0.8rem; padding: 0.4rem 0.6rem;" id="dash-search-emp" placeholder="Search by name, job, or department..." oninput="filterDashboardEmployees()">
                    </div>
                    <div class="table-wrap" style="max-height: 250px;">
                        <table>
                            <thead>
                                <tr>
                                    <th>Employee</th>
                                    <th>Role</th>
                                    <th>Joining</th>
                                </tr>
                            </thead>
                            <tbody id="dash-tbl-employees"></tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>

        <!-- ATTENDANCE TAB -->
        <div id="panel-attendance" class="tab-panel">
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

        <!-- PAYROLL TAB (Person 4: Salary Structure & Payroll Management) -->
        <div id="panel-payroll" class="tab-panel">
            <div class="header-row">
                <div>
                    <h1 class="header-title">Payroll & Salary Structure Management</h1>
                    <p class="header-sub">Manage base compensation, allowances, deductions, and salary disbursement</p>
                </div>
                <div id="admin-payroll-actions">
                    <button class="btn btn-primary" onclick="openSalaryModal(null)">+ Add Salary Record</button>
                </div>
            </div>

            <div class="stats-grid">
                <div class="stat-box">
                    <div class="metric-label">Total Monthly Payroll</div>
                    <div class="num" style="color: #60a5fa;" id="stat-payroll-total">₹0.00</div>
                </div>
                <div class="stat-box">
                    <div class="metric-label">Approved Records</div>
                    <div class="num" style="color: #34d399;" id="stat-payroll-approved">0</div>
                </div>
                <div class="stat-box">
                    <div class="metric-label">Paid Records</div>
                    <div class="num" style="color: #a78bfa;" id="stat-payroll-paid">0</div>
                </div>
                <div class="stat-box">
                    <div class="metric-label">Pending Drafts</div>
                    <div class="num" style="color: #fbbf24;" id="stat-payroll-draft">0</div>
                </div>
            </div>

            <div class="card">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 1rem;">
                    <h3 style="font-size: 1.05rem;">Employee Salary Structures & Compensation</h3>
                    <span id="payroll-rule-tag" style="font-size: 0.78rem; color: var(--text-muted);">Showing organizational payroll records</span>
                </div>
                <div class="table-wrap">
                    <table>
                        <thead>
                            <tr>
                                <th>Reference</th>
                                <th>Employee</th>
                                <th>Structure</th>
                                <th>Period</th>
                                <th style="text-align: right;">Base Salary</th>
                                <th style="text-align: right;">Allowances</th>
                                <th style="text-align: right;">Deductions</th>
                                <th style="text-align: right;">Net Salary</th>
                                <th style="text-align: center;">Status</th>
                                <th style="text-align: right;">Actions</th>
                            </tr>
                        </thead>
                        <tbody id="tbl-payroll"></tbody>
                    </table>
                </div>
            </div>
        </div>

    </div>

    <!-- Document File Preview Modal -->
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

    <!-- Edit Salary Modal (Person 4) -->
    <div id="salary-modal" class="modal" style="display: none;">
        <div class="modal-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <h3 style="font-size: 1.1rem;">Update Employee Salary Structure</h3>
                <button class="btn btn-secondary" onclick="closeSalaryModal()">✕</button>
            </div>
            <form onsubmit="handleSaveSalary(event)">
                <input type="hidden" id="modal-pay-id">
                <div class="form-row">
                    <div class="field">
                        <label>Employee Name</label>
                        <input type="text" id="modal-pay-emp" class="input" readonly>
                    </div>
                    <div class="field">
                        <label>Salary Structure Title</label>
                        <input type="text" id="modal-pay-struct" class="input" placeholder="e.g. Senior Technical">
                    </div>
                </div>
                <div class="form-row">
                    <div class="field">
                        <label>Base Salary (₹)</label>
                        <input type="number" id="modal-pay-base" class="input" oninput="calcModalNetSalary()" required>
                    </div>
                    <div class="field">
                        <label>Allowances (₹)</label>
                        <input type="number" id="modal-pay-allow" class="input" oninput="calcModalNetSalary()" required>
                    </div>
                    <div class="field">
                        <label>Deductions (₹)</label>
                        <input type="number" id="modal-pay-deduct" class="input" oninput="calcModalNetSalary()" required>
                    </div>
                </div>
                <div class="stat-box" style="background: var(--bg-card); margin-bottom: 1rem;">
                    <div class="metric-label">Calculated Net Salary (Base + Allowances - Deductions)</div>
                    <div class="num" style="color: #34d399;" id="modal-pay-net-preview">₹0.00</div>
                </div>
                <div style="display: flex; justify-content: flex-end; gap: 0.5rem;">
                    <button type="button" class="btn btn-secondary" onclick="closeSalaryModal()">Cancel</button>
                    <button type="submit" class="btn btn-primary">Save Salary Structure</button>
                </div>
            </form>
        </div>
    </div>

    <script>
        const DEFAULT_ATTENDANCE = [
            { id: 1, date: '2026-08-21', employee: 'John Doe', checkIn: '09:00 AM', checkOut: '05:30 PM', status: 'present', workedHours: 8.5, effectiveHours: 8.5, extraHours: 0.5 },
            { id: 2, date: '2026-08-20', employee: 'John Doe', checkIn: '08:50 AM', checkOut: '06:10 PM', status: 'present', workedHours: 9.3, effectiveHours: 9.3, extraHours: 1.3 },
            { id: 3, date: '2026-08-19', employee: 'John Doe', checkIn: '09:15 AM', checkOut: '01:00 PM', status: 'half_day', workedHours: 3.75, effectiveHours: 3.75, extraHours: 0.0 },
            { id: 4, date: '2026-08-22', employee: 'Jane Smith', checkIn: '09:05 AM', checkOut: '--', status: 'present', workedHours: 2.5, effectiveHours: 2.5, extraHours: 0.0 },
            { id: 5, date: '2026-08-22', employee: 'Robert Taylor', checkIn: '08:45 AM', checkOut: '--', status: 'present', workedHours: 2.8, effectiveHours: 2.8, extraHours: 0.0 }
        ];

        const DEFAULT_LEAVE = [
            { id: 101, employee: 'John Doe', type: 'sick', startDate: '2026-08-25', endDate: '2026-08-26', days: 2, remarks: 'Fever and rest recommended', status: 'pending', adminComments: '' },
            { id: 102, employee: 'Jane Smith', type: 'paid', startDate: '2026-08-28', endDate: '2026-08-30', days: 3, remarks: 'Family vacation', status: 'approved', adminComments: 'Approved by HR' },
            { id: 103, employee: 'Robert Taylor', type: 'paid', startDate: '2026-08-23', endDate: '2026-08-24', days: 2, remarks: 'Attending developer conference', status: 'pending', adminComments: '' }
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

        const DEFAULT_PAYROLL = [
            { id: 1, ref: 'PAY/2026/001', employee: 'John Doe', structure: 'Senior Technical', period: 'August 2026', base: 65000, allow: 12000, deduct: 4500, status: 'approved' },
            { id: 2, ref: 'PAY/2026/002', employee: 'Jane Smith', structure: 'HR Specialist Base', period: 'August 2026', base: 55000, allow: 8000, deduct: 3500, status: 'paid' },
            { id: 3, ref: 'PAY/2026/003', employee: 'Robert Taylor', structure: 'Product Lead', period: 'August 2026', base: 58000, allow: 9000, deduct: 3800, status: 'draft' }
        ];

        let state = {
            role: 'admin',
            currentEmployee: 'John Doe',
            isCheckedIn: false,
            activeCheckInTime: null,
            checkInTimestamp: null,
            tickerInterval: null,
            currentDocFilter: 'all',
            attendances: JSON.parse(localStorage.getItem('df_attendances')) || DEFAULT_ATTENDANCE,
            leaves: JSON.parse(localStorage.getItem('df_leaves')) || DEFAULT_LEAVE,
            employees: JSON.parse(localStorage.getItem('df_employees')) || DEFAULT_EMPLOYEES,
            documents: JSON.parse(localStorage.getItem('df_documents')) || DEFAULT_DOCUMENTS,
            payrolls: JSON.parse(localStorage.getItem('df_payrolls')) || DEFAULT_PAYROLL
        };

        function saveState() {
            localStorage.setItem('df_attendances', JSON.stringify(state.attendances));
            localStorage.setItem('df_leaves', JSON.stringify(state.leaves));
            localStorage.setItem('df_employees', JSON.stringify(state.employees));
            localStorage.setItem('df_documents', JSON.stringify(state.documents));
            localStorage.setItem('df_payrolls', JSON.stringify(state.payrolls));
        }

        function resetData() {
            localStorage.clear();
            state.attendances = JSON.parse(JSON.stringify(DEFAULT_ATTENDANCE));
            state.leaves = JSON.parse(JSON.stringify(DEFAULT_LEAVE));
            state.employees = JSON.parse(JSON.stringify(DEFAULT_EMPLOYEES));
            state.documents = JSON.parse(JSON.stringify(DEFAULT_DOCUMENTS));
            state.payrolls = JSON.parse(JSON.stringify(DEFAULT_PAYROLL));
            state.isCheckedIn = false;
            if (state.tickerInterval) clearInterval(state.tickerInterval);
            renderAll();
        }

        function formatCurrency(val) {
            return '₹' + Number(val || 0).toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
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

        /* Attendance actions */
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
            renderDashboard();
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
            renderDashboard();
        }

        /* Leave actions */
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
            renderDashboard();
            e.target.reset();
        }

        function handleApproveLeave(id) {
            const commentInput = document.getElementById('hr-leave-comment-' + id);
            const comment = commentInput ? commentInput.value : 'Approved by HR';
            const leave = state.leaves.find(l => l.id === id);
            if (leave) {
                leave.status = 'approved';
                leave.adminComments = comment || 'Approved by HR';
                saveState();
                renderAll();
            }
        }

        function handleRejectLeave(id) {
            const commentInput = document.getElementById('hr-leave-comment-' + id);
            const comment = commentInput ? commentInput.value : 'Rejected by HR';
            const leave = state.leaves.find(l => l.id === id);
            if (leave) {
                leave.status = 'rejected';
                leave.adminComments = comment || 'Rejected by HR';
                saveState();
                renderAll();
            }
        }

        /* Employee actions */
        function toggleEmpForm() {
            const card = document.getElementById('form-emp-card');
            card.style.display = card.style.display === 'none' ? 'block' : 'none';
        }

        function handleAddEmp(e) {
            e.preventDefault();
            const newEmp = {
                id: Date.now(),
                name: document.getElementById('emp-name').value,
                email: document.getElementById('emp-email').value,
                job: document.getElementById('emp-job').value,
                dept: document.getElementById('emp-dept').value,
                role: document.getElementById('emp-role').value,
                joining: document.getElementById('emp-joining').value,
                loginId: '',
                provisioned: false
            };
            state.employees.unshift(newEmp);

            // Also create an initial draft payroll entry for the new employee
            state.payrolls.push({
                id: Date.now(),
                ref: `PAY/2026/00${state.payrolls.length + 1}`,
                employee: newEmp.name,
                structure: 'Standard Base',
                period: 'August 2026',
                base: 45000,
                allow: 6000,
                deduct: 2500,
                status: 'draft'
            });

            saveState();
            renderAll();
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
                renderDashboard();
            }
        }

        /* Document actions */
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

        /* Payroll Modal & Actions (Person 4) */
        function openSalaryModal(payId) {
            const pay = state.payrolls.find(p => p.id === payId);
            if (pay) {
                document.getElementById('modal-pay-id').value = pay.id;
                document.getElementById('modal-pay-emp').value = pay.employee;
                document.getElementById('modal-pay-struct').value = pay.structure;
                document.getElementById('modal-pay-base').value = pay.base;
                document.getElementById('modal-pay-allow').value = pay.allow;
                document.getElementById('modal-pay-deduct').value = pay.deduct;
            } else {
                document.getElementById('modal-pay-id').value = '';
                document.getElementById('modal-pay-emp').value = state.employees[0]?.name || 'John Doe';
                document.getElementById('modal-pay-struct').value = 'Standard Base';
                document.getElementById('modal-pay-base').value = 50000;
                document.getElementById('modal-pay-allow').value = 7500;
                document.getElementById('modal-pay-deduct').value = 3000;
            }
            calcModalNetSalary();
            document.getElementById('salary-modal').style.display = 'flex';
        }

        function closeSalaryModal() {
            document.getElementById('salary-modal').style.display = 'none';
        }

        function calcModalNetSalary() {
            const base = parseFloat(document.getElementById('modal-pay-base').value) || 0;
            const allow = parseFloat(document.getElementById('modal-pay-allow').value) || 0;
            const deduct = parseFloat(document.getElementById('modal-pay-deduct').value) || 0;
            const net = base + allow - deduct;
            document.getElementById('modal-pay-net-preview').innerText = formatCurrency(net);
        }

        function handleSaveSalary(e) {
            e.preventDefault();
            const idVal = document.getElementById('modal-pay-id').value;
            const base = parseFloat(document.getElementById('modal-pay-base').value) || 0;
            const allow = parseFloat(document.getElementById('modal-pay-allow').value) || 0;
            const deduct = parseFloat(document.getElementById('modal-pay-deduct').value) || 0;
            const struct = document.getElementById('modal-pay-struct').value || 'Standard Base';

            if (idVal) {
                const pay = state.payrolls.find(p => p.id === parseInt(idVal));
                if (pay) {
                    pay.base = base;
                    pay.allow = allow;
                    pay.deduct = deduct;
                    pay.structure = struct;
                }
            } else {
                const emp = document.getElementById('modal-pay-emp').value;
                state.payrolls.push({
                    id: Date.now(),
                    ref: `PAY/2026/00${state.payrolls.length + 1}`,
                    employee: emp,
                    structure: struct,
                    period: 'August 2026',
                    base: base,
                    allow: allow,
                    deduct: deduct,
                    status: 'draft'
                });
            }

            saveState();
            closeSalaryModal();
            renderAll();
        }

        function handleApprovePayroll(id) {
            const pay = state.payrolls.find(p => p.id === id);
            if (pay) {
                pay.status = 'approved';
                saveState();
                renderPayroll();
                renderDashboard();
            }
        }

        function handlePayPayroll(id) {
            const pay = state.payrolls.find(p => p.id === id);
            if (pay) {
                pay.status = 'paid';
                saveState();
                renderPayroll();
                renderDashboard();
            }
        }

        /* Render Functions */
        function renderDashboard() {
            // Compute Live Metrics
            const totalEmp = state.employees.length;
            const presentToday = state.attendances.filter(a => a.status === 'present').length;
            const onLeave = state.leaves.filter(l => l.status === 'approved').length;
            const pendingLeaves = state.leaves.filter(l => l.status === 'pending');

            document.getElementById('dash-kpi-employees').innerText = totalEmp;
            document.getElementById('dash-kpi-present').innerText = presentToday;
            document.getElementById('dash-kpi-on-leave').innerText = onLeave;
            document.getElementById('dash-kpi-pending').innerText = pendingLeaves.length;
            document.getElementById('dash-badge-pending-count').innerText = `${pendingLeaves.length} Pending`;
            document.getElementById('dash-badge-present-count').innerText = `${presentToday} Active`;
            document.getElementById('dash-badge-total-emp').innerText = `${totalEmp} Total`;

            // Pending Leave Decisions Table
            const tbodyPending = document.getElementById('dash-tbl-pending-leaves');
            if (pendingLeaves.length === 0) {
                tbodyPending.innerHTML = `<tr><td colspan="5" style="text-align:center; color:var(--text-muted); padding:1.5rem;">🎉 No pending leave requests! All applications have been reviewed.</td></tr>`;
            } else {
                tbodyPending.innerHTML = pendingLeaves.map(l => `
                    <tr>
                        <td><strong>${l.employee}</strong></td>
                        <td><span class="badge badge-purple">${l.type.toUpperCase()}</span></td>
                        <td>${l.startDate} → ${l.endDate} (${l.days}d)</td>
                        <td style="color:var(--text-muted);">${l.remarks}</td>
                        <td style="text-align: right;">
                            <div style="display:inline-flex; gap:0.35rem;">
                                <button class="btn btn-success" style="padding:0.25rem 0.55rem; font-size:0.75rem;" onclick="handleApproveLeave(${l.id})">Approve</button>
                                <button class="btn btn-danger" style="padding:0.25rem 0.55rem; font-size:0.75rem;" onclick="handleRejectLeave(${l.id})">Reject</button>
                            </div>
                        </td>
                    </tr>
                `).join('');
            }

            // Today's Attendance Overview
            const tbodyAtt = document.getElementById('dash-tbl-today-attendance');
            tbodyAtt.innerHTML = state.attendances.slice(0, 5).map(a => `
                <tr>
                    <td><strong>${a.employee}</strong></td>
                    <td>${a.checkIn}</td>
                    <td>${a.checkOut}</td>
                    <td><span class="badge ${a.status==='present'?'badge-green':a.status==='half_day'?'badge-amber':'badge-red'}">${a.status.toUpperCase()}</span></td>
                </tr>
            `).join('');

            // Employee Directory Preview
            filterDashboardEmployees();
        }

        function filterDashboardEmployees() {
            const query = (document.getElementById('dash-search-emp')?.value || '').toLowerCase();
            const tbodyEmp = document.getElementById('dash-tbl-employees');
            const filtered = state.employees.filter(e => e.name.toLowerCase().includes(query) || e.job.toLowerCase().includes(query) || e.dept.toLowerCase().includes(query));

            tbodyEmp.innerHTML = filtered.map(e => `
                <tr>
                    <td>
                        <strong>${e.name}</strong>
                        <div style="font-size:0.75rem; color:var(--text-muted);">${e.job}</div>
                    </td>
                    <td><span class="badge badge-purple">${e.role}</span></td>
                    <td style="font-size:0.8rem; color:var(--text-muted);">${e.joining || '--'}</td>
                </tr>
            `).join('');
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

        function renderPayroll() {
            let data = state.payrolls;
            const tag = document.getElementById('payroll-rule-tag');
            const adminActions = document.getElementById('admin-payroll-actions');

            if (state.role === 'employee') {
                data = data.filter(p => p.employee === state.currentEmployee);
                if (tag) tag.innerText = 'Showing your personal salary structure (Record Rule Protected)';
                if (adminActions) adminActions.style.display = 'none';
            } else {
                if (tag) tag.innerText = 'Showing organizational payroll records (Admin HR Access)';
                if (adminActions) adminActions.style.display = 'block';
            }

            const totalNet = data.reduce((sum, p) => sum + (p.base + p.allow - p.deduct), 0);
            const approved = data.filter(p => p.status === 'approved').length;
            const paid = data.filter(p => p.status === 'paid').length;
            const draft = data.filter(p => p.status === 'draft').length;

            document.getElementById('stat-payroll-total').innerText = formatCurrency(totalNet);
            document.getElementById('stat-payroll-approved').innerText = approved;
            document.getElementById('stat-payroll-paid').innerText = paid;
            document.getElementById('stat-payroll-draft').innerText = draft;

            const tbody = document.getElementById('tbl-payroll');
            tbody.innerHTML = data.map(p => {
                const net = p.base + p.allow - p.deduct;
                const badgeClass = p.status === 'paid' ? 'badge-green' : p.status === 'approved' ? 'badge-blue' : 'badge-amber';
                let actions = '';

                if (state.role === 'admin') {
                    actions = `
                        <div style="display:flex; justify-content:flex-end; gap:0.3rem;">
                            <button class="btn btn-secondary" style="padding:0.2rem 0.5rem; font-size:0.75rem;" onclick="openSalaryModal(${p.id})">✎ Edit</button>
                            ${p.status === 'draft' ? `<button class="btn btn-primary" style="padding:0.2rem 0.5rem; font-size:0.75rem;" onclick="handleApprovePayroll(${p.id})">Approve</button>` : ''}
                            ${p.status === 'approved' ? `<button class="btn btn-success" style="padding:0.2rem 0.5rem; font-size:0.75rem;" onclick="handlePayPayroll(${p.id})">Pay</button>` : ''}
                        </div>
                    `;
                } else {
                    actions = `<span style="font-size:0.8rem; color:var(--text-muted);">View Only</span>`;
                }

                return `
                    <tr>
                        <td><strong style="color:var(--accent-purple-hover);">${p.ref}</strong></td>
                        <td><strong>${p.employee}</strong></td>
                        <td><span style="color:var(--text-muted); font-size:0.8rem;">${p.structure}</span></td>
                        <td><span class="badge badge-purple">${p.period}</span></td>
                        <td style="text-align: right;">${formatCurrency(p.base)}</td>
                        <td style="text-align: right; color:#34d399;">+ ${formatCurrency(p.allow)}</td>
                        <td style="text-align: right; color:#f87171;">- ${formatCurrency(p.deduct)}</td>
                        <td style="text-align: right; font-weight:700; color:#fff;">${formatCurrency(net)}</td>
                        <td style="text-align: center;"><span class="badge ${badgeClass}">${p.status.toUpperCase()}</span></td>
                        <td style="text-align: right;">${actions}</td>
                    </tr>
                `;
            }).join('');
        }

        function renderAll() {
            renderDashboard();
            renderAttendance();
            renderLeaves();
            renderEmployees();
            renderDocuments();
            renderPayroll();
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
    print(" Dayflow HRMS - Unified Live UI Preview Server")
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
