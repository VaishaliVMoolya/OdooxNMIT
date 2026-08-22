/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, onWillStart, useState } from "@odoo/owl";

export class DayflowDashboard extends Component {
    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.notification = useService("notification");

        this.state = useState({
            loading: true,
            kpi: {
                total_employees: 0,
                present_today: 0,
                on_leave_today: 0,
                pending_leave_requests: 0,
                total_payroll: "0.00",
            },
            pending_leaves: [],
            attendance: [],
            employees: [],
            payroll: [],
            employeeSearch: "",
            attendanceFilter: "all",
            activeTab: "overview",
            actionLoading: false,
        });

        onWillStart(async () => {
            await this.loadDashboardData();
        });
    }

    async loadDashboardData() {
        this.state.loading = true;
        try {
            const data = await this.orm.call("dayflow.dashboard", "get_dashboard_data", []);
            if (data) {
                this.state.kpi = data.kpi || this.state.kpi;
                this.state.pending_leaves = data.pending_leaves || [];
                this.state.attendance = data.attendance || [];
                this.state.employees = data.employees || [];
                this.state.payroll = data.payroll || [];
            }
        } catch (error) {
            console.error("Dayflow Dashboard fetch error:", error);
            if (this.notification) {
                this.notification.add("Failed to load Dayflow dashboard data.", {
                    type: "danger",
                });
            }
        } finally {
            this.state.loading = false;
        }
    }

    async refreshDashboard() {
        await this.loadDashboardData();
        if (this.notification) {
            this.notification.add("Dashboard metrics refreshed.", {
                type: "info",
            });
        }
    }

    setActiveTab(tabName) {
        this.state.activeTab = tabName;
    }

    setAttendanceFilter(filter) {
        this.state.attendanceFilter = filter;
    }

    onEmployeeSearchInput(ev) {
        this.state.employeeSearch = ev.target.value.toLowerCase();
    }

    get filteredEmployees() {
        if (!this.state.employeeSearch) {
            return this.state.employees;
        }
        const query = this.state.employeeSearch;
        return this.state.employees.filter((emp) => {
            return (
                (emp.name && emp.name.toLowerCase().includes(query)) ||
                (emp.department && emp.department.toLowerCase().includes(query)) ||
                (emp.designation && emp.designation.toLowerCase().includes(query)) ||
                (emp.barcode && emp.barcode.toLowerCase().includes(query)) ||
                (emp.work_email && emp.work_email.toLowerCase().includes(query))
            );
        });
    }

    get filteredAttendance() {
        if (this.state.attendanceFilter === "all") {
            return this.state.attendance;
        }
        return this.state.attendance.filter(
            (att) => att.dayflow_status === this.state.attendanceFilter
        );
    }

    // Navigation and Action Handlers
    openEmployees() {
        this.action.doAction("dayflow.action_dayflow_employee");
    }

    openEmployeeForm(empId) {
        this.action.doAction({
            type: "ir.actions.act_window",
            res_model: "hr.employee",
            res_id: empId,
            views: [[false, "form"]],
            target: "current",
        });
    }

    createEmployee() {
        this.action.doAction({
            type: "ir.actions.act_window",
            res_model: "hr.employee",
            views: [[false, "form"]],
            target: "current",
        });
    }

    openAttendance() {
        this.action.doAction("dayflow.action_dayflow_attendance");
    }

    openTodayAttendance() {
        this.action.doAction("dayflow.action_dayflow_attendance_today");
    }

    createAttendance() {
        this.action.doAction({
            type: "ir.actions.act_window",
            res_model: "hr.attendance",
            views: [[false, "form"]],
            target: "current",
        });
    }

    openLeaveRequests() {
        this.action.doAction("dayflow.action_dayflow_leave");
    }

    openPendingLeaves() {
        this.action.doAction("dayflow.action_dayflow_leave_pending");
    }

    openLeaveForm(leaveId) {
        this.action.doAction({
            type: "ir.actions.act_window",
            res_model: "hr.leave",
            res_id: leaveId,
            views: [[false, "form"]],
            target: "current",
        });
    }

    async approveLeave(leaveId, ev) {
        if (ev) ev.stopPropagation();
        this.state.actionLoading = true;
        try {
            const res = await this.orm.call(
                "dayflow.dashboard",
                "action_quick_approve_leave",
                [leaveId]
            );
            if (this.notification) {
                this.notification.add(res.message || "Leave approved.", {
                    type: res.success ? "success" : "warning",
                });
            }
            await this.loadDashboardData();
        } catch (error) {
            console.error("Error approving leave:", error);
            if (this.notification) {
                this.notification.add("Could not approve leave request.", {
                    type: "danger",
                });
            }
        } finally {
            this.state.actionLoading = false;
        }
    }

    async rejectLeave(leaveId, ev) {
        if (ev) ev.stopPropagation();
        this.state.actionLoading = true;
        try {
            const res = await this.orm.call(
                "dayflow.dashboard",
                "action_quick_reject_leave",
                [leaveId]
            );
            if (this.notification) {
                this.notification.add(res.message || "Leave rejected.", {
                    type: "info",
                });
            }
            await this.loadDashboardData();
        } catch (error) {
            console.error("Error rejecting leave:", error);
            if (this.notification) {
                this.notification.add("Could not reject leave request.", {
                    type: "danger",
                });
            }
        } finally {
            this.state.actionLoading = false;
        }
    }

    openPayroll() {
        this.action.doAction("dayflow.action_dayflow_payroll");
    }

    openPayrollForm(payrollId) {
        this.action.doAction({
            type: "ir.actions.act_window",
            res_model: "dayflow.payroll",
            res_id: payrollId,
            views: [[false, "form"]],
            target: "current",
        });
    }

    createPayroll() {
        this.action.doAction({
            type: "ir.actions.act_window",
            res_model: "dayflow.payroll",
            views: [[false, "form"]],
            target: "current",
        });
    }

    openDocuments() {
        this.action.doAction("dayflow.action_dayflow_document");
    }
}

DayflowDashboard.template = "dayflow.DayflowDashboard";

registry.category("actions").add("dayflow.dashboard", DayflowDashboard);
