from datetime import datetime

from pawpal_system import Pet, Task


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
