# -*- coding: utf-8 -*-
"""
Dayflow HRMS - Unified Live UI Preview Server
Odoo x NMIT Hackathon
All-in-One Dashboard, Employees, Attendance, Time Off (with New Button, Interactive Calendar, National Holidays & Pop-up Modal), Documents, Payroll, and Admin Profile
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import webbrowser

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dayflow HRMS — Workspace & Admin Console</title>
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

        .nav-right {
            display: flex;
            align-items: center;
            gap: 1rem;
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

        /* Interactive Calendar Grid */
        .cal-layout {
            display: grid;
            grid-template-columns: 2.2fr 1fr;
            gap: 1.25rem;
            margin-bottom: 1.25rem;
        }

        @media (max-width: 960px) {
            .cal-layout { grid-template-columns: 1fr; }
        }

        .cal-header-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
        }

        .cal-grid-days {
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 0.4rem;
        }

        .cal-day-name {
            text-align: center;
            font-size: 0.72rem;
            font-weight: 700;
            color: var(--text-muted);
            text-transform: uppercase;
            padding-bottom: 0.4rem;
        }

        .cal-cell {
            background-color: var(--bg-card);
            border: 1px solid var(--border-line);
            min-height: 75px;
            padding: 0.45rem;
            border-radius: 6px;
            font-size: 0.8rem;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            cursor: pointer;
            transition: all 0.15s ease;
            position: relative;
        }

        .cal-cell:hover {
            border-color: var(--accent-purple);
            background-color: rgba(113, 75, 103, 0.15);
        }

        .cal-cell.weekend {
            background-color: rgba(32, 36, 51, 0.4);
            opacity: 0.85;
        }

        .cal-cell.holiday {
            border-color: rgba(245, 158, 11, 0.6);
            background-color: rgba(245, 158, 11, 0.12);
        }

        .cal-cell.leave-day {
            border-color: rgba(59, 130, 246, 0.6);
            background-color: rgba(59, 130, 246, 0.15);
        }

        .cal-tag {
            display: block;
            font-size: 0.68rem;
            font-weight: 600;
            padding: 0.15rem 0.3rem;
            border-radius: 4px;
            margin-top: 0.2rem;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .cal-tag.tag-holiday {
            background-color: rgba(245, 158, 11, 0.25);
            color: #fbbf24;
            border: 1px solid rgba(245, 158, 11, 0.4);
        }

        .cal-tag.tag-leave {
            background-color: rgba(59, 130, 246, 0.25);
            color: #93c5fd;
            border: 1px solid rgba(59, 130, 246, 0.4);
        }

        /* Holiday List on Side */
        .holiday-list {
            display: flex;
            flex-direction: column;
            gap: 0.65rem;
        }

        .holiday-item {
            background-color: var(--bg-card);
            border: 1px solid var(--border-line);
            border-radius: 8px;
            padding: 0.75rem 0.9rem;
            display: flex;
            align-items: center;
            gap: 0.85rem;
            transition: all 0.15s ease;
        }

        .holiday-item:hover {
            border-color: var(--accent-amber);
            transform: translateX(2px);
        }

        .holiday-date-badge {
            background: rgba(245, 158, 11, 0.15);
            color: #fbbf24;
            border: 1px solid rgba(245, 158, 11, 0.3);
            border-radius: 6px;
            padding: 0.3rem 0.5rem;
            font-weight: 700;
            font-size: 0.78rem;
            text-align: center;
            min-width: 58px;
        }

        .holiday-name {
            font-size: 0.88rem;
            font-weight: 600;
            color: var(--text-main);
        }

        .holiday-type {
            font-size: 0.72rem;
            color: var(--text-muted);
            margin-top: 1px;
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
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .emp-card:hover {
            border-color: var(--accent-purple);
            transform: translateY(-2px);
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

        /* Profile Header Banner */
        .profile-hero {
            background: linear-gradient(135deg, rgba(113, 75, 103, 0.25), rgba(32, 36, 51, 0.95));
            border: 1px solid var(--border-line);
            border-radius: 12px;
            padding: 1.75rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
        }

        .profile-hero-left {
            display: flex;
            align-items: center;
            gap: 1.5rem;
        }

        .profile-avatar-lg {
            width: 72px;
            height: 72px;
            border-radius: 50%;
            background: linear-gradient(135deg, var(--accent-purple), #9333ea);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.75rem;
            font-weight: 800;
            color: #fff;
            border: 3px solid rgba(255,255,255,0.1);
        }

        .profile-chips {
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
            margin-top: 0.4rem;
        }

        .chip {
            background-color: rgba(255,255,255,0.06);
            border: 1px solid var(--border-line);
            padding: 0.25rem 0.6rem;
            border-radius: 14px;
            font-size: 0.75rem;
            color: var(--text-muted);
        }

        /* Profile Subtabs */
        .profile-subtabs {
            display: flex;
            gap: 0.5rem;
            border-bottom: 1px solid var(--border-line);
            margin-bottom: 1.25rem;
        }

        .profile-subtab {
            padding: 0.6rem 1.2rem;
            font-size: 0.88rem;
            font-weight: 600;
            color: var(--text-muted);
            cursor: pointer;
            border-bottom: 2px solid transparent;
            transition: all 0.15s ease;
        }

        .profile-subtab:hover {
            color: var(--text-main);
        }

        .profile-subtab.active {
            color: #fff;
            border-bottom-color: var(--accent-purple);
        }

        .profile-section { display: none; }
        .profile-section.active { display: block; }

        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 1rem;
            margin-bottom: 1.25rem;
        }

        .info-item {
            background-color: var(--bg-card);
            border: 1px solid var(--border-line);
            border-radius: 8px;
            padding: 0.85rem 1rem;
        }

        .info-item .lbl {
            font-size: 0.72rem;
            text-transform: uppercase;
            color: var(--text-muted);
            font-weight: 600;
        }

        .info-item .val {
            font-size: 0.95rem;
            font-weight: 600;
            color: var(--text-main);
            margin-top: 0.25rem;
        }

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
            padding: 1.5rem;
            max-height: 88vh;
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
            <li class="nav-tab" id="tab-btn-profile" onclick="openTab('profile')">Admin Profile</li>
        </ul>
        <div class="nav-right">
            <div class="user-pill">
                <span>Role:</span>
                <select id="user-role-select" onchange="onRoleChange(this.value)">
                    <option value="admin">HR Manager (Admin)</option>
                    <option value="employee">Employee (John Doe)</option>
                </select>
            </div>
            <div style="cursor: pointer;" onclick="openTab('profile')" title="View Admin Profile">
                <div class="avatar" style="width: 34px; height: 34px; font-size: 0.85rem;" id="nav-avatar">JS</div>
            </div>
        </div>
    </nav>

    <div class="container">

        <!-- DASHBOARD TAB -->
        <div id="panel-dashboard" class="tab-panel active">
            <div class="header-row">
                <div>
                    <h1 class="header-title">Dayflow HRMS Management Console</h1>
                    <p class="header-sub">Live organizational metrics, pending approvals, and executive summary</p>
                </div>
                <div style="display:flex; gap:0.5rem;">
                    <button class="btn btn-primary" onclick="openTab('profile')">👤 Admin Profile</button>
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

        <!-- TIME OFF / LEAVE TAB (With New Button, Calendar & National Holidays) -->
        <div id="panel-leave" class="tab-panel">
            <div class="header-row">
                <div>
                    <h1 class="header-title">Time Off & Leave Management</h1>
                    <p class="header-sub">Plan time off, view official national holidays, and track leave balances</p>
                </div>
                <button class="btn btn-primary" style="font-size: 0.95rem; padding: 0.5rem 1.3rem;" onclick="openLeaveModal(null)">+ New</button>
            </div>

            <!-- Balance Metric Cards -->
            <div class="stats-grid">
                <div class="stat-box">
                    <div class="metric-label">Paid Time Off (PTO)</div>
                    <div class="num" style="color: #34d399;">14 Days Available</div>
                </div>
                <div class="stat-box">
                    <div class="metric-label">Sick Leave</div>
                    <div class="num" style="color: #fbbf24;">07 Days Available</div>
                </div>
                <div class="stat-box">
                    <div class="metric-label">Unpaid Leave</div>
                    <div class="num" style="color: #60a5fa;">Unlimited</div>
                </div>
                <div class="stat-box">
                    <div class="metric-label">Upcoming National Holidays</div>
                    <div class="num" style="color: var(--accent-purple-hover);">4 This Year</div>
                </div>
            </div>

            <!-- Calendar & National Holidays Layout -->
            <div class="cal-layout">
                <!-- Left: Interactive Calendar Grid -->
                <div class="card" style="margin-bottom: 0;">
                    <div class="cal-header-bar">
                        <div style="display:flex; align-items:center; gap: 0.75rem;">
                            <h3 style="font-size: 1.1rem; color: #fff;">August 2026</h3>
                            <span class="badge badge-purple">Official Work Calendar</span>
                        </div>
                        <div style="display:flex; gap:0.4rem;">
                            <button class="btn btn-secondary" style="padding:0.25rem 0.6rem; font-size:0.75rem;">&lt;</button>
                            <button class="btn btn-secondary" style="padding:0.25rem 0.6rem; font-size:0.75rem;">Today</button>
                            <button class="btn btn-secondary" style="padding:0.25rem 0.6rem; font-size:0.75rem;">&gt;</button>
                        </div>
                    </div>

                    <!-- 7-Day Columns -->
                    <div class="cal-grid-days" style="margin-bottom: 0.4rem;">
                        <div class="cal-day-name">Mon</div>
                        <div class="cal-day-name">Tue</div>
                        <div class="cal-day-name">Wed</div>
                        <div class="cal-day-name">Thu</div>
                        <div class="cal-day-name">Fri</div>
                        <div class="cal-day-name" style="color:#f87171;">Sat</div>
                        <div class="cal-day-name" style="color:#f87171;">Sun</div>
                    </div>

                    <!-- Dynamic Calendar Tiles -->
                    <div class="cal-grid-days" id="cal-grid-tiles"></div>
                    
                    <p style="font-size:0.75rem; color:var(--text-muted); margin-top:0.75rem; text-align:center;">
                        💡 Click on any date tile above or click <strong>+ New</strong> to apply for leave.
                    </p>
                </div>

                <!-- Right: National & Public Holidays -->
                <div class="card" style="margin-bottom: 0;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 1rem;">
                        <h3 style="font-size: 1.05rem; color: #fbbf24;">🗓️ National Holidays 2026</h3>
                        <span class="badge badge-amber">Public / Paid</span>
                    </div>

                    <div class="holiday-list">
                        <div class="holiday-item">
                            <div class="holiday-date-badge">AUG 15<br><span style="font-size:0.65rem; font-weight:normal;">Sat</span></div>
                            <div>
                                <div class="holiday-name">🇮🇳 Independence Day</div>
                                <div class="holiday-type">Gazetted National Holiday</div>
                            </div>
                        </div>

                        <div class="holiday-item">
                            <div class="holiday-date-badge">AUG 19<br><span style="font-size:0.65rem; font-weight:normal;">Wed</span></div>
                            <div>
                                <div class="holiday-name">🌸 Raksha Bandhan</div>
                                <div class="holiday-type">Restricted Holiday</div>
                            </div>
                        </div>

                        <div class="holiday-item">
                            <div class="holiday-date-badge">AUG 26<br><span style="font-size:0.65rem; font-weight:normal;">Wed</span></div>
                            <div>
                                <div class="holiday-name">🦚 Janmashtami</div>
                                <div class="holiday-type">Gazetted Public Holiday</div>
                            </div>
                        </div>

                        <div class="holiday-item">
                            <div class="holiday-date-badge">SEP 07<br><span style="font-size:0.65rem; font-weight:normal;">Mon</span></div>
                            <div>
                                <div class="holiday-name">🐘 Ganesh Chaturthi</div>
                                <div class="holiday-type">Public Festival Holiday</div>
                            </div>
                        </div>

                        <div class="holiday-item">
                            <div class="holiday-date-badge">OCT 02<br><span style="font-size:0.65rem; font-weight:normal;">Fri</span></div>
                            <div>
                                <div class="holiday-name">🕊️ Gandhi Jayanti</div>
                                <div class="holiday-type">National Holiday</div>
                            </div>
                        </div>

                        <div class="holiday-item">
                            <div class="holiday-date-badge">NOV 01<br><span style="font-size:0.65rem; font-weight:normal;">Sun</span></div>
                            <div>
                                <div class="holiday-name">🪔 Diwali (Deepavali)</div>
                                <div class="holiday-type">Festival Holiday</div>
                            </div>
                        </div>
                    </div>

                    <div style="background-color: var(--bg-card); border: 1px solid var(--border-line); border-radius: 6px; padding: 0.65rem; margin-top: 1rem; font-size: 0.75rem; color: var(--text-muted);">
                        📌 <em>Company policy: Official national holidays are 100% paid and do not count against your annual PTO balance.</em>
                    </div>
                </div>
            </div>

            <!-- Time Off Requests & Review History Table -->
            <div class="card" style="margin-top: 1.25rem;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 0.9rem;">
                    <h3 style="font-size: 1.05rem;">Time Off Requests History</h3>
                    <span class="badge badge-purple">HR Governance</span>
                </div>
                <div class="table-wrap">
                    <table>
                        <thead>
                            <tr>
                                <th>Employee</th>
                                <th>Type</th>
                                <th>Start Date</th>
                                <th>End Date</th>
                                <th>Days</th>
                                <th>Reason / Remarks</th>
                                <th>Status</th>
                                <th>HR Decision</th>
                            </tr>
                        </thead>
                        <tbody id="tbl-leave"></tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- ADMIN PROFILE TAB -->
        <div id="panel-profile" class="tab-panel">
            <!-- Profile Hero Header -->
            <div class="profile-hero">
                <div class="profile-hero-left">
                    <div class="profile-avatar-lg" id="prof-hero-avatar">JS</div>
                    <div>
                        <div style="display:flex; align-items:center; gap:0.6rem;">
                            <h1 style="font-size: 1.45rem; font-weight: 800;" id="prof-hero-name">Jane Smith</h1>
                            <span class="badge badge-purple" id="prof-hero-badge">Admin / HR</span>
                            <span class="badge badge-green">Active</span>
                        </div>
                        <p style="font-size: 0.9rem; color: var(--text-muted); margin-top: 2px;" id="prof-hero-title">Head of Human Resources & Administration • Human Resources</p>
                        <div class="profile-chips">
                            <span class="chip" id="prof-hero-login">🔑 OIJASM20230002</span>
                            <span class="chip" id="prof-hero-email">✉️ jane.smith@dayflow.org</span>
                            <span class="chip" id="prof-hero-phone">📞 +91 98765 43212</span>
                            <span class="chip" id="prof-hero-joined">📅 Joined Jan 10, 2023</span>
                        </div>
                    </div>
                </div>
                <div style="display:flex; flex-direction:column; gap:0.5rem; align-items:flex-end;">
                    <button class="btn btn-primary" onclick="openEditPrivateModal()">✎ Edit Private Info</button>
                    <button class="btn btn-secondary" onclick="openSalaryModal(2)">💰 Update Salary Structure</button>
                </div>
            </div>

            <!-- Profile Subtabs -->
            <div class="profile-subtabs">
                <div class="profile-subtab active" id="psubtab-btn-private" onclick="openProfileSection('private')">🔒 Private Information</div>
                <div class="profile-subtab" id="psubtab-btn-salary" onclick="openProfileSection('salary')">💰 Salary & Compensation</div>
                <div class="profile-subtab" id="psubtab-btn-work" onclick="openProfileSection('work')">🏢 Work & Privileges</div>
                <div class="profile-subtab" id="psubtab-btn-docs" onclick="openProfileSection('docs')">📁 Verified Documents</div>
            </div>

            <!-- Section 1: Private Information -->
            <div id="psec-private" class="profile-section active">
                <div class="card">
                    <h3 style="font-size: 1.05rem; margin-bottom: 1rem; color: var(--accent-purple-hover);">Personal Details & Identification</h3>
                    <div class="info-grid">
                        <div class="info-item">
                            <div class="lbl">Date of Birth</div>
                            <div class="val" id="prof-dob">1990-06-15</div>
                        </div>
                        <div class="info-item">
                            <div class="lbl">Gender</div>
                            <div class="val" id="prof-gender">Female</div>
                        </div>
                        <div class="info-item">
                            <div class="lbl">Nationality</div>
                            <div class="val" id="prof-nationality">Indian</div>
                        </div>
                        <div class="info-item">
                            <div class="lbl">Marital Status</div>
                            <div class="val" id="prof-marital">Married</div>
                        </div>
                        <div class="info-item">
                            <div class="lbl">Aadhaar Number (UID)</div>
                            <div class="val" id="prof-aadhar">4589-2314-7890</div>
                        </div>
                        <div class="info-item">
                            <div class="lbl">PAN Number</div>
                            <div class="val" id="prof-pan">ABCPJ4589K</div>
                        </div>
                        <div class="info-item">
                            <div class="lbl">Passport Number</div>
                            <div class="val" id="prof-passport">Z9876543</div>
                        </div>
                        <div class="info-item">
                            <div class="lbl">Personal Mobile</div>
                            <div class="val" id="prof-personal-phone">+91 98765 11223</div>
                        </div>
                    </div>
                </div>

                <div class="two-col-grid">
                    <div class="card">
                        <h3 style="font-size: 1.05rem; margin-bottom: 1rem; color: var(--accent-purple-hover);">Home / Residential Address</h3>
                        <div style="display:flex; flex-direction:column; gap:0.5rem; font-size:0.9rem;">
                            <div><strong style="color:var(--text-muted);">Street:</strong> <span id="prof-addr-street">No. 42, 8th Main, 4th Cross, Indiranagar</span></div>
                            <div><strong style="color:var(--text-muted);">City / State:</strong> <span id="prof-addr-city">Bangalore, Karnataka</span></div>
                            <div><strong style="color:var(--text-muted);">PIN / Postal Code:</strong> <span id="prof-addr-pin">560038</span></div>
                            <div><strong style="color:var(--text-muted);">Country:</strong> <span id="prof-addr-country">India</span></div>
                        </div>
                    </div>

                    <div class="card">
                        <h3 style="font-size: 1.05rem; margin-bottom: 1rem; color: var(--accent-purple-hover);">Emergency Contact & Banking</h3>
                        <div style="display:flex; flex-direction:column; gap:0.5rem; font-size:0.9rem;">
                            <div><strong style="color:var(--text-muted);">Emergency Contact:</strong> <span id="prof-emg-name">Rajesh Smith (Spouse)</span></div>
                            <div><strong style="color:var(--text-muted);">Emergency Phone:</strong> <span id="prof-emg-phone">+91 98765 99887</span></div>
                            <hr style="border-color:var(--border-line); margin:0.3rem 0;">
                            <div><strong style="color:var(--text-muted);">Bank Name:</strong> <span id="prof-bank-name">HDFC Bank (Salary Account)</span></div>
                            <div><strong style="color:var(--text-muted);">Account Number:</strong> <code id="prof-bank-acc">50100234567890</code></div>
                            <div><strong style="color:var(--text-muted);">IFSC Code:</strong> <code id="prof-bank-ifsc">HDFC0001234</code></div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Section 2: Salary & Compensation Breakdown -->
            <div id="psec-salary" class="profile-section">
                <div class="stats-grid">
                    <div class="stat-box">
                        <div class="metric-label">Monthly Base Wage</div>
                        <div class="num" style="color: #60a5fa;" id="prof-sal-wage">₹55,000.00</div>
                    </div>
                    <div class="stat-box">
                        <div class="metric-label">Annual CTC</div>
                        <div class="num" style="color: #a78bfa;" id="prof-sal-ctc">₹6,60,000.00</div>
                    </div>
                    <div class="stat-box">
                        <div class="metric-label">Net Take-Home Salary</div>
                        <div class="num" style="color: #34d399;" id="prof-sal-net">₹59,500.00</div>
                    </div>
                    <div class="stat-box">
                        <div class="metric-label">Active Structure</div>
                        <div class="num" style="font-size:1.1rem; color: #fbbf24; margin-top:0.4rem;" id="prof-sal-struct">HR Specialist Base</div>
                    </div>
                </div>

                <div class="card">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 0.75rem;">
                        <h3 style="font-size: 1.05rem; color: var(--accent-green);">Earnings & Allowances Components</h3>
                        <span class="badge badge-green">Auto-Computed</span>
                    </div>
                    <div class="table-wrap">
                        <table>
                            <thead>
                                <tr>
                                    <th>Salary Component</th>
                                    <th>Computation Rule</th>
                                    <th style="text-align: right;">Monthly Amount</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td><strong>Basic Salary</strong></td>
                                    <td>50.00% of Monthly Wage</td>
                                    <td style="text-align: right;" id="prof-comp-basic">₹27,500.00</td>
                                </tr>
                                <tr>
                                    <td><strong>House Rent Allowance (HRA)</strong></td>
                                    <td>50.00% of Basic Salary</td>
                                    <td style="text-align: right;" id="prof-comp-hra">₹13,750.00</td>
                                </tr>
                                <tr>
                                    <td><strong>Executive Standard Allowance</strong></td>
                                    <td>16.67% of Wage</td>
                                    <td style="text-align: right;" id="prof-comp-std">₹9,168.50</td>
                                </tr>
                                <tr>
                                    <td><strong>Performance Bonus</strong></td>
                                    <td>8.33% of Wage</td>
                                    <td style="text-align: right;" id="prof-comp-bonus">₹4,581.50</td>
                                </tr>
                                <tr>
                                    <td><strong>Leave Travel Allowance (LTA)</strong></td>
                                    <td>8.33% of Wage</td>
                                    <td style="text-align: right;" id="prof-comp-lta">₹4,581.50</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <div class="card">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 0.75rem;">
                        <h3 style="font-size: 1.05rem; color: var(--accent-red);">Deductions & Statutory Taxes</h3>
                        <span class="badge badge-red">Statutory</span>
                    </div>
                    <div class="table-wrap">
                        <table>
                            <thead>
                                <tr>
                                    <th>Deduction Item</th>
                                    <th>Statutory Rate</th>
                                    <th style="text-align: right;">Monthly Amount</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td><strong>Provident Fund (PF) Employee Share</strong></td>
                                    <td>12.00% of Basic Salary</td>
                                    <td style="text-align: right; color:#f87171;" id="prof-comp-pf">- ₹3,300.00</td>
                                </tr>
                                <tr>
                                    <td><strong>Professional Tax (PT)</strong></td>
                                    <td>State Fixed Bracket</td>
                                    <td style="text-align: right; color:#f87171;">- ₹200.00</td>
                                </tr>
                                <tr>
                                    <td><strong>Health & Group Insurance</strong></td>
                                    <td>Corporate ESI / Health Plan</td>
                                    <td style="text-align: right; color:#f87171;">- ₹1,000.00</td>
                                </tr>
                                <tr style="background: rgba(255,255,255,0.03); font-weight: bold;">
                                    <td>Total Deductions</td>
                                    <td>PF + PT + Insurance</td>
                                    <td style="text-align: right; color:#f87171;" id="prof-comp-deduct-total">- ₹4,500.00</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- Section 3: Work & Privileges -->
            <div id="psec-work" class="profile-section">
                <div class="card">
                    <h3 style="font-size: 1.05rem; margin-bottom: 1rem; color: var(--accent-purple-hover);">Organizational Role & Security</h3>
                    <div class="info-grid">
                        <div class="info-item">
                            <div class="lbl">Job Title</div>
                            <div class="val">Head of Human Resources</div>
                        </div>
                        <div class="info-item">
                            <div class="lbl">Department</div>
                            <div class="val">Human Resources & Talent</div>
                        </div>
                        <div class="info-item">
                            <div class="lbl">Reports To</div>
                            <div class="val">Board of Directors / CEO</div>
                        </div>
                        <div class="info-item">
                            <div class="lbl">Work Location</div>
                            <div class="val">Bangalore Headquarters (HQ)</div>
                        </div>
                        <div class="info-item">
                            <div class="lbl">Working Schedule</div>
                            <div class="val">40 Hours / Week (Mon-Fri)</div>
                        </div>
                        <div class="info-item">
                            <div class="lbl">Security Group</div>
                            <div class="val"><span class="badge badge-purple">dayflow.group_dayflow_admin</span></div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Section 4: Verified Documents -->
            <div id="psec-docs" class="profile-section">
                <div class="card">
                    <h3 style="font-size: 1.05rem; margin-bottom: 1rem; color: var(--accent-purple-hover);">Attached Compliance & Verification Documents</h3>
                    <div class="table-wrap">
                        <table>
                            <thead>
                                <tr>
                                    <th>Document Title</th>
                                    <th>Type</th>
                                    <th>File Name</th>
                                    <th>Verified Date</th>
                                    <th>Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td><strong>Employment Contract 2026</strong></td>
                                    <td><span class="badge badge-purple">Contract</span></td>
                                    <td><code>jane_contract_2026.pdf</code></td>
                                    <td>2026-08-01</td>
                                    <td><span class="badge badge-green">VERIFIED</span></td>
                                </tr>
                                <tr>
                                    <td><strong>Master Degree in HR Management</strong></td>
                                    <td><span class="badge badge-purple">Certificate</span></td>
                                    <td><code>jane_degree_mba.pdf</code></td>
                                    <td>2023-01-10</td>
                                    <td><span class="badge badge-green">VERIFIED</span></td>
                                </tr>
                                <tr>
                                    <td><strong>Aadhaar Card Copy</strong></td>
                                    <td><span class="badge badge-purple">ID Proof</span></td>
                                    <td><code>jane_aadhaar.pdf</code></td>
                                    <td>2023-01-10</td>
                                    <td><span class="badge badge-green">VERIFIED</span></td>
                                </tr>
                            </tbody>
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

    <!-- LEAVE APPLICATION POP-UP MODAL (Excalidraw Design) -->
    <div id="modal-leave-app" class="modal" style="display: none;">
        <div class="modal-card" style="max-width: 560px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem;">
                <div style="display:flex; align-items:center; gap:0.6rem;">
                    <div style="background:rgba(113,75,103,0.3); border:1px solid var(--accent-purple); padding:0.35rem 0.6rem; border-radius:6px; font-size:1.1rem;">📅</div>
                    <div>
                        <h3 style="font-size: 1.15rem;">New Time Off Application</h3>
                        <p style="font-size: 0.78rem; color: var(--text-muted);">Submit leave request for HR / Admin review</p>
                    </div>
                </div>
                <button class="btn btn-secondary" onclick="closeLeaveModal()">✕</button>
            </div>

            <form onsubmit="handleLeaveModalSubmit(event)">
                <div class="field" style="margin-bottom: 0.85rem;">
                    <label>Employee Name</label>
                    <select id="mleave-emp" class="input" required>
                        <option value="John Doe">John Doe (Senior Software Engineer)</option>
                        <option value="Jane Smith">Jane Smith (Head of HR)</option>
                        <option value="Robert Taylor">Robert Taylor (Product Manager)</option>
                    </select>
                </div>

                <div class="field" style="margin-bottom: 0.85rem;">
                    <label>Time Off Category</label>
                    <select id="mleave-type" class="input" required>
                        <option value="paid">Paid Time Off (PTO)</option>
                        <option value="sick">Sick Leave</option>
                        <option value="unpaid">Unpaid Leave</option>
                        <option value="casual">Casual / Optional Leave</option>
                    </select>
                </div>

                <div class="form-row" style="margin-bottom: 0.85rem;">
                    <div class="field">
                        <label>Start Date</label>
                        <input type="date" id="mleave-start" class="input" onchange="calcLeaveDuration()" required>
                    </div>
                    <div class="field">
                        <label>End Date</label>
                        <input type="date" id="mleave-end" class="input" onchange="calcLeaveDuration()" required>
                    </div>
                </div>

                <div class="stat-box" style="background: var(--bg-card); padding: 0.65rem 1rem; margin-bottom: 0.85rem;">
                    <div class="metric-label">Calculated Duration</div>
                    <div style="font-size: 1.05rem; font-weight: 700; color: #60a5fa;" id="mleave-duration-preview">1 Working Day</div>
                </div>

                <div class="field" style="margin-bottom: 0.85rem;">
                    <label>Reason / Remarks</label>
                    <textarea id="mleave-reason" class="input" rows="2" placeholder="Explain the reason for your time off request..." required></textarea>
                </div>

                <div class="field" style="margin-bottom: 1.25rem;">
                    <label>Supporting Document / Medical Note (Optional)</label>
                    <input type="file" id="mleave-file" class="input" accept="image/*,.pdf,.doc,.docx">
                </div>

                <div style="display: flex; justify-content: flex-end; gap: 0.6rem;">
                    <button type="button" class="btn btn-secondary" onclick="closeLeaveModal()">Discard</button>
                    <button type="submit" class="btn btn-primary" style="padding: 0.5rem 1.4rem;">Submit Application</button>
                </div>
            </form>
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

    <!-- Edit Salary Modal -->
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
                        <input type="text" id="modal-pay-struct" class="input" placeholder="e.g. Executive Management Base">
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

    <!-- Edit Private Info Modal -->
    <div id="private-info-modal" class="modal" style="display: none;">
        <div class="modal-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <h3 style="font-size: 1.1rem;">Edit Private Information</h3>
                <button class="btn btn-secondary" onclick="closeEditPrivateModal()">✕</button>
            </div>
            <form onsubmit="handleSavePrivateInfo(event)">
                <div class="form-row">
                    <div class="field"><label>Date of Birth</label><input type="date" id="m-dob" class="input" value="1990-06-15" required></div>
                    <div class="field"><label>Gender</label><select id="m-gender" class="input"><option value="Female">Female</option><option value="Male">Male</option><option value="Other">Other</option></select></div>
                    <div class="field"><label>Marital Status</label><select id="m-marital" class="input"><option value="Married">Married</option><option value="Single">Single</option></select></div>
                </div>
                <div class="form-row">
                    <div class="field"><label>Personal Mobile</label><input type="text" id="m-phone" class="input" value="+91 98765 11223" required></div>
                    <div class="field"><label>Aadhaar Number</label><input type="text" id="m-aadhar" class="input" value="4589-2314-7890" required></div>
                    <div class="field"><label>PAN Number</label><input type="text" id="m-pan" class="input" value="ABCPJ4589K" required></div>
                </div>
                <div class="form-row">
                    <div class="field"><label>Bank Name</label><input type="text" id="m-bank-name" class="input" value="HDFC Bank" required></div>
                    <div class="field"><label>Bank Account Number</label><input type="text" id="m-bank-acc" class="input" value="50100234567890" required></div>
                    <div class="field"><label>IFSC Code</label><input type="text" id="m-bank-ifsc" class="input" value="HDFC0001234" required></div>
                </div>
                <div class="form-row">
                    <div class="field"><label>Residential Street Address</label><input type="text" id="m-street" class="input" value="No. 42, 8th Main, 4th Cross, Indiranagar" required></div>
                    <div class="field"><label>Emergency Contact (Name & Relationship)</label><input type="text" id="m-emg" class="input" value="Rajesh Smith (Spouse)" required></div>
                    <div class="field"><label>Emergency Phone</label><input type="text" id="m-emg-phone" class="input" value="+91 98765 99887" required></div>
                </div>
                <div style="display: flex; justify-content: flex-end; gap: 0.5rem; margin-top: 1rem;">
                    <button type="button" class="btn btn-secondary" onclick="closeEditPrivateModal()">Cancel</button>
                    <button type="submit" class="btn btn-primary">Save Changes</button>
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
            { id: 1, name: 'John Doe', email: 'john.doe@company.com', job: 'Senior Software Engineer', dept: 'Engineering', role: 'Employee', joining: '2024-03-15', loginId: 'OIJODO20240001', provisioned: true },
            { id: 2, name: 'Jane Smith', email: 'jane.smith@dayflow.org', job: 'Head of Human Resources', dept: 'Human Resources', role: 'Admin / HR', joining: '2023-01-10', loginId: 'OIJASM20230002', provisioned: true },
            { id: 3, name: 'Robert Taylor', email: 'robert.t@company.com', job: 'Product Manager', dept: 'Product', role: 'Employee', joining: '2025-06-01', loginId: 'OIROTA20250003', provisioned: false }
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

        const HOLIDAYS_AUG_2026 = {
            15: '🇮🇳 Independence Day',
            19: '🌸 Raksha Bandhan',
            26: '🦚 Janmashtami'
        };

        let state = {
            role: 'admin',
            currentEmployee: 'Jane Smith',
            isCheckedIn: false,
            activeCheckInTime: null,
            checkInTimestamp: null,
            tickerInterval: null,
            currentDocFilter: 'all',
            attendances: JSON.parse(localStorage.getItem('df_attendances')) || DEFAULT_ATTENDANCE,
            leaves: JSON.parse(localStorage.getItem('df_leaves')) || DEFAULT_LEAVE,
            employees: JSON.parse(localStorage.getItem('df_employees')) || DEFAULT_EMPLOYEES,
            documents: JSON.parse(localStorage.getItem('df_documents')) || DEFAULT_DOCUMENTS,
            payrolls: JSON.parse(localStorage.getItem('df_payrolls')) || DEFAULT_PAYROLL,
            adminProfile: JSON.parse(localStorage.getItem('df_admin_profile')) || {
                name: 'Jane Smith',
                role: 'Admin / HR',
                title: 'Head of Human Resources & Administration',
                dept: 'Human Resources',
                loginId: 'OIJASM20230002',
                email: 'jane.smith@dayflow.org',
                phone: '+91 98765 43212',
                joining: '2023-01-10',
                dob: '1990-06-15',
                gender: 'Female',
                nationality: 'Indian',
                marital: 'Married',
                aadhar: '4589-2314-7890',
                pan: 'ABCPJ4589K',
                passport: 'Z9876543',
                personalPhone: '+91 98765 11223',
                street: 'No. 42, 8th Main, 4th Cross, Indiranagar',
                city: 'Bangalore, Karnataka',
                pin: '560038',
                country: 'India',
                emgName: 'Rajesh Smith (Spouse)',
                emgPhone: '+91 98765 99887',
                bankName: 'HDFC Bank (Salary Account)',
                bankAcc: '50100234567890',
                bankIfsc: 'HDFC0001234',
                monthlyWage: 55000,
                struct: 'HR Specialist Base'
            }
        };

        function saveState() {
            localStorage.setItem('df_attendances', JSON.stringify(state.attendances));
            localStorage.setItem('df_leaves', JSON.stringify(state.leaves));
            localStorage.setItem('df_employees', JSON.stringify(state.employees));
            localStorage.setItem('df_documents', JSON.stringify(state.documents));
            localStorage.setItem('df_payrolls', JSON.stringify(state.payrolls));
            localStorage.setItem('df_admin_profile', JSON.stringify(state.adminProfile));
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

            if (tabId === 'profile') {
                renderAdminProfile();
            } else if (tabId === 'leave') {
                renderCalendar();
            }
        }

        function openProfileSection(secId) {
            document.querySelectorAll('.profile-subtab').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.profile-section').forEach(el => el.classList.remove('active'));

            const btn = document.getElementById('psubtab-btn-' + secId);
            if (btn) btn.classList.add('active');
            const sec = document.getElementById('psec-' + secId);
            if (sec) sec.classList.add('active');
        }

        function onRoleChange(role) {
            state.role = role;
            if (role === 'admin') {
                state.currentEmployee = 'Jane Smith';
                document.getElementById('nav-avatar').innerText = 'JS';
            } else {
                state.currentEmployee = 'John Doe';
                document.getElementById('nav-avatar').innerText = 'JD';
            }
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

        /* Leave Modal & Calendar actions */
        function openLeaveModal(prefilledDate) {
            document.getElementById('mleave-emp').value = state.currentEmployee;
            document.getElementById('mleave-type').value = 'paid';

            const defaultStart = prefilledDate || '2026-08-25';
            const defaultEnd = prefilledDate || '2026-08-26';
            document.getElementById('mleave-start').value = defaultStart;
            document.getElementById('mleave-end').value = defaultEnd;
            document.getElementById('mleave-reason').value = '';
            document.getElementById('mleave-file').value = '';

            calcLeaveDuration();
            document.getElementById('modal-leave-app').style.display = 'flex';
        }

        function closeLeaveModal() {
            document.getElementById('modal-leave-app').style.display = 'none';
        }

        function calcLeaveDuration() {
            const startVal = document.getElementById('mleave-start').value;
            const endVal = document.getElementById('mleave-end').value;

            if (startVal && endVal) {
                const s = new Date(startVal);
                const e = new Date(endVal);
                let diffDays = Math.ceil((e - s) / (1000 * 60 * 60 * 24)) + 1;
                if (diffDays <= 0) diffDays = 1;
                document.getElementById('mleave-duration-preview').innerText = `${diffDays} Working Day${diffDays > 1 ? 's' : ''}`;
            }
        }

        function handleLeaveModalSubmit(e) {
            e.preventDefault();
            const emp = document.getElementById('mleave-emp').value;
            const type = document.getElementById('mleave-type').value;
            const start = document.getElementById('mleave-start').value;
            const end = document.getElementById('mleave-end').value;
            const reason = document.getElementById('mleave-reason').value;

            const days = Math.max(1, Math.ceil((new Date(end) - new Date(start)) / (1000 * 60 * 60 * 24)) + 1);

            state.leaves.unshift({
                id: Date.now(),
                employee: emp,
                type: type,
                startDate: start,
                endDate: end,
                days: days,
                remarks: reason,
                status: 'pending',
                adminComments: ''
            });

            saveState();
            closeLeaveModal();
            renderLeaves();
            renderCalendar();
            renderDashboard();
            alert('🎉 Time off request submitted successfully! Pending HR approval.');
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

        /* Calendar Render (August 2026) */
        function renderCalendar() {
            const container = document.getElementById('cal-grid-tiles');
            if (!container) return;

            // August 2026 starts on Saturday (Aug 1).
            // In Mon-Sun grid: Mon=0, Tue=1, Wed=2, Thu=3, Fri=4, Sat=5, Sun=6.
            // Empty leading padding cells = 5.
            let html = '';
            for (let pad = 0; pad < 5; pad++) {
                html += `<div class="cal-cell weekend" style="opacity: 0.25; cursor: default;"></div>`;
            }

            for (let day = 1; day <= 31; day++) {
                const dayStr = day < 10 ? `0${day}` : `${day}`;
                const dateStr = `2026-08-${dayStr}`;

                // Calculate day of week
                const dObj = new Date(2026, 7, day);
                const dayOfWeek = dObj.getDay(); // 0 is Sun, 6 is Sat
                const isWeekend = (dayOfWeek === 0 || dayOfWeek === 6);

                const holidayName = HOLIDAYS_AUG_2026[day];

                // Check leaves
                const matchedLeave = state.leaves.find(l => {
                    const s = l.startDate;
                    const e = l.endDate;
                    return dateStr >= s && dateStr <= e;
                });

                let cellClasses = 'cal-cell';
                if (isWeekend) cellClasses += ' weekend';
                if (holidayName) cellClasses += ' holiday';
                if (matchedLeave) cellClasses += ' leave-day';

                let tagHtml = '';
                if (holidayName) {
                    tagHtml = `<span class="cal-tag tag-holiday" title="${holidayName}">${holidayName}</span>`;
                } else if (matchedLeave) {
                    const tagStyle = matchedLeave.status === 'approved' ? 'tag-leave' : 'tag-holiday';
                    tagHtml = `<span class="cal-tag ${tagStyle}" title="${matchedLeave.employee} (${matchedLeave.type})">✈️ ${matchedLeave.employee.split(' ')[0]} - ${matchedLeave.type.toUpperCase()}</span>`;
                }

                html += `
                    <div class="${cellClasses}" onclick="openLeaveModal('${dateStr}')" title="Click to apply leave on August ${day}, 2026">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <strong style="color:${isWeekend?'#f87171':'inherit'};">${day}</strong>
                            ${holidayName ? '<span style="font-size:0.65rem; color:#fbbf24;">★</span>' : ''}
                        </div>
                        <div>${tagHtml}</div>
                    </div>
                `;
            }

            container.innerHTML = html;
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

        /* Payroll Modal & Actions */
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

                    if (pay.employee === 'Jane Smith') {
                        state.adminProfile.monthlyWage = base;
                        state.adminProfile.struct = struct;
                    }
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

        /* Edit Private Info Modal Actions */
        function openEditPrivateModal() {
            const p = state.adminProfile;
            document.getElementById('m-dob').value = p.dob;
            document.getElementById('m-gender').value = p.gender;
            document.getElementById('m-marital').value = p.marital;
            document.getElementById('m-phone').value = p.personalPhone;
            document.getElementById('m-aadhar').value = p.aadhar;
            document.getElementById('m-pan').value = p.pan;
            document.getElementById('m-bank-name').value = p.bankName;
            document.getElementById('m-bank-acc').value = p.bankAcc;
            document.getElementById('m-bank-ifsc').value = p.bankIfsc;
            document.getElementById('m-street').value = p.street;
            document.getElementById('m-emg').value = p.emgName;
            document.getElementById('m-emg-phone').value = p.emgPhone;

            document.getElementById('private-info-modal').style.display = 'flex';
        }

        function closeEditPrivateModal() {
            document.getElementById('private-info-modal').style.display = 'none';
        }

        function handleSavePrivateInfo(e) {
            e.preventDefault();
            const p = state.adminProfile;
            p.dob = document.getElementById('m-dob').value;
            p.gender = document.getElementById('m-gender').value;
            p.marital = document.getElementById('m-marital').value;
            p.personalPhone = document.getElementById('m-phone').value;
            p.aadhar = document.getElementById('m-aadhar').value;
            p.pan = document.getElementById('m-pan').value;
            p.bankName = document.getElementById('m-bank-name').value;
            p.bankAcc = document.getElementById('m-bank-acc').value;
            p.bankIfsc = document.getElementById('m-bank-ifsc').value;
            p.street = document.getElementById('m-street').value;
            p.emgName = document.getElementById('m-emg').value;
            p.emgPhone = document.getElementById('m-emg-phone').value;

            saveState();
            closeEditPrivateModal();
            renderAdminProfile();
            alert('Admin Private Information updated successfully!');
        }

        /* Render Admin Profile */
        function renderAdminProfile() {
            const p = state.adminProfile;
            const wage = p.monthlyWage || 55000;
            const basic = Math.round(wage * 0.50);
            const hra = Math.round(basic * 0.50);
            const stdAllow = Math.round(wage * 0.1667);
            const bonus = Math.round(wage * 0.0833);
            const lta = Math.round(wage * 0.0833);
            const pf = Math.round(basic * 0.12);
            const pt = 200;
            const insurance = 1000;
            const totalEarnings = basic + hra + stdAllow + bonus + lta;
            const totalDeduct = pf + pt + insurance;
            const netSalary = totalEarnings - totalDeduct;

            document.getElementById('prof-hero-name').innerText = p.name;
            document.getElementById('prof-hero-title').innerText = `${p.title} • ${p.dept}`;
            document.getElementById('prof-hero-login').innerText = `🔑 ${p.loginId}`;
            document.getElementById('prof-hero-email').innerText = `✉️ ${p.email}`;
            document.getElementById('prof-hero-phone').innerText = `📞 ${p.phone}`;
            document.getElementById('prof-hero-joined').innerText = `📅 Joined Jan 10, 2023`;

            document.getElementById('prof-dob').innerText = p.dob;
            document.getElementById('prof-gender').innerText = p.gender;
            document.getElementById('prof-nationality').innerText = p.nationality;
            document.getElementById('prof-marital').innerText = p.marital;
            document.getElementById('prof-aadhar').innerText = p.aadhar;
            document.getElementById('prof-pan').innerText = p.pan;
            document.getElementById('prof-passport').innerText = p.passport;
            document.getElementById('prof-personal-phone').innerText = p.personalPhone;
            document.getElementById('prof-addr-street').innerText = p.street;
            document.getElementById('prof-addr-city').innerText = p.city;
            document.getElementById('prof-addr-pin').innerText = p.pin;
            document.getElementById('prof-addr-country').innerText = p.country;
            document.getElementById('prof-emg-name').innerText = p.emgName;
            document.getElementById('prof-emg-phone').innerText = p.emgPhone;
            document.getElementById('prof-bank-name').innerText = p.bankName;
            document.getElementById('prof-bank-acc').innerText = p.bankAcc;
            document.getElementById('prof-bank-ifsc').innerText = p.bankIfsc;

            document.getElementById('prof-sal-wage').innerText = formatCurrency(wage);
            document.getElementById('prof-sal-ctc').innerText = formatCurrency(wage * 12);
            document.getElementById('prof-sal-net').innerText = formatCurrency(netSalary);
            document.getElementById('prof-sal-struct').innerText = p.struct;
            document.getElementById('prof-comp-basic').innerText = formatCurrency(basic);
            document.getElementById('prof-comp-hra').innerText = formatCurrency(hra);
            document.getElementById('prof-comp-std').innerText = formatCurrency(stdAllow);
            document.getElementById('prof-comp-bonus').innerText = formatCurrency(bonus);
            document.getElementById('prof-comp-lta').innerText = formatCurrency(lta);
            document.getElementById('prof-comp-pf').innerText = `- ${formatCurrency(pf)}`;
            document.getElementById('prof-comp-deduct-total').innerText = `- ${formatCurrency(totalDeduct)}`;
        }

        /* Render Dashboard */
        function renderDashboard() {
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

            const tbodyAtt = document.getElementById('dash-tbl-today-attendance');
            tbodyAtt.innerHTML = state.attendances.slice(0, 5).map(a => `
                <tr>
                    <td><strong>${a.employee}</strong></td>
                    <td>${a.checkIn}</td>
                    <td>${a.checkOut}</td>
                    <td><span class="badge ${a.status==='present'?'badge-green':a.status==='half_day'?'badge-amber':'badge-red'}">${a.status.toUpperCase()}</span></td>
                </tr>
            `).join('');

            filterDashboardEmployees();
        }

        function filterDashboardEmployees() {
            const query = (document.getElementById('dash-search-emp')?.value || '').toLowerCase();
            const tbodyEmp = document.getElementById('dash-tbl-employees');
            const filtered = state.employees.filter(e => e.name.toLowerCase().includes(query) || e.job.toLowerCase().includes(query) || e.dept.toLowerCase().includes(query));

            tbodyEmp.innerHTML = filtered.map(e => `
                <tr onclick="openTab('profile')" style="cursor:pointer;" title="Click to view profile">
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
                        <td><span class="badge badge-purple">${l.type.toUpperCase()}</span></td>
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
                <div class="emp-card" onclick="openTab('profile')">
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
                        `<button class="btn btn-secondary" style="font-size:0.75rem; padding:0.25rem 0.5rem; margin-top:0.35rem;" onclick="event.stopPropagation(); handleProvision(${e.id})">Provision Account</button>`}
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
            renderAdminProfile();
            renderCalendar();
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
