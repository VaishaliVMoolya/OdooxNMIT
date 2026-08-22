# Dayflow — Shared Data Model Contract

This document serves as the single source of truth for Dayflow HRMS data entities, field definitions, relationships, constraints, and security rules within the Odoo ORM baseline.

---

## Data Architecture Overview

```
Odoo User (res.users)
    │
    ▼
hr.employee (Standard Extended)
    ├── hr.attendance (Standard Extended)
    ├── hr.leave (Standard Extended)
    ├── dayflow.payroll (Custom Dayflow Model)
    └── dayflow.document (Custom Dayflow Model)
```

- **Architecture Principle:** Standard Odoo models are inherited (`_inherit`) wherever standard HR concepts exist. Custom models (`_name`) are created only for Dayflow-specific extensions.
- **RBAC Authority:** `res.users` and `res.groups` (`group_dayflow_employee`, `group_dayflow_admin`) are the authoritative source of truth for Role-Based Access Control (RBAC). Custom fields like `dayflow_role` are **informational metadata only** and DO NOT control access rights.
- **Row-Level Security:** Record Rules (`ir.rule`) enforce that Employee users (`group_dayflow_employee`) can only access data belonging to their own `hr.employee` record (`[('employee_id.user_id', '=', user.id)]`). HR/Admin managers (`group_dayflow_admin`) possess organization-wide access (`[(1, '=', 1)]`).

---

## 1. Employee (`hr.employee`)

* **Odoo Base Model:** `hr.employee` (Module: `hr`)
* **Extension Type:** Inherited (`_inherit = 'hr.employee'`)
* **Purpose:** Core organizational member profile containing personal details, job metadata, document attachments, and payroll history.
* **Fields & Attributes:**
  * **Standard Odoo Fields Reused:** `name` (Char), `work_email` (Char), `phone` (Char), `job_id` (Many2one -> `hr.job`), `department_id` (Many2one -> `hr.department`), `user_id` (Many2one -> `res.users`), `image_1920` (Binary profile image).
  * `dayflow_role` (`Selection`: `employee` -> Employee, `hr` -> Admin / HR): **Informational metadata only.** Does not grant or restrict permissions.
  * `document_ids` (`One2many` -> `dayflow.document`, `employee_id`): Attached employee verification files.
  * `payroll_ids` (`One2many` -> `dayflow.payroll`, `employee_id`): Historical and current payroll records.
  * `notes` (`Text`): General employee notes.
* **Relationships & Inverse Fields:**
  * Belongs to one `res.users` (`user_id`).
  * Has many `hr.attendance` (`attendance_ids`).
  * Has many `hr.leave`.
  * Has many `dayflow.payroll` (`payroll_ids`).
  * Has many `dayflow.document` (`document_ids`).
* **Security Considerations:**
  * Record Rule `rule_hr_employee_dayflow_employee`: `[('user_id', '=', user.id)]` restricts employees to viewing their own employee record.
  * Record Rule `rule_hr_employee_dayflow_admin`: `[(1, '=', 1)]` allows HR/Admin full CRUD.

---

## 2. Attendance (`hr.attendance`)

* **Odoo Base Model:** `hr.attendance` (Module: `hr_attendance`)
* **Extension Type:** Inherited (`_inherit = 'hr.attendance'`)
* **Purpose:** Daily check-in/check-out timestamp logging, worked hours calculation, and Dayflow status tracking.
* **Fields & Attributes:**
  * **Standard Odoo Fields Reused:** `employee_id` (Many2one -> `hr.employee`), `check_in` (Datetime), `check_out` (Datetime), `worked_hours` (Float).
  * `dayflow_status` (`Selection`: `present` -> Present, `absent` -> Absent, `half_day` -> Half-day, `leave` -> Leave): Attendance status tracking.
  * `extra_hours` (`Float`, default `0.0`): Overtime or additional worked hours.
  * `remarks` (`Text`): Daily attendance notes.
* **Data Integrity Constraints:**
  * `@api.constrains('check_in', 'check_out')`: `check_out` timestamp cannot be earlier than `check_in` timestamp (`_check_validity_check_out`).
* **Relationships:**
  * Many2one -> `hr.employee` (`employee_id`, required, `ondelete='cascade'`).
* **Security Considerations:**
  * Record Rule `rule_hr_attendance_employee`: `[('employee_id.user_id', '=', user.id)]` ensures employees read/create/write only their own attendance records.
  * Record Rule `rule_hr_attendance_admin`: `[(1, '=', 1)]` grants HR/Admin full CRUD.

---

## 3. Leave Request (`hr.leave`)

* **Odoo Base Model:** `hr.leave` (Module: `hr_holidays`)
* **Extension Type:** Inherited (`_inherit = 'hr.leave'`)
* **Purpose:** Manage employee leave applications and approval workflows.
* **Source-of-Truth Fields:**
  * `holiday_status_id` (Many2one -> `hr.leave.type`): **Primary ORM Source of Truth for Leave Category** (Paid, Sick, Unpaid types configured in standard Odoo).
  * `state` (Selection): **Primary ORM Source of Truth for Leave State** (`confirm` -> Pending, `validate` -> Approved, `refuse` -> Rejected).
* **Dayflow Helper Fields (for Hackathon UI compatibility):**
  * `dayflow_leave_type` (`Selection`: `paid` -> Paid, `sick` -> Sick, `unpaid` -> Unpaid).
  * `dayflow_status` (`Selection`: `pending` -> Pending, `approved` -> Approved, `rejected` -> Rejected).
  * `remarks` (`Text`): Application remarks from employee.
  * `admin_comments` (`Text`): HR/Admin decision comments.
