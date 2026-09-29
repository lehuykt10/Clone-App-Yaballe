#!/usr/bin/env python3
"""Download Shopify's Dawn theme (pinned version) into ./theme and install the kit.

Usage (from the project folder):
    python .claude/skills/shopify-theme-kit/scripts/new_theme.py [--dir theme] [--version v16.0.0]
"""
import argparse
import shutil
import stat
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def on_rm_error(func, path, _):
    # Windows: git objects are read-only.
    Path(path).chmod(stat.S_IWRITE)
    func(path)


def rmtree(path):
    if sys.version_info >= (3, 12):
        shutil.rmtree(path, onexc=on_rm_error)
    else:
        shutil.rmtree(path, onerror=on_rm_error)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="theme")
    ap.add_argument("--version", default="v16.0.0", help="Dawn git tag")
    args = ap.parse_args()
    target = Path(args.dir).resolve()
    if (target / "sections/main-product.liquid").exists():
        print(f"{target} da co theme. Chi cai lai kit.")
    else:
        if target.exists() and any(target.iterdir()):
            print(f"LOI: {target} da ton tai va khong trong.")
            sys.exit(1)
        print(f"Dang tai Dawn {args.version} ...")
        subprocess.run(["git", "clone", "--depth", "1", "--branch", args.version,
                        "https://github.com/Shopify/dawn.git", str(target)], check=True)
        rmtree(target / ".git")
        for extra in (".github", "release-notes.md"):
            p = target / extra
            if p.is_dir():
                rmtree(p)
            elif p.exists():
                p.unlink()
    subprocess.run([sys.executable, str(HERE / "install_kit.py"), str(target)], check=True)


if __name__ == "__main__":
    main()
