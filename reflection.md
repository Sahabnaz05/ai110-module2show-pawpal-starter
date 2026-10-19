# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My initial design for PawPal+ includes four classes: Owner, Pet, Task, and Scheduler.

Owner: Stores the owner's name, manages multiple pets, and collects tasks from all pets.

Pet: Stores a pet's name and species, and manages that pet's care tasks.

Task: Stores a task's description, scheduled date and time, duration, priority, frequency, and completion status.

Scheduler: Retrieves tasks through Owner, then sorts and filters them, detects overlaps, and generates a schedule across multiple pets.

The main relationships are one Owner managing multiple Pets, each Pet managing its Tasks, and a Scheduler using an Owner to access all pets' tasks.

The app lets a user add pets and care tasks, mark tasks complete, and generate a schedule for a selected date and available time.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

After reviewing my initial class skeletons with AI, I decided to keep the original design because the four classes already had clear responsibilities and relationships. The review highlighted that Scheduler should retrieve tasks through Owner.get_all_tasks() to organize tasks across multiple pets. I implemented this relationship without changing the original class structure.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

My scheduler considers the selected schedule date, task completion status, task duration, available minutes, priority, and recurrence frequency. It supports once, daily, and weekly tasks. Completed tasks are left out. When there is a time limit, the scheduler considers high-priority tasks first and selects tasks that fit; it then displays the selected tasks in chronological order, using priority to break time ties. Owner preferences are not part of the current implementation.

When a daily or weekly task is completed in the app, the owning Pet marks it complete and creates the next occurrence one day or seven days later, respectively. If that matching next occurrence already exists, it is reused rather than duplicated. Completing a one-time task only marks it complete.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

When the available time is limited, the scheduler prioritizes high-priority tasks that fit rather than strictly choosing tasks in time order. This can leave a lower-priority task out even if it is earlier, but helps reserve limited care time for tasks marked most important. Tasks that do not fit are skipped rather than partially scheduled.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used AI to review my UML and class skeletons, implement the core class behavior and scheduling methods, connect the classes to the Streamlit interface, and help create focused tests and project documentation. The most helpful prompts described the required behavior and constraints clearly, such as keeping the four existing classes, using Owner to retrieve tasks across pets, and not adding features outside the current phase.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

One AI-generated implementation I reviewed needed a correction in the order of scheduling operations. The scheduler originally detected conflicts before filtering tasks by available time, which could report conflicts involving tasks that were not included in the final schedule. I asked AI to correct this so conflicts were detected after filtering. I verified the change using pytest and by testing overlapping tasks in the Streamlit app.
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?
I tested ten behaviors using pytest: marking tasks complete, adding tasks to pets, sorting by time and priority, excluding completed tasks, selecting tasks within an available-time budget, daily and weekly recurrence in schedules, detecting overlapping tasks across pets, excluding conflicts involving tasks left out by the time limit, and creating the next daily or weekly task occurrence when a recurring task is completed. The daily test checks that the next task is due tomorrow, and the weekly test checks that it is due seven days later; both also check that completing the same original task again does not add a duplicate. All ten tests passed. These tests were important because they helped verify that the scheduler and recurring completion behavior followed the project requirements.

I also tested the Streamlit interface manually by creating tasks for multiple pets, generating schedules with different available-time limits, and checking that overlapping tasks from different pets produced a conflict warning.
**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I am fairly confident that my scheduler works correctly for the main requirements because all ten pytest tests passed. I also tested the Streamlit interface manually and confirmed that it displayed overlapping tasks from different pets. If I had more time, I would test additional edge cases, such as zero available minutes, tasks that exactly fit the remaining time, and tasks that start exactly when another task ends.


---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I am most satisfied with connecting the four Python classes to the Streamlit interface. It was useful to see the information entered in the app turn into an actual daily schedule. I also liked seeing the conflict detection work when tasks from different pets overlapped.
**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

If I had another iteration, I would improve how tasks are scheduled when they overlap. Right now, the scheduler identifies conflicts but does not automatically resolve them. I would also improve the task entry form so users could choose a future date when creating a one-time task.
**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

One important thing I learned is that designing the classes before writing the full program made it easier to organize the code. I also learned that AI-generated code still needs to be reviewed and tested. Giving AI specific instructions and checking the results helped me keep the project aligned with the requirements.