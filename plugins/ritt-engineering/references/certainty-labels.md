# Certainty Labels

Material claims — diagnoses, results, external facts — carry one of four labels:

- `VERIFIED` — directly observed: command output, code read, primary documentation, supplied evidence.
- `INFERENCE` — follows from verified evidence but was not directly observed. Name the evidence.
- `HYPOTHESIS` — plausible explanation that still needs a discriminating test. Name the test.
- `UNVERIFIED` — not checked or not checkable right now. Say why.

Rules:

- Never report success without a `VERIFIED` check behind it; "should work" is `HYPOTHESIS`.
- Distinguish observed results from expected results in every report.
- Metrics and measurements are only reportable when actually measured.
- When evidence contradicts an earlier label, downgrade loudly — not silently.
