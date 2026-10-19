from datetime import date, datetime, time

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")
st.caption("Keep track of your pets' care tasks and view their daily schedule.")

if "owner" not in st.session_state:
    st.session_state.owner = Owner("")
if "owner_name" not in st.session_state:
    st.session_state.owner_name = st.session_state.owner.name
if "schedule" not in st.session_state:
    st.session_state.schedule = None
if "schedule_conflicts" not in st.session_state:
    st.session_state.schedule_conflicts = []
if "schedule_for_date" not in st.session_state:
    st.session_state.schedule_for_date = None
if "schedule_for_minutes" not in st.session_state:
    st.session_state.schedule_for_minutes = None

owner: Owner = st.session_state.owner
owner.name = st.text_input("Owner name", key="owner_name").strip()

st.subheader("Pets")
with st.form("add_pet_form", clear_on_submit=True):
    pet_name = st.text_input("Pet name")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    add_pet_submitted = st.form_submit_button("Add pet")

if add_pet_submitted:
    if pet_name.strip():
        owner.add_pet(Pet(name=pet_name.strip(), species=species))
        st.session_state.schedule = None
    else:
        st.warning("Enter a pet name before adding the pet.")

if owner.pets:
    st.write("Your pets:")
    for pet in owner.pets:
        st.write(f"- {pet.name} ({pet.species})")
else:
    st.info("Add a pet to start tracking care tasks.")

st.subheader("Care tasks")
if owner.pets:
    with st.form("add_task_form", clear_on_submit=True):
        selected_pet_index = st.selectbox(
            "Add task to",
            range(len(owner.pets)),
            format_func=lambda index: (
                f"{owner.pets[index].name} ({owner.pets[index].species})"
            ),
        )
        description = st.text_input("Task description")
        task_time = st.time_input("Scheduled time", value=time(8, 0))
        duration = st.number_input(
            "Duration (minutes)", min_value=1, max_value=240, value=20
        )
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
        frequency = st.selectbox(
            "Frequency", ["once", "daily", "weekly"], index=1
        )
        add_task_submitted = st.form_submit_button("Add task")

    if add_task_submitted:
        if description.strip():
            selected_pet = owner.pets[selected_pet_index]
            selected_pet.add_task(
                Task(
                    description=description.strip(),
                    due_time=datetime.combine(date.today(), task_time),
                    duration=int(duration),
                    priority=priority,
                    frequency=frequency,
                )
            )
            st.session_state.schedule = None
        else:
            st.warning("Enter a task description before adding the task.")

all_tasks = owner.get_all_tasks()
if all_tasks:
    st.write("Current tasks:")
    pet_by_task_id = {
        id(task): pet
        for pet in owner.pets
        for task in pet.list_tasks()
    }
    st.table(
        [
            {
                "Pet": pet_by_task_id[id(task)].name,
                "Task": task.description,
                "Scheduled time": task.due_time.strftime("%Y-%m-%d %I:%M %p"),
                "Duration (minutes)": task.duration,
                "Priority": task.priority,
                "Frequency": task.frequency,
                "Completed": task.completed,
            }
            for task in all_tasks
        ]
    )
    incomplete_tasks = [
        (index, task)
        for index, task in enumerate(all_tasks)
        if not task.completed
    ]
    if incomplete_tasks:
        with st.form("complete_task_form"):
            selected_task_index = st.selectbox(
                "Mark task complete",
                [index for index, _ in incomplete_tasks],
                format_func=lambda index: (
                    f"{pet_by_task_id[id(all_tasks[index])].name}: "
                    f"{all_tasks[index].description}"
                ),
            )
            mark_complete_submitted = st.form_submit_button("Mark complete")

        if mark_complete_submitted:
            all_tasks[selected_task_index].mark_complete()
            st.session_state.schedule = None
            st.session_state.schedule_conflicts = []
            st.session_state.schedule_for_date = None
            st.session_state.schedule_for_minutes = None
    else:
        st.info("All tasks are marked complete.")
else:
    st.info("No care tasks yet. Add a task above.")

st.subheader("Daily schedule")
selected_schedule_date = st.date_input("Schedule date", value=date.today())
available_minutes = st.number_input(
    "Available time (minutes)", min_value=0, max_value=1440, value=120
)
if st.button("Generate schedule", disabled=not all_tasks):
    scheduler = Scheduler(owner)
    st.session_state.schedule = scheduler.generate_schedule(
        schedule_date=selected_schedule_date,
        available_minutes=int(available_minutes),
    )
    st.session_state.schedule_conflicts = scheduler.conflicts
    st.session_state.schedule_for_date = selected_schedule_date
    st.session_state.schedule_for_minutes = int(available_minutes)

if st.session_state.schedule is not None:
    if (
        st.session_state.schedule_for_date != selected_schedule_date
        or st.session_state.schedule_for_minutes != int(available_minutes)
    ):
        st.info("Generate the schedule to apply the selected date and available time.")
    elif st.session_state.schedule:
        st.write(f"Schedule for {owner.name or 'your pets'}:")
        for task in st.session_state.schedule:
            pet = pet_by_task_id[id(task)]
            st.write(
                f"- {task.due_time:%I:%M %p} — {task.description} "
                f"({pet.name}, {task.duration} min, {task.priority} priority)"
            )
        if st.session_state.schedule_conflicts:
            st.write("Overlapping tasks:")
            for first_task, second_task in st.session_state.schedule_conflicts:
                first_pet = pet_by_task_id[id(first_task)]
                second_pet = pet_by_task_id[id(second_task)]
                st.warning(
                    f"{first_task.description} ({first_pet.name}, "
                    f"{first_task.due_time:%I:%M %p}) overlaps with "
                    f"{second_task.description} ({second_pet.name}, "
                    f"{second_task.due_time:%I:%M %p})."
                )
        else:
            st.success("No overlapping tasks in this schedule.")
    else:
        st.info("No incomplete tasks fit the selected date and available time.")
