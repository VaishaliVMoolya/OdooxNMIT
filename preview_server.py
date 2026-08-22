# -*- coding: utf-8 -*-
"""
Dayflow HRMS - Unified Live UI Preview Server
Odoo x NMIT Hackathon
All-in-One Dashboard, Employees, Attendance, Time Off, Documents, Payroll, Admin Profile, and Email & Notification Alert System
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import webbrowser

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dayflow HRMS — Workspace & Notification System</title>
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
            font-weight: 600;
        }

        .nav-right {
            display: flex;
            align-items: center;
            gap: 0.85rem;
        }

        .nav-btn-icon {
            position: relative;
            background: var(--bg-card);
            border: 1px solid var(--border-line);
            color: var(--text-main);
            width: 36px;
            height: 36px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            font-size: 1.1rem;
            transition: all 0.2s ease;
        }

        .nav-btn-icon:hover {
            background: var(--border-line);
            border-color: var(--accent-purple-hover);
        }

        .notif-badge-count {
            position: absolute;
            top: -4px;
            right: -4px;
            background: var(--accent-red);
            color: #fff;
            font-size: 0.65rem;
            font-weight: 800;
            border-radius: 9999px;
            padding: 2px 5px;
            border: 2px solid var(--bg-surface);
        }

        .avatar {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            background: linear-gradient(135deg, #ec4899, var(--accent-purple));
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.8rem;
            font-weight: 700;
            color: #fff;
        }

        .nav-user-info {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.85rem;
            color: var(--text-main);
        }

        .nav-signout-btn {
            background: transparent;
            border: 1px solid var(--border-line);
            color: var(--text-muted);
            padding: 0.3rem 0.65rem;
            border-radius: 6px;
            font-size: 0.78rem;
            cursor: pointer;
            transition: all 0.15s ease;
        }

        .nav-signout-btn:hover {
            border-color: var(--accent-red);
            color: #f87171;
            background: rgba(239, 68, 68, 0.08);
        }

        /* Container & Grid */
        .container {
            max-width: 1240px;
            margin: 0 auto;
            padding: 1.5rem;
            width: 100%;
            flex: 1;
        }

        .tab-panel {
            display: none;
            animation: fadeIn 0.15s ease;
        }

        .tab-panel.active {
            display: block;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(4px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .header-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
        }

        .header-title {
            font-size: 1.5rem;
            font-weight: 700;
            color: #fff;
        }

        .header-sub {
            font-size: 0.85rem;
            color: var(--text-muted);
            margin-top: 0.25rem;
        }

        /* Buttons & Forms */
        .btn {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            padding: 0.5rem 1rem;
            border-radius: 6px;
            font-size: 0.85rem;
            font-weight: 600;
            cursor: pointer;
            border: none;
            transition: all 0.15s ease;
            text-decoration: none;
        }

        .btn-primary {
            background-color: var(--accent-purple);
            color: #fff;
        }

        .btn-primary:hover {
            background-color: var(--accent-purple-hover);
        }

        .btn-secondary {
            background-color: var(--bg-card);
            color: var(--text-main);
            border: 1px solid var(--border-line);
        }

        .btn-secondary:hover {
            background-color: var(--border-line);
        }

        .btn-success { background-color: var(--accent-green); color: #fff; }
        .btn-danger { background-color: var(--accent-red); color: #fff; }
        .btn-warning { background-color: var(--accent-amber); color: #000; }

        .btn:disabled {
            opacity: 0.45;
            cursor: not-allowed;
        }

        .card {
            background-color: var(--bg-surface);
            border: 1px solid var(--border-line);
            border-radius: 8px;
            padding: 1.25rem;
            margin-bottom: 1.25rem;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
            gap: 1rem;
            margin-bottom: 1.5rem;
        }

        .stat-box {
            background-color: var(--bg-surface);
            border: 1px solid var(--border-line);
            border-radius: 8px;
            padding: 1rem 1.25rem;
        }

        .stat-box .metric-label {
            font-size: 0.8rem;
            color: var(--text-muted);
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.03em;
        }

        .stat-box .num {
            font-size: 1.5rem;
            font-weight: 700;
            margin-top: 0.35rem;
            color: #fff;
        }

        /* KPI Grid Cards */
        .kpi-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
            gap: 1rem;
            margin-bottom: 1.5rem;
        }

        .kpi-card {
            background: var(--bg-surface);
            border: 1px solid var(--border-line);
            border-radius: 8px;
            padding: 1.2rem;
            display: flex;
            align-items: center;
            gap: 1rem;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .kpi-card:hover {
            transform: translateY(-2px);
            border-color: var(--accent-purple-hover);
        }

        .kpi-icon-box {
            width: 48px;
            height: 48px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            flex-shrink: 0;
        }

        .kpi-blue .kpi-icon-box { background: rgba(59, 130, 246, 0.15); color: #60a5fa; }
        .kpi-green .kpi-icon-box { background: rgba(16, 185, 129, 0.15); color: #34d399; }
        .kpi-amber .kpi-icon-box { background: rgba(245, 158, 11, 0.15); color: #fbbf24; }
        .kpi-red .kpi-icon-box { background: rgba(239, 68, 68, 0.15); color: #f87171; }

        .kpi-label { font-size: 0.8rem; color: var(--text-muted); text-transform: uppercase; }
        .kpi-val { font-size: 1.45rem; font-weight: 700; color: #fff; margin: 2px 0; }
        .kpi-sub { font-size: 0.75rem; color: var(--text-muted); }

        /* Tables */
        .table-wrap {
            overflow-x: auto;
            border-radius: 6px;
            border: 1px solid var(--border-line);
        }

        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.85rem;
            text-align: left;
        }

        th {
            background-color: var(--bg-card);
            color: var(--text-muted);
            font-weight: 600;
            padding: 0.75rem 1rem;
            border-bottom: 1px solid var(--border-line);
        }

        td {
            padding: 0.75rem 1rem;
            border-bottom: 1px solid var(--border-line);
            color: var(--text-main);
        }

        tr:last-child td {
            border-bottom: none;
        }

        tr:hover td {
            background-color: rgba(255, 255, 255, 0.02);
        }

        .badge {
            display: inline-flex;
            align-items: center;
            padding: 0.2rem 0.55rem;
            border-radius: 9999px;
            font-size: 0.72rem;
            font-weight: 600;
            text-transform: uppercase;
        }

        .badge-green { background-color: rgba(16, 185, 129, 0.15); color: #34d399; }
        .badge-amber { background-color: rgba(245, 158, 11, 0.15); color: #fbbf24; }
        .badge-red { background-color: rgba(239, 68, 68, 0.15); color: #f87171; }
        .badge-blue { background-color: rgba(59, 130, 246, 0.15); color: #60a5fa; }
        .badge-purple { background-color: rgba(113, 75, 103, 0.25); color: #d8b4e2; }

        /* Input Controls */
        .form-row {
            display: flex;
            gap: 1rem;
            margin-bottom: 1rem;
            flex-wrap: wrap;
        }

        .field {
            flex: 1;
            min-width: 180px;
            display: flex;
            flex-direction: column;
            gap: 0.35rem;
        }

        .field label {
            font-size: 0.8rem;
            color: var(--text-muted);
            font-weight: 500;
        }

        .input {
            background-color: var(--bg-input);
            border: 1px solid var(--border-line);
            color: var(--text-main);
            padding: 0.5rem 0.75rem;
            border-radius: 6px;
            font-size: 0.85rem;
            outline: none;
            transition: border-color 0.15s ease;
        }

        .input:focus {
            border-color: var(--accent-purple-hover);
        }

        /* Modals */
        .modal {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: rgba(0, 0, 0, 0.7);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 100;
            backdrop-filter: blur(4px);
        }

        .modal-card {
            background-color: var(--bg-surface);
            border: 1px solid var(--border-line);
            border-radius: 8px;
            width: 90%;
            max-width: 580px;
            padding: 1.5rem;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
        }

        /* Banner & Ticker */
        .banner {
            background: linear-gradient(135deg, var(--bg-card), var(--bg-surface));
            border: 1px solid var(--border-line);
            border-radius: 8px;
            padding: 1.25rem;
            margin-bottom: 1.25rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .banner-metrics {
            display: flex;
            gap: 2rem;
            align-items: center;
        }

        .banner-metrics .metric {
            display: flex;
            flex-direction: column;
            gap: 0.2rem;
        }

        .banner-metrics .metric-val {
            font-size: 1.25rem;
            font-weight: 700;
            color: #fff;
            display: flex;
            align-items: center;
            gap: 0.4rem;
        }

        .dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            display: inline-block;
        }

        .dot.green { background-color: var(--accent-green); box-shadow: 0 0 8px var(--accent-green); }
        .dot.red { background-color: var(--accent-red); }

        /* Employee Grid */
        .emp-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
            gap: 1rem;
        }

        .emp-card {
            background-color: var(--bg-surface);
            border: 1px solid var(--border-line);
            border-radius: 8px;
            padding: 1.25rem;
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
            transition: all 0.2s ease;
        }

        .emp-card:hover {
            border-color: var(--accent-purple-hover);
            transform: translateY(-2px);
        }

        .emp-head {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .emp-head .avatar {
            width: 44px;
            height: 44px;
            font-size: 1.1rem;
        }

        .emp-name { font-weight: 700; color: #fff; font-size: 0.95rem; }
        .emp-job { font-size: 0.8rem; color: var(--text-muted); }

        /* Profile Excalidraw Style */
        .profile-hero {
            background: linear-gradient(135deg, var(--bg-surface), var(--bg-card));
            border: 1px solid var(--border-line);
            border-radius: 12px;
            padding: 1.75rem;
            margin-bottom: 1.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 1.5rem;
        }

        .profile-hero-left {
            display: flex;
            align-items: center;
            gap: 1.5rem;
        }

        .profile-avatar-lg {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            background: linear-gradient(135deg, #a78bfa, var(--accent-purple));
            color: #fff;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2rem;
            font-weight: 800;
            border: 3px solid var(--border-line);
        }

        .profile-chips {
            display: flex;
            gap: 0.5rem;
            margin-top: 0.5rem;
            flex-wrap: wrap;
        }

        .chip {
            background-color: var(--bg-input);
            border: 1px solid var(--border-line);
            border-radius: 6px;
            padding: 0.2rem 0.6rem;
            font-size: 0.75rem;
            color: var(--text-muted);
        }

        .profile-subtabs {
            display: flex;
            gap: 0.5rem;
            border-bottom: 1px solid var(--border-line);
            margin-bottom: 1.5rem;
        }

        .profile-subtab {
            padding: 0.65rem 1.25rem;
            font-size: 0.9rem;
            font-weight: 600;
            color: var(--text-muted);
            cursor: pointer;
            border-bottom: 2px solid transparent;
            transition: all 0.15s ease;
        }

        .profile-subtab.active {
            color: var(--accent-purple-hover);
            border-bottom-color: var(--accent-purple-hover);
        }

        .profile-section { display: none; }
        .profile-section.active { display: block; animation: fadeIn 0.15s ease; }

        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 1.25rem;
        }

        .info-item .lbl {
            font-size: 0.75rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }

        .info-item .val {
            font-size: 0.95rem;
            color: var(--text-main);
            font-weight: 600;
            margin-top: 0.25rem;
        }

        .two-col-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1.25rem;
        }

        @media (max-width: 768px) {
            .two-col-grid { grid-template-columns: 1fr; }
        }

        .filter-group {
            display: flex;
            gap: 0.4rem;
        }

        .pill-btn {
            background-color: var(--bg-card);
            border: 1px solid var(--border-line);
            color: var(--text-muted);
            padding: 0.3rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.78rem;
            font-weight: 500;
            cursor: pointer;
        }

        .pill-btn.active {
            background-color: var(--accent-purple);
            color: #fff;
            border-color: var(--accent-purple);
        }

        /* Calendar Styles */
        .cal-layout {
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 1.25rem;
        }

        @media (max-width: 900px) {
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
            gap: 4px;
        }

        .cal-day-name {
            text-align: center;
            font-size: 0.75rem;
            font-weight: 700;
            color: var(--text-muted);
            padding: 0.4rem 0;
            background-color: var(--bg-card);
            border-radius: 4px;
        }

        .cal-cell {
            background-color: var(--bg-surface);
            border: 1px solid var(--border-line);
            border-radius: 6px;
            min-height: 64px;
            padding: 0.35rem 0.45rem;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            font-size: 0.8rem;
            cursor: pointer;
            transition: all 0.15s ease;
        }

        .cal-cell:hover {
            border-color: var(--accent-purple-hover);
            background-color: rgba(255, 255, 255, 0.02);
        }

        .cal-cell.weekend {
            background-color: rgba(0, 0, 0, 0.2);
        }

        .cal-cell.holiday {
            border-color: rgba(245, 158, 11, 0.5);
            background-color: rgba(245, 158, 11, 0.08);
        }

        .cal-cell.leave-day {
            border-color: rgba(113, 75, 103, 0.7);
            background-color: rgba(113, 75, 103, 0.18);
        }

        .cal-tag {
            font-size: 0.65rem;
            padding: 1px 4px;
            border-radius: 3px;
            margin-top: 2px;
            display: block;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .tag-holiday { background: rgba(245, 158, 11, 0.25); color: #fbbf24; }
        .tag-leave { background: rgba(113, 75, 103, 0.4); color: #d8b4e2; }

        .holiday-list {
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
        }

        .holiday-item {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            padding: 0.65rem 0.85rem;
            background: var(--bg-card);
            border: 1px solid var(--border-line);
            border-radius: 6px;
        }

        .holiday-date-badge {
            background: rgba(245, 158, 11, 0.15);
            color: #fbbf24;
            padding: 0.3rem 0.5rem;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 700;
            text-align: center;
            min-width: 58px;
        }

        .holiday-name { font-weight: 600; font-size: 0.85rem; color: #fff; }
        .holiday-type { font-size: 0.75rem; color: var(--text-muted); }

        /* Toast Notifications */
        #toast-container {
            position: fixed;
            bottom: 1.5rem;
            right: 1.5rem;
            display: flex;
            flex-direction: column;
            gap: 0.6rem;
            z-index: 200;
        }

        .toast-msg {
            background: var(--bg-surface);
            border: 1px solid var(--accent-purple-hover);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.6);
            border-radius: 8px;
            padding: 0.85rem 1.15rem;
            display: flex;
            align-items: center;
            gap: 0.75rem;
            max-width: 380px;
            animation: slideUp 0.25s ease;
        }

        @keyframes slideUp {
            from { opacity: 0; transform: translateY(12px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Auth Wall Modal */
        #auth-wall {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(15, 17, 23, 0.95);
            backdrop-filter: blur(8px);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1000;
        }

        #auth-wall.hidden {
            display: none;
        }

        .auth-card {
            background: var(--bg-surface);
            border: 1px solid var(--border-line);
            border-radius: 12px;
            padding: 2.25rem 2rem;
            width: 100%;
            max-width: 440px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
        }
    </style>
</head>
<body>

    <!-- AUTH WALL MODAL -->
    <div id="auth-wall">
        <div class="auth-card">
            <div style="text-align: center; margin-bottom: 1.5rem;">
                <div style="display: inline-flex; align-items: center; gap: 0.6rem; margin-bottom: 0.75rem;">
                    <span class="brand-badge" style="font-size: 1.1rem; padding: 0.35rem 0.75rem;">DF</span>
                    <h2 style="font-size: 1.35rem; font-weight: 800; color: #fff;">Dayflow HRMS</h2>
                </div>
                <p style="font-size: 0.85rem; color: var(--text-muted);">Sign in to access your HR management workspace</p>
            </div>

            <div id="auth-error" style="display: none; background: rgba(239, 68, 68, 0.15); border: 1px solid rgba(239, 68, 68, 0.4); color: #f87171; padding: 0.6rem 0.9rem; border-radius: 6px; font-size: 0.82rem; margin-bottom: 1.25rem; text-align: center;">
                Invalid credentials. Please verify username and password.
            </div>

            <form id="auth-login-form" onsubmit="handleLogin(event)">
                <div class="field" style="margin-bottom: 1rem;">
                    <label>Username / Login ID</label>
                    <input type="text" id="auth-login-id" class="input" placeholder="e.g. admin or employee username" required autocomplete="username">
                </div>
                <div class="field" style="margin-bottom: 1.25rem;">
                    <label>Password</label>
                    <input type="password" id="auth-password" class="input" placeholder="Enter password" required autocomplete="current-password">
                </div>
                <button type="submit" class="btn btn-primary" style="width: 100%; justify-content: center; padding: 0.65rem; font-size: 0.95rem;">
                    Sign In
                </button>
            </form>

            <div style="margin-top: 1.25rem; padding-top: 1rem; border-top: 1px solid var(--border-line); font-size: 0.78rem; color: var(--text-muted); line-height: 1.5;">
                <div style="font-weight: 600; color: #fff; margin-bottom: 0.35rem;">Demo Credentials:</div>
                <div>🛡️ <strong>Admin / HR:</strong> <code>admin</code> / <code>admin123</code></div>
                <div>👤 <strong>Employee:</strong> <code>john</code> / <code>john123</code></div>
            </div>
        </div>
    </div>

    <!-- Top Navbar -->
    <nav class="navbar">
        <a href="#" class="brand">
            <span class="brand-badge">DF</span> Dayflow HRMS
        </a>
        <ul class="nav-links" id="nav-links-list">
            <li class="nav-tab active" id="tab-btn-dashboard" onclick="openTab('dashboard')">Dashboard</li>
            <li class="nav-tab" id="tab-btn-attendance" onclick="openTab('attendance')">Attendance</li>
            <li class="nav-tab" id="tab-btn-leave" onclick="openTab('leave')">Time Off</li>
            <li class="nav-tab nav-admin-only" id="tab-btn-employees" onclick="openTab('employees')">Employees</li>
            <li class="nav-tab" id="tab-btn-documents" onclick="openTab('documents')">Documents</li>
            <li class="nav-tab nav-admin-only" id="tab-btn-payroll" onclick="openTab('payroll')">Payroll</li>
            <li class="nav-tab" id="tab-btn-profile" onclick="state.viewingEmployeeId = null; openTab('profile')">My Profile</li>
        </ul>
        <div class="nav-right">
            <!-- In-App Notification Bell -->
            <div class="nav-btn-icon" onclick="toggleNotificationModal()" title="View Email & In-App Notifications">
                <span>🔔</span>
                <span class="notif-badge-count" id="notif-count">0</span>
            </div>
            <div class="nav-user-info" id="nav-user-info">
                <div class="avatar" style="width:30px;height:30px;font-size:0.78rem;" id="nav-avatar">JS</div>
                <strong id="nav-user-name">Jane Smith</strong>
                <span id="nav-user-role-badge" class="badge badge-purple" style="font-size:0.7rem;">Admin</span>
            </div>
            <button class="nav-signout-btn" onclick="handleSignOut()">Sign Out</button>
        </div>
    </nav>

    <!-- Toast Notification Container -->
    <div id="toast-container"></div>

    <div class="container">

        <!-- ADMIN DASHBOARD TAB -->
        <div id="panel-dashboard" class="tab-panel active">
            <div class="header-row">
                <div>
                    <h1 class="header-title">Dayflow HRMS Management Console</h1>
                    <p class="header-sub">Live organizational metrics, pending approvals, and email alert activity</p>
                </div>
                <div style="display:flex; gap:0.5rem;">
                    <button class="btn btn-primary" onclick="toggleNotificationModal()">🔔 Notification Center</button>
                    <button class="btn btn-secondary" onclick="resetData()">↺ Refresh</button>
                </div>
            </div>

            <!-- Email & System Health Banner -->
            <div class="card" style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.12), rgba(32, 36, 51, 0.95)); border: 1px solid rgba(16, 185, 129, 0.35); padding: 1rem 1.25rem; margin-bottom: 1.25rem;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div style="display:flex; align-items:center; gap:0.85rem;">
                        <div style="font-size:1.5rem;">✉️</div>
                        <div>
                            <div style="font-weight:700; font-size:0.95rem; color:#fff; display:flex; align-items:center; gap:0.5rem;">
                                <span>Dayflow Email & Notification Engine:</span>
                                <span class="badge badge-green">ACTIVE (Odoo Mail Server / Fallback Safe)</span>
                            </div>
                            <p style="font-size:0.8rem; color:var(--text-muted); margin-top:2px;">
                                Automated alerts active for: <strong>Login Security Alerts</strong>, <strong>Account Creation Invites</strong>, and <strong>Time Off Decision Workflow</strong>.
                            </p>
                        </div>
                    </div>
                    <button class="btn btn-secondary" style="font-size:0.75rem; padding:0.3rem 0.75rem;" onclick="toggleNotificationModal()">View Notification Log</button>
                </div>
            </div>

            <!-- Hero KPI Cards -->
            <div class="kpi-grid">
                <div class="kpi-card kpi-blue" onclick="openTab('employees')">
                    <div class="kpi-icon-box">👥</div>
                    <div>
                        <div class="kpi-label">Total Employees</div>
                        <div class="kpi-val" id="dash-kpi-employees">0</div>
                        <div class="kpi-sub" id="dash-badge-total-emp">Active in Directory</div>
                    </div>
                </div>

                <div class="kpi-card kpi-green" onclick="openTab('attendance')">
                    <div class="kpi-icon-box">⏱</div>
                    <div>
                        <div class="kpi-label">Present Today</div>
                        <div class="kpi-val" id="dash-kpi-present">0</div>
                        <div class="kpi-sub" id="dash-badge-present-count">Active Today</div>
                    </div>
                </div>

                <div class="kpi-card kpi-amber" onclick="openTab('leave')">
                    <div class="kpi-icon-box">🌴</div>
                    <div>
                        <div class="kpi-label">On Leave Today</div>
                        <div class="kpi-val" id="dash-kpi-on-leave">0</div>
                        <div class="kpi-sub">Approved Time Off</div>
                    </div>
                </div>

                <div class="kpi-card kpi-red" onclick="openTab('leave')">
                    <div class="kpi-icon-box">⏳</div>
                    <div>
                        <div class="kpi-label">Pending Requests</div>
                        <div class="kpi-val" id="dash-kpi-pending">0</div>
                        <div class="kpi-sub" id="dash-badge-pending-count">Awaiting Review</div>
                    </div>
                </div>
            </div>

            <!-- Decision Hub: Pending Leaves -->
            <div class="card" style="border-left: 4px solid var(--accent-purple-hover);">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 0.9rem;">
                    <div>
                        <h3 style="font-size: 1.05rem; color:#fff;">🛡️ Pending Time Off Applications (HR Decision Hub)</h3>
                        <p style="font-size: 0.8rem; color:var(--text-muted); margin-top:2px;">Decisions update employee records & trigger automated email notifications</p>
                    </div>
                    <button class="btn btn-secondary" style="font-size: 0.8rem;" onclick="openTab('leave')">View Full Queue</button>
                </div>
                <div class="table-wrap">
                    <table>
                        <thead>
                            <tr>
                                <th>Employee</th>
                                <th>Type</th>
                                <th>Dates</th>
                                <th>Reason</th>
                                <th style="text-align: right;">Action</th>
                            </tr>
                        </thead>
                        <tbody id="dash-tbl-pending-leaves"></tbody>
                    </table>
                </div>
            </div>

            <!-- Two Column Section -->
            <div class="two-col-grid">
                <div class="card">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 0.9rem;">
                        <h3 style="font-size: 1.05rem;">Today's Attendance Overview</h3>
                        <button class="btn btn-secondary" style="font-size: 0.75rem;" onclick="openTab('attendance')">View All</button>
                    </div>
                    <div class="table-wrap">
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
                        <h3 style="font-size: 1.05rem;">Employee Directory Preview</h3>
                        <input type="text" id="dash-search-emp" class="input" placeholder="Search by name/dept..." style="font-size:0.78rem; padding:0.25rem 0.5rem;" oninput="filterDashboardEmployees()">
                    </div>
                    <div class="table-wrap">
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

        <!-- EMPLOYEE DASHBOARD PANEL -->
        <div id="panel-emp-dashboard" class="tab-panel">
            <div class="header-row">
                <div>
                    <h1 class="header-title" id="emp-dash-greeting">Welcome, John Doe</h1>
                    <p class="header-sub" id="emp-dash-sub">Your personal HR summary for today</p>
                </div>
                <button class="btn btn-secondary" onclick="openTab('attendance')">📋 View Full Attendance</button>
            </div>

            <!-- Employee KPI Cards -->
            <div class="kpi-grid" style="grid-template-columns: repeat(auto-fill,minmax(200px,1fr));">
                <div class="kpi-card kpi-green">
                    <div class="kpi-icon-box">⏱</div>
                    <div>
                        <div class="kpi-label">Today's Status</div>
                        <div class="kpi-val" id="emp-dash-status">Not Checked In</div>
                        <div class="kpi-sub" id="emp-dash-checkin-time" style="color:#34d399;">--:--</div>
                    </div>
                </div>
                <div class="kpi-card kpi-blue">
                    <div class="kpi-icon-box">📅</div>
                    <div>
                        <div class="kpi-label">Paid Leave Left</div>
                        <div class="kpi-val" id="emp-dash-paid-bal">24</div>
                        <div class="kpi-sub" style="color:#60a5fa;">days remaining</div>
                    </div>
                </div>
                <div class="kpi-card kpi-amber">
                    <div class="kpi-icon-box">🏥</div>
                    <div>
                        <div class="kpi-label">Sick Leave Left</div>
                        <div class="kpi-val" id="emp-dash-sick-bal">7</div>
                        <div class="kpi-sub" style="color:#fbbf24;">days remaining</div>
                    </div>
                </div>
                <div class="kpi-card kpi-red">
                    <div class="kpi-icon-box">⏳</div>
                    <div>
                        <div class="kpi-label">Pending Requests</div>
                        <div class="kpi-val" id="emp-dash-pending">0</div>
                        <div class="kpi-sub" style="color:#f87171;">awaiting HR review</div>
                    </div>
                </div>
            </div>

            <!-- Quick Actions -->
            <div class="card">
                <h3 style="font-size:1rem;margin-bottom:1rem;">⚡ Quick Actions</h3>
                <div style="display:flex;gap:0.75rem;flex-wrap:wrap;">
                    <button class="btn btn-primary" onclick="openTab('attendance')">🕐 Check In / Check Out</button>
                    <button class="btn btn-secondary" onclick="openTab('leave')">📅 Apply for Leave</button>
                    <button class="btn btn-secondary" onclick="openTab('documents')">📎 Upload Document</button>
                    <button class="btn btn-secondary" onclick="openTab('profile')">👤 My Profile</button>
                </div>
            </div>

            <!-- Recent Leave Requests -->
            <div class="card">
                <h3 style="font-size:1rem;margin-bottom:1rem;">📋 My Recent Leave Requests</h3>
                <div class="table-wrap">
                    <table>
                        <thead>
                            <tr><th>Type</th><th>Start</th><th>End</th><th>Days</th><th>Reason</th><th>Status</th></tr>
                        </thead>
                        <tbody id="emp-dash-leave-tbl"></tbody>
                    </table>
                </div>
            </div>

            <!-- Recent Attendance -->
            <div class="card">
                <h3 style="font-size:1rem;margin-bottom:1rem;">📆 Recent Attendance (Last 5 Days)</h3>
                <div class="table-wrap">
                    <table>
                        <thead>
                            <tr><th>Date</th><th>Check In</th><th>Check Out</th><th>Status</th><th>Worked Hours</th></tr>
                        </thead>
                        <tbody id="emp-dash-att-tbl"></tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- PROFILE TAB (Admin & Employee) -->
        <div id="panel-profile" class="tab-panel">
            <div class="profile-hero">
                <div class="profile-hero-left">
                    <div class="profile-avatar-lg" id="prof-hero-avatar">--</div>
                    <div>
                        <div style="display:flex; align-items:center; gap:0.6rem;">
                            <h1 style="font-size: 1.45rem; font-weight: 800;" id="prof-hero-name">--</h1>
                            <span class="badge badge-purple" id="prof-hero-badge">--</span>
                            <span class="badge badge-green">Active</span>
                        </div>
                        <p style="font-size: 0.9rem; color: var(--text-muted); margin-top: 2px;" id="prof-hero-title">--</p>
                        <div class="profile-chips">
                            <span class="chip" id="prof-hero-login">🔑 --</span>
                            <span class="chip" id="prof-hero-email">✉️ --</span>
                            <span class="chip" id="prof-hero-phone">📞 --</span>
                            <span class="chip" id="prof-hero-joined">📅 --</span>
                        </div>
                    </div>
                </div>
                <div style="display:flex; flex-direction:column; gap:0.5rem; align-items:flex-end;">
                    <button class="btn btn-primary" onclick="openEditPrivateModal()">✎ Edit Personal Info</button>
                    <button class="btn btn-secondary prof-admin-edit-btn" onclick="openSalaryModal(null)">💰 Update Salary Structure</button>
                </div>
            </div>

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
                            <div class="val" id="prof-dob">--</div>
                        </div>
                        <div class="info-item">
                            <div class="lbl">Gender</div>
                            <div class="val" id="prof-gender">--</div>
                        </div>
                        <div class="info-item">
                            <div class="lbl">Nationality</div>
                            <div class="val" id="prof-nationality">--</div>
                        </div>
                        <div class="info-item">
                            <div class="lbl">Marital Status</div>
                            <div class="val" id="prof-marital">--</div>
                        </div>
                        <div class="info-item">
                            <div class="lbl">Aadhaar Number (UID)</div>
                            <div class="val" id="prof-aadhar">--</div>
                        </div>
                        <div class="info-item">
                            <div class="lbl">PAN Number</div>
                            <div class="val" id="prof-pan">--</div>
                        </div>
                        <div class="info-item">
                            <div class="lbl">Passport Number</div>
                            <div class="val" id="prof-passport">--</div>
                        </div>
                        <div class="info-item">
                            <div class="lbl">Personal Mobile</div>
                            <div class="val" id="prof-personal-phone">--</div>
                        </div>
                    </div>
                </div>

                <div class="two-col-grid">
                    <div class="card">
                        <h3 style="font-size: 1.05rem; margin-bottom: 1rem; color: var(--accent-purple-hover);">Home / Residential Address</h3>
                        <div style="display:flex; flex-direction:column; gap:0.5rem; font-size:0.9rem;">
                            <div><strong style="color:var(--text-muted);">Street:</strong> <span id="prof-addr-street">--</span></div>
                            <div><strong style="color:var(--text-muted);">City / State:</strong> <span id="prof-addr-city">--</span></div>
                            <div><strong style="color:var(--text-muted);">PIN / Postal Code:</strong> <span id="prof-addr-pin">--</span></div>
                            <div><strong style="color:var(--text-muted);">Country:</strong> <span id="prof-addr-country">--</span></div>
                        </div>
                    </div>

                    <div class="card">
                        <h3 style="font-size: 1.05rem; margin-bottom: 1rem; color: var(--accent-purple-hover);">Emergency Contact & Banking</h3>
                        <div style="display:flex; flex-direction:column; gap:0.5rem; font-size:0.9rem;">
                            <div><strong style="color:var(--text-muted);">Emergency Contact:</strong> <span id="prof-emg-name">--</span></div>
                            <div><strong style="color:var(--text-muted);">Emergency Phone:</strong> <span id="prof-emg-phone">--</span></div>
                            <hr style="border-color:var(--border-line); margin:0.3rem 0;">
                            <div><strong style="color:var(--text-muted);">Bank Name:</strong> <span id="prof-bank-name">--</span></div>
                            <div><strong style="color:var(--text-muted);">Account Number:</strong> <code id="prof-bank-acc">--</code></div>
                            <div><strong style="color:var(--text-muted);">IFSC Code:</strong> <code id="prof-bank-ifsc">--</code></div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Section 2: Salary & Compensation Breakdown -->
            <div id="psec-salary" class="profile-section">
                <div class="stats-grid">
                    <div class="stat-box">
                        <div class="metric-label">Monthly Base Wage</div>
                        <div class="num" style="color: #60a5fa;" id="prof-sal-wage">₹0.00</div>
                    </div>
                    <div class="stat-box">
                        <div class="metric-label">Annual CTC</div>
                        <div class="num" style="color: #a78bfa;" id="prof-sal-ctc">₹0.00</div>
                    </div>
                    <div class="stat-box">
                        <div class="metric-label">Net Take-Home Salary</div>
                        <div class="num" style="color: #34d399;" id="prof-sal-net">₹0.00</div>
                    </div>
                    <div class="stat-box">
                        <div class="metric-label">Active Structure</div>
                        <div class="num" style="font-size:1.1rem; color: #fbbf24; margin-top:0.4rem;" id="prof-sal-struct">--</div>
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
                                <tr><th>Salary Component</th><th>Computation Rule</th><th style="text-align: right;">Monthly Amount</th></tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td><strong>Basic Salary</strong></td>
                                    <td>50.00% of Base Wage</td>
                                    <td style="text-align: right; font-weight: 600;" id="prof-comp-basic">₹0.00</td>
                                </tr>
                                <tr>
                                    <td><strong>House Rent Allowance (HRA)</strong></td>
                                    <td>50.00% of Basic (25% of Base Wage)</td>
                                    <td style="text-align: right;" id="prof-comp-hra">₹0.00</td>
                                </tr>
                                <tr>
                                    <td><strong>Standard Allowance</strong></td>
                                    <td>16.67% of Wage</td>
                                    <td style="text-align: right;" id="prof-comp-std">₹0.00</td>
                                </tr>
                                <tr>
                                    <td><strong>Performance Bonus</strong></td>
                                    <td>8.33% of Wage</td>
                                    <td style="text-align: right;" id="prof-comp-bonus">₹0.00</td>
                                </tr>
                                <tr>
                                    <td><strong>Leave Travel Allowance (LTA)</strong></td>
                                    <td>8.33% of Wage</td>
                                    <td style="text-align: right;" id="prof-comp-lta">₹0.00</td>
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
                                <tr><th>Deduction Item</th><th>Statutory Rate</th><th style="text-align: right;">Monthly Amount</th></tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td><strong>Provident Fund (PF) Employee Share</strong></td>
                                    <td>12.00% of Basic Salary</td>
                                    <td style="text-align: right; color:#f87171;" id="prof-comp-pf">- ₹0.00</td>
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
                                    <td style="text-align: right; color:#f87171;" id="prof-comp-deduct-total">- ₹0.00</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- Section 3: Work & Privileges -->
            <div id="psec-work" class="profile-section">
                <div class="card">
                    <h3 style="font-size: 1.05rem; margin-bottom: 1rem; color: var(--accent-purple-hover);">Organizational Role &amp; Security</h3>
                    <div class="info-grid">
                        <div class="info-item">
                            <div class="lbl">Job Title</div>
                            <div class="val" id="prof-work-job">--</div>
                        </div>
                        <div class="info-item">
                            <div class="lbl">Department</div>
                            <div class="val" id="prof-work-dept">--</div>
                        </div>
                        <div class="info-item">
                            <div class="lbl">Reports To</div>
                            <div class="val" id="prof-work-manager">--</div>
                        </div>
                        <div class="info-item">
                            <div class="lbl">Work Location</div>
                            <div class="val" id="prof-work-location">Bangalore Headquarters (HQ)</div>
                        </div>
                        <div class="info-item">
                            <div class="lbl">Working Schedule</div>
                            <div class="val" id="prof-work-schedule">40 Hours / Week (Mon-Fri)</div>
                        </div>
                        <div class="info-item">
                            <div class="lbl">Security Group</div>
                            <div class="val"><span class="badge badge-purple" id="prof-work-sec-group">dayflow.group_dayflow_user</span></div>
                        </div>
                    </div>
                    <div id="prof-work-privileges-note" style="background-color: var(--bg-card); border: 1px solid var(--border-line); padding: 1rem; border-radius: 8px; font-size: 0.85rem; color: var(--text-muted); margin-top: 1rem;">
                        👤 <strong>Employee Access:</strong> Access to check-in/out attendance tracking, time-off leave applications, personal compensation records, and verified compliance document uploads.
                    </div>
                </div>
            </div>

            <!-- Section 4: Verified Documents -->
            <div id="psec-docs" class="profile-section">
                <div class="card">
                    <h3 style="font-size: 1.05rem; margin-bottom: 1rem; color: var(--accent-purple-hover);">Attached Compliance &amp; Verification Documents</h3>
                    <div class="table-wrap">
                        <table>
                            <thead>
                                <tr><th>Document Title</th><th>Type</th><th>File Name</th><th>Verified Date</th><th>Status</th></tr>
                            </thead>
                            <tbody id="prof-tbl-docs">
                                <tr><td colspan="5" style="text-align:center; color:var(--text-muted); padding:1rem;">No verified compliance documents on file.</td></tr>
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
                    <p class="header-sub">Daily check-in logs, break tracking, working hours calculation, and payroll ledger</p>
                </div>
                <div style="display: flex; gap: 0.5rem;">
                    <button class="btn btn-secondary" onclick="resetData()">Reset Data</button>
                </div>
            </div>

            <!-- Interactive Attendance Banner with Break Tracking -->
            <div class="banner">
                <div class="banner-metrics" style="gap: 1.8rem; flex-wrap: wrap;">
                    <div class="metric"><span class="metric-label">Status</span><div class="metric-val"><span id="dot-status" class="dot red"></span><span id="txt-status">Not Checked In</span></div></div>
                    <div class="metric"><span class="metric-label">Check-In</span><span class="metric-val" id="txt-checkin-time">--:--</span></div>
                    <div class="metric"><span class="metric-label">Total Time</span><span class="metric-val" id="txt-worked-hours" style="color: var(--accent-purple-hover);">0h 00m</span></div>
                    <div class="metric"><span class="metric-label">Break Duration</span><span class="metric-val" id="txt-break-hours" style="color: #fbbf24;">0h 00m</span></div>
                    <div class="metric"><span class="metric-label">Effective Hours</span><span class="metric-val" id="txt-effective-hours" style="color: #34d399; font-weight: 800;">0h 00m</span></div>
                </div>
                <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
                    <button id="btn-in" class="btn btn-success" onclick="handleCheckIn()">Check In</button>
                    <button id="btn-break" class="btn btn-secondary" onclick="handleBreakToggle()" disabled>☕ Take a Break</button>
                    <button id="btn-out" class="btn btn-danger" onclick="handleCheckOut()" disabled>Check Out</button>
                </div>
            </div>

            <!-- Attendance History Table -->
            <div class="card">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 0.85rem;">
                    <h3 style="font-size: 1.05rem;">Daily Attendance Logs</h3>
                    <span class="badge badge-purple" id="att-scope-tag">Attendance Log</span>
                </div>
                <div class="table-wrap">
                    <table>
                        <thead>
                            <tr><th>Date</th><th>Employee</th><th>Check In</th><th>Check Out</th><th>Status</th><th>Worked Hours</th><th>Effective Hours</th><th>Extra Hours</th></tr>
                        </thead>
                        <tbody id="tbl-attendance"></tbody>
                    </table>
                </div>
            </div>

            <!-- Monthly Attendance & Leave Payroll Ledger (Person 4 Cross-Module Integration) -->
            <div class="card" style="margin-top: 1.5rem; background: linear-gradient(135deg, rgba(24, 27, 36, 0.95), rgba(113, 75, 103, 0.15)); border: 1px solid rgba(113, 75, 103, 0.4);">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 0.85rem;">
                    <div>
                        <div style="display:flex; align-items:center; gap:0.5rem;">
                            <h3 style="font-size: 1.05rem;">📊 Monthly Attendance &amp; Leave Payroll Ledger</h3>
                            <span class="badge badge-green">Payroll Ready</span>
                        </div>
                        <p style="font-size: 0.78rem; color: var(--text-muted); margin-top: 3px;">
                            Calculates final payable days: <em>Payable Days = Present + (0.5 × Half-day) + Approved Paid Leaves</em>
                        </p>
                    </div>
                </div>
                <div class="table-wrap">
                    <table>
                        <thead>
                            <tr>
                                <th>Employee</th>
                                <th>Working Days</th>
                                <th>Present Days</th>
                                <th>Half Days (0.5d)</th>
                                <th>Approved Paid Leaves</th>
                                <th>Unpaid Leaves</th>
                                <th>Overtime Hours</th>
                                <th style="color: #34d399; font-weight: 700;">Final Payable Days</th>
                            </tr>
                        </thead>
                        <tbody id="tbl-payroll-ledger"></tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- TIME OFF / LEAVE TAB -->
        <div id="panel-leave" class="tab-panel">
            <div class="header-row">
                <div>
                    <h1 class="header-title" id="leave-header-title">Time Off & Leave Management</h1>
                    <p class="header-sub" id="leave-header-sub">Manage time off, view official company holidays, and track leave balances</p>
                </div>
                <button class="btn btn-primary" id="btn-leave-new" style="font-size: 0.95rem; padding: 0.5rem 1.3rem;" onclick="openLeaveModal(null)">+ NEW APPLICATION</button>
            </div>

            <!-- Leave Summary Cards -->
            <div class="stats-grid" id="leave-metrics-grid">
                <div class="stat-box">
                    <div class="metric-label" id="leave-lbl-p1">Paid Time Off</div>
                    <div class="num" style="color: #34d399;" id="leave-val-p1">24 Days Available</div>
                </div>
                <div class="stat-box">
                    <div class="metric-label" id="leave-lbl-p2">Sick Time Off</div>
                    <div class="num" style="color: #fbbf24;" id="leave-val-p2">07 Days Available</div>
                </div>
                <div class="stat-box">
                    <div class="metric-label" id="leave-lbl-p3">Unpaid Leaves</div>
                    <div class="num" style="color: #60a5fa;" id="leave-val-p3">Unlimited</div>
                </div>
                <div class="stat-box">
                    <div class="metric-label" id="leave-lbl-p4">Upcoming Holidays</div>
                    <div class="num" style="color: var(--accent-purple-hover);" id="leave-val-p4">4 This Year</div>
                </div>
            </div>

            <!-- Admin HR Decision Banner -->
            <div id="leave-admin-banner" class="card" style="display:none; background: linear-gradient(135deg, rgba(113, 75, 103, 0.22), rgba(32, 36, 51, 0.95)); border: 1px solid rgba(113, 75, 103, 0.45); margin-bottom: 1.25rem;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <div style="display:flex; align-items:center; gap:0.5rem;">
                            <h3 style="font-size: 1.1rem; color: #fff;">🛡️ HR Time Off Management & Decision Hub</h3>
                            <span class="badge badge-purple">Admin Mode</span>
                        </div>
                        <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 4px;">
                            Review all employee leave applications. Decisions trigger automated email alerts to the applicant.
                        </p>
                    </div>
                </div>
            </div>

            <!-- Calendar & National Holidays (Employee View) -->
            <div class="cal-layout" id="leave-cal-container">
                <div class="card" style="margin-bottom: 0;">
                    <div class="cal-header-bar">
                        <div style="display:flex; align-items:center; gap: 0.75rem;">
                            <h3 style="font-size: 1.1rem; color: #fff;">August 2026</h3>
                            <span class="badge badge-purple">My Work Calendar</span>
                        </div>
                        <div style="display:flex; gap:0.4rem;">
                            <button class="btn btn-secondary" style="padding:0.25rem 0.6rem; font-size:0.75rem;">&lt;</button>
                            <button class="btn btn-secondary" style="padding:0.25rem 0.6rem; font-size:0.75rem;">Today</button>
                            <button class="btn btn-secondary" style="padding:0.25rem 0.6rem; font-size:0.75rem;">&gt;</button>
                        </div>
                    </div>

                    <div class="cal-grid-days" style="margin-bottom: 0.4rem;">
                        <div class="cal-day-name">Mon</div>
                        <div class="cal-day-name">Tue</div>
                        <div class="cal-day-name">Wed</div>
                        <div class="cal-day-name">Thu</div>
                        <div class="cal-day-name">Fri</div>
                        <div class="cal-day-name" style="color:#f87171;">Sat</div>
                        <div class="cal-day-name" style="color:#f87171;">Sun</div>
                    </div>

                    <div class="cal-grid-days" id="cal-grid-tiles"></div>
                    
                    <p style="font-size:0.75rem; color:var(--text-muted); margin-top:0.75rem; text-align:center;">
                        💡 Click on any date tile above or click <strong>+ NEW APPLICATION</strong> to apply for leave.
                    </p>
                </div>

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
                        📌 <em>Official national holidays are fully paid and do not consume annual PTO balance.</em>
                    </div>
                </div>
            </div>

            <!-- Time Off Applications & Review Table -->
            <div class="card" style="margin-top: 1.25rem;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 0.9rem;">
                    <h3 style="font-size: 1.05rem;" id="leave-table-title">My Time Off</h3>
                    <span class="badge badge-purple" id="leave-table-tag">Personal Log</span>
                </div>
                <div class="table-wrap">
                    <table>
                        <thead>
                            <tr id="leave-table-head"></tr>
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
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 1rem;">
                    <h3 style="font-size: 1.05rem;">Create Employee Profile &amp; Login Account</h3>
                    <button type="button" class="btn btn-secondary" style="padding:0.2rem 0.6rem;" onclick="toggleEmpForm()">✕</button>
                </div>
                <div id="emp-create-error" style="display:none; background:rgba(239,68,68,0.15); border:1px solid rgba(239,68,68,0.4); color:#f87171; padding:0.6rem 0.9rem; border-radius:6px; font-size:0.85rem; margin-bottom:1rem;"></div>

                <form onsubmit="handleAddEmp(event)">
                    <!-- Basic Information -->
                    <div style="font-size:0.85rem; font-weight:700; color:var(--accent-purple-hover); margin-bottom:0.5rem;">1. Basic Details</div>
                    <div class="form-row">
                        <div class="field">
                            <label>Full Name *</label>
                            <input type="text" id="emp-name" class="input" placeholder="e.g. Rahul Sharma" required>
                        </div>
                        <div class="field">
                            <label>Employee Code</label>
                            <input type="text" id="emp-code" class="input" placeholder="e.g. EMP004 (Auto-generated if blank)">
                        </div>
                        <div class="field">
                            <label>Work Email *</label>
                            <input type="email" id="emp-email" class="input" placeholder="rahul@company.com" required>
                        </div>
                        <div class="field">
                            <label>Mobile Number</label>
                            <input type="text" id="emp-phone" class="input" placeholder="+91 98765 00000">
                        </div>
                    </div>
                    <div class="form-row">
                        <div class="field">
                            <label>Date of Birth</label>
                            <input type="date" id="emp-dob" class="input" value="1995-05-15">
                        </div>
                        <div class="field">
                            <label>City / Location</label>
                            <input type="text" id="emp-city" class="input" placeholder="Bangalore, Karnataka">
                        </div>
                    </div>

                    <!-- Work Details -->
                    <div style="font-size:0.85rem; font-weight:700; color:var(--accent-purple-hover); margin-top:1rem; margin-bottom:0.5rem;">2. Work Details</div>
                    <div class="form-row">
                        <div class="field">
                            <label>Job Title *</label>
                            <input type="text" id="emp-job" class="input" placeholder="e.g. QA Automation Engineer" required>
                        </div>
                        <div class="field">
                            <label>Department *</label>
                            <input type="text" id="emp-dept" class="input" placeholder="e.g. Engineering" required>
                        </div>
                        <div class="field">
                            <label>Role *</label>
                            <select id="emp-role" class="input" required>
                                <option value="Employee">Employee</option>
                                <option value="Admin / HR">Admin / HR</option>
                            </select>
                        </div>
                        <div class="field">
                            <label>Joining Date *</label>
                            <input type="date" id="emp-joining" class="input" required>
                        </div>
                    </div>

                    <!-- Login Credentials -->
                    <div style="font-size:0.85rem; font-weight:700; color:var(--accent-purple-hover); margin-top:1rem; margin-bottom:0.5rem;">3. Login Credentials</div>
                    <div class="form-row">
                        <div class="field">
                            <label>Login ID / Username *</label>
                            <input type="text" id="emp-login-id" class="input" placeholder="e.g. rahul123 or testemployee" required autocomplete="off">
                        </div>
                        <div class="field">
                            <label>Password *</label>
                            <input type="password" id="emp-password" class="input" placeholder="Enter password" required autocomplete="new-password">
                        </div>
                        <div class="field">
                            <label>Confirm Password *</label>
                            <input type="password" id="emp-confirm-password" class="input" placeholder="Confirm password" required autocomplete="new-password">
                        </div>
                    </div>

                    <!-- Compensation -->
                    <div style="font-size:0.85rem; font-weight:700; color:var(--accent-purple-hover); margin-top:1rem; margin-bottom:0.5rem;">4. Compensation Structure</div>
                    <div class="form-row">
                        <div class="field">
                            <label>Monthly Salary / Wage (₹) *</label>
                            <input type="number" id="emp-wage" class="input" value="50000" min="5000" step="1000" required>
                        </div>
                        <div class="field">
                            <label>Salary Structure</label>
                            <input type="text" id="emp-struct" class="input" value="Standard Base" placeholder="e.g. Senior Technical Base">
                        </div>
                    </div>

                    <div style="margin-top:1.25rem; display:flex; gap:0.75rem;">
                        <button type="submit" class="btn btn-success">✓ Create Employee &amp; Account</button>
                        <button type="button" class="btn btn-secondary" onclick="toggleEmpForm()">Cancel</button>
                    </div>
                </form>
            </div>

            <div class="emp-grid" id="grid-employees"></div>
        </div>

        <!-- DOCUMENTS TAB -->
        <div id="panel-documents" class="tab-panel">
            <div class="header-row"><h1 class="header-title">Employee Documents</h1></div>
            <div class="stats-grid">
                <div class="stat-box"><div class="metric-label">ID Proofs</div><div class="num" style="color: #60a5fa;" id="stat-id">0</div></div>
                <div class="stat-box"><div class="metric-label">Contracts</div><div class="num" style="color: #34d399;" id="stat-contract">0</div></div>
                <div class="stat-box"><div class="metric-label">Certificates</div><div class="num" style="color: #fbbf24;" id="stat-cert">0</div></div>
                <div class="stat-box"><div class="metric-label">Verified Documents</div><div class="num" style="color: var(--accent-purple-hover);" id="stat-verified">0</div></div>
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
                            <select id="doc-employee" class="input" required></select>
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
                            <tr><th>Title</th><th>Employee</th><th>Category</th><th>File Info</th><th>Uploaded</th><th>Status</th><th>Action</th><th>HR Review</th></tr>
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
                <div class="stat-box"><div class="metric-label">Total Monthly Payroll</div><div class="num" style="color: #60a5fa;" id="stat-payroll-total">₹0.00</div></div>
                <div class="stat-box"><div class="metric-label">Approved Records</div><div class="num" style="color: #34d399;" id="stat-payroll-approved">0</div></div>
                <div class="stat-box"><div class="metric-label">Paid Records</div><div class="num" style="color: #a78bfa;" id="stat-payroll-paid">0</div></div>
                <div class="stat-box"><div class="metric-label">Pending Drafts</div><div class="num" style="color: #fbbf24;" id="stat-payroll-draft">0</div></div>
            </div>

            <div class="card">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 1rem;">
                    <h3 style="font-size: 1.05rem;">Employee Salary Structures & Compensation</h3>
                    <span id="payroll-rule-tag" style="font-size: 0.78rem; color: var(--text-muted);">Showing organizational payroll records</span>
                </div>
                <div class="table-wrap">
                    <table>
                        <thead>
                            <tr><th>Reference</th><th>Employee</th><th>Structure</th><th>Period</th><th style="text-align: right;">Base Salary</th><th style="text-align: right;">Allowances</th><th style="text-align: right;">Deductions</th><th style="text-align: right;">Net Salary</th><th style="text-align: center;">Status</th><th style="text-align: right;">Actions</th></tr>
                        </thead>
                        <tbody id="tbl-payroll"></tbody>
                    </table>
                </div>
            </div>
        </div>

    </div>

    <!-- NOTIFICATION CENTER MODAL -->
    <div id="modal-notifications" class="modal" style="display: none;">
        <div class="modal-card" style="max-width: 620px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem;">
                <div style="display:flex; align-items:center; gap:0.6rem;">
                    <div style="background:rgba(113,75,103,0.3); border:1px solid var(--accent-purple); padding:0.35rem 0.6rem; border-radius:6px; font-size:1.1rem;">🔔</div>
                    <div>
                        <h3 style="font-size: 1.15rem;">Email & In-App Notification Center</h3>
                        <p style="font-size: 0.78rem; color: var(--text-muted);">Live audit log of sent Dayflow security alerts and transactional emails</p>
                    </div>
                </div>
                <button class="btn btn-secondary" onclick="toggleNotificationModal()">✕</button>
            </div>

            <div id="notif-list-container" style="display:flex; flex-direction:column; gap:0.75rem; max-height:420px; overflow-y:auto; padding-right:4px;">
            </div>

            <div style="display: flex; justify-content: space-between; align-items:center; margin-top: 1.25rem; border-top: 1px solid var(--border-line); padding-top: 0.75rem;">
                <span style="font-size: 0.75rem; color: var(--text-muted);">🔒 Native Odoo Outgoing Mail Queue Active (TLS/SSL)</span>
                <button class="btn btn-secondary" style="font-size:0.8rem;" onclick="clearNotifications()">Clear Log</button>
            </div>
        </div>
    </div>

    <!-- NEW LEAVE REQUEST MODAL (Employee View) -->
    <div id="modal-leave-app" class="modal" style="display: none;">
        <div class="modal-card" style="max-width: 560px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem;">
                <div style="display:flex; align-items:center; gap:0.6rem;">
                    <div style="background:rgba(113,75,103,0.3); border:1px solid var(--accent-purple); padding:0.35rem 0.6rem; border-radius:6px; font-size:1.1rem;">📅</div>
                    <div>
                        <h3 style="font-size: 1.15rem;">New Time Off Application</h3>
                        <p style="font-size: 0.78rem; color: var(--text-muted);">Submit leave request for review</p>
                    </div>
                </div>
                <button class="btn btn-secondary" onclick="closeLeaveModal()">✕</button>
            </div>

            <form onsubmit="handleLeaveModalSubmit(event)">
                <div class="field" style="margin-bottom: 0.85rem;">
                    <label>Employee Name</label>
                    <input type="text" id="mleave-emp-name" class="input" value="Jane Smith" readonly>
                </div>

                <div class="field" style="margin-bottom: 0.85rem;">
                    <label>Time Off Type</label>
                    <select id="mleave-type" class="input" required>
                        <option value="paid">Paid Time Off</option>
                        <option value="sick">Sick Leave</option>
                        <option value="unpaid">Unpaid Leave</option>
                    </select>
                </div>

                <div class="field" style="margin-bottom: 0.85rem;">
                    <label>Duration / Session</label>
                    <select id="mleave-session" class="input" onchange="calcLeaveDuration()" required>
                        <option value="full">Full Day (1.0 Day per date)</option>
                        <option value="half_am">First Half AM (0.5 Day)</option>
                        <option value="half_pm">Second Half PM (0.5 Day)</option>
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
                    <div class="metric-label">Allocation / Duration</div>
                    <div style="font-size: 1.05rem; font-weight: 700; color: #60a5fa;" id="mleave-duration-preview">1 Day</div>
                </div>

                <div class="field" style="margin-bottom: 0.85rem;">
                    <label>Remarks / Reason</label>
                    <textarea id="mleave-reason" class="input" rows="2" placeholder="State reason for your time off..." required></textarea>
                </div>

                <div class="field" style="margin-bottom: 1.25rem;">
                    <label>Attachment (Medical Certificate / Note)</label>
                    <input type="file" id="mleave-file" class="input" accept="image/*,.pdf,.doc,.docx">
                </div>

                <div style="display: flex; justify-content: flex-end; gap: 0.6rem;">
                    <button type="button" class="btn btn-secondary" onclick="closeLeaveModal()">Discard</button>
                    <button type="submit" class="btn btn-primary" style="padding: 0.5rem 1.4rem;">Submit</button>
                </div>
            </form>
        </div>
    </div>

    <!-- LEAVE REQUEST DETAILS MODAL (Admin Review) -->
    <div id="modal-leave-detail" class="modal" style="display: none;">
        <div class="modal-card" style="max-width: 580px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem;">
                <div>
                    <h3 style="font-size: 1.2rem;">Leave Request Details</h3>
                    <p style="font-size: 0.8rem; color: var(--text-muted);">Admin Review & Governance Decision</p>
                </div>
                <button class="btn btn-secondary" onclick="closeLeaveDetailModal()">✕</button>
            </div>

            <input type="hidden" id="ld-id">
            <div class="info-grid" style="grid-template-columns: 1fr 1fr; margin-bottom: 1rem;">
                <div class="info-item">
                    <div class="lbl">Employee</div>
                    <div class="val" id="ld-emp">John Doe</div>
                </div>
                <div class="info-item">
                    <div class="lbl">Time Off Type</div>
                    <div class="val" id="ld-type">Paid Time Off</div>
                </div>
                <div class="info-item">
                    <div class="lbl">Validity Period</div>
                    <div class="val" id="ld-dates">25 Aug 2026 → 27 Aug 2026</div>
                </div>
                <div class="info-item">
                    <div class="lbl">Allocation / Duration</div>
                    <div class="val" id="ld-days">3 Days</div>
                </div>
            </div>

            <div class="card" style="background: var(--bg-card); margin-bottom: 1rem;">
                <div class="lbl" style="margin-bottom: 0.25rem;">Employee Remarks</div>
                <div style="font-size: 0.9rem; color: #fff;" id="ld-remarks">Fever and rest recommended</div>
                <div style="margin-top: 0.6rem; font-size: 0.8rem; color: #34d399;" id="ld-attachment">📄 Attachment Attached</div>
            </div>

            <div class="field" style="margin-bottom: 1.25rem;">
                <label>Admin Decision Comments</label>
                <textarea id="ld-admin-comment" class="input" rows="2" placeholder="Add decision remarks or approval notes..."></textarea>
            </div>

            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div id="ld-status-badge"><span class="badge badge-amber">PENDING</span></div>
                <div style="display: flex; gap: 0.6rem;">
                    <button class="btn btn-danger" onclick="submitLeaveDecision('rejected')">Reject</button>
                    <button class="btn btn-success" onclick="submitLeaveDecision('approved')">Approve</button>
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
                    <div class="field"><label>Employee Name</label><input type="text" id="modal-pay-emp" class="input" readonly></div>
                    <div class="field"><label>Salary Structure Title</label><input type="text" id="modal-pay-struct" class="input" placeholder="e.g. Executive Management Base"></div>
                </div>
                <div class="form-row">
                    <div class="field"><label>Base Salary (₹)</label><input type="number" id="modal-pay-base" class="input" oninput="calcModalNetSalary()" required></div>
                    <div class="field"><label>Allowances (₹)</label><input type="number" id="modal-pay-allow" class="input" oninput="calcModalNetSalary()" required></div>
                    <div class="field"><label>Deductions (₹)</label><input type="number" id="modal-pay-deduct" class="input" oninput="calcModalNetSalary()" required></div>
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
        <div class="modal-card" style="max-width: 680px; max-height: 85vh; overflow-y: auto;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <h3 style="font-size: 1.1rem;">✎ Edit Profile &amp; Personal Details</h3>
                <button class="btn btn-secondary" onclick="closeEditPrivateModal()">✕</button>
            </div>
            <form onsubmit="handleSavePrivateInfo(event)">
                <div style="font-size:0.85rem; font-weight:700; color:var(--accent-purple-hover); margin-bottom:0.5rem;">1. Personal &amp; Identity Details</div>
                <div class="form-row">
                    <div class="field"><label>Date of Birth</label><input type="date" id="m-dob" class="input" required></div>
                    <div class="field"><label>Gender</label><select id="m-gender" class="input"><option value="Female">Female</option><option value="Male">Male</option><option value="Other">Other</option></select></div>
                    <div class="field"><label>Nationality</label><input type="text" id="m-nationality" class="input" placeholder="e.g. Indian"></div>
                    <div class="field"><label>Marital Status</label><select id="m-marital" class="input"><option value="Single">Single</option><option value="Married">Married</option></select></div>
                </div>
                <div class="form-row">
                    <div class="field"><label>Personal Mobile</label><input type="text" id="m-phone" class="input" placeholder="+91 98765 00000" required></div>
                    <div class="field"><label>Aadhaar Number</label><input type="text" id="m-aadhar" class="input" placeholder="4589-2314-7890"></div>
                    <div class="field"><label>PAN Number</label><input type="text" id="m-pan" class="input" placeholder="ABCPJ4589K"></div>
                    <div class="field"><label>Passport Number</label><input type="text" id="m-passport" class="input" placeholder="Z9876543"></div>
                </div>

                <div style="font-size:0.85rem; font-weight:700; color:var(--accent-purple-hover); margin-top:1rem; margin-bottom:0.5rem;">2. Home / Residential Address</div>
                <div class="form-row">
                    <div class="field" style="flex:2;"><label>Street Address</label><input type="text" id="m-street" class="input" placeholder="No. 42, 8th Main, Indiranagar"></div>
                    <div class="field"><label>City / State</label><input type="text" id="m-city" class="input" placeholder="Bangalore, Karnataka"></div>
                    <div class="field"><label>PIN / Postal Code</label><input type="text" id="m-pin" class="input" placeholder="560038"></div>
                    <div class="field"><label>Country</label><input type="text" id="m-country" class="input" placeholder="India"></div>
                </div>

                <div style="font-size:0.85rem; font-weight:700; color:var(--accent-purple-hover); margin-top:1rem; margin-bottom:0.5rem;">3. Emergency Contact &amp; Banking</div>
                <div class="form-row">
                    <div class="field"><label>Emergency Contact (Name &amp; Rel)</label><input type="text" id="m-emg" class="input" placeholder="e.g. Spouse / Parent"></div>
                    <div class="field"><label>Emergency Phone</label><input type="text" id="m-emg-phone" class="input" placeholder="+91 98765 00000"></div>
                </div>
                <div class="form-row">
                    <div class="field"><label>Bank Name</label><input type="text" id="m-bank-name" class="input" placeholder="e.g. HDFC Bank"></div>
                    <div class="field"><label>Bank Account Number</label><input type="text" id="m-bank-acc" class="input" placeholder="50100234567890"></div>
                    <div class="field"><label>IFSC Code</label><input type="text" id="m-bank-ifsc" class="input" placeholder="HDFC0001234"></div>
                </div>

                <!-- Admin-Only Work Info -->
                <div id="m-work-sec" style="display:none;">
                    <div style="font-size:0.85rem; font-weight:700; color:var(--accent-purple-hover); margin-top:1rem; margin-bottom:0.5rem;">4. Work &amp; Role Details (Admin Control)</div>
                    <div class="form-row">
                        <div class="field"><label>Job Title</label><input type="text" id="m-job" class="input"></div>
                        <div class="field"><label>Department</label><input type="text" id="m-dept" class="input"></div>
                        <div class="field"><label>Reports To</label><input type="text" id="m-manager" class="input"></div>
                    </div>
                    <div class="form-row">
                        <div class="field"><label>Work Location</label><input type="text" id="m-location" class="input"></div>
                        <div class="field"><label>Working Schedule</label><input type="text" id="m-schedule" class="input"></div>
                        <div class="field"><label>Role / Security</label><select id="m-role" class="input"><option value="Employee">Employee</option><option value="Admin / HR">Admin / HR</option></select></div>
                    </div>
                </div>

                <div style="display: flex; justify-content: flex-end; gap: 0.5rem; margin-top: 1.25rem;">
                    <button type="button" class="btn btn-secondary" onclick="closeEditPrivateModal()">Cancel</button>
                    <button type="submit" class="btn btn-primary">✓ Save Details</button>
                </div>
            </form>
        </div>
    </div>

    <script>
        const DEFAULT_ATTENDANCE = [
            { id: 1, employeeId: 1, date: '2026-08-21', employee: 'John Doe', checkIn: '09:00 AM', checkOut: '05:30 PM', checkInTimestamp: 1787302800000, checkOutTimestamp: 1787333400000, status: 'present', workedHours: 8.5, effectiveHours: 8.5, extraHours: 0.5, isActive: false },
            { id: 2, employeeId: 1, date: '2026-08-20', employee: 'John Doe', checkIn: '08:50 AM', checkOut: '06:10 PM', checkInTimestamp: 1787215800000, checkOutTimestamp: 1787249400000, status: 'present', workedHours: 9.3, effectiveHours: 9.3, extraHours: 1.3, isActive: false },
            { id: 3, employeeId: 1, date: '2026-08-19', employee: 'John Doe', checkIn: '09:15 AM', checkOut: '01:00 PM', checkInTimestamp: 1787130900000, checkOutTimestamp: 1787144400000, status: 'half_day', workedHours: 3.75, effectiveHours: 3.75, extraHours: 0.0, isActive: false },
            { id: 4, employeeId: 2, date: '2026-08-22', employee: 'Jane Smith', checkIn: '09:05 AM', checkOut: '--', checkInTimestamp: 1787389500000, checkOutTimestamp: null, status: 'present', workedHours: 2.5, effectiveHours: 2.5, extraHours: 0.0, isActive: false },
            { id: 5, employeeId: 3, date: '2026-08-22', employee: 'Robert Taylor', checkIn: '08:45 AM', checkOut: '--', checkInTimestamp: 1787388300000, checkOutTimestamp: null, status: 'present', workedHours: 2.8, effectiveHours: 2.8, extraHours: 0.0, isActive: false }
        ];

        const DEFAULT_LEAVE = [
            { id: 101, employeeId: 1, employee: 'John Doe', type: 'sick', startDate: '2026-08-25', endDate: '2026-08-27', days: 3, remarks: 'High fever and doctor prescribed rest', hasAttachment: true, status: 'pending', adminComments: '' },
            { id: 102, employeeId: 2, employee: 'Jane Smith', type: 'paid', startDate: '2026-08-28', endDate: '2026-08-30', days: 3, remarks: 'Family vacation', hasAttachment: false, status: 'approved', adminComments: 'Approved by HR Director' },
            { id: 103, employeeId: 3, employee: 'Robert Taylor', type: 'paid', startDate: '2026-08-23', endDate: '2026-08-24', days: 2, remarks: 'Attending Odoo Developers Conference', hasAttachment: false, status: 'pending', adminComments: '' },
            { id: 104, employeeId: 1, employee: 'John Doe', type: 'paid', startDate: '2026-08-10', endDate: '2026-08-10', days: 1, remarks: 'Personal domestic work', hasAttachment: false, status: 'approved', adminComments: 'Approved' }
        ];

        const DEFAULT_EMPLOYEES = [
            {
                id: 1,
                name: 'John Doe',
                email: 'john.doe@company.com',
                job: 'Senior Software Engineer',
                dept: 'Engineering',
                role: 'Employee',
                joining: '2024-03-15',
                loginId: 'OIJODO20240001',
                phone: '+91 98765 11111',
                personalPhone: '+91 98765 11111',
                dob: '1992-08-20',
                gender: 'Male',
                nationality: 'Indian',
                marital: 'Single',
                aadhar: '1234-5678-9012',
                pan: 'ABCDE1234F',
                passport: 'A1234567',
                street: 'Flat 302, Green Glen Layout, Bellandur',
                city: 'Bangalore, Karnataka',
                pin: '560103',
                country: 'India',
                emgName: 'Mary Doe (Sister)',
                emgPhone: '+91 98765 22222',
                bankName: 'ICICI Bank (Salary Account)',
                bankAcc: '001105001234',
                bankIfsc: 'ICIC0000011',
                monthlyWage: 65000,
                struct: 'Senior Technical',
                provisioned: true
            },
            {
                id: 2,
                name: 'Jane Smith',
                email: 'jane.smith@dayflow.org',
                job: 'Head of Human Resources',
                dept: 'Human Resources',
                role: 'Admin / HR',
                joining: '2023-01-10',
                loginId: 'OIJASM20230002',
                phone: '+91 98765 43212',
                personalPhone: '+91 98765 11223',
                dob: '1990-06-15',
                gender: 'Female',
                nationality: 'Indian',
                marital: 'Married',
                aadhar: '4589-2314-7890',
                pan: 'ABCPJ4589K',
                passport: 'Z9876543',
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
                struct: 'HR Specialist Base',
                provisioned: true
            },
            {
                id: 3,
                name: 'Robert Taylor',
                email: 'robert.t@company.com',
                job: 'Product Manager',
                dept: 'Product',
                role: 'Employee',
                joining: '2025-06-01',
                loginId: 'OIROTA20250003',
                phone: '+91 98765 44444',
                personalPhone: '+91 98765 44444',
                dob: '1989-11-05',
                gender: 'Male',
                nationality: 'Indian',
                marital: 'Married',
                aadhar: '9876-5432-1098',
                pan: 'XYZAB9876L',
                passport: 'B9876543',
                street: 'Villa 14, Palm Meadows, Whitefield',
                city: 'Bangalore, Karnataka',
                pin: '560066',
                country: 'India',
                emgName: 'Sarah Taylor (Spouse)',
                emgPhone: '+91 98765 55555',
                bankName: 'Axis Bank (Salary Account)',
                bankAcc: '912010045678901',
                bankIfsc: 'UTIB0000123',
                monthlyWage: 58000,
                struct: 'Product Lead',
                provisioned: false
            }
        ];

        const DEFAULT_DOCUMENTS = [
            { id: 1, employeeId: 1, title: 'Passport Verification ID', employee: 'John Doe', type: 'id_proof', filename: 'john_passport.pdf', size: '1.2 MB', date: '2026-08-10', status: 'verified', adminComments: 'Verified by HR', fileData: '' },
            { id: 2, employeeId: 2, title: 'Employment Contract 2026', employee: 'Jane Smith', type: 'contract', filename: 'jane_contract_2026.pdf', size: '450 KB', date: '2026-08-01', status: 'verified', adminComments: 'Signed contract on file', fileData: '' }
        ];

        const DEFAULT_PAYROLL = [
            { id: 1, employeeId: 1, ref: 'PAY/2026/001', employee: 'John Doe', structure: 'Senior Technical', period: 'August 2026', base: 65000, allow: 12000, deduct: 4500, status: 'approved' },
            { id: 2, employeeId: 2, ref: 'PAY/2026/002', employee: 'Jane Smith', structure: 'HR Specialist Base', period: 'August 2026', base: 55000, allow: 8000, deduct: 3500, status: 'paid' },
            { id: 3, employeeId: 3, ref: 'PAY/2026/003', employee: 'Robert Taylor', structure: 'Product Lead', period: 'August 2026', base: 58000, allow: 9000, deduct: 3800, status: 'draft' }
        ];

        const DEFAULT_NOTIFICATIONS = [
            { id: 1, title: 'Security: New Login Alert', recipient: 'jane.smith@dayflow.org', type: 'login', time: '2 mins ago', body: 'Security notification: Successful login from IP 192.168.1.10. No action required.' },
            { id: 2, title: 'Welcome: Account Created', recipient: 'john.doe@company.com', type: 'account', time: '1 hour ago', body: 'Your Dayflow account (OIJODO20240001) has been created. Login access granted.' },
            { id: 3, title: 'Time Off: Application Approved', recipient: 'john.doe@company.com', type: 'leave_approved', time: 'Yesterday', body: 'Your Paid Time Off request for 10 Aug 2026 has been approved by HR.' }
        ];

        const DEFAULT_USERS = [
            {
                userId: 'u_admin',
                loginId: 'admin',
                password: 'admin123',
                role: 'admin',
                employeeId: 2,
                name: 'Jane Smith',
                initials: 'JS',
                email: 'admin@dayflow.org'
            },
            {
                userId: 'u_1',
                loginId: 'john',
                password: 'john123',
                role: 'employee',
                employeeId: 1,
                name: 'John Doe',
                initials: 'JD',
                email: 'john.doe@company.com'
            },
            {
                userId: 'u_2',
                loginId: 'jane',
                password: 'jane123',
                role: 'admin',
                employeeId: 2,
                name: 'Jane Smith',
                initials: 'JS',
                email: 'jane.smith@dayflow.org'
            },
            {
                userId: 'u_3',
                loginId: 'robert',
                password: 'robert123',
                role: 'employee',
                employeeId: 3,
                name: 'Robert Taylor',
                initials: 'RT',
                email: 'robert.t@company.com'
            }
        ];

        const DEFAULT_ADMIN_PROFILE = {
            name: 'Jane Smith',
            title: 'Head of Human Resources',
            dept: 'Human Resources & Talent',
            reportsTo: 'Board of Directors / CEO',
            workLocation: 'Bangalore Headquarters (HQ)',
            workSchedule: '40 Hours / Week (Mon-Fri)',
            role: 'Admin / HR',
            loginId: 'admin',
            email: 'admin@dayflow.org',
            phone: '+91 98765 43210',
            dob: '1990-06-15',
            gender: 'Female',
            nationality: 'Indian',
            marital: 'Married',
            personalPhone: '+91 98765 11223',
            aadhar: '4589-2314-7890',
            pan: 'ABCPJ4589K',
            passport: 'Z9876543',
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
        };

        const HOLIDAYS_AUG_2026 = {
            15: '🇮🇳 Independence Day',
            19: '🌸 Raksha Bandhan',
            26: '🦚 Janmashtami'
        };

        let state = {
            role: 'admin',
            currentEmployee: 'Jane Smith',
            currentUserId: 'u_admin',
            currentEmployeeId: 2,
            viewingEmployeeId: null,
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
            notifications: JSON.parse(localStorage.getItem('df_notifications')) || DEFAULT_NOTIFICATIONS,
            users: JSON.parse(localStorage.getItem('df_users')) || DEFAULT_USERS,
            adminProfile: JSON.parse(localStorage.getItem('df_admin_profile')) || DEFAULT_ADMIN_PROFILE
        };

        /* Persistence helpers */
        function saveState() {
            localStorage.setItem('df_attendances', JSON.stringify(state.attendances));
            localStorage.setItem('df_leaves', JSON.stringify(state.leaves));
            localStorage.setItem('df_employees', JSON.stringify(state.employees));
            localStorage.setItem('df_documents', JSON.stringify(state.documents));
            localStorage.setItem('df_payrolls', JSON.stringify(state.payrolls));
            localStorage.setItem('df_notifications', JSON.stringify(state.notifications));
            localStorage.setItem('df_admin_profile', JSON.stringify(state.adminProfile));
            localStorage.setItem('df_users', JSON.stringify(state.users));
        }

        function resetData() {
            // Restore seed dataset into localStorage
            localStorage.setItem('df_users', JSON.stringify(DEFAULT_USERS));
            localStorage.setItem('df_employees', JSON.stringify(DEFAULT_EMPLOYEES));
            localStorage.setItem('df_attendances', JSON.stringify(DEFAULT_ATTENDANCE));
            localStorage.setItem('df_leaves', JSON.stringify(DEFAULT_LEAVE));
            localStorage.setItem('df_documents', JSON.stringify(DEFAULT_DOCUMENTS));
            localStorage.setItem('df_payrolls', JSON.stringify(DEFAULT_PAYROLL));
            localStorage.setItem('df_admin_profile', JSON.stringify(DEFAULT_ADMIN_PROFILE));
            localStorage.setItem('df_notifications', JSON.stringify(DEFAULT_NOTIFICATIONS));

            state.users = JSON.parse(JSON.stringify(DEFAULT_USERS));
            state.employees = JSON.parse(JSON.stringify(DEFAULT_EMPLOYEES));
            state.attendances = JSON.parse(JSON.stringify(DEFAULT_ATTENDANCE));
            state.leaves = JSON.parse(JSON.stringify(DEFAULT_LEAVE));
            state.documents = JSON.parse(JSON.stringify(DEFAULT_DOCUMENTS));
            state.payrolls = JSON.parse(JSON.stringify(DEFAULT_PAYROLL));
            state.adminProfile = JSON.parse(JSON.stringify(DEFAULT_ADMIN_PROFILE));
            state.notifications = JSON.parse(JSON.stringify(DEFAULT_NOTIFICATIONS));

            state.isCheckedIn = false;
            state.activeCheckInTime = null;
            state.checkInTimestamp = null;
            if (state.tickerInterval) { clearInterval(state.tickerInterval); state.tickerInterval = null; }

            // Re-apply the current session so role/nav stay correct
            const session = getSession();
            if (session) {
                applySession(session);
            } else {
                renderAll();
            }
        }

        /* Session / Auth Helpers */
        function getSession() {
            try {
                return JSON.parse(localStorage.getItem('df_session')) || null;
            } catch (e) {
                return null;
            }
        }

        function setSession(user) {
            const sessionObj = {
                userId: user.userId,
                loginId: user.loginId,
                role: user.role,
                employeeId: user.employeeId,
                name: user.name,
                initials: user.initials,
                email: user.email
            };
            localStorage.setItem('df_session', JSON.stringify(sessionObj));
        }

        function clearSession() {
            localStorage.removeItem('df_session');
        }

        function handleLogin(e) {
            e.preventDefault();
            const loginId = (document.getElementById('auth-login-id').value || '').trim();
            const password = document.getElementById('auth-password').value;
            const errEl = document.getElementById('auth-error');

            const userList = (state && state.users && state.users.length) ? state.users : (JSON.parse(localStorage.getItem('df_users')) || DEFAULT_USERS);
            const user = userList.find(u =>
                u.loginId.toLowerCase() === loginId.toLowerCase() && u.password === password
            );

            if (!user) {
                errEl.style.display = 'block';
                return;
            }
            errEl.style.display = 'none';
            setSession(user);
            applySession(user);

            triggerNotification(
                `Security: Login Alert (${user.name})`,
                user.email || `${user.loginId}@company.com`,
                'login',
                `Security notification: Successful login for account ${user.loginId} (${user.role.toUpperCase()}) at ${new Date().toLocaleTimeString()}.`
            );
        }

        function handleSignOut() {
            clearSession();
            // Reset transient state (but NOT data)
            state.role = 'admin';
            state.currentEmployee = 'Jane Smith';
            state.isCheckedIn = false;
            state.activeCheckInTime = null;
            state.checkInTimestamp = null;
            if (state.tickerInterval) { clearInterval(state.tickerInterval); state.tickerInterval = null; }
            document.getElementById('auth-login-id').value = '';
            document.getElementById('auth-password').value = '';
            document.getElementById('auth-wall').classList.remove('hidden');
        }

        function applySession(user) {
            // Find the employee record
            const emp = state.employees.find(e => e.id === user.employeeId || (e.loginId && e.loginId.toLowerCase() === user.loginId.toLowerCase()) || e.name === user.name) || state.employees[0];

            // Update in-memory state
            state.role = user.role;
            state.currentEmployee = emp ? emp.name : user.name;
            state.currentUserId = user.userId;
            state.currentEmployeeId = emp ? emp.id : user.employeeId;

            // Restore active check-in for this employee
            if (state.tickerInterval) { clearInterval(state.tickerInterval); state.tickerInterval = null; }
            state.isCheckedIn = false;
            state.activeCheckInTime = null;
            state.checkInTimestamp = null;
            const activeRec = state.attendances.find(a => a.isActive && ((a.employeeId && a.employeeId === state.currentEmployeeId) || a.employee === state.currentEmployee));
            if (activeRec) {
                state.isCheckedIn = true;
                state.activeCheckInTime = activeRec.checkIn;
                state.checkInTimestamp = activeRec.checkInTimestamp || activeRec.id || Date.now();
                state.tickerInterval = setInterval(updateLiveTicker, 1000);
            }

            // Update navbar
            document.getElementById('nav-avatar').innerText = user.initials || (user.name ? user.name.split(' ').map(n=>n[0]).join('').toUpperCase() : 'U');
            document.getElementById('nav-user-name').innerText = user.name;
            const roleBadge = document.getElementById('nav-user-role-badge');
            if (user.role === 'admin') {
                roleBadge.innerText = 'Admin';
                roleBadge.className = 'badge badge-purple';
            } else {
                roleBadge.innerText = 'Employee';
                roleBadge.className = 'badge badge-green';
            }

            // Show/hide admin-only nav items
            document.querySelectorAll('.nav-admin-only').forEach(el => {
                el.style.display = (user.role === 'admin') ? '' : 'none';
            });

            // Show the app, hide auth wall
            document.getElementById('auth-wall').classList.add('hidden');

            // Render everything for this role
            renderAll();

            // Navigate to the correct dashboard
            if (user.role === 'admin') {
                openTab('dashboard');
            } else {
                openTab('emp-dashboard');
            }
        }

        function guardAdminTab(tabId) {
            const adminOnlyTabs = ['employees', 'payroll'];
            if (adminOnlyTabs.includes(tabId) && state.role !== 'admin') {
                alert('⛔ Access Denied — This section is for HR Administrators only.');
                openTab('emp-dashboard');
                return false;
            }
            return true;
        }

        /* Notifications Engine */
        function triggerNotification(title, recipient, type, body) {
            const notif = {
                id: Date.now(),
                title: title,
                recipient: recipient,
                type: type,
                time: 'Just now',
                body: body
            };
            state.notifications.unshift(notif);
            saveState();
            renderNotifications();
            showToast(title, `${body} (Sent to: ${recipient})`);
        }

        function showToast(title, message) {
            const container = document.getElementById('toast-container');
            if (!container) return;
            const toast = document.createElement('div');
            toast.className = 'toast-msg';
            toast.innerHTML = `
                <div style="font-size: 1.3rem;">✉️</div>
                <div>
                    <div style="font-weight: 700; font-size: 0.88rem; color: #fff;">${title}</div>
                    <div style="font-size: 0.78rem; color: var(--text-muted); margin-top: 3px; line-height: 1.4;">${message}</div>
                </div>
            `;
            container.appendChild(toast);
            setTimeout(() => {
                toast.style.opacity = '0';
                toast.style.transform = 'translateY(10px)';
                toast.style.transition = 'all 0.3s ease';
                setTimeout(() => toast.remove(), 300);
            }, 5500);
        }

        function toggleNotificationModal() {
            const modal = document.getElementById('modal-notifications');
            modal.style.display = modal.style.display === 'none' ? 'flex' : 'none';
        }

        function clearNotifications() {
            state.notifications = [];
            saveState();
            renderNotifications();
        }

        function renderNotifications() {
            const countEl = document.getElementById('notif-count');
            if (countEl) countEl.innerText = state.notifications.length;

            const listEl = document.getElementById('notif-list-container');
            if (!listEl) return;
            if (state.notifications.length === 0) {
                listEl.innerHTML = `<div style="text-align:center; padding:2rem; color:var(--text-muted);">No notifications yet.</div>`;
                return;
            }

            listEl.innerHTML = state.notifications.map(n => {
                const icon = n.type.includes('leave_approved') ? '✅' : n.type.includes('leave_rejected') ? '❌' : n.type.includes('leave') ? '📅' : n.type.includes('login') ? '🔑' : '👤';
                return `
                    <div style="background: var(--bg-card); border: 1px solid var(--border-line); border-radius: 8px; padding: 0.85rem 1rem; display: flex; gap: 0.75rem; align-items: flex-start;">
                        <div style="font-size: 1.25rem;">${icon}</div>
                        <div style="flex: 1;">
                            <div style="display:flex; justify-content:space-between; align-items:center;">
                                <strong style="font-size:0.88rem; color:#fff;">${n.title}</strong>
                                <span style="font-size:0.72rem; color:var(--text-muted);">${n.time}</span>
                            </div>
                            <div style="font-size:0.8rem; color:var(--text-muted); margin-top:2px;">${n.body}</div>
                            <div style="font-size:0.72rem; color:#60a5fa; margin-top:4px;">Recipient: <code>${n.recipient}</code></div>
                        </div>
                    </div>
                `;
            }).join('');
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
            // Access control: enforce admin-only tabs
            if (!guardAdminTab(tabId)) return;

            document.querySelectorAll('.nav-tab').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.tab-panel').forEach(el => el.classList.remove('active'));

            const btn = document.getElementById('tab-btn-' + tabId);
            if (btn) btn.classList.add('active');
            const panel = document.getElementById('panel-' + tabId);
            if (panel) panel.classList.add('active');

            if (tabId === 'profile') renderAdminProfile();
            if (tabId === 'emp-dashboard') renderEmployeeDashboard();
            if (tabId === 'dashboard') renderDashboard();
            if (tabId === 'attendance') renderAttendance();
            if (tabId === 'leave') renderLeaves();
            if (tabId === 'employees') renderEmployees();
            if (tabId === 'documents') renderDocuments();
            if (tabId === 'payroll') renderPayroll();
        }

        function viewEmployeeProfile(empId) {
            state.viewingEmployeeId = empId;
            openTab('profile');
        }

        // onRoleChange is now replaced by login — kept as no-op for safety
        function onRoleChange(role) { /* deprecated: use handleLogin */ }

        function openProfileSection(secId) {
            document.querySelectorAll('.profile-subtab').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.profile-section').forEach(el => el.classList.remove('active'));

            const btn = document.getElementById('psubtab-btn-' + secId);
            if (btn) btn.classList.add('active');
            const sec = document.getElementById('psec-' + secId);
            if (sec) sec.classList.add('active');
        }

        /* Attendance actions with Break Tracking */
        function handleCheckIn() {
            if (state.isCheckedIn) return;
            const now = new Date();
            state.isCheckedIn = true;
            state.isOnBreak = false;
            state.breakSeconds = 0;
            state.breakStartTimestamp = null;
            state.activeCheckInTime = formatTime(now);
            state.checkInTimestamp = now.getTime();

            state.tickerInterval = setInterval(updateLiveTicker, 1000);

            // Add or update active record in attendances
            const todayStr = formatDate(now);
            const activeRec = {
                id: now.getTime(),
                employeeId: state.currentEmployeeId,
                date: todayStr,
                employee: state.currentEmployee,
                checkIn: state.activeCheckInTime,
                checkOut: '--',
                checkInTimestamp: state.checkInTimestamp,
                checkOutTimestamp: null,
                status: 'present',
                workedHours: 0.0,
                breakHours: 0.0,
                effectiveHours: 0.0,
                extraHours: 0.0,
                isActive: true
            };
            state.attendances.unshift(activeRec);

            saveState();
            renderAttendance();
            renderDashboard();
            renderEmployeeDashboard();
        }

        function handleBreakToggle() {
            if (!state.isCheckedIn) return;
            const now = Date.now();
            if (!state.isOnBreak) {
                // Start Break
                state.isOnBreak = true;
                state.breakStartTimestamp = now;
                const btn = document.getElementById('btn-break');
                if (btn) { btn.innerText = '▶️ Resume Work'; btn.className = 'btn btn-primary'; }
                const txt = document.getElementById('txt-status');
                if (txt) txt.innerHTML = '☕ <span style="color:#fbbf24;">On Break</span>';
            } else {
                // Resume Work
                state.isOnBreak = false;
                if (state.breakStartTimestamp) {
                    const elapsedBreak = Math.floor((now - state.breakStartTimestamp) / 1000);
                    state.breakSeconds = (state.breakSeconds || 0) + elapsedBreak;
                    state.breakStartTimestamp = null;
                }
                const btn = document.getElementById('btn-break');
                if (btn) { btn.innerText = '☕ Take a Break'; btn.className = 'btn btn-secondary'; }
                const txt = document.getElementById('txt-status');
                if (txt) txt.innerHTML = 'Present';
            }
            saveState();
            renderAttendance();
        }

        function handleCheckOut() {
            if (!state.isCheckedIn) return;
            const now = new Date();
            if (state.isOnBreak && state.breakStartTimestamp) {
                const elapsedBreak = Math.floor((now.getTime() - state.breakStartTimestamp) / 1000);
                state.breakSeconds = (state.breakSeconds || 0) + elapsedBreak;
                state.breakStartTimestamp = null;
                state.isOnBreak = false;
            }
            state.isCheckedIn = false;
            if (state.tickerInterval) {
                clearInterval(state.tickerInterval);
                state.tickerInterval = null;
            }

            const checkOutStr = formatTime(now);
            const checkOutTimestamp = now.getTime();
            const elapsedHours = state.checkInTimestamp
                ? parseFloat(((checkOutTimestamp - state.checkInTimestamp) / (1000 * 60 * 60)).toFixed(2))
                : 0.0;
            const breakHrs = parseFloat(((state.breakSeconds || 0) / 3600).toFixed(2));
            const effectiveHrs = Math.max(0.0, parseFloat((elapsedHours - breakHrs).toFixed(2)));

            const activeRec = state.attendances.find(a => a.isActive && ((a.employeeId && a.employeeId === state.currentEmployeeId) || a.employee === state.currentEmployee));
            if (activeRec) {
                activeRec.checkOut = checkOutStr;
                activeRec.checkOutTimestamp = checkOutTimestamp;
                activeRec.workedHours = elapsedHours;
                activeRec.breakHours = breakHrs;
                activeRec.effectiveHours = effectiveHrs;
                activeRec.extraHours = effectiveHrs > 8.0 ? parseFloat((effectiveHrs - 8.0).toFixed(2)) : 0.0;
                activeRec.status = effectiveHrs >= 4.0 ? 'present' : 'half_day';
                activeRec.isActive = false;
            }

            saveState();
            renderAttendance();
            renderDashboard();
            renderEmployeeDashboard();
        }

        function updateLiveTicker() {
            if (!state.isCheckedIn || !state.checkInTimestamp) return;
            const now = Date.now();
            const diffMs = now - state.checkInTimestamp;
            const totalSec = Math.floor(diffMs / 1000);
            
            let curBreakSec = state.breakSeconds || 0;
            if (state.isOnBreak && state.breakStartTimestamp) {
                curBreakSec += Math.floor((now - state.breakStartTimestamp) / 1000);
            }
            const effectiveSec = Math.max(0, totalSec - curBreakSec);

            const hrs = Math.floor(totalSec / 3600);
            const mins = Math.floor((totalSec % 3600) / 60);
            const secs = totalSec % 60;

            const bHrs = Math.floor(curBreakSec / 3600);
            const bMins = Math.floor((curBreakSec % 3600) / 60);

            const eHrs = Math.floor(effectiveSec / 3600);
            const eMins = Math.floor((effectiveSec % 3600) / 60);

            const elTotal = document.getElementById('txt-worked-hours');
            const elBreak = document.getElementById('txt-break-hours');
            const elEff = document.getElementById('txt-effective-hours');

            if (elTotal) elTotal.innerText = `${hrs}h ${String(mins).padStart(2,'0')}m ${String(secs).padStart(2,'0')}s`;
            if (elBreak) elBreak.innerText = `${bHrs}h ${String(bMins).padStart(2,'0')}m`;
            if (elEff) elEff.innerText = `${eHrs}h ${String(eMins).padStart(2,'0')}m`;
        }

        /* Leave Modal & Calendar actions */
        function openLeaveModal(prefilledDate) {
            document.getElementById('mleave-emp-name').value = state.currentEmployee;
            document.getElementById('mleave-type').value = 'paid';
            const sessionEl = document.getElementById('mleave-session');
            if (sessionEl) sessionEl.value = 'full';

            const defaultStart = prefilledDate || '2026-08-25';
            const defaultEnd = prefilledDate || '2026-08-27';
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
            const sessionEl = document.getElementById('mleave-session');
            const session = sessionEl ? sessionEl.value : 'full';

            if (startVal && endVal) {
                const s = new Date(startVal);
                const e = new Date(endVal);
                let diffDays = Math.ceil((e - s) / (1000 * 60 * 60 * 24)) + 1;
                if (diffDays <= 0) diffDays = 1;
                
                if (session === 'half_am' || session === 'half_pm') {
                    diffDays = 0.5;
                }
                document.getElementById('mleave-duration-preview').innerText = `${diffDays} Day${diffDays > 1 ? 's' : ''} (${session === 'full' ? 'Full Day' : session === 'half_am' ? 'First Half AM' : 'Second Half PM'})`;
            }
        }

        function handleLeaveModalSubmit(e) {
            e.preventDefault();
            const emp = state.currentEmployee;
            const type = document.getElementById('mleave-type').value;
            const sessionEl = document.getElementById('mleave-session');
            const session = sessionEl ? sessionEl.value : 'full';
            const start = document.getElementById('mleave-start').value;
            const end = document.getElementById('mleave-end').value;
            const reason = document.getElementById('mleave-reason').value;
            const fileInput = document.getElementById('mleave-file');

            if (new Date(end) < new Date(start)) {
                alert('End Date cannot be earlier than Start Date.');
                return;
            }

            let days = Math.max(1, Math.ceil((new Date(end) - new Date(start)) / (1000 * 60 * 60 * 24)) + 1);
            if (session === 'half_am' || session === 'half_pm') {
                days = 0.5;
            }

            state.leaves.unshift({
                id: Date.now(),
                employeeId: state.currentEmployeeId,
                employee: state.currentEmployee,
                type: type,
                session: session,
                isHalfDay: session !== 'full',
                halfDayPeriod: session === 'half_am' ? 'am' : session === 'half_pm' ? 'pm' : null,
                startDate: start,
                endDate: end,
                days: days,
                remarks: reason,
                hasAttachment: fileInput.files && fileInput.files.length > 0,
                status: 'pending',
                adminComments: ''
            });

            saveState();
            closeLeaveModal();
            renderLeaves();
            renderDashboard();
            renderEmployeeDashboard();

            // Trigger Outgoing Leave Submission Notification to HR
            triggerNotification(
                'Time Off: Application Submitted',
                'admin@dayflow.org',
                'leave_submitted',
                `New ${type.toUpperCase()} request from ${emp} (${start} to ${end}, ${days} days - ${session === 'full' ? 'Full Day' : 'Half Day'}). Pending review.`
            );
        }

        function openLeaveDetailModal(id) {
            const leave = state.leaves.find(l => l.id === id);
            if (!leave) return;

            document.getElementById('ld-id').value = leave.id;
            document.getElementById('ld-emp').innerText = leave.employee;
            document.getElementById('ld-type').innerText = leave.type === 'paid' ? 'Paid Time Off' : leave.type === 'sick' ? 'Sick Leave' : 'Unpaid Leave';
            document.getElementById('ld-dates').innerText = `${leave.startDate} → ${leave.endDate}`;
            document.getElementById('ld-days').innerText = `${leave.days} Day${leave.days > 1 ? 's' : ''}`;
            document.getElementById('ld-remarks').innerText = leave.remarks || '--';
            document.getElementById('ld-attachment').innerText = leave.hasAttachment ? '📄 Document / Certificate Attached' : 'No attachment provided';
            document.getElementById('ld-admin-comment').value = leave.adminComments || '';

            const badgeClass = leave.status === 'approved' ? 'badge-green' : leave.status === 'rejected' ? 'badge-red' : 'badge-amber';
            document.getElementById('ld-status-badge').innerHTML = `<span class="badge ${badgeClass}">${leave.status.toUpperCase()}</span>`;

            document.getElementById('modal-leave-detail').style.display = 'flex';
        }

        function closeLeaveDetailModal() {
            document.getElementById('modal-leave-detail').style.display = 'none';
        }

        function submitLeaveDecision(newStatus) {
            const id = parseInt(document.getElementById('ld-id').value);
            const comment = document.getElementById('ld-admin-comment').value;
            const leave = state.leaves.find(l => l.id === id);

            if (leave) {
                leave.status = newStatus;
                leave.adminComments = comment || (newStatus === 'approved' ? 'Approved by HR' : 'Rejected by HR');

                if (newStatus === 'approved') {
                    const targetStatus = leave.isHalfDay ? 'half_day' : 'leave';
                    const worked = leave.isHalfDay ? 4.0 : 0.0;
                    state.attendances.unshift({
                        id: Date.now(),
                        employeeId: leave.employeeId,
                        date: leave.startDate,
                        employee: leave.employee,
                        checkIn: leave.isHalfDay ? (leave.halfDayPeriod === 'pm' ? '01:00 PM' : '09:00 AM') : '--',
                        checkOut: leave.isHalfDay ? (leave.halfDayPeriod === 'pm' ? '05:00 PM' : '01:00 PM') : '--',
                        status: targetStatus,
                        workedHours: worked,
                        breakHours: 0.0,
                        effectiveHours: worked,
                        extraHours: 0.0
                    });
                }

                saveState();
                closeLeaveDetailModal();
                renderAll();

                // Trigger Outgoing Decision Email Notification to Employee
                const empObj = state.employees.find(e => e.name === leave.employee);
                const recipientEmail = empObj ? empObj.email : 'employee@company.com';
                const notifTitle = newStatus === 'approved' ? 'Time Off: Request Approved' : 'Time Off: Request Rejected';
                const notifBody = newStatus === 'approved' ? 
                    `Your ${leave.type.toUpperCase()} request (${leave.isHalfDay ? 'Half-Day' : 'Full Day'}) for ${leave.startDate} to ${leave.endDate} has been approved by HR.` :
                    `Your ${leave.type.toUpperCase()} request was rejected. Remarks: ${leave.adminComments}`;

                triggerNotification(
                    notifTitle,
                    recipientEmail,
                    newStatus === 'approved' ? 'leave_approved' : 'leave_rejected',
                    notifBody
                );
            }
        }

        function handleQuickApprove(id) {
            const leave = state.leaves.find(l => l.id === id);
            if (leave) {
                leave.status = 'approved';
                leave.adminComments = 'Approved by HR';

                const targetStatus = leave.isHalfDay ? 'half_day' : 'leave';
                const worked = leave.isHalfDay ? 4.0 : 0.0;
                state.attendances.unshift({
                    id: Date.now(),
                    employeeId: leave.employeeId,
                    date: leave.startDate,
                    employee: leave.employee,
                    checkIn: leave.isHalfDay ? (leave.halfDayPeriod === 'pm' ? '01:00 PM' : '09:00 AM') : '--',
                    checkOut: leave.isHalfDay ? (leave.halfDayPeriod === 'pm' ? '05:00 PM' : '01:00 PM') : '--',
                    status: targetStatus,
                    workedHours: worked,
                    breakHours: 0.0,
                    effectiveHours: worked,
                    extraHours: 0.0
                });

                saveState();
                renderAll();

                const empObj = state.employees.find(e => e.name === leave.employee);
                triggerNotification(
                    'Time Off: Request Approved',
                    empObj ? empObj.email : 'employee@company.com',
                    'leave_approved',
                    `Your leave request (${leave.isHalfDay ? 'Half-Day' : 'Full Day'}) for ${leave.startDate} to ${leave.endDate} has been approved by HR.`
                );
            }
        }

        function handleQuickReject(id) {
            const leave = state.leaves.find(l => l.id === id);
            if (leave) {
                leave.status = 'rejected';
                leave.adminComments = 'Rejected by HR';
                saveState();
                renderAll();

                const empObj = state.employees.find(e => e.name === leave.employee);
                triggerNotification(
                    'Time Off: Request Rejected',
                    empObj ? empObj.email : 'employee@company.com',
                    'leave_rejected',
                    `Your leave request for ${leave.startDate} to ${leave.endDate} has been rejected by HR.`
                );
            }
        }

        function handleLeaveSubmit(e) {
            handleLeaveModalSubmit(e);
        }

        function handleApproveLeave(id) {
            handleQuickApprove(id);
        }

        function handleRejectLeave(id) {
            handleQuickReject(id);
        }

        /* Calendar Render */
        function renderCalendar() {
            const container = document.getElementById('cal-grid-tiles');
            if (!container) return;

            let html = '';
            for (let pad = 0; pad < 5; pad++) {
                html += `<div class="cal-cell weekend" style="opacity: 0.25; cursor: default;"></div>`;
            }

            for (let day = 1; day <= 31; day++) {
                const dayStr = day < 10 ? `0${day}` : `${day}`;
                const dateStr = `2026-08-${dayStr}`;

                const dObj = new Date(2026, 7, day);
                const dayOfWeek = dObj.getDay();
                const isWeekend = (dayOfWeek === 0 || dayOfWeek === 6);

                const holidayName = HOLIDAYS_AUG_2026[day];

                const matchedLeave = state.leaves.find(l => {
                    const s = l.startDate;
                    const e = l.endDate;
                    return dateStr >= s && dateStr <= e && ((l.employeeId && l.employeeId === state.currentEmployeeId) || l.employee === state.currentEmployee);
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
                    tagHtml = `<span class="cal-tag ${tagStyle}" title="${matchedLeave.type.toUpperCase()}">${matchedLeave.type.toUpperCase()}</span>`;
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
            const errEl = document.getElementById('emp-create-error');
            if (errEl) { errEl.style.display = 'none'; errEl.innerText = ''; }
            card.style.display = card.style.display === 'none' ? 'block' : 'none';
        }

        function showCreateEmpError(msg) {
            const errEl = document.getElementById('emp-create-error');
            if (errEl) {
                errEl.innerText = msg;
                errEl.style.display = 'block';
            } else {
                alert(msg);
            }
        }

        function handleAddEmp(e) {
            e.preventDefault();
            const errEl = document.getElementById('emp-create-error');
            if (errEl) { errEl.style.display = 'none'; errEl.innerText = ''; }

            const name = (document.getElementById('emp-name')?.value || '').trim();
            const email = (document.getElementById('emp-email')?.value || '').trim();
            const phone = (document.getElementById('emp-phone')?.value || '').trim();
            const empCode = (document.getElementById('emp-code')?.value || '').trim();
            const dob = document.getElementById('emp-dob')?.value || '1996-05-15';
            const city = (document.getElementById('emp-city')?.value || '').trim();
            const job = (document.getElementById('emp-job')?.value || '').trim();
            const dept = (document.getElementById('emp-dept')?.value || '').trim();
            const role = document.getElementById('emp-role')?.value || 'Employee';
            const joining = document.getElementById('emp-joining')?.value;
            const loginId = (document.getElementById('emp-login-id')?.value || '').trim();
            const password = document.getElementById('emp-password')?.value;
            const confirmPassword = document.getElementById('emp-confirm-password')?.value;
            const wage = Number(document.getElementById('emp-wage')?.value) || 50000;
            const struct = (document.getElementById('emp-struct')?.value || '').trim() || 'Standard Base';

            // Validation 1: Required fields
            if (!name) {
                showCreateEmpError('Validation Error: Full Name is required.');
                return;
            }
            if (!email) {
                showCreateEmpError('Validation Error: Work Email is required.');
                return;
            }
            if (!job) {
                showCreateEmpError('Validation Error: Job Title is required.');
                return;
            }
            if (!dept) {
                showCreateEmpError('Validation Error: Department is required.');
                return;
            }
            if (!joining) {
                showCreateEmpError('Validation Error: Joining Date is required.');
                return;
            }
            if (!loginId) {
                showCreateEmpError('Validation Error: Login ID / Username is required.');
                return;
            }
            if (!password) {
                showCreateEmpError('Validation Error: Password is required.');
                return;
            }

            // Validation 2: Password matching
            if (password !== confirmPassword) {
                showCreateEmpError('Validation Error: Password and Confirm Password do not match.');
                return;
            }

            // Validation 3: Duplicate Login ID
            const loginLower = loginId.toLowerCase();
            const userList = (state && state.users) ? state.users : DEFAULT_USERS;
            if (userList.some(u => (u.loginId || '').toLowerCase() === loginLower) ||
                state.employees.some(emp => (emp.loginId || '').toLowerCase() === loginLower)) {
                showCreateEmpError(`Validation Error: Login ID "${loginId}" is already in use. Please choose another username.`);
                return;
            }

            // Generate unique employee ID
            const newId = state.employees.reduce((max, emp) => Math.max(max, Number(emp.id) || 0), 0) + 1;

            const newEmp = {
                id: newId,
                code: empCode || `EMP${String(newId).padStart(3, '0')}`,
                name: name,
                email: email,
                phone: phone || '+91 98765 00000',
                personalPhone: phone || '+91 98765 00000',
                job: job,
                dept: dept,
                role: role,
                joining: joining,
                dob: dob || '1995-01-01',
                gender: 'Male',
                nationality: 'Indian',
                marital: 'Single',
                aadhar: '--',
                pan: '--',
                passport: '--',
                street: '--',
                city: city || 'Bangalore, Karnataka',
                pin: '--',
                country: 'India',
                emgName: '--',
                emgPhone: '--',
                bankName: 'HDFC Bank (Salary Account)',
                bankAcc: '--',
                bankIfsc: '--',
                loginId: loginId,
                monthlyWage: wage,
                struct: struct,
                provisioned: true
            };

            const newUser = {
                userId: `u_${newId}`,
                loginId: loginId,
                password: password,
                role: role === 'Admin / HR' ? 'admin' : 'employee',
                employeeId: newId,
                name: name,
                initials: name.split(' ').map(n=>n[0]).join('').toUpperCase() || 'U',
                email: email
            };

            state.employees.push(newEmp);
            state.users.push(newUser);

            state.payrolls.push({
                id: Date.now(),
                employeeId: newId,
                ref: `PAY/2026/00${state.payrolls.length + 1}`,
                employee: newEmp.name,
                structure: newEmp.struct,
                period: 'August 2026',
                base: Math.round(wage * 0.8),
                allow: Math.round(wage * 0.2),
                deduct: Math.round(wage * 0.08),
                status: 'draft'
            });

            saveState();
            renderAll();
            e.target.reset();
            toggleEmpForm();

            // Trigger Outgoing Account Creation Welcome Email
            triggerNotification(
                'Welcome: Dayflow Account Created',
                newEmp.email,
                'account_created',
                `Hello ${newEmp.name}, your Dayflow account (${newEmp.loginId}) has been created. Login access granted.`
            );

            alert(`✅ Employee "${name}" created successfully!
Login ID: ${loginId}
Role: ${newUser.role.toUpperCase()}`);
        }

        function handleProvision(id) {
            const emp = state.employees.find(e => e.id === id);
            if (emp) {
                const year = emp.joining ? emp.joining.split('-')[0] : '2026';
                emp.provisioned = true;
                emp.loginId = `DAYFLOW-${emp.name.replace(/[^A-Z]/gi, '').toUpperCase()}-${year}-000${Math.floor(Math.random() * 90 + 10)}`;
                const userList = (state && state.users) ? state.users : DEFAULT_USERS;
                if (!userList.some(u => u.loginId === emp.loginId)) {
                    state.users.push({
                        userId: `u_${emp.id}`,
                        loginId: emp.loginId,
                        password: 'emp123',
                        role: emp.role === 'Admin / HR' ? 'admin' : 'employee',
                        employeeId: emp.id,
                        name: emp.name,
                        initials: emp.name.split(' ').map(n=>n[0]).join('').toUpperCase() || 'U'
                    });
                }
                saveState();
                renderEmployees();
                renderDashboard();

                triggerNotification(
                    'Welcome: Account Provisioned',
                    emp.email,
                    'account_created',
                    `Hello ${emp.name}, your Dayflow credentials have been provisioned (${emp.loginId}).`
                );
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
                const targetEmp = (state.role === 'employee') ? state.currentEmployee : (document.getElementById('doc-employee')?.value || state.currentEmployee);
                const targetEmpRec = state.employees.find(emp => emp.name === targetEmp || (state.currentEmployeeId && emp.id === state.currentEmployeeId));
                const targetEmpId = targetEmpRec ? targetEmpRec.id : state.currentEmployeeId;

                state.documents.unshift({
                    id: Date.now(),
                    employeeId: targetEmpId,
                    title: document.getElementById('doc-title').value || file.name,
                    employee: targetEmp,
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
                renderEmployeeDashboard();
                e.target.reset();
                alert('Document uploaded successfully.');
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
            let targetEmp;
            if (payId) {
                const pay = state.payrolls.find(p => p.id === payId);
                if (pay) {
                    targetEmp = state.employees.find(e => (pay.employeeId && e.id === pay.employeeId) || e.name === pay.employee) || { name: pay.employee, monthlyWage: pay.base, struct: pay.structure };
                }
            }
            if (!targetEmp) {
                const targetId = (state.role === 'admin' && state.viewingEmployeeId) ? state.viewingEmployeeId : state.currentEmployeeId;
                targetEmp = state.employees.find(e => e.id === targetId || (state.currentEmployeeId && e.id === state.currentEmployeeId) || e.name === state.currentEmployee) || state.employees[0];
            }

            const wage = Number(targetEmp.monthlyWage) || 50000;
            const struct = targetEmp.struct || 'Standard Base';
            const payRec = state.payrolls.find(p => (targetEmp.id && p.employeeId === targetEmp.id) || p.employee === targetEmp.name);

            document.getElementById('modal-pay-id').value = payRec ? payRec.id : (payId || '');
            document.getElementById('modal-pay-emp').value = targetEmp.name;
            document.getElementById('modal-pay-struct').value = struct;
            document.getElementById('modal-pay-base').value = wage;
            document.getElementById('modal-pay-allow').value = payRec ? payRec.allow : Math.round(wage * 0.2);
            document.getElementById('modal-pay-deduct').value = payRec ? payRec.deduct : Math.round(wage * 0.08);

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
            const base = parseFloat(document.getElementById('modal-pay-base').value) || 50000;
            const allow = parseFloat(document.getElementById('modal-pay-allow').value) || Math.round(base * 0.2);
            const deduct = parseFloat(document.getElementById('modal-pay-deduct').value) || Math.round(base * 0.08);
            const struct = document.getElementById('modal-pay-struct').value || 'Standard Base';
            const empName = document.getElementById('modal-pay-emp').value;

            const emp = state.employees.find(e => e.name === empName || (state.currentEmployeeId && e.id === state.currentEmployeeId));
            if (emp) {
                emp.monthlyWage = base;
                emp.struct = struct;
            }

            let pay = idVal ? state.payrolls.find(p => p.id === parseInt(idVal)) : null;
            if (!pay) {
                pay = state.payrolls.find(p => (emp && emp.id && p.employeeId === emp.id) || p.employee === empName);
            }

            if (pay) {
                pay.base = base;
                pay.allow = allow;
                pay.deduct = deduct;
                pay.structure = struct;
                if (emp && emp.id) pay.employeeId = emp.id;
            } else {
                state.payrolls.push({
                    id: Date.now(),
                    employeeId: emp ? emp.id : state.currentEmployeeId,
                    ref: `PAY/2026/00${state.payrolls.length + 1}`,
                    employee: empName,
                    structure: struct,
                    period: 'August 2026',
                    base: base,
                    allow: allow,
                    deduct: deduct,
                    status: 'draft'
                });
            }

            if (emp && (emp.name === 'Jane Smith' || emp.id === 2)) {
                state.adminProfile.monthlyWage = base;
                state.adminProfile.struct = struct;
            }

            saveState();
            closeSalaryModal();
            renderAdminProfile();
            renderPayroll();
            renderDashboard();
            alert('Salary structure updated successfully!');
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
            const targetId = (state.role === 'admin' && state.viewingEmployeeId) ? state.viewingEmployeeId : state.currentEmployeeId;
            let p;
            if (state.role === 'employee') {
                p = state.employees.find(e => (state.currentEmployeeId && e.id === state.currentEmployeeId) || e.name === state.currentEmployee) || state.employees[0];
                const workSec = document.getElementById('m-work-sec');
                if (workSec) workSec.style.display = 'none';
            } else {
                const empRec = state.employees.find(e => e.id === targetId || (state.currentEmployeeId && e.id === state.currentEmployeeId) || e.name === state.currentEmployee);
                p = Object.assign({}, (targetId === 2 ? state.adminProfile : {}), empRec || {});
                const workSec = document.getElementById('m-work-sec');
                if (workSec) {
                    workSec.style.display = 'block';
                    document.getElementById('m-job').value = (p.job && p.job !== '--') ? p.job : ((p.title && p.title !== '--') ? p.title : '');
                    document.getElementById('m-dept').value = (p.dept && p.dept !== '--') ? p.dept : '';
                    document.getElementById('m-manager').value = p.reportsTo || (p.role === 'Admin / HR' ? 'Board of Directors / CEO' : 'Jane Smith (HR Head)');
                    document.getElementById('m-location').value = p.workLocation || (p.city ? `${p.city} Office` : 'Bangalore Headquarters (HQ)');
                    document.getElementById('m-schedule').value = p.workSchedule || '40 Hours / Week (Mon-Fri)';
                    document.getElementById('m-role').value = p.role || 'Admin / HR';
                }
            }

            document.getElementById('m-dob').value = (p.dob && p.dob !== '--') ? p.dob : '';
            document.getElementById('m-gender').value = (p.gender && p.gender !== '--') ? p.gender : 'Male';
            document.getElementById('m-nationality').value = (p.nationality && p.nationality !== '--') ? p.nationality : 'Indian';
            document.getElementById('m-marital').value = (p.marital && p.marital !== '--') ? p.marital : 'Single';
            document.getElementById('m-phone').value = (p.personalPhone && p.personalPhone !== '--') ? p.personalPhone : (p.phone && p.phone !== '--' ? p.phone : '');
            document.getElementById('m-aadhar').value = (p.aadhar && p.aadhar !== '--') ? p.aadhar : '';
            document.getElementById('m-pan').value = (p.pan && p.pan !== '--') ? p.pan : '';
            document.getElementById('m-passport').value = (p.passport && p.passport !== '--') ? p.passport : '';

            document.getElementById('m-street').value = (p.street && p.street !== '--') ? p.street : '';
            document.getElementById('m-city').value = (p.city && p.city !== '--') ? p.city : '';
            document.getElementById('m-pin').value = (p.pin && p.pin !== '--') ? p.pin : '';
            document.getElementById('m-country').value = (p.country && p.country !== '--') ? p.country : 'India';

            document.getElementById('m-emg').value = (p.emgName && p.emgName !== '--') ? p.emgName : '';
            document.getElementById('m-emg-phone').value = (p.emgPhone && p.emgPhone !== '--') ? p.emgPhone : '';
            document.getElementById('m-bank-name').value = (p.bankName && p.bankName !== '--') ? p.bankName : '';
            document.getElementById('m-bank-acc').value = (p.bankAcc && p.bankAcc !== '--') ? p.bankAcc : '';
            document.getElementById('m-bank-ifsc').value = (p.bankIfsc && p.bankIfsc !== '--') ? p.bankIfsc : '';

            document.getElementById('private-info-modal').style.display = 'flex';
        }

        function closeEditPrivateModal() {
            document.getElementById('private-info-modal').style.display = 'none';
        }

        function handleSavePrivateInfo(e) {
            e.preventDefault();
            const targetId = (state.role === 'admin' && state.viewingEmployeeId) ? state.viewingEmployeeId : state.currentEmployeeId;

            const dob = document.getElementById('m-dob').value;
            const gender = document.getElementById('m-gender').value;
            const nationality = document.getElementById('m-nationality').value;
            const marital = document.getElementById('m-marital').value;
            const phone = document.getElementById('m-phone').value;
            const aadhar = document.getElementById('m-aadhar').value;
            const pan = document.getElementById('m-pan').value;
            const passport = document.getElementById('m-passport').value;

            const street = document.getElementById('m-street').value;
            const city = document.getElementById('m-city').value;
            const pin = document.getElementById('m-pin').value;
            const country = document.getElementById('m-country').value;

            const emgName = document.getElementById('m-emg').value;
            const emgPhone = document.getElementById('m-emg-phone').value;
            const bankName = document.getElementById('m-bank-name').value;
            const bankAcc = document.getElementById('m-bank-acc').value;
            const bankIfsc = document.getElementById('m-bank-ifsc').value;

            let emp = state.employees.find(e => e.id === targetId || (state.currentEmployeeId && e.id === state.currentEmployeeId) || e.name === state.currentEmployee);
            if (emp) {
                emp.dob = dob;
                emp.gender = gender;
                emp.nationality = nationality;
                emp.marital = marital;
                emp.personalPhone = phone;
                emp.phone = phone || emp.phone;
                emp.aadhar = aadhar;
                emp.pan = pan;
                emp.passport = passport;
                emp.street = street;
                emp.city = city;
                emp.pin = pin;
                emp.country = country;
                emp.emgName = emgName;
                emp.emgPhone = emgPhone;
                emp.bankName = bankName;
                emp.bankAcc = bankAcc;
                emp.bankIfsc = bankIfsc;

                if (state.role === 'admin') {
                    const job = document.getElementById('m-job')?.value;
                    const dept = document.getElementById('m-dept')?.value;
                    const manager = document.getElementById('m-manager')?.value;
                    const loc = document.getElementById('m-location')?.value;
                    const sched = document.getElementById('m-schedule')?.value;
                    const role = document.getElementById('m-role')?.value;

                    if (job) emp.job = job;
                    if (dept) emp.dept = dept;
                    if (manager) emp.reportsTo = manager;
                    if (loc) emp.workLocation = loc;
                    if (sched) emp.workSchedule = sched;
                    if (role) emp.role = role;
                }
            }

            if (state.role === 'admin' && (targetId === 2 || !state.viewingEmployeeId)) {
                Object.assign(state.adminProfile, {
                    dob, gender, nationality, marital, personalPhone: phone, phone,
                    aadhar, pan, passport, street, city, pin, country,
                    emgName, emgPhone, bankName, bankAcc, bankIfsc
                });
                const job = document.getElementById('m-job')?.value;
                const dept = document.getElementById('m-dept')?.value;
                const manager = document.getElementById('m-manager')?.value;
                const loc = document.getElementById('m-location')?.value;
                const sched = document.getElementById('m-schedule')?.value;
                const role = document.getElementById('m-role')?.value;
                if (job) state.adminProfile.title = job;
                if (dept) state.adminProfile.dept = dept;
                if (manager) state.adminProfile.reportsTo = manager;
                if (loc) state.adminProfile.workLocation = loc;
                if (sched) state.adminProfile.workSchedule = sched;
                if (role) state.adminProfile.role = role;
            }

            saveState();
            closeEditPrivateModal();
            renderAdminProfile();
            renderDashboard();
            renderEmployees();
            alert('Profile details updated successfully!');
        }

        /* Render Admin / Employee Profile */
        function renderAdminProfile() {
            const targetId = (state.role === 'admin' && state.viewingEmployeeId) ? state.viewingEmployeeId : state.currentEmployeeId;
            let p;
            if (state.role === 'employee') {
                p = state.employees.find(e => (state.currentEmployeeId && e.id === state.currentEmployeeId) || e.name === state.currentEmployee);
                if (!p) p = state.employees[0];
            } else {
                const empRec = state.employees.find(e => e.id === targetId || (state.currentEmployeeId && e.id === state.currentEmployeeId) || e.name === state.currentEmployee);
                p = Object.assign({}, (targetId === 2 ? state.adminProfile : {}), empRec || {});
            }

            const wage = Number(p.monthlyWage) || 50000;
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

            // Hero
            document.getElementById('prof-hero-name').innerText = p.name || '--';
            document.getElementById('prof-hero-avatar').innerText = (p.name || 'U').split(' ').map(n=>n[0]).join('').toUpperCase();
            document.getElementById('prof-hero-title').innerText = `${p.job || p.title || '--'} • ${p.dept || '--'}`;
            document.getElementById('prof-hero-login').innerText = `🔑 ${p.loginId || '--'}`;
            document.getElementById('prof-hero-email').innerText = `✉️ ${p.email || '--'}`;
            document.getElementById('prof-hero-phone').innerText = `📞 ${p.phone || p.personalPhone || '--'}`;
            const joinDate = p.joining ? new Date(p.joining).toLocaleDateString('en-US', {month:'short', day:'numeric', year:'numeric'}) : '--';
            document.getElementById('prof-hero-joined').innerText = `📅 Joined ${joinDate}`;

            // Update role badge
            const badge = document.getElementById('prof-hero-badge');
            if (badge) { badge.innerText = p.role || 'Employee'; }

            // Hide admin-only edit buttons for employees
            document.querySelectorAll('.prof-admin-edit-btn').forEach(b => {
                b.style.display = state.role === 'admin' ? '' : 'none';
            });

            // Section 1: Private Info
            document.getElementById('prof-dob').innerText = p.dob || '--';
            document.getElementById('prof-gender').innerText = p.gender || '--';
            document.getElementById('prof-nationality').innerText = p.nationality || 'Indian';
            document.getElementById('prof-marital').innerText = p.marital || '--';
            document.getElementById('prof-aadhar').innerText = p.aadhar || '--';
            document.getElementById('prof-pan').innerText = p.pan || '--';
            document.getElementById('prof-passport').innerText = p.passport || '--';
            document.getElementById('prof-personal-phone').innerText = p.personalPhone || p.phone || '--';
            document.getElementById('prof-addr-street').innerText = p.street || '--';
            document.getElementById('prof-addr-city').innerText = p.city || '--';
            document.getElementById('prof-addr-pin').innerText = p.pin || '--';
            document.getElementById('prof-addr-country').innerText = p.country || 'India';
            document.getElementById('prof-emg-name').innerText = p.emgName || '--';
            document.getElementById('prof-emg-phone').innerText = p.emgPhone || '--';
            document.getElementById('prof-bank-name').innerText = p.bankName || '--';
            document.getElementById('prof-bank-acc').innerText = p.bankAcc || '--';
            document.getElementById('prof-bank-ifsc').innerText = p.bankIfsc || '--';

            // Section 2: Salary Breakdown
            document.getElementById('prof-sal-wage').innerText = formatCurrency(wage);
            document.getElementById('prof-sal-ctc').innerText = formatCurrency(wage * 12);
            document.getElementById('prof-sal-net').innerText = formatCurrency(netSalary);
            document.getElementById('prof-sal-struct').innerText = p.struct || 'Standard Base';
            document.getElementById('prof-comp-basic').innerText = formatCurrency(basic);
            document.getElementById('prof-comp-hra').innerText = formatCurrency(hra);
            document.getElementById('prof-comp-std').innerText = formatCurrency(stdAllow);
            document.getElementById('prof-comp-bonus').innerText = formatCurrency(bonus);
            document.getElementById('prof-comp-lta').innerText = formatCurrency(lta);
            document.getElementById('prof-comp-pf').innerText = `- ${formatCurrency(pf)}`;
            document.getElementById('prof-comp-deduct-total').innerText = `- ${formatCurrency(totalDeduct)}`;

            // Section 3: Work & Privileges
            const jobEl = document.getElementById('prof-work-job');
            if (jobEl) jobEl.innerText = p.job || p.title || '--';
            const deptEl = document.getElementById('prof-work-dept');
            if (deptEl) deptEl.innerText = p.dept || '--';
            const mgrEl = document.getElementById('prof-work-manager');
            if (mgrEl) mgrEl.innerText = p.role === 'Admin / HR' ? 'Board of Directors / CEO' : 'Jane Smith (HR Head)';
            const locEl = document.getElementById('prof-work-location');
            if (locEl) locEl.innerText = p.city ? `${p.city} Office` : 'Bangalore Headquarters (HQ)';
            const schedEl = document.getElementById('prof-work-schedule');
            if (schedEl) schedEl.innerText = '40 Hours / Week (Mon-Fri)';
            const secEl = document.getElementById('prof-work-sec-group');
            if (secEl) secEl.innerText = p.role === 'Admin / HR' ? 'dayflow.group_dayflow_admin' : 'dayflow.group_dayflow_user';
            const privNote = document.getElementById('prof-work-privileges-note');
            if (privNote) {
                if (p.role === 'Admin / HR') {
                    privNote.innerHTML = '🛡️ <strong>Admin Privileges:</strong> Full authorization to approve/reject time off requests, verify compliance documents, adjust employee salary structures, provision user accounts, and review executive metrics.';
                } else {
                    privNote.innerHTML = '👤 <strong>Employee Access:</strong> Access to check-in/out attendance tracking, time-off leave applications, personal compensation records, and verified compliance document uploads.';
                }
            }

            // Section 4: Verified Documents
            const docTbl = document.getElementById('prof-tbl-docs');
            if (docTbl) {
                const myVerifiedDocs = state.documents.filter(d => (d.employeeId === p.id || d.employee === p.name) && d.status === 'verified');
                if (myVerifiedDocs.length === 0) {
                    docTbl.innerHTML = '<tr><td colspan="5" style="text-align:center; color:var(--text-muted); padding:1rem;">No verified compliance documents on file.</td></tr>';
                } else {
                    docTbl.innerHTML = myVerifiedDocs.map(d => `
                        <tr>
                            <td><strong>${d.title}</strong></td>
                            <td><span class="badge badge-purple">${(d.type || '').toUpperCase()}</span></td>
                            <td><code>${d.filename}</code></td>
                            <td>${d.date}</td>
                            <td><span class="badge badge-green">VERIFIED</span></td>
                        </tr>
                    `).join('');
                }
            }
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
                                <button class="btn btn-success" style="padding:0.25rem 0.55rem; font-size:0.75rem;" onclick="handleQuickApprove(${l.id})">Approve</button>
                                <button class="btn btn-danger" style="padding:0.25rem 0.55rem; font-size:0.75rem;" onclick="handleQuickReject(${l.id})">Reject</button>
                            </div>
                        </td>
                    </tr>
                `).join('');
            }

            const tbodyAtt = document.getElementById('dash-tbl-today-attendance');
            tbodyAtt.innerHTML = state.attendances.slice(0, 5).map(a => `
                <tr onclick="openTab('attendance')" style="cursor:pointer;" title="Click to view Attendance">
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
                <tr onclick="viewEmployeeProfile(${e.id})" style="cursor:pointer;" title="Click to view profile">
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
            const btnBreak = document.getElementById('btn-break');
            const btnOut = document.getElementById('btn-out');

            if (state.isCheckedIn) {
                dot.className = 'dot green';
                txt.innerText = state.isOnBreak ? '☕ On Break' : 'Present';
                checkIn.innerText = state.activeCheckInTime || '--:--';
                btnIn.disabled = true;
                if (btnBreak) {
                    btnBreak.disabled = false;
                    btnBreak.innerText = state.isOnBreak ? '▶️ Resume Work' : '☕ Take a Break';
                    btnBreak.className = state.isOnBreak ? 'btn btn-primary' : 'btn btn-secondary';
                }
                btnOut.disabled = false;
            } else {
                dot.className = 'dot red';
                txt.innerText = 'Not Checked In';
                checkIn.innerText = '--:--';
                document.getElementById('txt-worked-hours').innerText = '0h 00m';
                const elBreak = document.getElementById('txt-break-hours');
                const elEff = document.getElementById('txt-effective-hours');
                if (elBreak) elBreak.innerText = '0h 00m';
                if (elEff) elEff.innerText = '0h 00m';
                btnIn.disabled = false;
                if (btnBreak) {
                    btnBreak.disabled = true;
                    btnBreak.innerText = '☕ Take a Break';
                    btnBreak.className = 'btn btn-secondary';
                }
                btnOut.disabled = true;
            }
            renderAttendanceTbl();
            renderPayrollLedger();
        }

        function renderAttendanceTbl() {
            const tbody = document.getElementById('tbl-attendance');
            let data = state.role === 'employee' ? state.attendances.filter(a => (a.employeeId && a.employeeId === state.currentEmployeeId) || a.employee === state.currentEmployee) : state.attendances;

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

        /* Monthly Payroll Attendance Ledger (Person 4 Cross-Module Integration) */
        function renderPayrollLedger() {
            const tbody = document.getElementById('tbl-payroll-ledger');
            if (!tbody) return;

            const employees = state.employees || [];
            tbody.innerHTML = employees.map(emp => {
                const empAtts = state.attendances.filter(a => a.employeeId === emp.id || a.employee === emp.name);
                const empLeaves = state.leaves.filter(l => (l.employeeId === emp.id || l.employee === emp.name) && l.status === 'approved');

                const presentCount = empAtts.filter(a => a.status === 'present').length;
                const halfDayCount = empAtts.filter(a => a.status === 'half_day').length;
                const paidLeavesCount = empLeaves.filter(l => l.type === 'paid' || l.type === 'sick').reduce((s, l) => s + (l.days || 0), 0);
                const unpaidLeavesCount = empLeaves.filter(l => l.type === 'unpaid').reduce((s, l) => s + (l.days || 0), 0);
                const totalOvertime = empAtts.reduce((s, a) => s + (a.extraHours || 0), 0).toFixed(1);

                // Standard Working Days for month (22 business days)
                const workingDays = 22;
                // Final Payable Days = Present + (0.5 * Half-Day) + Paid Leaves
                const payableDays = Math.min(workingDays, (presentCount + (0.5 * halfDayCount) + paidLeavesCount)).toFixed(1);

                return `
                    <tr>
                        <td>
                            <strong>${emp.name}</strong>
                            <div style="font-size:0.75rem; color:var(--text-muted);">${emp.job} (${emp.dept})</div>
                        </td>
                        <td>${workingDays} Days</td>
                        <td><span class="badge badge-green">${presentCount} Days</span></td>
                        <td><span class="badge badge-amber">${halfDayCount} (0.5d)</span></td>
                        <td><span class="badge badge-purple">${paidLeavesCount} Days</span></td>
                        <td><span class="badge ${unpaidLeavesCount > 0 ? 'badge-red' : 'badge-secondary'}">${unpaidLeavesCount} Days</span></td>
                        <td style="color:${parseFloat(totalOvertime) > 0 ? '#34d399' : 'inherit'}; font-weight:600;">${totalOvertime}h</td>
                        <td><strong style="color:#34d399; font-size:1rem;">${payableDays} / ${workingDays}</strong></td>
                    </tr>
                `;
            }).join('');
        }

        /* Render Leaves */
        function renderLeaves() {
            const calContainer = document.getElementById('leave-cal-container');
            const adminBanner = document.getElementById('leave-admin-banner');
            const headerSub = document.getElementById('leave-header-sub');
            const tblTitle = document.getElementById('leave-table-title');
            const tblTag = document.getElementById('leave-table-tag');
            const thead = document.getElementById('leave-table-head');
            const tbody = document.getElementById('tbl-leave');

            const lbl1 = document.getElementById('leave-lbl-p1');
            const val1 = document.getElementById('leave-val-p1');
            const lbl2 = document.getElementById('leave-lbl-p2');
            const val2 = document.getElementById('leave-val-p2');
            const lbl3 = document.getElementById('leave-lbl-p3');
            const val3 = document.getElementById('leave-val-p3');
            const lbl4 = document.getElementById('leave-lbl-p4');
            const val4 = document.getElementById('leave-val-p4');

            if (state.role === 'employee') {
                // EMPLOYEE VIEW: Dynamic balance calculation
                const myLeaves = state.leaves.filter(l => (l.employeeId && l.employeeId === state.currentEmployeeId) || l.employee === state.currentEmployee);
                const usedPaid = myLeaves.filter(l => l.type === 'paid' && l.status === 'approved').reduce((sum, l) => sum + (l.days || 0), 0);
                const usedSick = myLeaves.filter(l => l.type === 'sick' && l.status === 'approved').reduce((sum, l) => sum + (l.days || 0), 0);
                const remPaid = Math.max(0, 24 - usedPaid);
                const remSick = Math.max(0, 7 - usedSick);

                if (calContainer) calContainer.style.display = 'grid';
                if (adminBanner) adminBanner.style.display = 'none';
                if (headerSub) headerSub.innerText = 'Manage your time off, view official company holidays, and track leave balances';
                if (tblTitle) tblTitle.innerText = 'My Time Off';
                if (tblTag) tblTag.innerText = 'Personal Leave Log';

                if (lbl1) lbl1.innerText = 'Paid Time Off';
                if (val1) { val1.innerText = `${remPaid} Days Available`; val1.style.color = '#34d399'; }
                if (lbl2) lbl2.innerText = 'Sick Time Off';
                if (val2) { val2.innerText = `${remSick} Days Available`; val2.style.color = '#fbbf24'; }
                if (lbl3) lbl3.innerText = 'Unpaid Leaves';
                if (val3) { val3.innerText = 'Unlimited'; val3.style.color = '#60a5fa'; }
                if (lbl4) lbl4.innerText = 'Upcoming Holidays';
                if (val4) { val4.innerText = '4 This Year'; val4.style.color = 'var(--accent-purple-hover)'; }

                thead.innerHTML = `
                    <tr>
                        <th>Type</th>
                        <th>Start</th>
                        <th>End</th>
                        <th>Duration</th>
                        <th>Remarks</th>
                        <th>Status</th>
                        <th>HR Comments</th>
                    </tr>
                `;

                if (myLeaves.length === 0) {
                    tbody.innerHTML = `<tr><td colspan="7" style="text-align:center; color:var(--text-muted); padding:1.5rem;">You have not applied for any leaves yet. Click <strong>+ NEW APPLICATION</strong> to apply.</td></tr>`;
                } else {
                    tbody.innerHTML = myLeaves.map(l => {
                        const badge = l.status === 'approved' ? 'badge-green' : l.status === 'rejected' ? 'badge-red' : 'badge-amber';
                        const typeLabel = l.type === 'paid' ? 'Paid Time Off' : l.type === 'sick' ? 'Sick Leave' : 'Unpaid Leave';
                        return `
                            <tr>
                                <td><strong>${typeLabel}</strong></td>
                                <td>${l.startDate}</td>
                                <td>${l.endDate}</td>
                                <td>${l.days} Day${l.days>1?'s':''}</td>
                                <td style="color:var(--text-muted);">${l.remarks}</td>
                                <td><span class="badge ${badge}">${l.status.toUpperCase()}</span></td>
                                <td style="color:var(--text-muted); font-size:0.8rem;">${l.adminComments || '--'}</td>
                            </tr>
                        `;
                    }).join('');
                }

                renderCalendar();
            } else {
                // ADMIN / HR VIEW
                if (calContainer) calContainer.style.display = 'none';
                if (adminBanner) adminBanner.style.display = 'block';
                if (headerSub) headerSub.innerText = 'Review, approve, or reject employee time off applications across the organization';
                if (tblTitle) tblTitle.innerText = 'All Employee Time Off Applications (HR Decision Hub)';
                if (tblTag) tblTag.innerText = 'Organization-Wide Queue';

                const totalPending = state.leaves.filter(l => l.status === 'pending').length;
                const totalApproved = state.leaves.filter(l => l.status === 'approved').length;

                if (lbl1) lbl1.innerText = 'Paid Time Off Available';
                if (val1) { val1.innerText = '24 Days Standard'; val1.style.color = '#34d399'; }
                if (lbl2) lbl2.innerText = 'Sick Leave Available';
                if (val2) { val2.innerText = '07 Days Standard'; val2.style.color = '#fbbf24'; }
                if (lbl3) lbl3.innerText = 'Total Pending Requests';
                if (val3) { val3.innerText = `${totalPending} Pending`; val3.style.color = '#f87171'; }
                if (lbl4) lbl4.innerText = 'Total Approved Leaves';
                if (val4) { val4.innerText = `${totalApproved} Approved`; val4.style.color = '#60a5fa'; }

                thead.innerHTML = `
                    <tr>
                        <th>Employee</th>
                        <th>Start Date</th>
                        <th>End Date</th>
                        <th>Duration</th>
                        <th>Time Off Type</th>
                        <th>Status</th>
                        <th style="text-align: right;">Actions</th>
                    </tr>
                `;

                if (state.leaves.length === 0) {
                    tbody.innerHTML = `<tr><td colspan="7" style="text-align:center; color:var(--text-muted); padding:1.5rem;">No leave requests found.</td></tr>`;
                } else {
                    tbody.innerHTML = state.leaves.map(l => {
                        const badge = l.status === 'approved' ? 'badge-green' : l.status === 'rejected' ? 'badge-red' : 'badge-amber';
                        const typeLabel = l.type === 'paid' ? 'Paid Time Off' : l.type === 'sick' ? 'Sick Leave' : 'Unpaid Leave';
                        
                        let actionsHtml = '';
                        if (l.status === 'pending') {
                            actionsHtml = `
                                <div style="display:inline-flex; gap:0.35rem; justify-content:flex-end;">
                                    <button class="btn btn-secondary" style="padding:0.2rem 0.5rem; font-size:0.75rem;" onclick="openLeaveDetailModal(${l.id})">👁️ Details</button>
                                    <button class="btn btn-success" style="padding:0.2rem 0.5rem; font-size:0.75rem;" onclick="handleQuickApprove(${l.id})">Approve</button>
                                    <button class="btn btn-danger" style="padding:0.2rem 0.5rem; font-size:0.75rem;" onclick="handleQuickReject(${l.id})">Reject</button>
                                </div>
                            `;
                        } else {
                            actionsHtml = `
                                <div style="display:inline-flex; gap:0.35rem; justify-content:flex-end;">
                                    <button class="btn btn-secondary" style="padding:0.2rem 0.5rem; font-size:0.75rem;" onclick="openLeaveDetailModal(${l.id})">👁️ View Details</button>
                                </div>
                            `;
                        }

                        return `
                            <tr>
                                <td><strong>${l.employee}</strong></td>
                                <td>${l.startDate}</td>
                                <td>${l.endDate}</td>
                                <td>${l.days} Day${l.days>1?'s':''}</td>
                                <td><span class="badge badge-purple">${typeLabel}</span></td>
                                <td><span class="badge ${badge}">${l.status.toUpperCase()}</span></td>
                                <td style="text-align: right;">${actionsHtml}</td>
                            </tr>
                        `;
                    }).join('');
                }
            }
        }

        function renderEmployees() {
            const grid = document.getElementById('grid-employees');
            if (!grid) return;
            grid.innerHTML = state.employees.map(e => `
                <div class="emp-card" onclick="viewEmployeeProfile(${e.id})" style="cursor:pointer;" title="Click to view full profile">
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

            const docEmpSelect = document.getElementById('doc-employee');
            if (docEmpSelect) {
                if (state.role === 'employee') {
                    docEmpSelect.innerHTML = `<option value="${state.currentEmployee}">${state.currentEmployee}</option>`;
                    docEmpSelect.disabled = true;
                } else {
                    docEmpSelect.disabled = false;
                    docEmpSelect.innerHTML = state.employees.map(e => `
                        <option value="${e.name}" ${e.name === state.currentEmployee ? 'selected' : ''}>${e.name} (${e.dept || e.job})</option>
                    `).join('');
                }
            }

            const tbody = document.getElementById('tbl-documents');
            let data = state.documents;
            if (state.role === 'employee') data = data.filter(d => (d.employeeId && d.employeeId === state.currentEmployeeId) || d.employee === state.currentEmployee);

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
                data = data.filter(p => (p.employeeId && p.employeeId === state.currentEmployeeId) || p.employee === state.currentEmployee);
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

        function renderEmployeeDashboard() {
            const empName = state.currentEmployee;
            const empId = state.currentEmployeeId;
            const today = new Date().toISOString().split('T')[0];

            // Greeting
            const greet = document.getElementById('emp-dash-greeting');
            if (greet) greet.innerText = `Welcome, ${empName}`;
            const sub = document.getElementById('emp-dash-sub');
            if (sub) sub.innerText = `Your personal HR summary — ${today}`;

            // Today's attendance status
            const todayAtt = state.attendances.find(a => ((a.employeeId && a.employeeId === empId) || a.employee === empName) && a.date === today);
            const statusEl = document.getElementById('emp-dash-status');
            const timeEl = document.getElementById('emp-dash-checkin-time');
            if (statusEl) {
                if (state.isCheckedIn) {
                    statusEl.innerText = 'Checked In';
                    if (timeEl) timeEl.innerText = state.activeCheckInTime || '--:--';
                } else if (todayAtt && todayAtt.checkOut && todayAtt.checkOut !== '--') {
                    statusEl.innerText = 'Checked Out';
                    if (timeEl) timeEl.innerText = `In: ${todayAtt.checkIn} → Out: ${todayAtt.checkOut}`;
                } else {
                    statusEl.innerText = 'Not Checked In';
                    if (timeEl) timeEl.innerText = '--:--';
                }
            }

            // Leave balances
            const approvedLeaves = state.leaves.filter(l => ((l.employeeId && l.employeeId === empId) || l.employee === empName) && l.status === 'approved');
            const usedPaid = approvedLeaves.filter(l => l.type === 'paid').reduce((s, l) => s + (l.days || 0), 0);
            const usedSick = approvedLeaves.filter(l => l.type === 'sick').reduce((s, l) => s + (l.days || 0), 0);
            const paidEl = document.getElementById('emp-dash-paid-bal');
            const sickEl = document.getElementById('emp-dash-sick-bal');
            if (paidEl) paidEl.innerText = Math.max(0, 24 - usedPaid);
            if (sickEl) sickEl.innerText = Math.max(0, 7 - usedSick);

            // Pending count
            const myPending = state.leaves.filter(l => ((l.employeeId && l.employeeId === empId) || l.employee === empName) && l.status === 'pending').length;
            const pendEl = document.getElementById('emp-dash-pending');
            if (pendEl) pendEl.innerText = myPending;

            // Recent leave requests table
            const leaveTbl = document.getElementById('emp-dash-leave-tbl');
            if (leaveTbl) {
                const myLeaves = state.leaves.filter(l => (l.employeeId && l.employeeId === empId) || l.employee === empName).slice(-5).reverse();
                if (myLeaves.length === 0) {
                    leaveTbl.innerHTML = `<tr><td colspan="6" style="text-align:center;color:var(--text-muted);padding:1rem;">No leave requests yet.</td></tr>`;
                } else {
                    const badgeClass = { approved: 'badge-green', pending: 'badge-amber', rejected: 'badge-red' };
                    leaveTbl.innerHTML = myLeaves.map(l => `<tr>
                        <td><span class="badge badge-purple">${l.type.toUpperCase()}</span></td>
                        <td>${l.startDate}</td><td>${l.endDate}</td><td>${l.days}d</td>
                        <td style="color:var(--text-muted);font-size:0.82rem;">${l.remarks || '--'}</td>
                        <td><span class="badge ${badgeClass[l.status] || 'badge-amber'}">${l.status.toUpperCase()}</span></td>
                    </tr>`).join('');
                }
            }

            // Recent attendance table (last 5)
            const attTbl = document.getElementById('emp-dash-att-tbl');
            if (attTbl) {
                const myAtt = state.attendances.filter(a => (a.employeeId && a.employeeId === empId) || a.employee === empName).slice(-5).reverse();
                if (myAtt.length === 0) {
                    attTbl.innerHTML = `<tr><td colspan="5" style="text-align:center;color:var(--text-muted);padding:1rem;">No attendance records yet.</td></tr>`;
                } else {
                    const badgeClass = { present: 'badge-green', absent: 'badge-red', half_day: 'badge-amber' };
                    attTbl.innerHTML = myAtt.map(a => `<tr>
                        <td>${a.date}</td>
                        <td>${a.checkIn || '--'}</td>
                        <td>${a.checkOut || '--'}</td>
                        <td><span class="badge ${badgeClass[a.status] || 'badge-purple'}">${(a.status||'').toUpperCase()}</span></td>
                        <td>${a.workedHours || a.effectiveHours || '--'}</td>
                    </tr>`).join('');
                }
            }
        }

        function renderAll() {
            renderDashboard();
            renderAdminProfile();
            renderAttendance();
            renderLeaves();
            renderEmployees();
            renderDocuments();
            renderPayroll();
            renderEmployeeDashboard();
            renderNotifications();
        }

        window.addEventListener('DOMContentLoaded', () => {
            const session = getSession();
            if (session) {
                applySession(session);
            } else {
                // No session — show auth wall
            }
        });

    </script>
</body>
</html>
"""

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

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
