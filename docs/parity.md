# Parity Baseline

This project targets behavioral parity with the latest official Spine 4.3 runtime tag.

## Upstream Pin

- Source: `https://github.com/EsotericSoftware/spine-runtimes`
- Target version: `4.3-latest-tag`
- Upstream ref: `spine-flutter-4.3.4`
- Target commit: `80dc680a4345ac09cdc5d4c1a77ec572a3f295d1`

The official repository does not publish a plain global `4.3.4` runtime tag. The newest available 4.3 tag is package-specific, `spine-flutter-4.3.4`, so the baseline pins that exact ref and commit.

Local verification shows no `spine-c`, `spine-cpp`, or `examples` drift between `spine-libgdx-4.3.2`, `spine-flutter-4.3.4`, and the current `4.3` branch head.

## Verification

Run `scripts/check_upstream_baseline.py` to verify the configured ref resolves to the expected commit and has no `spine-c`, `spine-cpp`, or `examples` drift from the official `4.3` branch.

Golden oracle SOURCE metadata under `spine2d/tests/golden/` records the same target version, upstream ref, and commit. When this baseline changes, regenerate pose and render oracle goldens before judging parity failures.
