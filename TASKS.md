# Dayflow — Hackathon Task Tracker

## Pre-development & Baseline Setup

- [x] Verify Odoo development environment
- [x] Verify repository structure
- [x] Verify required dependencies (Native Odoo module architecture selected)
- [x] Create minimal Odoo module scaffold (`dayflow/`)
- [x] Establish baseline context & shared data model contract (`DATA_MODEL.md`)
- [x] Agree on architecture details (`ARCHITECTURE.md`)
- [x] Agree on finalized data models & field definitions
- [x] Implement core Odoo ORM models (`hr.employee`, `hr.attendance`, `hr.leave`, `dayflow.payroll`, `dayflow.document`)
- [x] Implement RBAC security groups & ACL rules (`dayflow_security.xml`, `ir.model.access.csv`)
- [x] Implement basic UI menus & views (`menu_views.xml`, `employee_views.xml`, `attendance_views.xml`, `leave_views.xml`, `payroll_views.xml`, `document_views.xml`)
- [x] Validate Python syntax, XML schemas, and CSV access rules

---

## Parallel Team Work Areas (Ready for Team Development)

### Person 1 — Authentication / RBAC
- [ ] Investigate Odoo's built-in user/group/role mechanisms (`res.users`, `res.groups`).
- [ ] Refine Employee vs. HR/Admin role access in Odoo security XML.
- [ ] Implement employee creation & login credentials workflow.

### Person 2 — Employee Domain
- [ ] Build out employee profile UI & views (personal info, job info, profile picture, documents).
- [ ] Extend `hr.employee` views with refined layouts and document upload UI.

### Person 3 — Attendance & Leave Domain
- [ ] Implement attendance check-in / check-out actions & daily/weekly logs.
- [ ] Implement leave application workflow (Paid/Sick/Unpaid; Pending/Approved/Rejected).
- [ ] Implement HR leave decisioning workflow (approval/rejection with admin comments).

### Person 4 — Admin & Payroll Domain
- [ ] Build out HR dashboard overview.
- [ ] Implement organization-wide attendance view.
- [ ] Implement payroll and salary structure management views.

### Integration / Data Model Owner
- [x] Maintain `DATA_MODEL.md` as single source of truth.
- [x] Coordinate entity relationships (`Employee` -> `Attendance`, `Leave`, `Payroll`, `Document`).
- [x] Deliver runnable initial Dayflow foundation for team parallel work.
