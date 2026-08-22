# Dayflow HRMS

**Odoo × NMIT 8-Hour Hackathon — Human Resource Management System**

Dayflow is a modern, modular Human Resource Management System (HRMS) built as a native custom Odoo addon module (`dayflow`). It provides an end-to-end organizational workspace covering Employee Directory & Document Compliance, Attendance & Break Tracking, Leave/Time Off Decision Hubs, and Payroll Management under strict Role-Based Access Control (RBAC).

---

## 🚀 How to Run the Application

You can run Dayflow in two ways:

### Option 1: Live Interactive Workspace & UI Console (Zero-Dependency)

A lightweight standalone Python preview server is included to instantly launch and demo the full unified Dayflow HRMS experience without requiring external database setup:

1. Open your terminal in the repository root:
   ```bash
   python preview_server.py
   # or
   python run_dashboard_preview.py
   ```

2. Open your web browser and navigate to:
   ```
   http://localhost:8000
   ```

---

### Option 2: Native Odoo Module Deployment

To install Dayflow into an active Odoo instance (Odoo 16/17):

1. Clone or symlink the `dayflow` directory into your Odoo `addons_path`:
   ```bash
   git clone https://github.com/VaishaliVMoolya/OdooxNMIT.git
   ```

2. Start the Odoo server with module installation/upgrade flag:
   ```bash
   odoo-bin -c odoo.conf -d <your_database> -i dayflow --dev=all
   ```

3. Open Odoo in your browser, log in as Administrator, navigate to **Apps**, remove the *Apps* search filter, search for `Dayflow`, and click **Install** / **Upgrade**.

4. Access the **Dayflow HRMS** app from the main application switcher.

---

## 📂 Repository Structure

```
OdooxNMIT/
├── dayflow/                                 # Core Native Odoo Addon Module
│   ├── __init__.py                          # Python package entry point
│   ├── __manifest__.py                      # Odoo module metadata & assets manifest
│   ├── controllers/
│   │   ├── __init__.py
│   │   └── landing.py                       # Public landing page routes & controllers
│   ├── data/
│   │   ├── dayflow_sequence.xml             # Employee code / Payroll reference sequences
│   │   ├── leave_data.xml                   # Master leave types (Paid, Sick, Unpaid)
│   │   └── mail_template_data.xml           # Automated email & notification templates
│   ├── models/                              # Domain business logic & ORM extensions
│   │   ├── __init__.py
│   │   ├── account_provision_wizard.py      # Account creation & password generator wizard
│   │   ├── attendance.py                    # hr.attendance extension (statuses, break & extra hours)
│   │   ├── auth.py                          # res.users login security hooks
│   │   ├── document.py                      # dayflow.document verification workflow
│   │   ├── employee.py                      # hr.employee extension (roles, profiles, links)
│   │   ├── leave.py                         # hr.leave extension (half-day, approval & attendance sync)
│   │   └── payroll.py                       # dayflow.payroll salary structure model
│   ├── security/                            # Security groups and Row-Level Access Rules
│   │   ├── dayflow_security.xml             # Security groups & employee isolation rules
│   │   └── ir.model.access.csv              # Model Access Control Lists (ACL)
│   ├── static/                              # Static UI assets (SCSS, JavaScript, XML templates)
│   │   └── src/
│   │       ├── js/                          # Frontend JS logic & OWL components
│   │       ├── scss/                        # Custom Dayflow stylesheets & auth styling
│   │       └── xml/                         # Frontend QWeb templates
│   └── views/                               # Odoo XML UI Views & Action Menus
│       ├── account_provision_wizard_views.xml
│       ├── attendance_views.xml
│       ├── auth_login_templates.xml
│       ├── dashboard_views.xml
│       ├── document_views.xml
│       ├── employee_views.xml
│       ├── landing_templates.xml
│       ├── leave_views.xml
│       ├── menu_views.xml
│       └── payroll_views.xml
├── ARCHITECTURE.md                          # Technical architecture specification
├── DATA_MODEL.md                            # Shared data model contract & field specifications
├── INTEGRATION_PERSON_4.md                  # API & ORM query contract for Admin/Payroll integration
├── preview_server.py                        # Standalone interactive UI server
├── run_dashboard_preview.py                 # Quick-launch alias runner
└── README.md                                # Project documentation
```

---

## ✨ Key Feature Domains

### 1. Authentication & Role-Based Access Control (RBAC)
* **Dual Roles:** `Employee` vs. `Admin / HR Manager`.
* **Account Provisioning Wizard:** Auto-generates employee credentials with automated email invitations.
* **Row-Level Security:** Record rules isolate employee records while providing organization-wide management to HR Admins.

### 2. Employee Profile & Document Compliance
* Employee directory with job positions, department filtering, and personal/banking details.
* Document management system supporting ID proofs, contracts, and certificates with verification workflows.

### 3. Attendance & Break Time Tracking
* **Real-time Stopwatch:** Tracks live work duration from check-in to check-out.
* **Break Tracking:** Calculates exact **Effective Working Hours** vs. **Total Elapsed Time**.
* **Categorization:** Automatic classification into `Present`, `Half-day`, `Absent`, and `Leave`.
* **Overtime Computation:** Extra hours automatically recorded for shifts exceeding 8.0 hours.

### 4. Time Off & Leave Management Hub
* **Multi-Type Balances:** Tracking of Paid Time Off, Sick Leave, and Unpaid Leaves.
* **Half-Day Leave Support:** Supports Full-Day and Half-Day (0.5d) leave sessions.
* **Automatic Attendance Synchronization:** Approving a leave automatically marks attendance as `Leave` or `Half-day`.
* **National Holiday Calendar:** Highlights gazetted public holidays and auto-excludes non-working days.

### 5. Payroll & Executive Attendance Ledger
* **Monthly Attendance & Leave Payroll Ledger:** Consolidated ledger calculating:
  $$\text{Payable Days} = \text{Present Days} + (0.5 \times \text{Half Days}) + \text{Approved Paid Leaves}$$
* **Salary Structure Engine:** Calculates Basic Wage, HRA, allowances, and statutory deductions with Net Pay computation.

### 6. Email & Notification Alert Engine
* Automated notifications for security login alerts, leave application queue updates, and account invitations.

---

## 👥 Hackathon Team Roles

* **Person 1:** Authentication & RBAC workflows (`auth.py`, `account_provision_wizard.py`, login templates)
* **Person 2:** Employee profile, directory & document management (`employee.py`, `document.py`, views)
* **Person 3:** Attendance tracking, break tracking & leave approval workflows (`attendance.py`, `leave.py`)
* **Person 4:** Admin dashboard, executive analytics & payroll management (`payroll.py`, dashboard views)

---

## 📜 License
Licensed under the [LGPL-3](https://www.gnu.org/licenses/lgpl-3.0.html) license.
