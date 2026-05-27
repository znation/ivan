#!/usr/bin/env bash
# auto-complete-plan.sh — Iteratively address TODO items in HIGH_LEVEL_PLAN.md via pi.dev
set -euo pipefail

while true; do
    # Temp file for capturing the raw JSON event stream
    JSON_FILE=$(mktemp)

    echo "=== Starting pi ===" >&2

    # Run pi in JSON mode, streaming all events to stdout while saving raw events
    pi --mode json \
        'Address the next TODO item in EXECUTION_PLAN.md. To get more context about what we'\''re attempting, feel free to take a look at HIGH_LEVEL_PLAN.md. Once your one TODO item is done, write back to EXECUTION_PLAN.md indicating it'\''s complete, and commit any changes. Then respond with a JSON block on its own line: {"done": true} if all TODO items are finished, or {"done": false} if there are more TODO items remaining.' \
        2>&1 | tee "$JSON_FILE"

    # Check for explicit failure events before anything else.
    AUTO_RETRY_FAILURE=$(jq -r '
        [.[] | select(.type == "auto_retry_end") | .success] | last // empty
    ' "$JSON_FILE" 2>/dev/null || true)

    if [ "$AUTO_RETRY_FAILURE" = "false" ]; then
        echo "" >&2
        echo "ERROR: pi failed after retries." >&2
        jq -r '[.[] | select(.type == "auto_retry_end")] | last | .finalError // empty' "$JSON_FILE" 2>/dev/null || true | while read -r line; do
            [ -n "$line" ] && echo "  Final error: $line" >&2
        done
        rm -f "$JSON_FILE"
        exit 1
    fi

    # Check for agent-level errors (last agent_end stopReason != "finish").
    STOP_REASON=$(jq -r '
        [.[] | select(.type == "agent_end") | .stopReason // "unknown"] | last
    ' "$JSON_FILE" 2>/dev/null || true)

    if [ "$STOP_REASON" != "finish" ] && [ "$STOP_REASON" != "end_turn" ]; then
        echo "" >&2
        echo "ERROR: Agent ended with stopReason='$STOP_REASON'." >&2
        jq -r '[.[] | select(.type == "agent_end")] | last | .errorMessage // empty' "$JSON_FILE" 2>/dev/null || true | while read -r line; do
            [ -n "$line" ] && echo "  Error: $line" >&2
        done
        rm -f "$JSON_FILE"
        exit 1
    fi

    # Extract the final assistant message content from agent_end event.
    # This avoids matching "DONE"/"MORE" in tool args, file contents,
    # thinking text, or any other part of the JSON stream.
    FINAL_TEXT=$(jq -r '
        select(.type == "agent_end") |
        [.messages[] | select(.role == "assistant")] | last |
        [.content[] | select(.type == "text") | .text] | join("\n")
    ' "$JSON_FILE" 2>/dev/null || true)

    if [ -z "$FINAL_TEXT" ]; then
        echo "" >&2
        echo "ERROR: Could not extract assistant message from pi output." >&2
        rm -f "$JSON_FILE"
        exit 1
    fi

    # Look for the structured JSON signal in the final response text only.
    # Handles both bare JSON and markdown-wrapped blocks like ```json {"done": true}```
    if echo "$FINAL_TEXT" | grep -qE '(```[a-z]*\s*)?\{"done":\s*true\s*\}(\s*```)?'; then
        echo ""
        echo "=== All TODO items complete. ==="
        rm -f "$JSON_FILE"
        exit 0
    elif echo "$FINAL_TEXT" | grep -qE '(```[a-z]*\s*)?\{"done":\s*false\s*\}(\s*```)?'; then
        echo ""
        echo "=== More work remaining, continuing... ==="
        rm -f "$JSON_FILE"
        continue
    else
        # Fallback: check for the old DONE/MORE keywords in case model didn't use structured output
        if echo "$FINAL_TEXT" | grep -qi '\bDONE\b'; then
            echo ""
            echo "=== All TODO items complete. ==="
            rm -f "$JSON_FILE"
            exit 0
        elif echo "$FINAL_TEXT" | grep -qi '\bMORE\b'; then
            echo ""
            echo "=== More work remaining, continuing... ==="
            rm -f "$JSON_FILE"
            continue
        fi

        # Nothing found — show the model's response for debugging and retry
        echo "" >&2
        echo "ERROR: Could not find completion signal in pi output." >&2
        echo "Final assistant message:" >&2
        echo "---" >&2
        echo "$FINAL_TEXT" >&2
        echo "---" >&2
        rm -f "$JSON_FILE"
        exit 1
    fi
done
