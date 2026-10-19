from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import Optional


_PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


@dataclass
class Task:
    description: str
    due_time: datetime
    duration: int
    priority: str
    frequency: str
    completed: bool = False

    def mark_complete(self) -> None:
        self.completed = True


@dataclass
class Pet:
    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def list_tasks(self) -> list[Task]:
        return self.tasks

    def complete_task(self, task: Task) -> Optional[Task]:
        if not any(existing_task is task for existing_task in self.tasks):
            raise ValueError("Task does not belong to this pet.")

        if task.frequency == "daily":
            next_due_time = task.due_time + timedelta(days=1)
        elif task.frequency == "weekly":
            next_due_time = task.due_time + timedelta(days=7)
        elif task.frequency == "once":
            task.mark_complete()
            return None
        else:
            raise ValueError(f"Unsupported task frequency: {task.frequency}")

        task.mark_complete()
        for existing_task in self.tasks:
            if (
                existing_task.description == task.description
                and existing_task.due_time == next_due_time
                and existing_task.duration == task.duration
                and existing_task.priority == task.priority
                and existing_task.frequency == task.frequency
            ):
                return existing_task

        next_task = Task(
            description=task.description,
            due_time=next_due_time,
            duration=task.duration,
            priority=task.priority,
            frequency=task.frequency,
        )
        self.add_task(next_task)
        return next_task


class Owner:
    name: str
    pets: list[Pet]

    def __init__(self, name: str, pets: Optional[list[Pet]] = None) -> None:
        self.name = name
        self.pets = pets if pets is not None else []

    def add_pet(self, pet: Pet) -> None:
        self.pets.append(pet)

    def get_all_tasks(self) -> list[Task]:
        return [task for pet in self.pets for task in pet.list_tasks()]


class Scheduler:
    owner: Owner

    def __init__(self, owner: Owner) -> None:
        self.owner = owner
        self.conflicts: list[tuple[Task, Task]] = []

    def sort_by_time(
        self,
        tasks: Optional[list[Task]] = None,
        schedule_date: Optional[date] = None,
    ) -> list[Task]:
        tasks_to_sort = self.owner.get_all_tasks() if tasks is None else tasks
        return sorted(
            tasks_to_sort,
            key=lambda task: (
                datetime.combine(schedule_date, task.due_time.time())
                if schedule_date is not None
                else task.due_time,
                _PRIORITY_ORDER.get(task.priority.lower(), len(_PRIORITY_ORDER)),
            ),
        )

    def filter_tasks(
        self,
        available_minutes: Optional[int] = None,
        tasks: Optional[list[Task]] = None,
    ) -> list[Task]:
        tasks_to_filter = self.owner.get_all_tasks() if tasks is None else tasks
        candidates = sorted(
            (task for task in tasks_to_filter if not task.completed),
            key=lambda task: (
                _PRIORITY_ORDER.get(task.priority.lower(), len(_PRIORITY_ORDER)),
                task.due_time.time(),
            ),
        )

        if available_minutes is None:
            return candidates

        selected = []
        remaining_minutes = max(0, available_minutes)
        for task in candidates:
            if task.duration <= remaining_minutes:
                selected.append(task)
                remaining_minutes -= task.duration
        return selected

    def detect_conflicts(
        self,
        tasks: Optional[list[Task]] = None,
        schedule_date: Optional[date] = None,
    ) -> list[tuple[Task, Task]]:
        target_date = schedule_date or date.today()
        tasks_to_check = self.owner.get_all_tasks() if tasks is None else tasks
        scheduled_tasks = [
            task
            for task in tasks_to_check
            if not task.completed and self._occurs_on(task, target_date)
        ]

        conflicts = []
        for index, first_task in enumerate(scheduled_tasks):
            first_start = datetime.combine(target_date, first_task.due_time.time())
            first_end = first_start + timedelta(minutes=first_task.duration)
            for second_task in scheduled_tasks[index + 1 :]:
                second_start = datetime.combine(target_date, second_task.due_time.time())
                second_end = second_start + timedelta(minutes=second_task.duration)
                if first_start < second_end and second_start < first_end:
                    conflicts.append((first_task, second_task))
        return conflicts

    def generate_schedule(
        self,
        schedule_date: Optional[date] = None,
        available_minutes: Optional[int] = None,
    ) -> list[Task]:
        target_date = schedule_date or date.today()
        recurring_tasks = [
            task
            for task in self.owner.get_all_tasks()
            if self._occurs_on(task, target_date)
        ]
        selected_tasks = self.filter_tasks(
            available_minutes=available_minutes,
            tasks=recurring_tasks,
        )
        self.conflicts = self.detect_conflicts(
            tasks=selected_tasks,
            schedule_date=target_date,
        )
        return self.sort_by_time(selected_tasks, schedule_date=target_date)

    @staticmethod
    def _occurs_on(task: Task, schedule_date: date) -> bool:
        task_date = task.due_time.date()
        if task.frequency == "once":
            return task_date == schedule_date
        if task.frequency == "daily":
            return schedule_date >= task_date
        if task.frequency == "weekly":
            return schedule_date >= task_date and schedule_date.weekday() == task_date.weekday()
        raise ValueError(f"Unsupported task frequency: {task.frequency}")
