#!/bin/bash

# Minimarbles Loop - Continuous Claude agent execution
# Each agent completes ONE task then exits

cd "$(dirname "$0")"

agent_num=1

while true; do
    echo ""
    echo "========================================"
    echo "=== Starting Claude agent #$agent_num ==="
    echo "=== $(date) ==="
    echo "========================================"
    echo ""

    # Call claude in one-shot mode (--print exits after completion)
    # Permissions configured in .claude/settings.json
    claude --print --verbose "$(cat prompt.md)"

    EXIT_CODE=$?

    echo ""
    echo "========================================"
    echo "=== Agent #$agent_num exited with code $EXIT_CODE ==="
    echo "========================================"

    # Check if all tasks complete (no unchecked boxes remain)
    if ! grep -q "\- \[ \]" tasks.md 2>/dev/null; then
        echo "=== All tasks complete! Exiting loop ==="
        break
    fi

    # Check if blocked (agent needs human help)
    if grep -q "^STATUS: BLOCKED" status.md 2>/dev/null; then
        echo "=== Agent is blocked. Check status.md for details ==="
        break
    fi

    # Show current task progress
    echo ""
    echo "=== Current tasks.md state ==="
    cat tasks.md
    echo ""

    sleep 2
    agent_num=$((agent_num + 1))
done
