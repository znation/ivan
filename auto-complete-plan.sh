#!/usr/bin/env bash
# auto-complete-plan.sh — Iteratively address TODO items in HIGH_LEVEL_PLAN.md via pi.dev
set -euo pipefail
set -x

PLAN_FILE="HIGH_LEVEL_PLAN.md"

while true; do
    # Invoke pi with the prompt, capture stdout and stderr to a temp file
    OUTPUT_FILE=$(mktemp)

    pi "$PLAN_FILE" \
        "Address the next TODO item in HIGH_LEVEL_PLAN.md. Once it's done, write back to HIGH_LEVEL_PLAN.md indicating it's complete, and commit any changes. Then, respond MORE if there are more TODO items, or DONE if all are done." \
        --print 2>&1 | tee "$OUTPUT_FILE"

    # Check for DONE or MORE in the output
    if grep -q "DONE" "$OUTPUT_FILE"; then
        echo ""
        echo "=== All TODO items complete. ==="
        rm -f "$OUTPUT_FILE"
        exit 0
    elif grep -q "MORE" "$OUTPUT_FILE"; then
        echo ""
        echo "=== More work remaining, continuing... ==="
        rm -f "$OUTPUT_FILE"
        continue
    else
        echo ""
        echo "ERROR: Could not find 'DONE' or 'MORE' in pi's output." >&2
        echo "Full output:" >&2
        cat "$OUTPUT_FILE" >&2
        rm -f "$OUTPUT_FILE"
        exit 1
    fi
done
