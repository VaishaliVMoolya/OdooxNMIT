# -*- coding: utf-8 -*-
"""
Dayflow HRMS — 100% Wireframe Aligned Live Preview Server
Implements Wireframes 1 - 6:
- Wireframe 1: Sign In & Sign Up Modals + Auto Login ID Formula (OIJODO20260001)
- Wireframe 2: Systray Check-In Widget + Avatar Dropdown + Employee Cards with Status Dots
- Wireframes 3 & 4: My Profile Modal + Private Info + Admin-only Salary Info Breakdown
- Wireframe 5: Dual-Mode Attendance Views (Employee Metrics vs Admin Searchbar)
- Wireframe 6: Time Off Calendar View + Request Modal with Medical Certificate Upload + HR Approval
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

        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', system-ui, sans-serif; }
        body { background-color: var(--bg-body); color: var(--text-main); min-height: 100vh; display: flex; flex-direction: column; }

        /* Top Navbar */
        .navbar {
            background-color: var(--bg-surface);
            border-bottom: 1px solid var(--border-line);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0.6rem 1.5rem;
            position: sticky; top: 0; z-index: 50;
        }

        .brand { display: flex; align-items: center; gap: 0.6rem; font-weight: 700; font-size: 1.15rem; color: #fff; text-decoration: none; }
        .brand-badge { background: linear-gradient(135deg, var(--accent-purple), #8b5cf6); color: #fff; padding: 0.25rem 0.55rem; border-radius: 6px; font-size: 0.85rem; font-weight: 800; }

        .nav-links { display: flex; gap: 0.35rem; list-style: none; }
        .nav-tab { padding: 0.45rem 0.9rem; border-radius: 6px; color: var(--text-muted); font-size: 0.875rem; font-weight: 500; cursor: pointer; transition: all 0.15s ease; }
        .nav-tab:hover { color: var(--text-main); background-color: rgba(255, 255, 255, 0.04); }
        .nav-tab.active { color: #fff; background-color: var(--accent-purple); }

        /* Systray Widgets */
        .systray { display: flex; align-items: center; gap: 1rem; }

        .systray-checkin {
            background-color: var(--bg-input);
            border: 1px solid var(--border-line);
            padding: 0.35rem 0.85rem;
            border-radius: 20px;
            display: flex;
            align-items: center;
            gap: 0.6rem;
            font-size: 0.8rem;
        }

        .systray-dot { width: 9px; height: 9px; border-radius: 50%; background-color: var(--accent-red); }
        .systray-dot.green { background-color: var(--accent-green); box-shadow: 0 0 8px var(--accent-green); }

        .avatar-menu { position: relative; cursor: pointer; }
        .avatar-circle {
            width: 36px; height: 36px; border-radius: 50%;
            background: linear-gradient(135deg, var(--accent-purple), var(--accent-blue));
            display: flex; align-items: center; justify-content: center;
            font-weight: 700; color: #fff; font-size: 0.9rem;
            border: 2px solid var(--border-line);
        }

        .dropdown-box {
            position: absolute; right: 0; top: 44px;
            background-color: var(--bg-surface);
            border: 1px solid var(--border-line);
            border-radius: 8px; width: 160px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5);
            display: none; flex-direction: column; overflow: hidden; z-index: 60;
        }
        .dropdown-item { padding: 0.65rem 1rem; font-size: 0.85rem; color: var(--text-main); cursor: pointer; }
        .dropdown-item:hover { background-color: var(--bg-card); }

        /* Container Layout */
        .container { max-width: 1200px; margin: 0 auto; padding: 1.5rem; width: 100%; flex: 1; }
        .header-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem; }
        .header-title { font-size: 1.35rem; font-weight: 700; }

        .card { background-color: var(--bg-surface); border: 1px solid var(--border-line); border-radius: 10px; padding: 1.25rem 1.5rem; margin-bottom: 1.25rem; }

        /* Buttons */
        .btn { padding: 0.45rem 1.1rem; border-radius: 6px; border: none; font-weight: 600; font-size: 0.85rem; cursor: pointer; transition: all 0.15s ease; display: inline-flex; align-items: center; gap: 0.4rem; }
        .btn:disabled { opacity: 0.4; cursor: not-allowed; }
        .btn-primary { background-color: var(--accent-purple); color: #fff; }
        .btn-primary:hover:not(:disabled) { background-color: var(--accent-purple-hover); }
        .btn-success { background-color: var(--accent-green); color: #fff; }
        .btn-danger { background-color: var(--accent-red); color: #fff; }
        .btn-secondary { background-color: var(--bg-input); color: var(--text-main); border: 1px solid var(--border-line); }

        /* Metrics Grid */
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 1.25rem; }
        .stat-box { background-color: var(--bg-card); border: 1px solid var(--border-line); padding: 1rem 1.25rem; border-radius: 8px; }
        .stat-box .num { font-size: 1.5rem; font-weight: 700; margin-top: 0.25rem; }

        /* Employee Cards Grid (Wireframe 2) */
        .emp-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1rem; }
        .emp-card {
            background-color: var(--bg-card);
            border: 1px solid var(--border-line);
            border-radius: 8px; padding: 1.1rem;
            display: flex; flex-direction: column; gap: 0.6rem;
            position: relative; cursor: pointer; transition: all 0.15s ease;
        }
        .emp-card:hover { border-color: var(--accent-purple); transform: translateY(-2px); }

        .emp-status-dot { position: absolute; top: 12px; right: 12px; font-size: 0.8rem; }
        .dot-green { color: #34d399; }
        .dot-yellow { color: #fbbf24; }
        .dot-airplane { color: #60a5fa; }

        .emp-head { display: flex; align-items: center; gap: 0.85rem; }
        .emp-name { font-size: 1rem; font-weight: 700; }
        .emp-job { font-size: 0.78rem; color: var(--text-muted); }

        /* Tables */
        .table-wrap { width: 100%; overflow-x: auto; }
        table { width: 100%; border-collapse: collapse; text-align: left; font-size: 0.875rem; }
        th { background-color: var(--bg-card); color: var(--text-muted); padding: 0.65rem 0.9rem; font-weight: 600; border-bottom: 1px solid var(--border-line); font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.5px; }
        td { padding: 0.75rem 0.9rem; border-bottom: 1px solid rgba(45, 51, 69, 0.6); }
        tr:hover td { background-color: rgba(255, 255, 255, 0.015); }

        /* Badges */
        .badge { display: inline-flex; align-items: center; padding: 0.2rem 0.55rem; border-radius: 12px; font-size: 0.73rem; font-weight: 600; }
        .badge-green { background-color: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); }
        .badge-amber { background-color: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3); }
        .badge-red { background-color: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); }
        .badge-purple { background-color: rgba(113, 75, 103, 0.3); color: #e9d5ff; border: 1px solid rgba(113, 75, 103, 0.5); }

        /* Forms */
        .form-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1rem; margin-bottom: 1rem; }
        .field { display: flex; flex-direction: column; gap: 0.35rem; }
        .field label { font-size: 0.8rem; font-weight: 600; color: var(--text-muted); }
        .input { background-color: var(--bg-input); border: 1px solid var(--border-line); color: var(--text-main); padding: 0.55rem 0.75rem; border-radius: 6px; font-size: 0.875rem; outline: none; }
        .input:focus { border-color: var(--accent-purple); }

        /* Calendar Wireframe 6 */
        .calendar-grid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 0.4rem; margin-top: 1rem; }
        .cal-day { background-color: var(--bg-card); border: 1px solid var(--border-line); min-height: 70px; padding: 0.4rem; border-radius: 6px; font-size: 0.8rem; }
        .cal-day.leave-day { border-color: var(--accent-purple); background-color: rgba(113, 75, 103, 0.2); }

        /* Modal */
        .modal { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background-color: rgba(0, 0, 0, 0.8); display: flex; align-items: center; justify-content: center; z-index: 100; }
        .modal-card { background-color: var(--bg-surface); border: 1px solid var(--border-line); border-radius: 10px; max-width: 750px; width: 90%; padding: 1.5rem; max-height: 88vh; overflow-y: auto; }

        .subtabs { display: flex; gap: 0.5rem; border-bottom: 1px solid var(--border-line); margin-bottom: 1rem; }
        .subtab { padding: 0.5rem 1rem; font-size: 0.85rem; font-weight: 600; color: var(--text-muted); cursor: pointer; border-bottom: 2px solid transparent; }
        .subtab.active { color: var(--text-main); border-bottom-color: var(--accent-purple); }

        .tab-panel { display: none; }
        .tab-panel.active { display: block; }
    </style>
</head>
<body>

    <!-- Top Navbar with Systray (Wireframe 2) -->
    <nav class="navbar">
        <a href="#" class="brand">
            <span class="brand-badge">DF</span> Dayflow HRMS
        </a>
        <ul class="nav-links">
            <li class="nav-tab active" id="tab-btn-employees" onclick="openTab('employees')">Employees</li>
            <li class="nav-tab" id="tab-btn-attendance" onclick="openTab('attendance')">Attendance</li>
            <li class="nav-tab" id="tab-btn-leave" onclick="openTab('leave')">Time Off</li>
            <li class="nav-tab" id="tab-btn-documents" onclick="openTab('documents')">Documents</li>
            <li class="nav-tab" id="tab-btn-payroll" onclick="openTab('payroll')">Payroll</li>
        </ul>
        <div class="systray">
            <!-- Systray Check-In Widget -->
            <div class="systray-checkin">
                <span id="systray-dot" class="systray-dot"></span>
                <span id="systray-status">Check IN -&gt;</span>
                <button id="btn-systray-toggle" class="btn btn-primary" style="padding: 0.2rem 0.6rem; font-size: 0.75rem;" onclick="toggleSystrayCheckIn()">Check IN</button>
            </div>

            <!-- Avatar Dropdown (Wireframe 2) -->
            <div class="avatar-menu" onclick="toggleAvatarDropdown()">
                <div class="avatar-circle" id="user-avatar-initials">JD</div>
                <div class="dropdown-box" id="avatar-dropdown">
                    <div class="dropdown-item" onclick="openMyProfileModal()">👤 My Profile</div>
                    <div class="dropdown-item" onclick="toggleAuthModal()">🔒 Sign In / Up</div>
                    <div class="dropdown-item" style="color: var(--accent-red);" onclick="resetData()">↺ Reset State</div>
                </div>
            </div>
        </div>
    </nav>

    <div class="container">

        <!-- EMPLOYEES TAB (Wireframe 2) -->
        <div id="panel-employees" class="tab-panel active">
            <div class="header-row">
                <h1 class="header-title">Employee Directory</h1>
                <div style="display:flex; gap:0.5rem; align-items:center;">
                    <select id="user-role-select" class="input" style="padding:0.3rem 0.6rem; font-size:0.8rem;" onchange="onRoleChange(this.value)">
                        <option value="employee">Role: Standard Employee</option>
                        <option value="admin">Role: HR / Admin Manager</option>
                    </select>
                    <button class="btn btn-primary" onclick="toggleEmpForm()">+ Add Employee</button>
                </div>
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
                            <label>Joining Date</label>
                            <input type="date" id="emp-joining" class="input" required>
                        </div>
                    </div>
                    <button type="submit" class="btn btn-success">Save Profile</button>
                </form>
            </div>

            <!-- Employee Cards Grid with Status Indicators (Wireframe 2) -->
            <div class="emp-grid" id="grid-employees"></div>
        </div>

        <!-- ATTENDANCE TAB (Wireframe 5) -->
        <div id="panel-attendance" class="tab-panel">
            <div class="header-row">
                <h1 class="header-title">Attendance Tracking</h1>
                <div id="admin-att-search" style="display:none;">
                    <input type="text" class="input" placeholder="Search employee..." onkeyup="filterAttTable(this.value)">
                </div>
            </div>

            <!-- Employee Summary Metric Cards (Wireframe 5) -->
            <div id="emp-att-metrics" class="stats-grid">
                <div class="stat-box">
                    <div class="metric-label">Days Present</div>
                    <div class="num" style="color: #34d399;" id="metric-days-present">18 Days</div>
                </div>
                <div class="stat-box">
                    <div class="metric-label">Leaves Count</div>
                    <div class="num" style="color: #fbbf24;" id="metric-leaves-count">2 Days</div>
                </div>
                <div class="stat-box">
                    <div class="metric-label">Total Working Days</div>
                    <div class="num" style="color: #60a5fa;">22 Days</div>
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
                                <th>Work Hours</th>
                                <th>Extra Hours</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody id="tbl-attendance"></tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- TIME OFF / LEAVE TAB (Wireframe 6) -->
        <div id="panel-leave" class="tab-panel">
            <div class="header-row">
                <h1 class="header-title">Time Off Management</h1>
                <button class="btn btn-primary" onclick="openTimeOffRequestModal()">+ Time Off Request</button>
            </div>

            <!-- Balance Metric Cards (Wireframe 6) -->
            <div class="stats-grid">
                <div class="stat-box">
                    <div class="metric-label">Paid Time Off</div>
                    <div class="num" style="color: #34d399;">24 Days Available</div>
                </div>
                <div class="stat-box">
                    <div class="metric-label">Sick Time Off</div>
                    <div class="num" style="color: #fbbf24;">07 Days Available</div>
                </div>
                <div class="stat-box">
                    <div class="metric-label">Unpaid Leaves</div>
                    <div class="num" style="color: #60a5fa;">Unlimited</div>
                </div>
            </div>

            <!-- Calendar View Grid (Wireframe 6) -->
            <div class="card">
                <h3 style="font-size: 1.05rem; margin-bottom: 0.5rem;">Time Off Calendar (August 2026)</h3>
                <div class="calendar-grid" id="cal-grid"></div>
            </div>

            <!-- Table -->
            <div class="card">
                <h3 style="font-size: 1.05rem; margin-bottom: 0.9rem;">Time Off Requests & HR Decisioning</h3>
                <div class="table-wrap">
                    <table>
                        <thead>
                            <tr>
                                <th>Employee</th>
                                <th>Time Off Type</th>
                                <th>Start Date</th>
                                <th>End Date</th>
                                <th>Days</th>
                                <th>Medical Certificate / Attachment</th>
                                <th>Status</th>
                                <th>HR Decision</th>
                            </tr>
                        </thead>
                        <tbody id="tbl-leave"></tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- DOCUMENTS TAB -->
        <div id="panel-documents" class="tab-panel">
            <div class="header-row">
                <h1 class="header-title">Employee Documents</h1>
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
                            <label>Select File</label>
                            <input type="file" id="real-file-input" class="input" accept="image/*,.pdf,.doc,.docx,.txt" required>
                        </div>
                    </div>
                    <button type="submit" class="btn btn-primary">Upload Document</button>
                </form>
            </div>

            <div class="card">
                <div class="table-wrap">
                    <table>
                        <thead>
                            <tr>
                                <th>Title</th>
                                <th>Employee</th>
                                <th>Category</th>
                                <th>File Name</th>
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
                <p style="color:var(--text-muted); margin-top:0.35rem; font-size:0.875rem;">Managed by Person 4 (Base salary, allowances, deductions, net salary).</p>
            </div>
        </div>

    </div>

    <!-- MY PROFILE MODAL (Wireframes 3 & 4) -->
    <div id="modal-profile" class="modal" style="display: none;">
        <div class="modal-card">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem;">
                <div style="display: flex; gap: 1rem; align-items: center;">
                    <div class="avatar-circle" style="width: 60px; height: 60px; font-size: 1.5rem;" id="prof-avatar">JD</div>
                    <div>
                        <h2 id="prof-name" style="font-size: 1.25rem;">John Doe</h2>
                        <p id="prof-login-id" style="font-size: 0.85rem; color: #34d399; font-weight: 600;">OIJODO20240001</p>
                        <p id="prof-job" style="font-size: 0.8rem; color: var(--text-muted);">Senior Software Engineer • Engineering</p>
                    </div>
                </div>
                <button class="btn btn-secondary" onclick="closeProfileModal()">✕</button>
            </div>

            <div class="subtabs">
                <div class="subtab active" id="subtab-btn-resume" onclick="openProfileSubtab('resume')">Resume</div>
                <div class="subtab" id="subtab-btn-private" onclick="openProfileSubtab('private')">Private Info</div>
                <div class="subtab" id="subtab-btn-salary" onclick="openProfileSubtab('salary')">Salary Info (Admin Only)</div>
                <div class="subtab" id="subtab-btn-security" onclick="openProfileSubtab('security')">Security</div>
            </div>

            <!-- Resume Subtab -->
            <div id="subtab-resume" class="profile-subpanel">
                <div class="form-row">
                    <div class="field"><label>About</label><p style="font-size:0.85rem; color:var(--text-muted);">Senior engineer specializing in Python & Odoo ORM customization.</p></div>
                    <div class="field"><label>Skills</label><p style="font-size:0.85rem; color:var(--text-muted);">Python, PostgreSQL, Odoo XML, OWL Framework</p></div>
                </div>
            </div>

            <!-- Private Info Subtab (Wireframe 4) -->
            <div id="subtab-private" class="profile-subpanel" style="display:none;">
                <h4 style="font-size: 0.95rem; margin-bottom: 0.75rem; color: var(--accent-purple-hover);">Personal Details & Bank Info</h4>
                <div class="form-row">
                    <div class="field"><label>Date of Birth</label><input type="text" class="input" value="1995-04-12" readonly></div>
                    <div class="field"><label>Gender</label><input type="text" class="input" value="Male" readonly></div>
                    <div class="field"><label>Nationality</label><input type="text" class="input" value="Indian" readonly></div>
                    <div class="field"><label>Marital Status</label><input type="text" class="input" value="Single" readonly></div>
                    <div class="field"><label>Bank Account Number</label><input type="text" class="input" value="9876543210123" readonly></div>
                    <div class="field"><label>Bank Name</label><input type="text" class="input" value="HDFC Bank" readonly></div>
                    <div class="field"><label>IFSC Code</label><input type="text" class="input" value="HDFC0001234" readonly></div>
                    <div class="field"><label>PAN No</label><input type="text" class="input" value="ABCDE1234F" readonly></div>
                    <div class="field"><label>Aadhar No</label><input type="text" class="input" value="1234-5678-9012" readonly></div>
                </div>
            </div>

            <!-- Salary Info Subtab (Wireframes 3 & 4 - Admin Only) -->
            <div id="subtab-salary" class="profile-subpanel" style="display:none;">
                <div id="salary-admin-view">
                    <div class="stats-grid" style="margin-bottom: 1rem;">
                        <div class="stat-box"><div class="metric-label">Monthly Wage</div><div class="num" style="color: #34d399;">₹50,000 / Month</div></div>
                        <div class="stat-box"><div class="metric-label">Yearly Wage</div><div class="num" style="color: #60a5fa;">₹6,00,000 / Year</div></div>
                        <div class="stat-box"><div class="metric-label">Working Schedule</div><div class="num" style="font-size:1.1rem; margin-top:0.5rem;">5 Days / Week</div></div>
                    </div>

                    <h4 style="font-size: 0.9rem; margin-bottom: 0.5rem; color: var(--accent-purple-hover);">Salary Components Breakdown (Auto-Calculated)</h4>
                    <table style="margin-bottom: 1rem;">
                        <thead>
                            <tr><th>Component</th><th>Percentage</th><th>Monthly Amount</th></tr>
                        </thead>
                        <tbody>
                            <tr><td><strong>Basic Salary</strong></td><td>50.00%</td><td>₹25,000.00 / month</td></tr>
                            <tr><td><strong>House Rent Allowance (HRA)</strong></td><td>50.00% of Basic</td><td>₹12,500.00 / month</td></tr>
                            <tr><td><strong>Standard Allowance</strong></td><td>16.67%</td><td>₹4,167.50 / month</td></tr>
                            <tr><td><strong>Performance Bonus</strong></td><td>8.33%</td><td>₹2,082.50 / month</td></tr>
                            <tr><td><strong>Leave Travel Allowance (LTA)</strong></td><td>8.33%</td><td>₹2,082.50 / month</td></tr>
                            <tr><td><strong>Fixed Allowance</strong></td><td>Remainder</td><td>₹4,167.50 / month</td></tr>
                        </tbody>
                    </table>

                    <h4 style="font-size: 0.9rem; margin-bottom: 0.5rem; color: var(--accent-red);">Deductions & PF</h4>
                    <table>
                        <thead>
                            <tr><th>Deduction Item</th><th>Rate</th><th>Monthly Amount</th></tr>
                        </thead>
                        <tbody>
                            <tr><td><strong>Provident Fund (PF) Contribution</strong></td><td>12.00% of Basic</td><td>₹3,000.00 / month</td></tr>
                            <tr><td><strong>Professional Tax</strong></td><td>Fixed</td><td>₹200.00 / month</td></tr>
                        </tbody>
                    </table>
                </div>
                <div id="salary-emp-restricted" style="display:none; text-align:center; padding: 2rem; color: var(--accent-amber);">
                    🔒 <strong>Restricted Access:</strong> Salary Information tab is visible ONLY to Admin & HR Officers.
                </div>
            </div>

            <!-- Security Subtab -->
            <div id="subtab-security" class="profile-subpanel" style="display:none;">
                <div class="field" style="margin-bottom: 1rem;"><label>Change Password</label><input type="password" class="input" placeholder="Enter new password"></div>
                <button class="btn btn-primary">Update Password</button>
            </div>
        </div>
    </div>

    <!-- AUTH MODAL (Wireframe 1) -->
    <div id="modal-auth" class="modal" style="display: none;">
        <div class="modal-card" style="max-width: 480px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem;">
                <h3 id="auth-title" style="font-size:1.15rem;">Sign In to Dayflow</h3>
                <button class="btn btn-secondary" onclick="toggleAuthModal()">✕</button>
            </div>

            <!-- Sign In Form -->
            <form id="form-signin" onsubmit="handleSignIn(event)">
                <div class="field" style="margin-bottom:0.85rem;"><label>Login ID / Email</label><input type="text" id="signin-login" class="input" placeholder="e.g. OIJODO20240001" required></div>
                <div class="field" style="margin-bottom:1.25rem;"><label>Password</label><input type="password" id="signin-pass" class="input" placeholder="••••••••" required></div>
                <button type="submit" class="btn btn-primary" style="width:100%; justify-content:center;">SIGN IN</button>
                <p style="text-align:center; font-size:0.8rem; margin-top:1rem; color:var(--text-muted);">
                    Don't have an Account? <a href="#" style="color:var(--accent-purple-hover);" onclick="switchAuthMode('signup')">Sign Up</a>
                </p>
            </form>

            <!-- Sign Up Form (Wireframe 1) -->
            <form id="form-signup" onsubmit="handleSignUp(event)" style="display:none;">
                <div class="field" style="margin-bottom:0.75rem;"><label>Company Name</label><input type="text" id="signup-company" class="input" value="Odoo India (OI)" required></div>
                <div class="field" style="margin-bottom:0.75rem;"><label>Full Name</label><input type="text" id="signup-name" class="input" placeholder="John Doe" required></div>
                <div class="field" style="margin-bottom:0.75rem;"><label>Email</label><input type="email" id="signup-email" class="input" placeholder="john@company.com" required></div>
                <div class="field" style="margin-bottom:0.75rem;"><label>Phone</label><input type="text" id="signup-phone" class="input" placeholder="+91 98765 43210" required></div>
                <div class="field" style="margin-bottom:0.75rem;"><label>Password</label><input type="password" id="signup-pass" class="input" required></div>
                <div class="field" style="margin-bottom:1rem;"><label>Confirm Password</label><input type="password" id="signup-pass2" class="input" required></div>
                
                <div style="background-color:var(--bg-input); padding:0.6rem; border-radius:6px; font-size:0.75rem; color:#34d399; margin-bottom:1rem;">
                    💡 Auto-Generated Login ID Formula:<br><code>OI + First 2 Letters + Joining Year + Serial (e.g., OIJODO20260001)</code>
                </div>

                <button type="submit" class="btn btn-success" style="width:100%; justify-content:center;">Sign Up</button>
                <p style="text-align:center; font-size:0.8rem; margin-top:1rem; color:var(--text-muted);">
                    Already have an account? <a href="#" style="color:var(--accent-purple-hover);" onclick="switchAuthMode('signin')">Sign In</a>
                </p>
            </form>
        </div>
    </div>

    <!-- TIME OFF REQUEST MODAL (Wireframe 6) -->
    <div id="modal-timeoff-req" class="modal" style="display: none;">
        <div class="modal-card" style="max-width: 520px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem;">
                <h3 style="font-size:1.15rem;">Time Off Type Request</h3>
                <button class="btn btn-secondary" onclick="closeTimeOffRequestModal()">✕</button>
            </div>
            <form onsubmit="handleTimeOffRequestSubmit(event)">
                <div class="field" style="margin-bottom:0.75rem;">
                    <label>Employee Name</label>
                    <input type="text" class="input" value="John Doe" readonly>
                </div>
                <div class="field" style="margin-bottom:0.75rem;">
                    <label>Time Off Type</label>
                    <select id="req-type" class="input" required>
                        <option value="paid">Paid Time Off</option>
                        <option value="sick">Sick Leave</option>
                        <option value="unpaid">Unpaid Leaves</option>
                    </select>
                </div>
                <div class="form-row">
                    <div class="field"><label>Start Date</label><input type="date" id="req-start" class="input" required></div>
                    <div class="field"><label>End Date</label><input type="date" id="req-end" class="input" required></div>
                </div>
                <div class="field" style="margin-bottom:0.75rem;">
                    <label>Medical Certificate Attachment (Required for Sick Leave)</label>
                    <input type="file" id="req-file" class="input" accept="image/*,.pdf">
                </div>
                <div style="display:flex; gap:0.5rem; justify-content:flex-end; margin-top:1.25rem;">
                    <button type="button" class="btn btn-secondary" onclick="closeTimeOffRequestModal()">Discard</button>
                    <button type="submit" class="btn btn-primary">Submit Request</button>
                </div>
            </form>
        </div>
    </div>

    <script>
        const DEFAULT_EMPLOYEES = [
            { id: 1, name: 'John Doe', email: 'john.doe@company.com', job: 'Senior Software Engineer', dept: 'Engineering', role: 'employee', joining: '2024-03-15', loginId: 'OIJODO20240001', status: 'present' },
            { id: 2, name: 'Jane Smith', email: 'jane.smith@company.com', job: 'HR Specialist', dept: 'Human Resources', role: 'admin', joining: '2023-01-10', loginId: 'OIJASM20230002', status: 'leave' },
            { id: 3, name: 'Robert Taylor', email: 'robert.t@company.com', job: 'Product Manager', dept: 'Product', role: 'employee', joining: '2025-06-01', loginId: 'OIROTA20250003', status: 'absent' }
        ];

        const DEFAULT_ATTENDANCE = [
            { id: 1, date: '2026-08-21', employee: 'John Doe', checkIn: '09:00 AM', checkOut: '05:30 PM', status: 'present', workedHours: 8.5, extraHours: 0.5 },
            { id: 2, date: '2026-08-20', employee: 'John Doe', checkIn: '08:50 AM', checkOut: '06:10 PM', status: 'present', workedHours: 9.3, extraHours: 1.3 }
        ];

        const DEFAULT_LEAVE = [
            { id: 101, employee: 'John Doe', type: 'sick', startDate: '2026-08-25', endDate: '2026-08-26', days: 2, hasAttachment: true, status: 'pending', adminComments: '' },
            { id: 102, employee: 'Jane Smith', type: 'paid', startDate: '2026-08-28', endDate: '2026-08-30', days: 3, hasAttachment: false, status: 'approved', adminComments: 'Approved by HR' }
        ];

        let state = {
            role: 'employee',
            currentEmployee: 'John Doe',
            isCheckedIn: false,
            activeCheckInTime: null,
            checkInTimestamp: null,
            employees: JSON.parse(localStorage.getItem('df_employees')) || DEFAULT_EMPLOYEES,
            attendances: JSON.parse(localStorage.getItem('df_attendances')) || DEFAULT_ATTENDANCE,
            leaves: JSON.parse(localStorage.getItem('df_leaves')) || DEFAULT_LEAVE,
            documents: JSON.parse(localStorage.getItem('df_documents')) || []
        };

        function saveState() {
            localStorage.setItem('df_employees', JSON.stringify(state.employees));
            localStorage.setItem('df_attendances', JSON.stringify(state.attendances));
            localStorage.setItem('df_leaves', JSON.stringify(state.leaves));
        }

        function resetData() {
            localStorage.clear();
            state.employees = JSON.parse(JSON.stringify(DEFAULT_EMPLOYEES));
            state.attendances = JSON.parse(JSON.stringify(DEFAULT_ATTENDANCE));
            state.leaves = JSON.parse(JSON.stringify(DEFAULT_LEAVE));
            state.isCheckedIn = false;
            renderAll();
        }

        function openTab(tabId) {
            document.querySelectorAll('.nav-tab').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.tab-panel').forEach(el => el.classList.remove('active'));

            document.getElementById('tab-btn-' + tabId)?.classList.add('active');
            document.getElementById('panel-' + tabId)?.classList.add('active');
        }

        function onRoleChange(role) {
            state.role = role;
            const searchBox = document.getElementById('admin-att-search');
            const metrics = document.getElementById('emp-att-metrics');

            if (role === 'admin') {
                if (searchBox) searchBox.style.display = 'block';
                if (metrics) metrics.style.display = 'none';
            } else {
                if (searchBox) searchBox.style.display = 'none';
                if (metrics) metrics.style.display = 'grid';
            }

            renderAll();
        }

        function toggleSystrayCheckIn() {
            const btn = document.getElementById('btn-systray-toggle');
            const dot = document.getElementById('systray-dot');
            const txt = document.getElementById('systray-status');

            if (!state.isCheckedIn) {
                state.isCheckedIn = true;
                const now = new Date();
                const timeStr = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: true });
                dot.className = 'systray-dot green';
                txt.innerText = 'Since ' + timeStr;
                btn.innerText = 'Check OUT';
                btn.className = 'btn btn-danger';
            } else {
                state.isCheckedIn = false;
                dot.className = 'systray-dot';
                txt.innerText = 'Check IN ->';
                btn.innerText = 'Check IN';
                btn.className = 'btn btn-primary';
            }
        }

        function toggleAvatarDropdown() {
            const box = document.getElementById('avatar-dropdown');
            box.style.display = box.style.display === 'flex' ? 'none' : 'flex';
        }

        function openMyProfileModal() {
            toggleAvatarDropdown();
            document.getElementById('modal-profile').style.display = 'flex';
            openProfileSubtab('resume');
        }

        function closeProfileModal() {
            document.getElementById('modal-profile').style.display = 'none';
        }

        function openProfileSubtab(subId) {
            document.querySelectorAll('.subtab').forEach(s => s.classList.remove('active'));
            document.querySelectorAll('.profile-subpanel').forEach(p => p.style.display = 'none');

            document.getElementById('subtab-btn-' + subId)?.classList.add('active');
            document.getElementById('subtab-' + subId).style.display = 'block';

            if (subId === 'salary') {
                const adminView = document.getElementById('salary-admin-view');
                const empRestricted = document.getElementById('salary-emp-restricted');
                if (state.role === 'admin') {
                    adminView.style.display = 'block';
                    empRestricted.style.display = 'none';
                } else {
                    adminView.style.display = 'none';
                    empRestricted.style.display = 'block';
                }
            }
        }

        function toggleAuthModal() {
            toggleAvatarDropdown();
            const modal = document.getElementById('modal-auth');
            modal.style.display = modal.style.display === 'flex' ? 'none' : 'flex';
        }

        function switchAuthMode(mode) {
            if (mode === 'signup') {
                document.getElementById('auth-title').innerText = 'Sign Up for Dayflow';
                document.getElementById('form-signin').style.display = 'none';
                document.getElementById('form-signup').style.display = 'block';
            } else {
                document.getElementById('auth-title').innerText = 'Sign In to Dayflow';
                document.getElementById('form-signin').style.display = 'block';
                document.getElementById('form-signup').style.display = 'none';
            }
        }

        function handleSignIn(e) {
            e.preventDefault();
            alert('Signed in successfully!');
            document.getElementById('modal-auth').style.display = 'none';
        }

        function handleSignUp(e) {
            e.preventDefault();
            const name = document.getElementById('signup-name').value;
            const parts = name.trim().split(' ');
            const code = parts.length >= 2 ? (parts[0].substring(0, 2) + parts[parts.length-1].substring(0, 2)).toUpperCase() : 'JODO';
            const generatedId = `OI${code}20260004`;

            state.employees.unshift({
                id: Date.now(),
                name: name,
                email: document.getElementById('signup-email').value,
                job: 'Software Engineer',
                dept: 'Engineering',
                role: 'employee',
                joining: '2026-08-22',
                loginId: generatedId,
                status: 'present'
            });

            saveState();
            renderEmployees();
            alert(`Account Created Successfully!\n\nYour System-Generated Login ID: ${generatedId}\nInitial Password has been sent to your email.`);
            document.getElementById('modal-auth').style.display = 'none';
        }

        function openTimeOffRequestModal() {
            document.getElementById('modal-timeoff-req').style.display = 'flex';
        }

        function closeTimeOffRequestModal() {
            document.getElementById('modal-timeoff-req').style.display = 'none';
        }

        function handleTimeOffRequestSubmit(e) {
            e.preventDefault();
            const type = document.getElementById('req-type').value;
            const start = document.getElementById('req-start').value;
            const end = document.getElementById('req-end').value;
            const fileInput = document.getElementById('req-file');

            state.leaves.unshift({
                id: Date.now(),
                employee: state.currentEmployee,
                type: type,
                startDate: start,
                endDate: end,
                days: 2,
                hasAttachment: fileInput.files.length > 0,
                status: 'pending',
                adminComments: ''
            });

            saveState();
            renderLeaves();
            closeTimeOffRequestModal();
            alert('Time Off Request submitted successfully!');
        }

        function handleApproveLeave(id) {
            const leave = state.leaves.find(l => l.id === id);
            if (leave) {
                leave.status = 'approved';
                leave.adminComments = 'Approved by HR';
                saveState();
                renderLeaves();
            }
        }

        function handleRejectLeave(id) {
            const leave = state.leaves.find(l => l.id === id);
            if (leave) {
                leave.status = 'rejected';
                leave.adminComments = 'Rejected by HR';
                saveState();
                renderLeaves();
            }
        }

        function renderEmployees() {
            const grid = document.getElementById('grid-employees');
            grid.innerHTML = state.employees.map(e => {
                const dot = e.status === 'present' ? '<span class="emp-status-dot dot-green">🟢</span>' :
                            e.status === 'leave' ? '<span class="emp-status-dot dot-airplane">✈️</span>' : '<span class="emp-status-dot dot-yellow">🟡</span>';

                return `
                    <div class="emp-card" onclick="openMyProfileModal()">
                        ${dot}
                        <div class="emp-head">
                            <div class="avatar-circle">${e.name.split(' ').map(n=>n[0]).join('')}</div>
                            <div>
                                <div class="emp-name">${e.name}</div>
                                <div class="emp-job">${e.job} • ${e.dept}</div>
                            </div>
                        </div>
                        <div style="font-size:0.75rem; color:#34d399; margin-top:0.2rem;">
                            <code>${e.loginId}</code>
                        </div>
                    </div>
                `;
            }).join('');
        }

        function renderAttendance() {
            const tbody = document.getElementById('tbl-attendance');
            let data = state.role === 'employee' ? state.attendances.filter(a => a.employee === state.currentEmployee) : state.attendances;

            tbody.innerHTML = data.map(a => `
                <tr>
                    <td><strong>${a.date}</strong></td>
                    <td>${a.employee}</td>
                    <td>${a.checkIn}</td>
                    <td>${a.checkOut}</td>
                    <td>${a.workedHours}h</td>
                    <td>${a.extraHours}h</td>
                    <td><span class="badge ${a.status==='present'?'badge-green':'badge-amber'}">${a.status.toUpperCase()}</span></td>
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
                            <button class="btn btn-success" style="padding:0.2rem 0.5rem; font-size:0.75rem;" onclick="handleApproveLeave(${l.id})">✓ Approve</button>
                            <button class="btn btn-danger" style="padding:0.2rem 0.5rem; font-size:0.75rem;" onclick="handleRejectLeave(${l.id})">✕ Reject</button>
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
                        <td>${l.hasAttachment ? '📄 Attached' : 'None'}</td>
                        <td><span class="badge ${badge}">${l.status.toUpperCase()}</span></td>
                        <td>${action}</td>
                    </tr>
                `;
            }).join('');

            // Calendar Wireframe 6 Grid
            const calGrid = document.getElementById('cal-grid');
            let daysHtml = '';
            for(let i=1; i<=31; i++) {
                const isLeave = (i >= 25 && i <= 26);
                daysHtml += `<div class="cal-day ${isLeave ? 'leave-day' : ''}"><strong>${i}</strong> ${isLeave ? '<br><span style="font-size:0.7rem; color:#60a5fa;">Sick Leave</span>' : ''}</div>`;
            }
            calGrid.innerHTML = daysHtml;
        }

        function renderAll() {
            renderEmployees();
            renderAttendance();
            renderLeaves();
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
    print(" Dayflow HRMS - 100% Wireframe Aligned Workspace")
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
