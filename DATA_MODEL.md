# Dayflow — Shared Data Model Contract

This document serves as the single source of truth for Dayflow HRMS data entities, field definitions, and entity relationships within the Odoo ORM baseline.

---

## 1. Employee (`hr.employee` — Extended Standard Odoo Model)

* **Odoo Base Model:** `hr.employee` (Module: `hr`)
* **Extension:** Inherited in `dayflow/models/employee.py` (`_inherit = 'hr.employee'`)
* **Purpose:** Core profile representing an organization member, their role access, personal info, job details, and linked documents/payroll records.
* **Fields & Attributes:**
  * Standard Odoo fields reused: `name`, `work_email`, `image_1920`, `user_id`, `job_id`, `department_id`, `phone`.
  * `dayflow_role` (`Selection`: `employee` -> Employee, `hr` -> Admin / HR Manager)
  * `document_ids` (`One2many` -> `dayflow.document`)
  * `payroll_ids` (`One2many` -> `dayflow.payroll`)
  * `notes` (`Text`)
* **Relationships:**
  * Belongs to one `res.users` (`user_id`).
  * Has many `hr.attendance` (`attendance_ids`).
  * Has many `hr.leave`.
  * Has many `dayflow.payroll` (`payroll_ids`).
  * Has many `dayflow.document` (`document_ids`).

---

## 2. Attendance (`hr.attendance` — Extended Standard Odoo Model)

* **Odoo Base Model:** `hr.attendance` (Module: `hr_attendance`)
* **Extension:** Inherited in `dayflow/models/attendance.py` (`_inherit = 'hr.attendance'`)
* **Purpose:** Track daily check-in, check-out, work hours, and status per employee.
* **Fields & Attributes:**
  * Standard Odoo fields reused: `employee_id` (Many2one -> `hr.employee`), `check_in` (Datetime), `check_out` (Datetime), `worked_hours` (Float).
  * `dayflow_status` (`Selection`: `present` -> Present, `absent` -> Absent, `half_day` -> Half-day, `leave` -> Leave)
  * `extra_hours` (`Float`)
  * `remarks` (`Text`)

---

## 3. Leave Request / Time Off (`hr.leave` — Extended Standard Odoo Model)

* **Odoo Base Model:** `hr.leave` (Module: `hr_holidays`)
* **Extension:** Inherited in `dayflow/models/leave.py` (`_inherit = 'hr.leave'`)
* **Purpose:** Enable employees to apply for leave and allow HR/Admin to review, approve, reject, and comment on applications.
* **Fields & Attributes:**
  * Standard Odoo fields reused: `employee_id` (Many2one -> `hr.employee`), `holiday_status_id` (Many2one -> `hr.leave.type`), `request_date_from` (Date), `request_date_to` (Date), `number_of_days` (Float), `state` (Selection).
  * `dayflow_leave_type` (`Selection`: `paid` -> Paid, `sick` -> Sick, `unpaid` -> Unpaid)
  * `dayflow_status` (`Selection`: `pending` -> Pending, `approved` -> Approved, `rejected` -> Rejected)
  * `remarks` (`Text` — Employee reason/notes)
  * `admin_comments` (`Text` — HR/Admin decision comments)

---

## 4. Leave Type (`hr.leave.type` — Standard Odoo Model)

* **Odoo Base Model:** `hr.leave.type` (Module: `hr_holidays`)
* **Purpose:** Categorize permitted leave types (`Paid`, `Sick`, `Unpaid`). Reused standard Odoo model.

---

## 5. Payroll (`dayflow.payroll` — Custom Dayflow Model)

* **Custom Model:** `dayflow.payroll` (Defined in `dayflow/models/payroll.py`)
* **Purpose:** Manage salary structures and payroll entries per employee.
* **Fields & Attributes:**
  * `name` (`Char`, required, reference ID e.g. `PAY/2026/001`)
  * `employee_id` (`Many2one` -> `hr.employee`, required)
  * `salary_structure` (`Char`, default `'Standard Base'`)
  * `base_salary` (`Float`, required, default `0.0`)
  * `allowances` (`Float`, default `0.0`)
  * `deductions` (`Float`, default `0.0`)
  * `net_salary` (`Float`, computed from `base_salary + allowances - deductions`, stored)
  * `payroll_status` (`Selection`: `draft` -> Draft, `approved` -> Approved, `paid` -> Paid)
  * `pay_period` (`Char`, e.g. `'August 2026'`)
  * `notes` (`Text`)

---

## 6. Documents (`dayflow.document` — Custom Dayflow Model)

* **Custom Model:** `dayflow.document` (Defined in `dayflow/models/document.py`)
* **Purpose:** Store and attach employee verification documents.
* **Fields & Attributes:**
  * `name` (`Char`, required, document title)
  * `employee_id` (`Many2one` -> `hr.employee`, required)
  * `document_type` (`Selection`: `id_proof` -> ID Proof, `contract` -> Contract, `certificate` -> Certificate, `other` -> Other)
  * `document_file` (`Binary`, required file data)
  * `file_name` (`Char`, filename string)
  * `upload_date` (`Date`, default current date)
  * `notes` (`Text`)

---

## 7. Security Groups (`res.groups`)

* **Dayflow Employee (`group_dayflow_employee`):** Read-only access to own profile/payroll; read/write access to check-in/out and leave requests.
* **Dayflow HR Admin (`group_dayflow_admin`):** Full read/write/create/delete access across all Dayflow entities, leave decisioning, and payroll management.
