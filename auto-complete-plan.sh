#!/usr/bin/env bash
# auto-complete-plan.sh — Iteratively address TODO items in HIGH_LEVEL_PLAN.md via pi.dev
set -euo pipefail
set -x

while true; do
    # Temp files for capturing the full JSON stream and assembled text response
    JSON_FILE=$(mktemp)
    TEXT_FILE=$(mktemp)

    # Run pi in JSON mode, streaming deltas to stdout while saving raw events
    # stdbuf forces line buffering (without it, piped programs use block buffering and you see nothing until the end)
    # jq -u enables unbuffered output so text appears immediately as deltas arrive
    stdbuf -oL pi --mode json \
        "Address the next TODO item in HIGH_LEVEL_PLAN.md. Once it's done, write back to HIGH_LEVEL_PLAN.md indicating it's complete, and commit any changes. Then, respond MORE if there are more TODO items, or DONE if all are done." \
        2>&1 | stdbuf -oL tee "$JSON_FILE" \
        | stdbuf -oL jq -u -r 'select(.type == "message_update") | .assistantMessageEvent.delta // empty' \
        > "$TEXT_FILE"

    # Check for DONE or MORE in the assembled text response
    if grep -q "DONE" "$TEXT_FILE"; then
        echo ""
        echo "=== All TODO items complete. ==="
        rm -f "$JSON_FILE" "$TEXT_FILE"
        exit 0
    elif grep -q "MORE" "$TEXT_FILE"; then
        echo ""
        echo "=== More work remaining, continuing... ==="
        rm -f "$JSON_FILE" "$TEXT_FILE"
        continue
    else
        echo ""
        echo "ERROR: Could not find 'DONE' or 'MORE' in pi's output." >&2
        echo "Full text response:" >&2
        cat "$TEXT_FILE" >&2
        rm -f "$JSON_FILE" "$TEXT_FILE"
        exit 1
    fi
done
