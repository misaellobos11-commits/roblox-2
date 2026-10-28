# Industrial Expansion Implementation Plan

> **For agentic workers:** Use superpowers:executing-plans inline; user requests execution without further design questions.

**Goal:** Deliver 20 additional machines with 40 connected recipes and resource models.
**Architecture:** Add a declarative expansion registry to the stage8 XML overlay pipeline. Generate catalog/economy extensions and original procedural models; reuse authoritative simulation and corrected port geometry.
**Tech Stack:** Python XML generation, Luau modules and CLI adapters, Roblox Studio place format.
**Spec:** docs/superpowers/specs/2026-10-28-industrial-expansion-design.md

## Global Constraints

- Preserve imported machines, transport routing, world and day/night.
- Every new recipe has at most two ingredients, quantities 1–2, output quantity 1.
- Levels 1–5 unchanged; new thresholds 10000, 25000, 60000.
- Work on isolated branch; do not stage unrelated root checkout changes.

## Review Focus

- Every recipe is reachable at its advertised tier and has enough input capacity.
- Missing ingredients or blocked outputs must not destroy or duplicate products.
- All four orientations align physical mouths with server ports.
- New types remain placeable, configurable and selectable in the icon catalog.
- Test/demo entry must preserve existing server authorization and explicit destructive-demo rules.

### Task 1: Catalog and production

Files: stage8/expansion/content.py, stage8/build_821.py,
stage8/tests/build_expansion.py, stage8/tests/expansion.luau.
Interface: content.MACHINES declares machines and recipes; generated overlay extends C and E before freeze.
- [ ] Write/run tests against 8.20, expect missing additional machines.
- [ ] Add 20 machines/40 recipes, data-driven input ports, full filter list and recipe descriptions.
- [ ] Execute actual simulation for all recipes: missing/full/valid inputs, routing, sales and tiers.
- [ ] Commit verified content.

### Task 2: Visuals and access

Files: stage8/expansion/models.py, cargo.py, runtime-ui patches and tests.
Interface: generated MachineVisual uses registered machine/cargo part specifications; existing Visual.create/setCargo contracts preserved.
- [ ] Add failing tests for unique models, ports and all cargo clearances.
- [ ] Generate distinctive machine silhouettes, compact resources and catalog previews.
- [ ] Provide accessible filter selection and an expansion test using current demo permissions.
- [ ] Run visual/catalog tests and old transport regressions; inspect auxiliary model preview.
- [ ] Commit verified models/UI.

### Task 3: Review and delivery

Files: stage8/check_821.sh, stage8/GUIA_PRUEBA_8_21.txt,
stage8/expansion/RECETAS_8_21.md, downloads/Matterloom_8_21_Expansion_Industrial.zip.
- [ ] Build place, compile changed scripts, verify XML isolation and full regression suite.
- [ ] Independent whole-change review; fix material findings with regression tests.
- [ ] Package place/guide/recipes, push feature branch and verify public ZIP byte-for-byte.
