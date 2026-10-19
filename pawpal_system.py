from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Task:
    description: str
    due_time: datetime
    duration: int
    priority: str
    frequency: str
    completed: bool

    def mark_complete(self) -> None:
        pass


@dataclass
class Pet:
    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass

    def list_tasks(self) -> list[Task]:
        pass


class Owner:
    name: str
    pets: list[Pet]

    def __init__(self, name: str, pets: Optional[list[Pet]] = None) -> None:
        self.name = name
        self.pets = pets if pets is not None else []

    def add_pet(self, pet: Pet) -> None:
        pass

    def get_all_tasks(self) -> list[Task]:
        pass


class Scheduler:
    owner: Owner

    def __init__(self, owner: Owner) -> None:
        self.owner = owner

    def sort_by_time(self) -> None:
        pass

    def filter_tasks(self) -> None:
        pass

    def detect_conflicts(self) -> None:
        pass

    def generate_schedule(self) -> None:
        pass
