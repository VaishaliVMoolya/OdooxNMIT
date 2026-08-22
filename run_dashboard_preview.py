# -*- coding: utf-8 -*-
"""
Dayflow HRMS — Official Live UI Server Alias
Redirects to the clean, unified Dayflow workspace server (preview_server.py).
"""
import sys
from preview_server import run_server

if __name__ == '__main__':
    run_server(8000)
