#!/usr/bin/env python3
"""Create private repositories from validated data, running ONLY from trusted main."""
import base64
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

API = "https://api.github.com"
OWNER = "ai-app-user"
SOURCE = "ai-app-user/infra"
NAME = re.compile(r"[A-Za-z0-9_][A-Za-z0-9_.-]{0,79}\Z")


def api(token, endpoint, method="GET", data=None):
    payload = None if data is None else json.dumps(data).encode()
    req = urllib.request.Request(API + endpoint, data=payload, method=method, headers={
        "Authorization": "Bearer " + token,
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Content-Type": "application/json",
        "User-Agent": "infra-bootstrap",
    })
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            return response.status, json.load(response)
    except urllib.error.HTTPError as error:
        if error.code in (403, 404, 422):
            return error.code, None
        raise ValueError(f"GitHub request failed (HTTP {error.code})") from None


def validate(data, branch):
    if not isinstance(data, dict) or set(data) != {"schema", "owner", "name", "private"}:
        raise ValueError("invalid request schema")
    name = data["name"]
    if data["schema"] != 1 or data["owner"] != OWNER or data["private"] is not True:
        raise ValueError("only private repositories in the approved owner are allowed")
    if not isinstance(name, str) or not NAME.fullmatch(name) or name in (".", ".."):
        raise ValueError("invalid repository name")
    if branch != "bootstrap-requests/" + name:
        raise ValueError("request branch does not match the repository name")
    return name


def main():
    read_token = os.environ.get("GH_READ_TOKEN")
    token = os.environ.get("BOOTSTRAP_GITHUB_TOKEN")
    sha = os.environ.get("REQUEST_SHA", "")
    branch = os.environ.get("REQUEST_BRANCH", "")
    if not read_token or not token:
        raise ValueError("Actions authentication or BOOTSTRAP_GITHUB_TOKEN missing")
    if not re.fullmatch(r"[0-9a-f]{40}", sha) or not branch.startswith("bootstrap-requests/"):
        raise ValueError("invalid triggering commit or branch")
    status, entry = api(read_token, f"/repos/{SOURCE}/contents/bootstrap-request.json?ref={sha}")
    if status != 200 or not isinstance(entry, dict) or entry.get("encoding") != "base64":
        raise ValueError(f"cannot retrieve request data (HTTP {status})")
    try:
        data = base64.b64decode(entry["content"])
        if len(data) > 2048:
            raise ValueError("request too large")
        request = json.loads(data)
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError("invalid request JSON") from exc
    name = validate(request, branch)
    status, existing = api(token, f"/repos/{OWNER}/{urllib.parse.quote(name)}")
    if status == 200:
        if existing.get("full_name") != f"{OWNER}/{name}" or not existing.get("private"):
            raise ValueError("existing repository conflicts with private target")
        print(f"Already exists: https://github.com/{OWNER}/{name}")
        return
    if status != 404:
        raise ValueError(f"unable to verify repository absence (HTTP {status})")
    status, created = api(token, "/user/repos", "POST", {
        "name": name, "private": True, "auto_init": False,
        "description": "Bootstrapped by ai-app-user/infra"
    })
    if status != 201 or not isinstance(created, dict):
        raise ValueError(f"repository creation failed (HTTP {status}); verify token permission")
    if created.get("full_name") != f"{OWNER}/{name}" or not created.get("private"):
        raise ValueError("unexpected repository returned by API")
    print(f"Created private repository: https://github.com/{OWNER}/{name}")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, urllib.error.URLError, TimeoutError) as error:
        print(f"bootstrap request failed: {error}", file=sys.stderr)
        sys.exit(1)
