# Minimarbles - Agent Prompt

## Your Workflow
1. Read `tasks.md` and find the first unchecked task (`- [ ]`)
2. Write a failing test for that task
3. Write the minimum code to make the test pass
4. Run `pytest` to verify
5. Mark the task as complete in `tasks.md` (change `- [ ]` to `- [x]`)
6. Commit with a descriptive message
7. If all tasks are complete, output `<promise>COMPLETE</promise>`. Otherwise just stop - a new agent will pick up the next task.

## Important Rules
- **One task per session.** Complete one task, commit, then exit.
- **TDD strictly.** Write the test FIRST. Watch it fail. Then write code.
- **Explain as you go.** The user is learning - explain what you're doing and why.
- **One task only.** After the commit, stop. Don't start the next task.
- **If blocked:** If you can't complete a task (need human input, unclear requirements, unexpected error), write the issue to `status.md` and output `<promise>BLOCKED</promise>`. The loop will pause for human review.

## Project Overview
A web app for friends to record trades with each other using a virtual currency called "minimarbles".

## Tech Stack
- **Flask** - Python web framework
- **SQLite** - Database (via Flask-SQLAlchemy when we add it)
- **pytest** - Testing framework
- **GitHub** - Version control

## Key Business Rules

### Trade Types
1. **Binary:** Yes/no outcome with asymmetric stakes (e.g., 20:10 odds)
   - Party A stakes X, Party B stakes Y
   - If outcome is YES: A wins Y, B loses Y
   - If outcome is NO: B wins X, A loses X

2. **Underlying:** Linear exposure to a price
   - Long party and short party agree on trade price and lot size
   - P&L = lot_size × (settlement_price - trade_price)
   - Long gains if price goes up, short gains if price goes down

### Minimarbles
- Each user starts with 1000 (admin-configurable)
- Zero-sum: minimarbles are conserved across all trades
- Users must have sufficient balance to trade (but no margin checks for underlying)

## Testing Commands
```bash
source venv/bin/activate
pytest                    # Run all tests
pytest -v                 # Verbose output
pytest tests/test_file.py # Run specific file
pytest -x                 # Stop on first failure
```

## File Structure
```
trading-website/
├── app/
│   ├── __init__.py       # Flask app factory
│   ├── routes.py         # URL handlers
│   ├── models.py         # Database models (create when needed)
│   └── logic.py          # Pure business logic (create when needed)
├── tests/
│   └── test_*.py         # Test files
├── tasks.md              # Task list - check off completed tasks
└── prompt.md             # This file
```
