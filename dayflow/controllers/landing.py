# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class DayflowLandingController(http.Controller):
    """Public landing page only — no auth, sessions, or user management."""

    @http.route(
        '/',
        type='http',
        auth='public',
        website=False,
        sitemap=False,
        priority=20,
    )
    def landing(self, **kwargs):
        return request.render('dayflow.landing_page', {})
