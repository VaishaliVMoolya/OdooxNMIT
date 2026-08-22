# Dayflow HRMS — Person 4 Integration Contract (Admin Dashboard & Payroll)

This document provides the exact model fields, methods, and queries for **Person 4 (Admin Dashboard & Payroll)** to integrate with **Person 3's Attendance & Leave** module.

---

## 1. Payroll Integration (Attendance & Payable Days)

The problem statement and wireframe require:
> *"Attendance data serves as the basis for payroll generation. Total present days and unpaid leaves/missing attendance should automatically adjust payable days during payroll computation."*

### Querying Payable Days for an Employee in a Pay Period
```python
# Example calculation in dayflow.payroll or compute method:
def _compute_payable_days(self, employee_id, date_start, date_end):
    attendances = self.env['hr.attendance'].search([
        ('employee_id', '=', employee_id.id),
        ('check_in', '>=', date_start),
        ('check_in', '<=', date_end),
    ])
    
    total_present_days = 0.0
    total_overtime_hours = 0.0
    
    for att in attendances:
        if att.dayflow_status == 'present':
            total_present_days += 1.0
        elif att.dayflow_status == 'half_day':
            total_present_days += 0.5
        elif att.dayflow_status == 'leave':
            # Check leave type: Paid leave is payable, Unpaid leave is not
            leave = self.env['hr.leave'].search([
                ('employee_id', '=', employee_id.id),
                ('request_date_from', '<=', att.check_in.date()),
                ('request_date_to', '>=', att.check_in.date()),
                ('dayflow_status', '=', 'approved'),
            ], limit=1)
            
            if leave and leave.dayflow_leave_type != 'unpaid':
                total_present_days += 1.0  # Paid / Sick leave counts as paid
            else:
                total_present_days += 0.0  # Unpaid leave
                
        total_overtime_hours += (att.extra_hours or 0.0)
        
    return {
        'payable_days': total_present_days,
        'overtime_hours': total_overtime_hours,
    }
```

---

## 2. Admin Dashboard Integration (Time Off Decisions)

### Fetching Pending Leave Applications
```python
pending_leaves = self.env['hr.leave'].search([
    ('dayflow_status', '=', 'pending')
])
```

### Approving a Leave Request (with Attendance Auto-Sync)
```python
# Call the Dayflow approve method on hr.leave record:
leave_record.write({'admin_comments': 'Approved by HR Manager'})
leave_record.action_dayflow_approve()
# Note: action_dayflow_approve automatically creates/updates hr.attendance records with status='leave'
```

### Rejecting a Leave Request
```python
leave_record.write({'admin_comments': 'Rejection reason / comments'})
leave_record.action_dayflow_reject()
```

---

## 3. Organization Attendance Statistics (Admin Overview)

```python
today_start = fields.Datetime.now().replace(hour=0, minute=0, second=0)
today_end = fields.Datetime.now().replace(hour=23, minute=59, second=59)

today_attendances = self.env['hr.attendance'].search([
    ('check_in', '>=', today_start),
    ('check_in', '<=', today_end),
])

stats = {
    'total_present': len(today_attendances.filtered(lambda a: a.dayflow_status == 'present')),
    'total_half_day': len(today_attendances.filtered(lambda a: a.dayflow_status == 'half_day')),
    'total_on_leave': len(today_attendances.filtered(lambda a: a.dayflow_status == 'leave')),
}
```

---

## 4. UI Actions Available for Admin Dashboard

| Action XML ID | Name | Target Model | Domain / Purpose |
|---|---|---|---|
| `dayflow.action_dayflow_attendance_all` | All Attendances | `hr.attendance` | Full org attendance table |
| `dayflow.action_dayflow_leave_to_approve` | Time Off to Approve | `hr.leave` | `[('dayflow_status', '=', 'pending')]` |
| `dayflow.action_dayflow_leave_all` | All Requests | `hr.leave` | Complete time-off history |
