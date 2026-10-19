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
else:
    st.info("No care tasks yet. Add a task above.")

st.subheader("Today's schedule")
if st.button("Generate schedule", disabled=not all_tasks):
    st.session_state.schedule = Scheduler(owner).generate_schedule()

if st.session_state.schedule is not None:
    if st.session_state.schedule:
        st.write(f"Schedule for {owner.name or 'your pets'}:")
        for task in st.session_state.schedule:
            pet = pet_by_task_id[id(task)]
            st.write(
                f"- {task.due_time:%I:%M %p} — {task.description} "
                f"({pet.name}, {task.duration} min, {task.priority} priority)"
            )
    else:
        st.info("There are no tasks to schedule.")
