#!/usr/bin/env bash
# auto-complete-plan.sh — Iteratively address TODO items in HIGH_LEVEL_PLAN.md via pi.dev
set -euo pipefail
set -x

while true; do
    # Temp file for capturing the raw JSON event stream
    JSON_FILE=$(mktemp)

    # Run pi in JSON mode, streaming all events to stdout while saving raw events
    # Show each event as it arrives so we can see thinking, tool calls, and text deltas
    echo "=== Starting pi ===" >&2
    pi --mode json \
        "Address the next TODO item in HIGH_LEVEL_PLAN.md. Once it's done, write back to HIGH_LEVEL_PLAN.md indicating it's complete, and commit any changes. Then, respond MORE if there are more TODO items, or DONE if all are done." \
        2>&1 | tee "$JSON_FILE"

    # Check for DONE or MORE in the raw JSON stream
    if grep -q '"DONE"' "$JSON_FILE"; then
        echo ""
        echo "=== All TODO items complete. ==="
        rm -f "$JSON_FILE"
        exit 0
    elif grep -q '"MORE"' "$JSON_FILE"; then
        echo ""
        echo "=== More work remaining, continuing... ==="
        rm -f "$JSON_FILE"
        continue
    else
        echo ""
        echo "ERROR: Could not find 'DONE' or 'MORE' in pi's output." >&2
        echo "Full JSON response:" >&2
        cat "$JSON_FILE" >&2
        rm -f "$JSON_FILE"
        exit 1
    fi
done
