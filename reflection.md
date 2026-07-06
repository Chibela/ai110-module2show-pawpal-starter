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
  - There a was slight mismatch between the UML and the system design. 
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

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
