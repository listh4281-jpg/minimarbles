#!/bin/bash

# Minimarbles Loop - Continuous Claude agent execution
# Each agent completes ONE task then exits

cd "$(dirname "$0")"

while true; do
    echo ""
    echo "========================================"
    echo "=== Starting new Claude agent ==="
    echo "=== $(date) ==="
    echo "========================================"
    echo ""

    # Call claude with verbose output to see thinking
    # --verbose shows reasoning, --print outputs to terminal
    claude --print --verbose "$(cat prompt.md)"

    EXIT_CODE=$?

    echo ""
    echo "========================================"
    echo "=== Agent exited with code $EXIT_CODE ==="
    echo "========================================"

    # Check if all tasks complete (no unchecked boxes remain)
    if ! grep -q "\- \[ \]" tasks.md 2>/dev/null; then
        echo "=== All tasks complete! Exiting loop ==="
        break
    fi

    # Show current task progress
    echo ""
    echo "=== Current tasks.md state ==="
    cat tasks.md
    echo ""

    sleep 2
done
