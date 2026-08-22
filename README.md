# Dayflow

**Odoo × NMIT Hackathon — Human Resource Management System (HRMS)**

Dayflow is a streamlined HRMS built as a native custom Odoo addon module (`dayflow`). It manages employee profiles, document uploads, check-in/check-out attendance tracking, leave requests and decision workflows, and payroll structure records under a clear role-based access control system (Employee vs. Admin/HR Manager).

---

## Repository Structure

```
OdooxNMIT/
├── dayflow/                     # Core Odoo Custom Addon Module
│   ├── __init__.py              # Module entry point
│   ├── __manifest__.py          # Odoo module manifest
│   ├── models/                  # Python ORM domain models
│   │   ├── __init__.py
│   │   ├── employee.py          # hr.employee extension
│   │   ├── attendance.py        # hr.attendance extension
│   │   ├── leave.py             # hr.leave extension
│   │   ├── payroll.py           # dayflow.payroll custom model
│   │   └── document.py          # dayflow.document custom model
│   ├── security/                # Access control & RBAC rules
│   │   ├── dayflow_security.xml # Security groups (Employee, HR Admin)
│   │   └── ir.model.access.csv  # Model Access Control List
│   └── views/                   # Odoo XML UI views & menus
│       ├── menu_views.xml       # Main Dayflow menu structure & actions
│       ├── employee_views.xml   # Employee views extension
│       ├── attendance_views.xml # Attendance views extension
│       ├── leave_views.xml      # Leave / Time Off views extension
│       ├── payroll_views.xml    # Payroll custom views
│       └── document_views.xml   # Document custom views
├── ARCHITECTURE.md              # Verified architecture specification
├── DATA_MODEL.md                # Shared data model contract & field spec
├── ENVIRONMENT_REPORT.md        # Environment verification & testing report
├── README.md                    # Project documentation
├── TASKS.md                     # Hackathon task tracker & work breakdown
└── TEAM_CONTEXT.md              # Shared team context & requirements
```

---

## Core Data Models & Reuse Strategy

Instead of duplicating standard entities, Dayflow extends native Odoo HR models:

1. **`hr.employee`** -> Extended with `dayflow_role` (`Employee` / `HR Admin`), document links (`document_ids`), and payroll links (`payroll_ids`).
2. **`hr.attendance`** -> Extended with `dayflow_status` (`Present`, `Absent`, `Half-day`, `Leave`) and extra hours tracking.
3. **`hr.leave`** -> Extended with `dayflow_leave_type` (`Paid`, `Sick`, `Unpaid`), `dayflow_status` (`Pending`, `Approved`, `Rejected`), employee remarks, and HR admin decision comments.
4. **`dayflow.payroll`** -> Custom model managing salary structures, base salary, allowances, deductions, and computed net salary.
5. **`dayflow.document`** -> Custom model managing employee file attachments (ID proof, contracts, certificates).

---

## Security & Access Control (RBAC)

Defined in `dayflow/security/dayflow_security.xml` and `dayflow/security/ir.model.access.csv`:

* **Dayflow Employee (`group_dayflow_employee`):** View personal profile, personal payroll; submit/view check-ins and leave requests.
* **Dayflow HR Admin (`group_dayflow_admin`):** Manage organization employees, view all attendance, approve/reject leave requests with comments, and manage salary/payroll records.

---

## Installation & Execution

1. Place or symlink the `dayflow` directory inside your Odoo `addons` path.
2. Update the app list in your Odoo database or install via CLI:
   ```bash
   odoo-bin -c odoo.conf -d <your_database> -i dayflow
   ```
3. Access the **Dayflow** application menu from the top left menu bar.

---

## Team Task Responsibilities

* **Person 1:** Authentication & RBAC workflows
* **Person 2:** Employee profile & document UI
* **Person 3:** Attendance & leave approval workflows
* **Person 4:** Admin dashboard & payroll views
* **Integration Owner:** Repository baseline & shared data contract (`DATA_MODEL.md`)
