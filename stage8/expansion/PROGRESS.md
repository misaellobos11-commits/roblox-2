# Ledger — plan: docs/superpowers/plans/2026-10-28-industrial-expansion.md

Base 246b1a5. Isolated worktree /workspace/matterloom-821.
Preflight: catalog identifiers feed visuals, UI and simulation; one registry is the authority.
Baseline: original 8.20 cargo test passes for all 14 items.
Decision: execute directly after user requested more machines instead of continuing design questions.
Decision: keep credit purchasing; use advanced products in recipes and sales. No answer authorizes replacing purchasing with item costs.

Task 1: complete (e8e739a). RED on missing 20 machines; GREEN on 53 recipes,
54 reachable resources, 212 rotated deliveries, consume/block/sale and filters.
Tier reachability caught ConductiveWire requiring a tier-4 ingredient; moved
WireDrawer to tier 4 before delivery.
Task 2: RED on missing authored models/cargo; RED on invisible category cards;
RED on missing demo staging. GREEN on 20 unique models/80 port placements,
54 cargo models, all 44 UI cards, searchable filter selection, finite 240-sale
demo and empty/foreign plot guards. Auxiliary preview/full regression next.

Task 2: complete (bcac490). Full check_821.sh GREEN, including legacy demos,
directional transport, continuous animation, automatic elevator placement and
Roblox XML geometry round-trip. Blender auxiliary gallery inspected: all 20
models visible and distinct; this is not Studio render validation.

Final independent review: review_expansion_821, no critical/important issues.
Found stale controller catalogOpen after F hid the catalog directly. Treated as
a user-visible navigation fix: RED test reproduced B requiring a second press;
GREEN after closing through the catalog callback. Entire suite GREEN afterward.
No deferred review findings. Studio rendering/performance and economy pacing
remain explicit manual validation items; complete network handler not emulated.

Task 3: complete. Public ZIP (4,714,047 bytes) downloaded and byte-compared
against local archive and exact built place. 33 PASS groups in check_821.sh;
offline catalog JS syntax checked. Feature branch pushed, no main merge.
Delivery commit: 52453df. Existing root checkout untouched.
