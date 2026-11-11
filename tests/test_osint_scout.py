import json
import os
import socket
import subprocess
import threading
import time
import urllib.error
import urllib.request
from http.server import HTTPServer
import pytest

import sys
REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO_DIR)

import server as osint_server


@pytest.fixture(scope="module")
def live_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    sock.close()

    httpd = HTTPServer(("127.0.0.1", port), osint_server.OSINTScoutHandler)
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    time.sleep(0.15)
    yield f"http://127.0.0.1:{port}"
    httpd.shutdown()
    httpd.server_close()


def test_health_endpoint(live_server):
    with urllib.request.urlopen(f"{live_server}/health", timeout=3) as resp:
        assert resp.status == 200
        data = json.loads(resp.read().decode("utf-8"))
        assert data["status"] == "healthy"
        assert data["service"] == "osint-scout-skill"
        assert "100% Free" in data["license"]


def test_api_health_alias(live_server):
    with urllib.request.urlopen(f"{live_server}/api/health", timeout=3) as resp:
        assert resp.status == 200
        data = json.loads(resp.read().decode("utf-8"))
        assert data["tool"] == "Domain Intel OSINT Scout"


def test_api_recon_missing_domain(live_server):
    with pytest.raises(urllib.error.HTTPError) as exc:
        urllib.request.urlopen(f"{live_server}/api/recon", timeout=3)
    assert exc.value.code == 400


def test_api_recon_localhost(live_server):
    with urllib.request.urlopen(f"{live_server}/api/recon?domain=localhost", timeout=3) as resp:
        assert resp.status == 200
        data = json.loads(resp.read().decode("utf-8"))
        assert data["target"] == "localhost"
        assert data["status"] == "success"
        assert "A" in data["records"]


def test_static_index_html_served(live_server):
    with urllib.request.urlopen(f"{live_server}/", timeout=3) as resp:
        assert resp.status == 200
        html = resp.read().decode("utf-8")
        assert "Domain Intel OSINT Scout" in html
        assert "application/ld+json" in html


def test_open_access_and_coffee_support_invariants():
    index_path = os.path.join(REPO_DIR, "public", "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        html = f.read()
    assert "https://buy.stripe.com/3cIfZg27PdKo2D64Ocfw40X" in html
    assert "GG2eQbVh8ut1BK6j1A2tz7pSySdLpD38BgyEhGcxdXoK" in html
    assert "openDePayCheckout" not in html
    assert "WebApplication" in html
    assert "FAQPage" in html


def _cli_cmd(*args):
    local_bin = os.path.join(REPO_DIR, "bin", "osint-scout-skill")
    if os.path.exists(local_bin):
        return [sys.executable, local_bin, *args]
    return ["osint-scout-skill", *args]


def test_cli_help_and_version():
    res = subprocess.run(_cli_cmd("--help"), capture_output=True, text=True, check=True)
    assert "Domain Intel OSINT Scout" in res.stdout
    assert "scan" in res.stdout


def test_cli_json_telemetry():
    res = subprocess.run(_cli_cmd("--json"), capture_output=True, text=True, check=True)
    data = json.loads(res.stdout)
    assert data["id"] == "osint-scout-skill"
    assert data["installed"] is True
    assert "100% Free" in data["license"]


def test_cli_scan_subcommand():
    res = subprocess.run(_cli_cmd("scan", "localhost"), capture_output=True, text=True, check=True)
    data = json.loads(res.stdout)
    assert data["target"] == "localhost"
    assert "records" in data
