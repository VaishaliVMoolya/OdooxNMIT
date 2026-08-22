/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

class DayflowAccountProvisionSuccess extends Component {
    setup() {
        this.action = useService("action");
        this.notification = useService("notification");
    }

    async copyCredential(value, label) {
        try {
            await navigator.clipboard.writeText(value);
            this.notification.add(`${label} copied.`, { type: "success" });
        } catch {
            this.notification.add(`Unable to copy ${label.toLowerCase()}.`, { type: "danger" });
        }
    }

    close() {
        this.action.doAction({ type: "ir.actions.act_window_close" });
    }
}

DayflowAccountProvisionSuccess.template = "dayflow.AccountProvisionSuccess";
registry.category("actions").add("dayflow.account_provision_success", DayflowAccountProvisionSuccess);
