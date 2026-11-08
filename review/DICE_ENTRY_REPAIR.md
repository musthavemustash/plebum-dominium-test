# Dice-entry regression repair

Scope: authoritative staging source `docs/dice-converter.html`. Production,
historical root HTML, and previously published ZIPs are not modified by this repair.

## Evidence and correction

The tester's T3 recording shows individual dice buttons leaving the counters at
zero while the test-fill control populates the roll list. Full-controller execution
against the unmodified staging source reproduces `ReferenceError: netBlocked is
not defined` at startup. The strict-mode controller assigned that variable without
declaring it. This aborts initialization before network listeners are registered;
manual entry and validation also reference the missing variable. The prior
function-only network test supplied the variable itself, masking this failure.

Declare and initialize `netBlocked` inside the controller before handler setup.
Keep the existing local-file/explicit-offline policy and cryptographic algorithms.

The regression test also exposed stale mnemonic output after Undo reduced manual
input from 256 to 254 bits. Rendering now clears manual-derived words whenever
the recorded input is incomplete, while preserving valid pasted-input output.

## Completed automated checks

`node scripts/test_dice_controller.cjs` executes the shipped core and controller
with DOM and network doubles. An observation wrapper tracks async dice-handler
promises; the test does not inject a network-block variable or replace the guards.
Coverage includes:

- Startup, all six buttons, skipped faces, keyboard entry and input focus.
- Counters, bit mapping, 256-bit limit, Undo/Clear and stale-output removal.
- Test-fill, paste/manual transitions, invalid input, and all eight public vectors.
- Twenty protocol/network startup combinations; sensitive controls stay blocked
  outside a local file with an explicit offline signal.
- Reconnect clearing, offline resumption, unknown-state rejection, and button-tap
  rechecks after missed online/offline events.

The test fails before the declaration fix, then fails at stale output until the
Undo correction is applied. Existing network tests and the 96-page staging
validator also pass. The dedicated PR/main workflow runs these controller checks
without publishing or deploying the site.

## Remaining verification and packaging

These are controller tests, not execution in Edge or proof of network isolation.
Repeat T2 and affected T3 checks in the target browser against the replacement
package, including keyboard entry, Undo after generating words, reconnect wiping,
and reopening. Physical Tails remains unverified.

The original `alpha-20261105-7240f0d` ZIP retains its original bytes and defects.
This source repair does not fix already downloaded copies. A separately versioned
test package with regenerated manifests/checksums and rebuilt complete/tools-only
downloads is required before asking testers to use the repaired tools.
