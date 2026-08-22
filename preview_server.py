# -*- coding: utf-8 -*-
"""
Dayflow HRMS - Interactive UI Live Preview Server
Renders the complete Dayflow HRMS interface (Attendance + Time Off + Admin Approval Workflow)
matching the exact Excalidraw wireframes and Odoo views.
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
            --accent-purple: #714B67; /* Odoo brand color */
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

        /* Top Navbar */
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
            cursor: pointer;
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

        /* Container */
        .container {
            max-width: 1280px;
            margin: 0 auto;
            padding: 1.5rem;
            width: 100%;
            flex: 1;
        }

        /* Header Title Row */
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

        .btn {
            padding: 0.5rem 1rem;
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

        .btn-primary {
            background-color: var(--accent-purple);
            color: white;
        }

        .btn-primary:hover {
            background-color: var(--accent-purple-hover);
        }

        .btn-success {
            background-color: var(--accent-green);
            color: white;
        }

        .btn-success:hover {
            filter: brightness(1.1);
        }

        .btn-danger {
            background-color: var(--accent-red);
            color: white;
        }

        .btn-danger:hover {
            filter: brightness(1.1);
        }

        .btn-secondary {
            background-color: var(--bg-input);
            color: var(--text-primary);
            border: 1px solid var(--border-color);
        }

        .btn-secondary:hover {
            background-color: #383e54;
        }

        /* Cards Grid */
        .cards-row {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 1rem;
            margin-bottom: 1.5rem;
        }

        .stat-card {
            background-color: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 1.25rem;
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }

        .stat-card-title {
            color: var(--text-secondary);
            font-size: 0.85rem;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .stat-card-val {
            font-size: 1.75rem;
            font-weight: 700;
            color: var(--text-primary);
        }

        .stat-card-desc {
            font-size: 0.8rem;
            color: var(--text-secondary);
        }

        /* Checkin Box */
        .checkin-banner {
            background: linear-gradient(135deg, #1e293b, #0f172a);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 1.25rem 1.5rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 1.5rem;
        }

        .checkin-info {
            display: flex;
            align-items: center;
            gap: 1.5rem;
        }

        .status-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background-color: var(--accent-green);
            box-shadow: 0 0 10px var(--accent-green);
        }

        /* Table */
        .table-container {
            background-color: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            overflow: hidden;
            margin-bottom: 1.5rem;
        }

        .table-header-bar {
            padding: 1rem 1.25rem;
            border-bottom: 1px solid var(--border-color);
            display: flex;
            justify-content: space-between;
            align-items: center;
            background-color: rgba(255, 255, 255, 0.02);
        }

        .table-title {
            font-weight: 600;
            font-size: 1rem;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            font-size: 0.9rem;
        }

        th {
            background-color: rgba(0, 0, 0, 0.2);
            color: var(--text-secondary);
            font-weight: 600;
            padding: 0.75rem 1rem;
            border-bottom: 1px solid var(--border-color);
        }

        td {
            padding: 0.85rem 1rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            color: var(--text-primary);
        }

        tr:hover td {
            background-color: rgba(255, 255, 255, 0.02);
        }

        /* Badges */
        .badge {
            padding: 0.25rem 0.65rem;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 600;
            display: inline-block;
        }

        .badge-success { background: rgba(16, 185, 129, 0.15); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.3); }
        .badge-warning { background: rgba(245, 158, 11, 0.15); color: #f59e0b; border: 1px solid rgba(245, 158, 11, 0.3); }
        .badge-danger { background: rgba(239, 68, 68, 0.15); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.3); }
        .badge-info { background: rgba(59, 130, 246, 0.15); color: #3b82f6; border: 1px solid rgba(59, 130, 246, 0.3); }

        /* Modal */
        .modal-backdrop {
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0, 0, 0, 0.7);
            display: none;
            justify-content: center;
            align-items: center;
            z-index: 100;
            backdrop-filter: blur(4px);
        }

        .modal {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            width: 100%;
            max-width: 500px;
            padding: 1.5rem;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
        }

        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.25rem;
        }

        .modal-title {
            font-size: 1.2rem;
            font-weight: 700;
        }

        .form-group {
            margin-bottom: 1rem;
        }

        .form-label {
            display: block;
            font-size: 0.85rem;
            font-weight: 500;
            color: var(--text-secondary);
            margin-bottom: 0.4rem;
        }

        .form-control {
            width: 100%;
            padding: 0.6rem 0.8rem;
            background: var(--bg-input);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            color: var(--text-primary);
            font-size: 0.9rem;
            outline: none;
        }

        .form-control:focus {
            border-color: var(--accent-purple);
        }

        .modal-footer {
            display: flex;
            justify-content: flex-end;
            gap: 0.75rem;
            margin-top: 1.5rem;
        }

        /* Weekly View Grid */
        .week-grid {
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 0.5rem;
            margin-top: 1rem;
        }

        .day-box {
            background: var(--bg-input);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            padding: 0.75rem;
            text-align: center;
        }

        .day-name {
            font-size: 0.8rem;
            color: var(--text-secondary);
            font-weight: 600;
        }

        .day-date {
            font-size: 1.1rem;
            font-weight: 700;
            margin: 0.35rem 0;
        }

        .hidden { display: none !important; }
    </style>
</head>
<body>

    <!-- TOP NAVBAR -->
    <nav class="navbar">
        <a href="#" class="navbar-brand">
            <div class="navbar-logo">DF</div>
            <span>Dayflow HRMS</span>
        </a>
        <ul class="navbar-nav">
            <li class="nav-item" onclick="switchTab('employees')">Employees</li>
            <li class="nav-item active" onclick="switchTab('attendance')">Attendance</li>
            <li class="nav-item" onclick="switchTab('timeoff')">Time Off</li>
            <li class="nav-item" onclick="switchTab('payroll')">Payroll</li>
            <li class="nav-item" onclick="switchTab('documents')">Documents</li>
        </ul>
        <div class="nav-right">
            <div class="role-badge">
                <span>Role:</span>
                <select id="roleSelector" onchange="toggleRole(this.value)">
                    <option value="employee">Employee (John Doe)</option>
                    <option value="admin">Admin / HR Officer</option>
                </select>
            </div>
        </div>
    </nav>

    <!-- MAIN CONTAINER -->
    <div class="container">

        <!-- ================= ATTENDANCE SECTION ================= -->
        <section id="section-attendance">
            <div class="page-header">
                <div>
                    <h1 class="page-title">Attendance Tracking</h1>
                    <p style="color: var(--text-secondary); font-size: 0.875rem;">Daily logs, check-in/out, and working hours calculation</p>
                </div>
                <div style="display: flex; gap: 0.5rem;">
                    <button class="btn btn-secondary" onclick="toggleAttendanceView('daily')">Daily View</button>
                    <button class="btn btn-secondary" onclick="toggleAttendanceView('weekly')">Weekly View</button>
                </div>
            </div>

            <!-- Checkin Banner (for Employee) -->
            <div class="checkin-banner" id="employeeCheckinBanner">
                <div class="checkin-info">
                    <div class="status-dot" id="statusDot"></div>
                    <div>
                        <div style="font-size: 0.8rem; color: var(--text-secondary);">Today's Status</div>
                        <div style="font-size: 1.1rem; font-weight: 700;" id="todayStatusText">Present (Checked In)</div>
                    </div>
                    <div style="border-left: 1px solid var(--border-color); padding-left: 1.5rem;">
                        <div style="font-size: 0.8rem; color: var(--text-secondary);">Check In Time</div>
                        <div style="font-size: 1rem; font-weight: 600;" id="checkinTimeText">09:00 AM</div>
                    </div>
                    <div style="border-left: 1px solid var(--border-color); padding-left: 1.5rem;">
                        <div style="font-size: 0.8rem; color: var(--text-secondary);">Working Hours</div>
                        <div style="font-size: 1rem; font-weight: 600; color: #10b981;" id="workedHoursText">4h 15m</div>
                    </div>
                </div>
                <div style="display: flex; gap: 0.75rem;">
                    <button class="btn btn-success" id="btnCheckIn" onclick="handleCheckIn()">Check In</button>
                    <button class="btn btn-danger" id="btnCheckOut" onclick="handleCheckOut()">Check Out</button>
                </div>
            </div>

            <!-- Weekly View Container -->
            <div class="table-container hidden" id="weeklyViewBox" style="padding: 1.25rem;">
                <div class="table-title" style="margin-bottom: 0.75rem;">Weekly Attendance Overview (Oct 13 - Oct 19, 2025)</div>
                <div class="week-grid">
                    <div class="day-box">
                        <div class="day-name">Mon</div>
                        <div class="day-date">13</div>
                        <span class="badge badge-success">Present (8.5h)</span>
                    </div>
                    <div class="day-box">
                        <div class="day-name">Tue</div>
                        <div class="day-date">14</div>
                        <span class="badge badge-success">Present (8.0h)</span>
                    </div>
                    <div class="day-box">
                        <div class="day-name">Wed</div>
                        <div class="day-date">15</div>
                        <span class="badge badge-info">Leave (Paid)</span>
                    </div>
                    <div class="day-box">
                        <div class="day-name">Thu</div>
                        <div class="day-date">16</div>
                        <span class="badge badge-warning">Half-day (3.5h)</span>
                    </div>
                    <div class="day-box">
                        <div class="day-name">Fri</div>
                        <div class="day-date">17</div>
                        <span class="badge badge-success">Present (9.0h)</span>
                    </div>
                    <div class="day-box">
                        <div class="day-name">Sat</div>
                        <div class="day-date">18</div>
                        <span class="badge" style="color: var(--text-secondary);">Weekend</span>
                    </div>
                    <div class="day-box">
                        <div class="day-name">Sun</div>
                        <div class="day-date">19</div>
                        <span class="badge" style="color: var(--text-secondary);">Weekend</span>
                    </div>
                </div>
            </div>

            <!-- Attendance History Table -->
            <div class="table-container" id="dailyViewBox">
                <div class="table-header-bar">
                    <div class="table-title">Attendance Log &amp; Working Hours</div>
                    <div style="font-size: 0.85rem; color: var(--text-secondary);" id="attendanceSubtext">Showing personal attendance logs</div>
                </div>
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
                    <tbody id="attendanceTableBody">
                        <!-- Rendered by JS -->
                    </tbody>
                </table>
            </div>
        </section>

        <!-- ================= TIME OFF / LEAVE SECTION ================= -->
        <section id="section-timeoff" class="hidden">
            <div class="page-header">
                <div>
                    <h1 class="page-title">Time Off &amp; Leave Management</h1>
                    <p style="color: var(--text-secondary); font-size: 0.875rem;">Apply for leave and manage employee time-off approval requests</p>
                </div>
                <div>
                    <button class="btn btn-primary" onclick="openLeaveModal()">+ Apply for Time Off</button>
                </div>
            </div>

            <!-- Balance Cards Row -->
            <div class="cards-row">
                <div class="stat-card">
                    <div class="stat-card-title">Paid Time Off</div>
                    <div class="stat-card-val" style="color: #10b981;">24 Days</div>
                    <div class="stat-card-desc">Annual &amp; Casual Leave available</div>
                </div>
                <div class="stat-card">
                    <div class="stat-card-title">Sick Leave</div>
                    <div class="stat-card-val" style="color: #3b82f6;">19 Days</div>
                    <div class="stat-card-desc">Medical certificate required &gt; 2 days</div>
                </div>
                <div class="stat-card">
                    <div class="stat-card-title">Unpaid Leaves</div>
                    <div class="stat-card-val" style="color: #f59e0b;">Available</div>
                    <div class="stat-card-desc">Subject to HR / Admin approval</div>
                </div>
            </div>

            <!-- Time Off Requests Table -->
            <div class="table-container">
                <div class="table-header-bar">
                    <div class="table-title">Time Off Applications</div>
                    <div style="font-size: 0.85rem; color: var(--text-secondary);">Review approval statuses and admin remarks</div>
                </div>
                <table>
                    <thead>
                        <tr>
                            <th>Employee</th>
                            <th>Leave Type</th>
                            <th>Start Date</th>
                            <th>End Date</th>
                            <th>Allocation</th>
                            <th>Status</th>
                            <th>Reason / Remarks</th>
                            <th>HR Comments</th>
                            <th id="actionsHeader">Actions</th>
                        </tr>
                    </thead>
                    <tbody id="leaveTableBody">
                        <!-- Rendered by JS -->
                    </tbody>
                </table>
            </div>
        </section>

        <!-- Other Sections Placeholder -->
        <section id="section-employees" class="hidden">
            <div class="page-header">
                <h1 class="page-title">Employee Directory (Person 2 Domain)</h1>
            </div>
            <div class="stat-card">
                <p>Employee Profile Management, Onboarding, Documents, and Personal Information owned by Person 2.</p>
            </div>
        </section>

        <section id="section-payroll" class="hidden">
            <div class="page-header">
                <h1 class="page-title">Payroll &amp; Salary Structure (Person 4 Domain)</h1>
            </div>
            <div class="stat-card">
                <p>Organization Salary Calculation, Base Wage, Allowances, Deductions, and Net Pay owned by Person 4.</p>
            </div>
        </section>

        <section id="section-documents" class="hidden">
            <div class="page-header">
                <h1 class="page-title">Verification Documents (Person 2 Domain)</h1>
            </div>
            <div class="stat-card">
                <p>File Uploads, ID Proofs, Certificates, and Document Archival owned by Person 2.</p>
            </div>
        </section>

    </div>

    <!-- TIME OFF APPLICATION MODAL (Matching Wireframe 4) -->
    <div class="modal-backdrop" id="leaveModal">
        <div class="modal">
            <div class="modal-header">
                <div class="modal-title">Time Off Type Request</div>
                <span style="cursor: pointer; font-size: 1.25rem;" onclick="closeLeaveModal()">&times;</span>
            </div>
            <div class="form-group">
                <label class="form-label">Employee</label>
                <input type="text" class="form-control" value="John Doe (EMP001)" readonly>
            </div>
            <div class="form-group">
                <label class="form-label">Time Off Type</label>
                <select class="form-control" id="leaveTypeInput">
                    <option value="Paid Time Off">Paid Time Off</option>
                    <option value="Sick Leave">Sick Leave</option>
                    <option value="Unpaid Leaves">Unpaid Leaves</option>
                </select>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem;">
                <div class="form-group">
                    <label class="form-label">Start Date</label>
                    <input type="date" class="form-control" id="startDateInput" value="2025-10-22">
                </div>
                <div class="form-group">
                    <label class="form-label">End Date</label>
                    <input type="date" class="form-control" id="endDateInput" value="2025-10-23">
                </div>
            </div>
            <div class="form-group">
                <label class="form-label">Allocation (Days)</label>
                <input type="number" class="form-control" id="allocationDaysInput" value="2" min="1">
            </div>
            <div class="form-group" style="display: flex; align-items: center; gap: 0.5rem; margin-top: 0.5rem;">
                <input type="checkbox" id="attachmentInput" style="width: 16px; height: 16px;">
                <label for="attachmentInput" class="form-label" style="margin-bottom: 0;">Medical Certificate / Document Attached (For Sick Leave)</label>
            </div>
            <div class="form-group">
                <label class="form-label">Remarks / Reason</label>
                <textarea class="form-control" id="remarksInput" rows="2" placeholder="Family event / Medical recovery..."></textarea>
            </div>
            <div class="modal-footer">
                <button class="btn btn-secondary" onclick="closeLeaveModal()">Discard</button>
                <button class="btn btn-primary" onclick="submitLeaveRequest()">Submit Application</button>
            </div>
        </div>
    </div>

    <!-- JAVASCRIPT STATE & LOGIC -->
    <script>
        let currentRole = 'employee'; // 'employee' or 'admin'

        // Sample Attendance Data
        let attendances = [
            { id: 1, date: '2025-10-22', employee: 'John Doe', checkIn: '09:00 AM', checkOut: '--', status: 'Present', worked: '4.2h', effective: '4.2h', extra: '0.0h' },
            { id: 2, date: '2025-10-21', employee: 'John Doe', checkIn: '08:50 AM', checkOut: '06:10 PM', status: 'Present', worked: '9.3h', effective: '9.3h', extra: '1.3h' },
            { id: 3, date: '2025-10-20', employee: 'John Doe', checkIn: '09:15 AM', checkOut: '01:00 PM', status: 'Half-day', worked: '3.7h', effective: '3.7h', extra: '0.0h' },
            { id: 4, date: '2025-10-19', employee: 'Parzival', checkIn: '09:05 AM', checkOut: '05:30 PM', status: 'Present', worked: '8.4h', effective: '8.4h', extra: '0.4h' },
            { id: 5, date: '2025-10-18', employee: 'Subhadeep Mistry', checkIn: '--', checkOut: '--', status: 'Leave', worked: '0.0h', effective: '0.0h', extra: '0.0h' }
        ];

        // Sample Leave Requests
        let leaveRequests = [
            { id: 101, employee: 'John Doe', type: 'Paid Time Off', start: '2025-10-25', end: '2025-10-26', days: 2, status: 'Pending', remarks: 'Attending family wedding', adminComment: '' },
            { id: 102, employee: 'John Doe', type: 'Sick Leave', start: '2025-10-10', end: '2025-10-10', days: 1, status: 'Approved', remarks: 'Flu recovery', adminComment: 'Get well soon. Approved.' },
            { id: 103, employee: 'Parzival', type: 'Unpaid Leaves', start: '2025-10-28', end: '2025-10-29', days: 2, status: 'Pending', remarks: 'Personal project work', adminComment: '' },
            { id: 104, employee: 'Subhadeep Mistry', type: 'Paid Time Off', start: '2025-10-18', end: '2025-10-18', days: 1, status: 'Approved', remarks: 'Personal errand', adminComment: 'Approved by HR.' }
        ];

        function renderAttendanceTable() {
            const tbody = document.getElementById('attendanceTableBody');
            tbody.innerHTML = '';

            let list = attendances;
            if (currentRole === 'employee') {
                list = attendances.filter(a => a.employee === 'John Doe');
                document.getElementById('attendanceSubtext').innerText = 'Showing your personal attendance logs (Record Rule Protected)';
            } else {
                document.getElementById('attendanceSubtext').innerText = 'Admin / HR Overview: Viewing all organization attendance logs';
            }

            list.forEach(item => {
                let badgeClass = 'badge-success';
                if (item.status === 'Half-day') badgeClass = 'badge-warning';
                if (item.status === 'Absent') badgeClass = 'badge-danger';
                if (item.status === 'Leave') badgeClass = 'badge-info';

                tbody.innerHTML += `
                    <tr>
                        <td><strong>${item.date}</strong></td>
                        <td>${item.employee}</td>
                        <td>${item.checkIn}</td>
                        <td>${item.checkOut}</td>
                        <td><span class="badge ${badgeClass}">${item.status}</span></td>
                        <td>${item.worked}</td>
                        <td>${item.effective}</td>
                        <td style="color: ${parseFloat(item.extra) > 0 ? '#10b981' : 'inherit'}">${item.extra}</td>
                    </tr>
                `;
            });
        }

        function renderLeaveTable() {
            const tbody = document.getElementById('leaveTableBody');
            tbody.innerHTML = '';

            let list = leaveRequests;
            if (currentRole === 'employee') {
                list = leaveRequests.filter(l => l.employee === 'John Doe');
            }

            list.forEach(req => {
                let badgeClass = 'badge-warning';
                if (req.status === 'Approved') badgeClass = 'badge-success';
                if (req.status === 'Rejected') badgeClass = 'badge-danger';

                let actionHtml = '--';
                if (currentRole === 'admin' && req.status === 'Pending') {
                    actionHtml = `
                        <div style="display: flex; gap: 0.35rem;">
                            <button class="btn btn-success" style="padding: 0.25rem 0.5rem; font-size: 0.75rem;" onclick="approveLeave(${req.id})">Approve</button>
                            <button class="btn btn-danger" style="padding: 0.25rem 0.5rem; font-size: 0.75rem;" onclick="rejectLeave(${req.id})">Reject</button>
                        </div>
                    `;
                } else if (req.status === 'Approved') {
                    actionHtml = '<span style="color: #10b981; font-size: 0.8rem; font-weight: 600;">✓ Synced to Attendance</span>';
                }

                tbody.innerHTML += `
                    <tr>
                        <td><strong>${req.employee}</strong></td>
                        <td>${req.type}</td>
                        <td>${req.start}</td>
                        <td>${req.end}</td>
                        <td>${req.days} Day(s)</td>
                        <td><span class="badge ${badgeClass}">${req.status}</span></td>
                        <td>${req.remarks || '--'}</td>
                        <td style="color: var(--text-secondary);">${req.adminComment || '--'}</td>
                        <td>${actionHtml}</td>
                    </tr>
                `;
            });
        }

        function toggleRole(role) {
            currentRole = role;
            if (role === 'admin') {
                document.getElementById('employeeCheckinBanner').classList.add('hidden');
            } else {
                document.getElementById('employeeCheckinBanner').classList.remove('hidden');
            }
            renderAttendanceTable();
            renderLeaveTable();
        }

        function switchTab(tabName) {
            document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
            event.target.classList.add('active');

            ['attendance', 'timeoff', 'employees', 'payroll', 'documents'].forEach(t => {
                const sec = document.getElementById('section-' + t);
                if (sec) sec.classList.add('hidden');
            });

            const activeSec = document.getElementById('section-' + tabName);
            if (activeSec) activeSec.classList.remove('hidden');
        }

        function toggleAttendanceView(view) {
            if (view === 'weekly') {
                document.getElementById('weeklyViewBox').classList.remove('hidden');
                document.getElementById('dailyViewBox').classList.add('hidden');
            } else {
                document.getElementById('weeklyViewBox').classList.add('hidden');
                document.getElementById('dailyViewBox').classList.remove('hidden');
            }
        }

        function handleCheckIn() {
            alert('Check-in recorded! Timestamp saved to Attendance log.');
            attendances.unshift({
                id: Date.now(),
                date: new Date().toISOString().split('T')[0],
                employee: 'John Doe',
                checkIn: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
                checkOut: '--',
                status: 'Present',
                worked: '0.0h',
                effective: '0.0h',
                extra: '0.0h'
            });
            renderAttendanceTable();
        }

        function handleCheckOut() {
            alert('Check-out recorded! Working hours calculated.');
            if (attendances[0] && attendances[0].checkOut === '--') {
                attendances[0].checkOut = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
                attendances[0].worked = '8.2h';
                attendances[0].effective = '8.2h';
                attendances[0].extra = '0.2h';
            }
            renderAttendanceTable();
        }

        function openLeaveModal() {
            document.getElementById('leaveModal').style.display = 'flex';
        }

        function closeLeaveModal() {
            document.getElementById('leaveModal').style.display = 'none';
        }

        function submitLeaveRequest() {
            const type = document.getElementById('leaveTypeInput').value;
            const start = document.getElementById('startDateInput').value;
            const end = document.getElementById('endDateInput').value;
            const days = document.getElementById('allocationDaysInput').value;
            const remarks = document.getElementById('remarksInput').value;

            leaveRequests.unshift({
                id: Date.now(),
                employee: 'John Doe',
                type: type,
                start: start,
                end: end,
                days: parseFloat(days),
                status: 'Pending',
                remarks: remarks,
                adminComment: ''
            });

            closeLeaveModal();
            renderLeaveTable();
            alert('Time off application submitted with status: Pending. Awaiting HR approval.');
        }

        function approveLeave(id) {
            const req = leaveRequests.find(l => l.id === id);
            if (req) {
                req.status = 'Approved';
                req.adminComment = 'Approved by HR Manager.';

                // Integrate with Attendance! Add record with status = 'Leave'
                attendances.unshift({
                    id: Date.now(),
                    date: req.start,
                    employee: req.employee,
                    checkIn: '09:00 AM',
                    checkOut: '05:00 PM',
                    status: 'Leave',
                    worked: '0.0h',
                    effective: '0.0h',
                    extra: '0.0h'
                });

                renderLeaveTable();
                renderAttendanceTable();
                alert(`Approved leave for ${req.employee}. Attendance for ${req.start} automatically updated with status: Leave!`);
            }
        }

        function rejectLeave(id) {
            const comment = prompt('Enter HR rejection comment:', 'Operational requirements during project deadline.');
            const req = leaveRequests.find(l => l.id === id);
            if (req) {
                req.status = 'Rejected';
                req.adminComment = comment || 'Rejected by HR.';
                renderLeaveTable();
            }
        }

        // Initial render
        renderAttendanceTable();
        renderLeaveTable();
    </script>
</body>
</html>
"""

class PreviewHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(HTML_CONTENT.encode('utf-8'))

def run_server():
    port = 8069
    server = HTTPServer(('127.0.0.1', port), PreviewHandler)
    print(f"==================================================")
    print(f" Dayflow HRMS Live Preview Server Running at:")
    print(f" http://localhost:{port}")
    print(f" Open this link in your browser to view the UI!")
    print(f"==================================================")
    server.serve_forever()

if __name__ == '__main__':
    run_server()
