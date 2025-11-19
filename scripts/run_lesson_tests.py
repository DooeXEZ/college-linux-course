#!/usr/bin/env python3

import subprocess
import sys
from pathlib import Path
import requests

RAW_URLS = {
    "01-initial-setup": "https://raw.githubusercontent.com/virusneo1997-del/college-linux-course/refs/heads/main/lessons/01-initial-setup/README.md",
    "02-users-permissions": "https://raw.githubusercontent.com/virusneo1997-del/college-linux-course/refs/heads/main/lessons/02-users-permissions/README.md",
    "03-web-server": "https://raw.githubusercontent.com/virusneo1997-del/college-linux-course/refs/heads/main/lessons/03-web-server/README.md",
    "04-monitoring": "https://raw.githubusercontent.com/virusneo1997-del/college-linux-course/refs/heads/main/lessons/04-monitoring/README.md",
    "05-databases-backups": "https://raw.githubusercontent.com/virusneo1997-del/college-linux-course/refs/heads/main/lessons/05-databases-backups/README.md",
    "06-docker-containers": "https://raw.githubusercontent.com/virusneo1997-del/college-linux-course/refs/heads/main/lessons/06-docker-containers/README.md",
}

def download_readme(lesson_name):
    url = RAW_URLS.get(lesson_name)
    if not url:
        return None

    resp = requests.get(url)
    resp.raise_for_status()
    folder = Path("tests") / lesson_name
    folder.mkdir(parents=True, exist_ok=True)
    readme_path = folder / "README.md"
    readme_path.write_text(resp.text, encoding="utf-8")
    return readme_path

def run_pytest(lesson_name):
    print(f"Running tests for lesson {lesson_name}")
    res = subprocess.run(["pytest", "-q", str(Path("tests") / lesson_name)], check=False)
    return res.returncode

def main():
    # Можно брать уроки из аргументов или просто запускать для всех
    exit_code = 0
    for lesson in RAW_URLS:
        path = download_readme(lesson)
        if path:
            code = run_pytest(lesson)
            if code != 0:
                exit_code = code
        else:
            print(f"No README URL for {lesson}")
    sys.exit(exit_code)

if __name__ == "__main__":
    main()

