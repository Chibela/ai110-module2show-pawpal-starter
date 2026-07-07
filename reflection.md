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
  - I used AI to help brainstorm ideas for the system design, generate UML diagrams, and provide suggestions for implementing the scheduling logic. It also helped with debugging by suggesting potential fixes for errors in the code.
- What kinds of prompts or questions were most helpful?
  - For the prompts, I was specific with the task I wanted help with, such as "Generate a UML diagram for a pet care scheduling system" or "Suggest an algorithm for scheduling tasks based on priority and time constraints." I also asked for explanations of concepts I was unsure about, like "Explain how a greedy algorithm works in scheduling." I would also ask other suggestions on top of mine so that I could pick the best one.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
  - There were a number of moments where I had to reject its suggestions or implementations. One notable example is task addition specifically on the time input. It suggested that the app should have a dropdown with all the possible times in a day incremented by 1 minute. This would be a very long list and not user-friendly, so I rejected that idea and instead implemented a time picker that allows the user to select any time in a more intuitive way.
- How did you evaluate or verify what the AI suggested?
  - I evaluated the AI's suggestions by considering the user experience and practicality of the implementation. I also cross-referenced with best practices in UI/UX design.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
   - I tested these behaviours (in `tests/test_pawpal.py`) for three areas: Task behavior (completion, priority validation, recurrence), time-math helpers (minute-to-HH:MM and end-time calculations, including midnight wrap), and scheduling logic for both `Scheduler` and `MultiPetScheduler` (priority ordering, time-budget enforcement, concurrent-group scheduling without double-counting owner minutes, and anchor/missed-anchor handling).
- Why were these tests important?
  - These are the places where a small logic mistake would silently produce a wrong plan rather than a crash — for example, double-counting owner minutes for a concurrent group would make the owner look busier than they actually are, and getting the anchor-vs-priority ordering wrong could bump a real time commitment (like medication at a specific time) later in the day. Since these bugs don't throw errors, they're the kind I'd only catch by writing explicit tests that check the resulting plan's contents, not just that the code runs.

**b. Confidence**

- How confident are you that your scheduler works correctly?
  - I'm fairly confident in the core logic — the concurrent-group scheduling in particular went through several rounds of edge-case tests (a group where one sibling task got edited or removed and is now a lone leftover, a group that doesn't fit and must be dropped atomically instead of partially scheduling it, two differently-anchored tasks at the same priority processing in chronological order rather than shortest-first). I'm less confident about the parts that aren't covered by these tests, mainly `app.py`, since the test suite only exercises `pawpal_system.py` directly and I haven't automated any UI-level checks.
  - What edge cases would you test next if you had more time?
  - A few I'd add: three or more pets with overlapping anchors that span midnight at the same time; an owner with 0 available minutes; a tie where two units have identical priority, anchor time, and duration; editing a task's duration after it's already part of a confirmed concurrent group (does the group's "max duration" recompute correctly?); ensuring the scheduler never adds more tasks than the owner's available time allows; and end-to-end tests that drive `app.py` itself rather than only the underlying `pawpal_system.py` functions.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
  - I was satisfied with the UML design and the scheduling logic. The UML design was clear and helped guide the implementation, while the scheduling logic effectively prioritized tasks based on constraints and priorities.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
  - If I had another iteration, I would improve the user interface to make it more intuitive and visually appealing. I would also consider adding more features, such as notifications for upcoming tasks or the ability to track task completion over time.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
  - One important takeaway is that while AI can be a powerful tool for brainstorming and generating ideas, it is crucial to apply human judgment and consider the practical implications of its suggestions. The combination of AI assistance and human oversight can lead to more effective and user-friendly solutions.
