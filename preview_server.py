# -*- coding: utf-8 -*-
"""
Dayflow HRMS — Live UI Preview Server with Sign In / Sign Up Authentication
Odoo x NMIT Hackathon
All-in-One Management Console with Person 1 Auth System (Sign In, Sign Up, Auto Login ID Generator)
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import webbrowser

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dayflow HRMS — Workspace & Authentication</title>
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

        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', system-ui, sans-serif; }
        body { background-color: var(--bg-body); color: var(--text-main); min-height: 100vh; display: flex; flex-direction: column; }

        /* Top Navbar */
        .navbar {
            background-color: var(--bg-surface);
            border-bottom: 1px solid var(--border-line);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0.65rem 1.75rem;
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
            border-radius: 8px; width: 170px;
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

        /* Stats Grid */
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 1.25rem; }
        .stat-box { background-color: var(--bg-card); border: 1px solid var(--border-line); padding: 1rem 1.25rem; border-radius: 8px; }
        .stat-box .num { font-size: 1.5rem; font-weight: 700; margin-top: 0.25rem; }

        /* Employee Cards Grid */
        .emp-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1rem; }
        .emp-card { background-color: var(--bg-card); border: 1px solid var(--border-line); border-radius: 8px; padding: 1.1rem; display: flex; flex-direction: column; gap: 0.6rem; position: relative; }

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

        /* Modal */
        .modal { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background-color: rgba(0, 0, 0, 0.8); display: flex; align-items: center; justify-content: center; z-index: 100; }
        .modal-card { background-color: var(--bg-surface); border: 1px solid var(--border-line); border-radius: 10px; max-width: 650px; width: 90%; padding: 1.5rem; max-height: 88vh; overflow-y: auto; }

        .tab-panel { display: none; }
        .tab-panel.active { display: block; }
    </style>
</head>
<body>

    <!-- Top Navbar with Auth & Systray -->
    <nav class="navbar">
        <a href="#" class="brand">
            <span class="brand-badge">DF</span> Dayflow HRMS
        </a>
        <ul class="nav-links">
            <li class="nav-tab active" id="tab-btn-dashboard" onclick="openTab('dashboard')">Dashboard</li>
            <li class="nav-tab" id="tab-btn-documents" onclick="openTab('documents')">Documents</li>
            <li class="nav-tab" id="tab-btn-attendance" onclick="openTab('attendance')">Attendance</li>
            <li class="nav-tab" id="tab-btn-leave" onclick="openTab('leave')">Time Off</li>
            <li class="nav-tab" id="tab-btn-employees" onclick="openTab('employees')">Employees</li>
            <li class="nav-tab" id="tab-btn-payroll" onclick="openTab('payroll')">Payroll</li>
        </ul>
        <div class="systray">
            <button class="btn btn-primary" style="padding:0.35rem 0.85rem; font-size:0.8rem;" onclick="openAuthModal('signin')">🔑 Sign In / Sign Up</button>

            <!-- Active User Display -->
            <div style="font-size:0.8rem; color:var(--text-muted);">
                Logged in as: <strong id="lbl-current-user" style="color:#fff;">John Doe (Employee)</strong>
            </div>

            <!-- Avatar Dropdown with Sign In / Sign Up Trigger -->
            <div class="avatar-menu" onclick="toggleAvatarDropdown()">
                <div class="avatar-circle" id="user-avatar-initials">JD</div>
                <div class="dropdown-box" id="avatar-dropdown">
                    <div class="dropdown-item" onclick="openAuthModal('signin')">🔑 Sign In</div>
                    <div class="dropdown-item" onclick="openAuthModal('signup')">📝 Sign Up</div>
                    <div class="dropdown-item" style="color: var(--accent-amber);" onclick="switchRole('admin')">👑 Switch to Admin</div>
                    <div class="dropdown-item" style="color: var(--accent-blue);" onclick="switchRole('employee')">👤 Switch to Employee</div>
                </div>
            </div>
        </div>
    </nav>

    <div class="container">

        <!-- DASHBOARD TAB -->
        <div id="panel-dashboard" class="tab-panel active">
            <div class="header-row">
                <div>
                    <h1 class="header-title">Dayflow Management Console</h1>
                    <p style="color:var(--text-muted); font-size:0.85rem; margin-top:0.25rem;">Live organizational metrics, pending approvals, and executive summary</p>
                </div>
                <button class="btn btn-primary" onclick="openAuthModal('signin')">🔒 Account Sign In</button>
            </div>

            <div class="stats-grid">
                <div class="stat-box"><div class="metric-label">Total Employees</div><div class="num" style="color: #60a5fa;">3</div></div>
                <div class="stat-box"><div class="metric-label">Present Today</div><div class="num" style="color: #34d399;">2</div></div>
                <div class="stat-box"><div class="metric-label">On Leave</div><div class="num" style="color: #fbbf24;">1</div></div>
                <div class="stat-box"><div class="metric-label">Verified Documents</div><div class="num" style="color: var(--accent-purple-hover);">2</div></div>
            </div>
        </div>

        <!-- DOCUMENTS TAB -->
        <div id="panel-documents" class="tab-panel">
            <div class="header-row">
                <h1 class="header-title">Employee Verification Documents</h1>
            </div>
            <div class="card">
                <h3 style="font-size: 1.05rem; margin-bottom: 1rem;">Upload Document</h3>
                <form onsubmit="handleDocUpload(event)">
                    <div class="form-row">
                        <div class="field"><label>Document Title</label><input type="text" id="doc-title" class="input" placeholder="Passport Copy" required></div>
                        <div class="field">
                            <label>Employee</label>
                            <select id="doc-employee" class="input" required>
                                <option value="John Doe">John Doe</option>
                                <option value="Jane Smith">Jane Smith</option>
                            </select>
                        </div>
                        <div class="field">
                            <label>Category</label>
                            <select id="doc-type" class="input" required>
                                <option value="id_proof">ID Proof</option>
                                <option value="contract">Contract</option>
                                <option value="certificate">Certificate</option>
                            </select>
                        </div>
                        <div class="field"><label>Select File</label><input type="file" id="real-file-input" class="input" required></div>
                    </div>
                    <button type="submit" class="btn btn-primary">Upload Document</button>
                </form>
            </div>
        </div>

        <!-- ATTENDANCE TAB -->
        <div id="panel-attendance" class="tab-panel">
            <div class="header-row"><h1 class="header-title">Attendance Tracking</h1></div>
            <div class="card"><p style="color:var(--text-muted);">Attendance logs and check-in / out controls.</p></div>
        </div>

        <!-- LEAVE TAB -->
        <div id="panel-leave" class="tab-panel">
            <div class="header-row"><h1 class="header-title">Time Off Management</h1></div>
            <div class="card"><p style="color:var(--text-muted);">Time off applications and leave balances.</p></div>
        </div>

        <!-- EMPLOYEES TAB -->
        <div id="panel-employees" class="tab-panel">
            <div class="header-row"><h1 class="header-title">Employee Directory</h1></div>
            <div class="card"><p style="color:var(--text-muted);">Employee directory profiles.</p></div>
        </div>

        <!-- PAYROLL TAB -->
        <div id="panel-payroll" class="tab-panel">
            <div class="header-row"><h1 class="header-title">Payroll Management</h1></div>
            <div class="card"><p style="color:var(--text-muted);">Base salary, allowances, deductions, net salary.</p></div>
        </div>

    </div>

    <!-- PERSON 1: SIGN IN / SIGN UP AUTH MODAL -->
    <div id="modal-auth" class="modal" style="display: none;">
        <div class="modal-card" style="max-width: 480px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem;">
                <h3 id="auth-title" style="font-size:1.15rem;">Sign In to Dayflow</h3>
                <button class="btn btn-secondary" onclick="closeAuthModal()">✕</button>
            </div>

            <!-- Sign In Form (Wireframe 1) -->
            <form id="form-signin" onsubmit="handleSignIn(event)">
                <div class="field" style="margin-bottom:0.85rem;">
                    <label>Login ID / Email</label>
                    <input type="text" id="signin-login" class="input" placeholder="e.g. OIJODO20240001 or john@company.com" required>
                </div>
                <div class="field" style="margin-bottom:1.25rem;">
                    <label>Password</label>
                    <input type="password" id="signin-pass" class="input" placeholder="••••••••" required>
                </div>
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

    <script>
        function openTab(tabId) {
            document.querySelectorAll('.nav-tab').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.tab-panel').forEach(el => el.classList.remove('active'));

            document.getElementById('tab-btn-' + tabId)?.classList.add('active');
            document.getElementById('panel-' + tabId)?.classList.add('active');
        }

        function toggleAvatarDropdown() {
            const box = document.getElementById('avatar-dropdown');
            box.style.display = box.style.display === 'flex' ? 'none' : 'flex';
        }

        function openAuthModal(mode) {
            const box = document.getElementById('avatar-dropdown');
            if (box) box.style.display = 'none';
            document.getElementById('modal-auth').style.display = 'flex';
            switchAuthMode(mode);
        }

        function closeAuthModal() {
            document.getElementById('modal-auth').style.display = 'none';
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

        function switchRole(role) {
            const lbl = document.getElementById('lbl-current-user');
            if (role === 'admin') {
                lbl.innerText = 'Jane Smith (HR / Admin Manager)';
            } else {
                lbl.innerText = 'John Doe (Employee)';
            }
            toggleAvatarDropdown();
        }

        function handleSignIn(e) {
            e.preventDefault();
            const login = document.getElementById('signin-login').value;
            alert(`Signed In Successfully!\n\nWelcome back, ${login}`);
            closeAuthModal();
        }

        function handleSignUp(e) {
            e.preventDefault();
            const name = document.getElementById('signup-name').value;
            const parts = name.trim().split(' ');
            const code = parts.length >= 2 ? (parts[0].substring(0, 2) + parts[parts.length-1].substring(0, 2)).toUpperCase() : 'JODO';
            const generatedId = `OI${code}20260005`;

            alert(`Account Provisioned Successfully!\n\nGenerated System Login ID: ${generatedId}\nWelcome to Dayflow, ${name}!`);
            closeAuthModal();
        }
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
    print(" Dayflow HRMS - Workspace & Auth Preview Server")
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
