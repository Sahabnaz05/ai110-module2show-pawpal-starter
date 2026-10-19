from datetime import datetime

from pawpal_system import Owner, Pet, Scheduler, Task


owner = Owner("Jordan")
mochi = Pet("Mochi", "dog")
miso = Pet("Miso", "cat")
owner.add_pet(mochi)
owner.add_pet(miso)

today = datetime.now()
mochi.add_task(
    Task(
        "Morning walk",
        today.replace(hour=8, minute=0, second=0, microsecond=0),
        30,
        "high",
        "daily",
    )
)
miso.add_task(
    Task(
        "Breakfast",
        today.replace(hour=8, minute=30, second=0, microsecond=0),
        10,
        "high",
        "daily",
    )
)
mochi.add_task(
    Task(
        "Afternoon playtime",
        today.replace(hour=16, minute=0, second=0, microsecond=0),
        20,
        "medium",
        "daily",
    )
)

scheduler = Scheduler(owner)
tasks = sorted(scheduler.generate_schedule(), key=lambda task: task.due_time)

print("Today's Schedule")
for task in tasks:
    print(f"{task.due_time:%I:%M %p} — {task.description}")
