# PawPal+ (Module 2 Project)

**PawPal+** is a Streamlit app that helps a pet owner plan care tasks for their pets.

## Scenario
A busy pet owner needs help staying consistent with pet care. They want an assistant that can:
- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan
The projecgit statust includes a UML design, Python classes for owners, pets, tasks, and scheduling, a Streamlit interface, and tests for core behaviors. The final UML diagram is [uml_final.mmd](diagrams/uml_final.mmd); the original draft remains in [uml_draft.mmd](diagrams/uml_draft.mmd).

## What you will build

The app currently:
- Lets a user enter an owner and add multiple pets
- Lets a user add care tasks with scheduled time, duration, priority, and frequency
- Generates a schedule for a selected date within an available-minutes limit
- Excludes completed tasks and reports overlaps among tasks selected for the schedule
- Includes tests for task management and scheduling behaviors

## Getting started

### Setup

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in app.py.
7. Refine UML so it matches what you actually built.
The terminal demo can be run with python main.py. To launch the Streamlit interface, run:
python -m streamlit run app.py

## 🖥️ Sample Output

Run the terminal demo with:
python main.py
The demo retrieves tasks from multiple pets and displays them by scheduled time.
Today's Schedule
08:00 AM — Morning walk
08:30 AM — Breakfast
04:00 PM — Afternoon playtime

## 🧪 Testing PawPal+

```bash
python -m pytest
```

Current test output:

```text
8 passed
```

## 📐 Smarter Scheduling

Feature	Method(s)	Notes
Task sorting	Scheduler.sort_by_time()	Sorts by scheduled time; priority (high, medium, low) breaks ties.
Filtering	Scheduler.filter_tasks()	Excludes completed tasks and selects tasks that fit the available-minutes budget, prioritizing higher priority.
Conflict handling	Scheduler.detect_conflicts()	Detects overlapping task intervals. generate_schedule() stores conflicts among tasks selected for the schedule in Scheduler.conflicts.
Recurring tasks	Scheduler._occurs_on(); Scheduler.generate_schedule()	once tasks occur on their due date, daily tasks recur on and after that date, and weekly tasks recur on the same weekday on and after that date. Original task dates are not changed.

## 📸 Demo Walkthrough
Run python -m streamlit run app.py and enter the owner's name.
Add each pet by entering its name and selecting its species.
Select a pet, then add a care task with its description, scheduled time, duration, priority, and frequency.
Review the task list; select an incomplete task and choose Mark complete to exclude it from future schedules.
Choose a schedule date and available minutes, then select Generate schedule to view selected tasks in chronological order.
Review any reported overlaps, which identify both tasks and their pets. Only tasks included in the generated schedule are checked for conflicts.