* **Data Integrity Constraints:**
  * `@api.constrains('request_date_from', 'request_date_to', 'date_from', 'date_to')`: Leave end date cannot be earlier than leave start date (`_check_leave_dates_validity`).
* **Relationships:**
  * Many2one -> `hr.employee` (`employee_id`, required, `ondelete='cascade'`).
* **Security Considerations:**
  * Record Rule `rule_hr_leave_employee`: `[('employee_id.user_id', '=', user.id)]` restricts employees to their own leave requests.
  * Record Rule `rule_hr_leave_admin`: `[(1, '=', 1)]` grants HR/Admin full access for decisioning.

---

## 4. Payroll (`dayflow.payroll`)

* **Custom Model:** `dayflow.payroll` (Defined in `dayflow/models/payroll.py`)
* **Extension Type:** Custom New Model (`_name = 'dayflow.payroll'`)
* **Purpose:** Salary structure definitions, base salary, allowances, deductions, and net salary entries per pay period.
* **Fields & Attributes:**
  * `name` (`Char`, required, default `'New'`, reference ID e.g. `PAY/2026/001`).
  * `employee_id` (`Many2one` -> `hr.employee`, required, `ondelete='cascade'`).
  * `salary_structure` (`Char`, default `'Standard Base'`).
  * `base_salary` (`Float`, required, default `0.0`).
  * `allowances` (`Float`, default `0.0`).
  * `deductions` (`Float`, default `0.0`).
  * `net_salary` (`Float`, compute='_compute_net_salary', store=True, readonly=True): Formula `net_salary = base_salary + allowances - deductions`.
  * `payroll_status` (`Selection`: `draft` -> Draft, `approved` -> Approved, `paid` -> Paid).
  * `pay_period` (`Char`, e.g. `'August 2026'`).
  * `notes` (`Text`).
* **Data Integrity Constraints:**
  * `@api.constrains('base_salary', 'allowances', 'deductions')`: `base_salary`, `allowances`, and `deductions` cannot be negative (`_check_non_negative_amounts`).
  * `net_salary` is `readonly=True` to prevent manual overrides.
* **Relationships:**
  * Inverse field on `hr.employee`: `payroll_ids` (`One2many` -> `dayflow.payroll`).
* **Security Considerations:**
  * Record Rule `rule_dayflow_payroll_employee`: `[('employee_id.user_id', '=', user.id)]` grants employees Read-Only access to their own payroll entries (`perm_read=True`, `perm_write=False`, `perm_create=False`).
  * Record Rule `rule_dayflow_payroll_admin`: `[(1, '=', 1)]` grants HR/Admin full CRUD.

---

## 5. Documents (`dayflow.document`)

* **Custom Model:** `dayflow.document` (Defined in `dayflow/models/document.py`)
* **Extension Type:** Custom New Model (`_name = 'dayflow.document'`)
* **Purpose:** File attachment and document classification for employee verification files (contracts, ID proofs, certificates).
* **Fields & Attributes:**
  * `name` (`Char`, required, document title).
  * `employee_id` (`Many2one` -> `hr.employee`, required, `ondelete='cascade'`).
  * `document_type` (`Selection`: `id_proof` -> ID Proof, `contract` -> Contract, `certificate` -> Certificate, `other` -> Other).
  * `document_file` (`Binary`, required file payload).
  * `file_name` (`Char`, filename string).
  * `upload_date` (`Date`, default current date).
  * `notes` (`Text`).
* **Data Integrity Constraints:**
  * `employee_id`, `document_file`, and `name` are mandatory (`required=True`).
* **Relationships:**
  * Inverse field on `hr.employee`: `document_ids` (`One2many` -> `dayflow.document`).
* **Security Considerations:**
  * Record Rule `rule_dayflow_document_employee`: `[('employee_id.user_id', '=', user.id)]` permits employees to manage their own document attachments.
  * Record Rule `rule_dayflow_document_admin`: `[(1, '=', 1)]` grants HR/Admin full access.

---

## 6. Security Foundation Summary

| Model | Group | Read | Write | Create | Unlink | Record Rule Domain |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| `hr.employee` | `group_dayflow_employee` | Yes | No | No | No | `[('user_id', '=', user.id)]` |
| `hr.employee` | `group_dayflow_admin` | Yes | Yes | Yes | Yes | `[(1, '=', 1)]` |
| `hr.attendance` | `group_dayflow_employee` | Yes | Yes | Yes | No | `[('employee_id.user_id', '=', user.id)]` |
| `hr.attendance` | `group_dayflow_admin` | Yes | Yes | Yes | Yes | `[(1, '=', 1)]` |
| `hr.leave` | `group_dayflow_employee` | Yes | Yes | Yes | No | `[('employee_id.user_id', '=', user.id)]` |
| `hr.leave` | `group_dayflow_admin` | Yes | Yes | Yes | Yes | `[(1, '=', 1)]` |
| `dayflow.payroll` | `group_dayflow_employee` | Yes | No | No | No | `[('employee_id.user_id', '=', user.id)]` |
| `dayflow.payroll` | `group_dayflow_admin` | Yes | Yes | Yes | Yes | `[(1, '=', 1)]` |
| `dayflow.document` | `group_dayflow_employee` | Yes | Yes | Yes | No | `[('employee_id.user_id', '=', user.id)]` |
| `dayflow.document` | `group_dayflow_admin` | Yes | Yes | Yes | Yes | `[(1, '=', 1)]` |
