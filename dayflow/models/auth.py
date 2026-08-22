# -*- coding: utf-8 -*-
import logging
from datetime import datetime
from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    _inherit = 'res.users'

    def _update_last_login(self):
        """Standard Odoo hook triggered on successful authentication only."""
        super()._update_last_login()
        for user in self:
            user._send_dayflow_login_alert()

    def _send_dayflow_login_alert(self):
        """Send a security email notification when the user logs into their Dayflow account."""
        self.ensure_one()
        # Avoid sending for system internal users or empty logins
        if self._is_system_user() or not (self.email or '@' in (self.login or '')):
            return

        try:
            template = self.env.ref('dayflow.email_template_dayflow_login_alert', raise_if_not_found=False)
            if template:
                login_time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')
                template.with_context(
                    login_time=login_time_str,
                ).send_mail(self.id, force_send=False, raise_exception=False)
                _logger.info("Dayflow login security alert sent/queued for user: %s (%s)", self.name, self.email or self.login)
        except Exception as e:
            # Crucial: Must never block user authentication if mail delivery temporarily fails
            _logger.warning("Could not send Dayflow login alert for user %s: %s", self.login, e)

    def _is_system_user(self):
        """Check if the user is a system/public user."""
        try:
            root_user = self.env.ref('base.user_root', raise_if_not_found=False)
            if root_user and self.id == root_user.id:
                return True
        except Exception:
            pass
        return self._is_superuser() or self._is_public()
