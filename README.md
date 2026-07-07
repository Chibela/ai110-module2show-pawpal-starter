# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

```text
=========================================================
                PAWPAL+ TODAY'S SCHEDULE
=========================================================

  Owner: John Smith

  TIME         PET       TASK                        DUR
  -------------------------------------------------------
  08:00 AM     Bella     Feed breakfast              10 min
  08:00 AM     Max       Morning feeding [bg]        10 min
  08:10 AM     Bella     Give medication             5 min
  08:15 AM     Max       Walk around the park        30 min
  08:45 AM     Max       Grooming session            15 min

  [bg] = runs in background, no owner needed

=========================================================
  Total Pets:  2
  Total Tasks: 5
  Owner time:  60 min
=========================================================
```

## 🧪 Testing PawPal+

Run the test suite with:

```bash
python -m pytest
```

The 27 tests in `tests/test_pawpal.py` cover three layers of the system:

- **Task behavior** — a task starts incomplete and can be marked complete, invalid priorities raise a `ValueError`, and `daily`/`weekly`/`once` recurrence correctly decide whether a task is due again after completion.
- **Time-math helpers** — converting minutes to `HH:MM` and computing a task's end time, including wrapping past midnight.
- **Scheduling logic** — the single-pet `Scheduler` (priority ordering, dropping tasks that don't fit the time budget) and the multi-pet `MultiPetScheduler` (detecting same-time conflicts across pets, confirming and scheduling concurrent groups as one atomic unit, advancing the clock by the group's longest task instead of the sum, not double-counting owner minutes, and correctly ordering anchored vs. flexible tasks — including when a group partially falls apart or a clock has already passed a preferred time).

Terminal output from a successful run:

```
============================= test session starts =============================
platform win32 -- Python 3.13.13, pytest-9.1.1, pluggy-1.6.0 -- C:\Users\chibe\Desktop\CodePath\ai110-module2show-pawpal-starter\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\chibe\Desktop\CodePath\ai110-module2show-pawpal-starter
plugins: anyio-4.14.0
collecting ... collected 27 items

tests/test_pawpal.py::test_task_starts_incomplete_and_marks_complete PASSED [  3%]
tests/test_pawpal.py::test_add_task_increases_pet_task_count PASSED      [  7%]
tests/test_pawpal.py::test_invalid_priority_raises PASSED                [ 11%]
tests/test_pawpal.py::test_daily_task_is_due_again_the_next_day PASSED   [ 14%]
tests/test_pawpal.py::test_weekly_task_is_not_due_until_a_week_passes PASSED [ 18%]
tests/test_pawpal.py::test_once_task_is_never_due_again_after_completion PASSED [ 22%]
tests/test_pawpal.py::test_minutes_to_time_wraps_past_midnight PASSED    [ 25%]
tests/test_pawpal.py::test_compute_end_time PASSED                       [ 29%]
tests/test_pawpal.py::test_compute_end_time_wraps_past_midnight PASSED   [ 33%]
tests/test_pawpal.py::test_apply_edit_clears_concurrent_group_when_time_changes PASSED [ 37%]
tests/test_pawpal.py::test_apply_edit_clears_concurrent_group_when_owner_required_becomes_false PASSED [ 40%]
tests/test_pawpal.py::test_apply_edit_preserves_concurrent_group_when_unrelated_field_changes PASSED [ 44%]
tests/test_pawpal.py::test_apply_edit_invalid_priority_raises PASSED     [ 48%]
tests/test_pawpal.py::test_find_time_conflicts_detects_two_tasks_same_preferred_time PASSED [ 51%]
tests/test_pawpal.py::test_find_time_conflicts_ignores_confirmed_group PASSED [ 55%]
tests/test_pawpal.py::test_find_time_conflicts_ignores_background_tasks PASSED [ 59%]
tests/test_pawpal.py::test_find_time_conflicts_ignores_not_due_tasks PASSED [ 62%]
tests/test_pawpal.py::test_find_time_conflicts_flags_growing_group PASSED [ 66%]
tests/test_pawpal.py::test_confirm_concurrent_group_sets_group_id_on_all_members PASSED [ 70%]
tests/test_pawpal.py::test_concurrent_group_schedules_at_identical_start_time PASSED [ 74%]
tests/test_pawpal.py::test_concurrent_group_advances_clock_by_max_duration_not_sum PASSED [ 77%]
tests/test_pawpal.py::test_concurrent_group_owner_minutes_not_double_counted PASSED [ 81%]
tests/test_pawpal.py::test_group_with_one_member_present_falls_back_to_solo_anchor_behavior PASSED [ 85%]
tests/test_pawpal.py::test_group_unscheduled_atomically_when_max_duration_does_not_fit PASSED [ 88%]
tests/test_pawpal.py::test_missed_anchor_recorded_for_whole_group_when_clock_already_passed PASSED [ 92%]
tests/test_pawpal.py::test_anchored_group_not_preempted_by_shorter_unanchored_same_priority_task PASSED [ 96%]
tests/test_pawpal.py::test_two_differently_anchored_units_process_in_chronological_anchor_order PASSED [100%]

============================= 27 passed in 0.07s ==============================
```

