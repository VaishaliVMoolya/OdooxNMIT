# Dayflow — Shared Team Context

## Project Overview
* **Project Name:** Dayflow
* **Project Type:** Human Resource Management System (HRMS)
* **Hackathon:** Odoo × NMIT Hackathon
* **Duration:** 8 hours
* **Team Size:** 4 people (2 CS students, 2 VLSI students)
* **Current Status:** Pre-development / Shared Context & Verification Stage

---

## Problem Statement
Dayflow is a streamlined HRMS designed to manage employee profiles, attendance, leave management, and payroll with clear role-based access for Employees and Admin/HR staff.

---

## User Roles & Functional Requirements

### 1. Employee Role
* **Authentication:** Registration, Login, Role-based Access
* **Dashboard:** Employee personal dashboard
* **Profile:** View and edit permitted profile information, profile picture, and uploaded documents
* **Attendance:** Daily and weekly attendance view, Check-in / Check-out functionality, personal attendance history
* **Leave Management:** Apply for leave, view leave request status
* **Payroll:** View personal salary and payroll information

### 2. Admin / HR Role
* **Authentication:** Login, Role-based Access Control (RBAC)
* **Dashboard:** Admin/HR central dashboard
* **Employee Management:** View employee list and detailed employee information
* **Attendance Overview:** View attendance across all employees
* **Leave Decisioning:** View pending leave requests, approve/reject leave applications, add comments to decisions
* **Payroll Management:** View organization payroll, update employee salary structures

---

## Domain Enums & Statuses

### Attendance Statuses
* `Present`
* `Absent`
* `Half-day`
* `Leave`

### Leave Types
* `Paid`
* `Sick`
* `Unpaid`

### Leave Request Statuses
* `Pending`
* `Approved`
* `Rejected`

---

## Intended Demo Flow
```
Employee Login
  ➔ Employee Dashboard
  ➔ Check In
  ➔ Apply for Leave
  ➔ HR Login
  ➔ HR Dashboard
  ➔ Approve Leave
  ➔ Employee sees updated Leave Status
  ➔ Employee views Payroll
```

---

## Planned Team Responsibilities *(Provisional)*

| Team Member | Domain / Responsibilities | Status |
| :--- | :--- | :--- |
| **Person 1** | Authentication, Registration, Login, Role-Based Access Control (RBAC) | *Provisional* |
| **Person 2** | Employee Dashboard, Profile (Personal/Job Info), Profile Picture, Documents | *Provisional* |
| **Person 3** | Attendance (Check-in/out, Daily/Weekly), Leave Application & Approval Workflow | *Provisional* |
| **Person 4** | Admin/HR Dashboard, Employee List, Attendance Overview, Payroll/Salary Management | *Provisional* |
| **Integration Lead** | Git coordination, repository merging, baseline execution owner | *Provisional* |

*Note: Specific task divisions will be finalized once the hackathon tech stack and Odoo environment setup are verified.*

---

## Important Constraints & Guidelines
1. **Architecture = TBD:** Do NOT assume React + Node.js + SQL Server or any specific stack until the hackathon environment is inspected and verified.
2. **No Dependency Installation:** Do NOT install PostgreSQL, SQL Server, Node.js, React, Odoo, or major dependencies prior to architecture verification.
3. **No Code Modification Yet:** Establish environment baseline and shared context first.
4. **No Database Creation Yet:** Database schemas and ORM selections will follow approved architecture.
5. **No Scope Inflation:** Lower priority features (email notifications, advanced analytics, reports) are deferred to future enhancements.
