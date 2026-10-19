from datetime import date, datetime

from pawpal_system import Owner, Pet, Scheduler, Task


def test_mark_complete_sets_task_completed() -> None:
    task = Task(
        description="Morning walk",
        due_time=datetime(2026, 10, 19, 8, 0),
        duration=30,
        priority="high",
        frequency="daily",
    )

    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_pet_task_count() -> None:
    pet = Pet(name="Mochi", species="dog")
    task = Task(
        description="Morning walk",
        due_time=datetime(2026, 10, 19, 8, 0),
        duration=30,
        priority="high",
        frequency="daily",
    )

    initial_task_count = len(pet.list_tasks())
    pet.add_task(task)

    assert len(pet.list_tasks()) == initial_task_count + 1


def test_scheduler_sorts_by_time_and_priority() -> None:
    schedule_date = date(2026, 10, 19)
    earlier = Task("Earlier", datetime(2026, 10, 19, 7, 0), 10, "low", "once")
    low_priority = Task(
        "Low priority", datetime(2026, 10, 19, 8, 0), 10, "low", "once"
    )
    high_priority = Task(
        "High priority", datetime(2026, 10, 19, 8, 0), 10, "high", "once"
    )
    owner = Owner(
        "Jordan",
        [
            Pet("Mochi", "dog", [low_priority, earlier]),
            Pet("Miso", "cat", [high_priority]),
        ],
    )

    schedule = Scheduler(owner).generate_schedule(schedule_date=schedule_date)

    assert schedule == [earlier, high_priority, low_priority]


def test_generated_schedule_excludes_completed_tasks() -> None:
    schedule_date = date(2026, 10, 19)
    incomplete = Task("Walk", datetime(2026, 10, 19, 8, 0), 30, "high", "once")
    completed = Task(
        "Feeding", datetime(2026, 10, 19, 9, 0), 10, "medium", "once", completed=True
    )
    owner = Owner("Jordan", [Pet("Mochi", "dog", [incomplete, completed])])

    schedule = Scheduler(owner).generate_schedule(schedule_date=schedule_date)

    assert schedule == [incomplete]


def test_available_minutes_favor_high_priority_tasks_that_fit() -> None:
    schedule_date = date(2026, 10, 19)
    high_priority = Task(
        "Medication", datetime(2026, 10, 19, 8, 0), 20, "high", "once"
    )
    medium_priority = Task(
        "Feeding", datetime(2026, 10, 19, 9, 0), 10, "medium", "once"
    )
    low_priority = Task(
        "Grooming", datetime(2026, 10, 19, 10, 0), 15, "low", "once"
    )
    owner = Owner(
        "Jordan",
        [Pet("Mochi", "dog", [low_priority, medium_priority, high_priority])],
    )

    schedule = Scheduler(owner).generate_schedule(
        schedule_date=schedule_date,
        available_minutes=30,
    )

    assert schedule == [high_priority, medium_priority]


def test_daily_and_weekly_tasks_appear_on_their_recurrence_dates() -> None:
    daily = Task("Daily feeding", datetime(2026, 10, 18, 8, 0), 10, "high", "daily")
    weekly = Task("Weekly grooming", datetime(2026, 10, 12, 9, 0), 30, "medium", "weekly")
    owner = Owner("Jordan", [Pet("Mochi", "dog", [daily, weekly])])
    scheduler = Scheduler(owner)

    monday_schedule = scheduler.generate_schedule(schedule_date=date(2026, 10, 19))
    tuesday_schedule = scheduler.generate_schedule(schedule_date=date(2026, 10, 20))

    assert monday_schedule == [daily, weekly]
    assert tuesday_schedule == [daily]
    assert daily.due_time == datetime(2026, 10, 18, 8, 0)
    assert weekly.due_time == datetime(2026, 10, 12, 9, 0)


def test_scheduler_detects_overlaps_across_different_pets() -> None:
    schedule_date = date(2026, 10, 19)
    first_task = Task("Walk", datetime(2026, 10, 19, 8, 0), 30, "high", "once")
    second_task = Task("Medication", datetime(2026, 10, 19, 8, 20), 10, "medium", "once")
    owner = Owner(
        "Jordan",
        [Pet("Mochi", "dog", [first_task]), Pet("Miso", "cat", [second_task])],
    )
    scheduler = Scheduler(owner)

    scheduler.generate_schedule(schedule_date=schedule_date)

    assert scheduler.conflicts == [(first_task, second_task)]


def test_conflicts_exclude_tasks_omitted_by_available_minutes_limit() -> None:
    schedule_date = date(2026, 10, 19)
    selected_task = Task("Walk", datetime(2026, 10, 19, 8, 0), 30, "high", "once")
    omitted_task = Task("Medication", datetime(2026, 10, 19, 8, 20), 10, "low", "once")
    owner = Owner(
        "Jordan",
        [Pet("Mochi", "dog", [selected_task]), Pet("Miso", "cat", [omitted_task])],
    )
    scheduler = Scheduler(owner)

    schedule = scheduler.generate_schedule(
        schedule_date=schedule_date,
        available_minutes=30,
    )

    assert schedule == [selected_task]
    assert scheduler.conflicts == []