**Confidence Level: ★★★★☆ (4/5)**

All 27 tests pass, and the trickiest logic — concurrent-group scheduling across multiple pets — has dedicated coverage for its edge cases (partial groups, atomic drop when a group doesn't fit, missed anchors, anchor-vs-priority ordering). It's not a 5 because these tests only exercise `pawpal_system.py` directly; there's no automated coverage of `app.py`'s Streamlit UI, so UI-level regressions wouldn't be caught by `python -m pytest` alone.

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_tasks`, `MultiPetScheduler.generate_plan` (`units.sort`) | Sorted high → low priority; within a tier, anchored tasks (a fixed preferred time) always come before flexible ones, earliest anchor first, then shortest duration first. |
| Filtering | `Scheduler.filter_by_time` | Walks the sorted task list and keeps adding tasks while they still fit in the owner's remaining `available_minutes`; anything that would push the total over the budget is dropped into `unscheduled` instead of partially scheduled. |
| Conflict handling | `find_time_conflicts`, `confirm_concurrent_group`, `MultiPetScheduler.generate_plan` | Detects when two or more pets have owner-required tasks anchored to the same clock time and surfaces them in the UI so the owner can confirm they really happen simultaneously (e.g. feeding two pets at once). Once confirmed, the group is scheduled as a single unit that starts together and advances the clock by its *longest* task, not the sum — so owner time isn't double-charged. |
| Recurring tasks | `Task.is_due`, `Task.mark_complete` | Each task tracks `recurrence` (`daily`, `weekly`, `once`) and `last_completed_date`. `is_due()` re-derives whether it needs doing today from those two fields, so daily tasks reset every day, weekly tasks reset after 7 days, and one-off tasks never reappear once completed. |

## 📸 Demo Walkthrough

1. **Save owner info** — enter your name and how many minutes you have available today (10–480 min), plus any optional preferences, and click "Save Owner."
2. **Add pets** — give each pet a name, species, age, and optional breed. Every pet you add shows up in a list with a task count and a "Remove" button.
3. **Add tasks per pet** — pick a pet, then add a task with a title, duration, and priority (low/medium/high). Optionally mark it as not requiring the owner's presence (e.g. a pet eating on its own) or anchor it to a specific time of day (e.g. medication at 8:00 AM). Existing tasks can be edited or removed inline.
4. **Resolve time conflicts** — if two pets end up with tasks anchored to the same time, PawPal+ flags it before you can generate a schedule and asks you to confirm whether they really happen at once (e.g. feeding two pets together) or should be retimed.
5. **Generate the schedule** — once an owner and at least one task exist and there are no unresolved conflicts, click "Generate schedule" to produce a daily plan ordered by priority and anchor time, respecting your available minutes.
6. **Review and check off tasks** — the plan lists each task's scheduled time, pet, and duration (background tasks are labeled `(bg)`), lets you check tasks off as completed, and shows a progress count plus any tasks that didn't fit or missed their preferred time. Expand "Why was this plan chosen?" to see the reasoning behind the ordering.

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
