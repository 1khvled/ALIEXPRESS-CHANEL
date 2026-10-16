import re
import subprocess
import tempfile
import os
import pytest
from api.user_site import USER_WEBSITE_HTML
from api.admin_dashboard import DASHBOARD_HTML

def test_user_site_html_scripts_valid_javascript():
    """Ensure all inline scripts in USER_WEBSITE_HTML have 100% valid JavaScript syntax."""
    script_matches = re.findall(r'<script(?![^>]*src)(?![^>]*ld\+json)[^>]*>(.*?)</script>', USER_WEBSITE_HTML, re.DOTALL)
    assert len(script_matches) >= 2, "Expected at least 2 inline script blocks in USER_WEBSITE_HTML"

    for idx, s in enumerate(script_matches):
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
            f.write(s)
            tmp_path = f.name
        try:
            res = subprocess.run(["node", "-c", tmp_path], capture_output=True, text=True)
            assert res.returncode == 0, f"Script block {idx} in USER_WEBSITE_HTML has JS syntax error:\n{res.stderr}"
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

def test_admin_dashboard_scripts_valid_javascript():
    """Ensure all inline scripts in DASHBOARD_HTML have 100% valid JavaScript syntax."""
    script_matches = re.findall(r'<script(?![^>]*src)(?![^>]*ld\+json)[^>]*>(.*?)</script>', DASHBOARD_HTML, re.DOTALL)
    for idx, s in enumerate(script_matches):
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
            f.write(s)
            tmp_path = f.name
        try:
            res = subprocess.run(["node", "-c", tmp_path], capture_output=True, text=True)
            assert res.returncode == 0, f"Script block {idx} in DASHBOARD_HTML has JS syntax error:\n{res.stderr}"
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
