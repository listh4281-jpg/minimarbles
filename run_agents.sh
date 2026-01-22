#!/bin/bash

# Minimarbles Loop - Continuous Claude agent execution
# Each agent completes ONE task then exits
# Usage: ./run_agents.sh <max_iterations>

cd "$(dirname "$0")"

if [ -z "$1" ]; then
  echo "Usage: $0 <iterations>"
  exit 1
fi

for ((i=1; i<=$1; i++)); do
    echo ""
    echo "========================================"
    echo "=== Starting Claude agent #$i ==="
    echo "=== $(date) ==="
    echo "========================================"
    echo ""

    result=$(claude -p "$(cat prompt.md)" --output-format text 2>&1) || true

    echo "$result"

    # Check if all tasks complete
    if [[ "$result" == *"<promise>COMPLETE</promise>"* ]]; then
        echo ""
        echo "========================================"
        echo "=== All tasks complete after $i iterations ==="
        echo "========================================"
        exit 0
    fi

    # Check if blocked
    if [[ "$result" == *"<promise>BLOCKED</promise>"* ]]; then
        echo ""
        echo "========================================"
        echo "=== Agent is blocked. Check status.md ==="
        echo "========================================"
        exit 1
    fi

    echo ""
    echo "=== End of iteration $i ==="
    echo ""

    sleep 2
done

echo "Reached max iterations ($1)"
exit 1
