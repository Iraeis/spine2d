# Spine 4.3 Latest Tag Upstream Audit Map

This document anchors module-by-module parity work to the latest official Spine 4.3 runtime tag.

## Baseline

- Upstream repo: `https://github.com/EsotericSoftware/spine-runtimes`
- Target version: `4.3-latest-tag`
- Pinned ref: `spine-flutter-4.3.4`
- Pinned commit: `80dc680a4345ac09cdc5d4c1a77ec572a3f295d1`
- Primary reference paths: `spine-cpp/`, `spine-c/`, `examples/`

## Why This Tag

Official 4.3 refs currently include:

- `spine-libgdx-4.3.2`
- `spine-flutter-4.3.3`
- `spine-flutter-4.3.4`

There is no plain `4.3.2` tag in the official repository. Local verification shows empty diffs for `spine-c` and `spine-cpp` between `spine-libgdx-4.3.2` and both the current `4.3` branch and `spine-flutter-4.3.4`.

The project now pins `spine-flutter-4.3.4` because it is the newest official 4.3 tag. The comparison gate still checks the moving `4.3` branch for drift across `spine-c`, `spine-cpp`, and `examples`.

## Audit Workflow

For each runtime module:

1. Compare Rust behavior against `spine-cpp` first.
2. Use `spine-c` when C symbols or generated code define the behavior more directly.
3. Add or update an oracle scenario before changing behavior when the difference is observable.
4. Record any intentional deviation in a follow-up decision document.

## Priority Areas

- AnimationState mixing and timeline property gating.
- JSON and binary data format fields introduced or stabilized in 4.3.
- Physics, slider, IK, transform, and path constraint update ordering.
- Slot attachment, draw order, event, deform, sequence, and clipping semantics.
