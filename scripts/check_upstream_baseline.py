#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from upstream_baseline import load_upstream_baseline


def run(argv: list[str], *, cwd: Path | None = None) -> str:
    proc = subprocess.run(
        argv,
        cwd=str(cwd) if cwd else None,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(
            "Command failed:\n"
            f"  cwd: {cwd}\n"
            f"  cmd: {' '.join(argv)}\n"
            f"  code: {proc.returncode}\n"
            f"  stdout:\n{proc.stdout}\n"
            f"  stderr:\n{proc.stderr}\n"
        )
    return proc.stdout.strip()


def ensure_checkout(repo_url: str, cache: Path) -> None:
    if (cache / ".git").is_dir():
        return
    if cache.exists():
        raise RuntimeError(f"Cache exists but is not a git checkout: {cache}")
    cache.parent.mkdir(parents=True, exist_ok=True)
    run(["git", "clone", "--filter=blob:none", "--no-checkout", repo_url, str(cache)])


def fetch_ref(cache: Path, ref: str) -> str:
    run(["git", "-C", str(cache), "fetch", "--depth", "1", "origin", ref])
    return run(["git", "-C", str(cache), "rev-parse", "FETCH_HEAD"])


def main(argv: list[str]) -> int:
    baseline = load_upstream_baseline()
    ap = argparse.ArgumentParser(
        description="Verify the pinned upstream Spine runtime baseline."
    )
    ap.add_argument("--cache", default=".cache/spine-runtimes-baseline")
    ap.add_argument("--repo-url", default=baseline.repo_url)
    ap.add_argument("--ref", default=baseline.upstream_ref)
    ap.add_argument("--comparison-branch", default=baseline.comparison_branch)
    args = ap.parse_args(argv)

    cache = Path(args.cache).resolve()
    ensure_checkout(args.repo_url, cache)

    pinned_commit = fetch_ref(cache, args.ref)
    branch_commit = fetch_ref(cache, args.comparison_branch)

    if args.ref == baseline.upstream_ref and pinned_commit != baseline.target_commit:
        raise RuntimeError(
            f"Configured ref {args.ref} resolved to {pinned_commit}, "
            f"expected {baseline.target_commit}"
        )

    diff = run(
        [
            "git",
            "-C",
            str(cache),
            "diff",
            "--name-status",
            f"{pinned_commit}..{branch_commit}",
            "--",
            *baseline.runtime_paths,
        ]
    )
    if diff:
        print(diff, file=sys.stderr)
        raise RuntimeError(
            f"Runtime paths drifted between {args.ref} and {args.comparison_branch}"
        )

    print("Upstream Spine runtime baseline verified:")
    print(f"  repo:              {args.repo_url}")
    print(f"  target version:    {baseline.target_version}")
    print(f"  pinned ref:        {args.ref}")
    print(f"  pinned commit:     {pinned_commit}")
    print(f"  comparison branch: {args.comparison_branch}")
    print(f"  comparison commit: {branch_commit}")
    print(f"  runtime paths:     {', '.join(baseline.runtime_paths)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
