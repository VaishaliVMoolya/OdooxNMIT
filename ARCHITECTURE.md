# Architecture Decision Document — Dayflow HRMS

---

## 1. Executive Summary

**Dayflow** is implemented as a **native custom Odoo addon module** (`dayflow`). It extends Odoo's standard Human Resources framework (`base`, `hr`, `hr_attendance`, `hr_holidays`) using the standard Odoo ORM, XML views, and security architecture.

---

## 2. Verified Technology Stack

* **Framework:** Native Odoo 16/17 Custom Module (`dayflow`)
* **Backend Language:** Python 3 (Tested with Python 3.11 / 3.14)
* **Data Access Layer:** Odoo ORM (Mapping to PostgreSQL tables)
* **Security & Auth:** Native Odoo Security Groups (`res.groups`) & Model Access Control List (`ir.model.access.csv`)
* **UI/Views:** Odoo XML Views (Form, Tree, Kanban) & Menu Item Actions (`ir.actions.act_window`)

---

## 3. Module Dependencies & Architecture

```
                       +-------------------+
                       |    Odoo Base      |
                       +---------+---------+
                                 |
         +-----------------------+-----------------------+
         |                       |                       |
+--------v-------+      +--------v-------+      +--------v-------+
|   hr.employee  |      | hr.attendance  |      |   hr.leave     |
|   (Profile)    |      | (Attendance)   |      |  (Time Off)    |
+--------+-------+      +--------+-------+      +--------+-------+
         |                       |                       |
         +-----------------------+-----------------------+
                                 | extended by
                        +--------v--------+
                        |  Dayflow Module |
                        |   ('dayflow')   |
                        +--------+--------+
                                 | defines custom models
               +-----------------+-----------------+
               |                                   |
    +----------v----------+             +----------v----------+
    |   dayflow.payroll   |             |   dayflow.document  |
    | (Salary Structures) |             | (File Attachments)  |
    +---------------------+             +---------------------+
```

* **Module Name:** `dayflow`
* **Dependencies:** `['base', 'hr', 'hr_attendance', 'hr_holidays']`
* **Installable:** `True`
* **Application:** `True`

---

## 4. RBAC Security Architecture

Access control uses native Odoo groups defined in `dayflow/security/dayflow_security.xml`:

1. **Employee Group (`group_dayflow_employee`):**
   - Implies `base.group_user`.
   - Access: Read-only access to payroll entries; read/write access to personal attendance records and leave applications.
2. **HR / Admin Manager Group (`group_dayflow_admin`):**
   - Implies `group_dayflow_employee`.
   - Access: Full CRUD permissions across employees, attendance logs, leave decisioning (approval/rejection), and organization payroll entries.

---

## 5. Verification & Testing Baseline

- **Python Syntax:** Verified using `python -m py_compile` across all model and manifest files.
- **XML Syntax & Structure:** Verified using `xml.etree.ElementTree` parsing across all view and security XML files.
- **Security ACLs:** 10 access rules verified in `ir.model.access.csv`.
