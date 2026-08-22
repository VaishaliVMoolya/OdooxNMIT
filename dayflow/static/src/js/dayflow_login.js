/** @odoo-module **/

document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector(".o_dayflow_login_container .oe_login_form");
    if (!form) {
        return;
    }

    const password = form.querySelector("#password");
    const toggle = form.querySelector(".o_dayflow_password_toggle");
    if (password && toggle) {
        toggle.addEventListener("click", () => {
            const visible = password.type === "text";
            password.type = visible ? "password" : "text";
            toggle.setAttribute("aria-pressed", String(!visible));
            toggle.setAttribute("aria-label", visible ? "Show password" : "Hide password");
            const icon = toggle.querySelector("i");
            if (icon) {
                icon.classList.toggle("fa-eye", visible);
                icon.classList.toggle("fa-eye-slash", !visible);
            }
        });
    }

    form.addEventListener("submit", () => {
        const submit = form.querySelector(".o_dayflow_login_submit");
        if (!submit || submit.disabled) {
            return;
        }
        submit.disabled = true;
        submit.setAttribute("aria-busy", "true");
        submit.textContent = submit.dataset.loadingLabel || "Signing in…";
    });
});
