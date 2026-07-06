# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
  - The system has 5 classes which allows the owner add their details and pets, add tasks and generate a daily plan based on taks and constraints. The classes are: Owner, Pet, Task, Scheduler, and DailyPlan. 

- What classes did you include, and what responsibilities did you assign to each?
  - **Owner**: stores their details, their available time and general preferences.
  - **Pet**: stores metatdata about the pet, such as name, type, and age.
  - **Task**: stores the task details, such as name, duration, recurrence, priority and notes.
  - **Scheduler**: takes the owner, pet, and tasks as input and generates a daily plan based on constraints and priorities.
  - **DailyPlan**: represents the final scheduled plan, including time slots, total minutes used, and reasoning.

**b. Design changes**

- Did your design change during implementation?
  - Yes
- If yes, describe at least one change and why you made it.
  - There a was slight mismatch between the UML and the system design. The initial UML showed the owner as directly connected to the pet and tasks while it was just responsible for storing and managing data. So I changed the UML to show that the Scheduler class is responsible for generating the daily plan based on the owner, pet, and tasks.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
  - The scheduler considers three constraints. First, the owner's available time — any task that would push the total over the owner's daily time budget is skipped entirely. Second, task priority — tasks are sorted from high to low so the most important ones are always scheduled first. Third, whether the owner is physically required for a task — tasks marked as background (like a pet eating from a bowl) do not consume the owner's time and can run at the same time as other tasks, while tasks that require the owner's presence are placed on a shared clock so no two of them overlap.

- How did you decide which constraints mattered most?
  - Time is treated as the hard ceiling because it is a physical limit, there is simply no way to do a task if the owner has no time left. Priority comes next because within that time budget, the goal is to make sure the most critical care happens first. Owner availability was added later after noticing that running a separate scheduler per pet caused two owner-required tasks to be assigned the same time slot, which is impossible in practice.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
  - The scheduler uses a priority-first, greedy approach. It goes through tasks in priority order and adds each one if it fits in the remaining time. This means a long high-priority task can use up most of the time budget, and a short low-priority task might still squeeze in at the end  but a medium-priority task of average length might get skipped entirely if it does not fit after the high-priority tasks have run.

- Why is that tradeoff reasonable for this scenario?
  - For pet care, ensuring that the most critical tasks always happen is more important than maximising the total number of tasks completed. A missed medication is a much bigger problem than a missed grooming session. So accepting that some medium tasks might get dropped in favour of guaranteeing high-priority ones is the right call for this domain.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
