#!/usr/bin/env python3
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


BASELINE_PATH = Path(__file__).resolve().with_name("upstream_baseline.json")


@dataclass(frozen=True)
class UpstreamBaseline:
    repo_url: str
    target_version: str
    upstream_ref: str
    target_commit: str
    comparison_branch: str
    runtime_paths: tuple[str, ...]


def load_upstream_baseline(path: Path = BASELINE_PATH) -> UpstreamBaseline:
    data = json.loads(path.read_text(encoding="utf-8"))
    return UpstreamBaseline(
        repo_url=str(data["repo_url"]),
        target_version=str(data["target_version"]),
        upstream_ref=str(data["upstream_ref"]),
        target_commit=str(data["target_commit"]),
        comparison_branch=str(data["comparison_branch"]),
        runtime_paths=tuple(str(p) for p in data["runtime_paths"]),
    )
