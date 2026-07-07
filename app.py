import streamlit as st
from pawpal_system import (
    Owner,
    Pet,
    Task,
    MultiPetScheduler,
    compute_end_time,
    confirm_concurrent_group,
    find_time_conflicts,
)

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

# ---------------------------------------------------------------------------
# Helper — display formatting only, no business logic
# ---------------------------------------------------------------------------
def _to_12h(time_str: str) -> str:
    h, m = map(int, time_str.split(":"))
    period = "AM" if h < 12 else "PM"
    h12 = h % 12 or 12
    return f"{h12:02d}:{m:02d} {period}"


def _to_24h(hour12: int, minute: int, period: str) -> str:
    """Combine a 12-hour clock entry (hour/minute/AM-PM boxes) into 'HH:MM' 24h."""
    h = hour12 % 12
    if period == "PM":
        h += 12
    return f"{h:02d}:{minute:02d}"


def _from_24h(time_str: str) -> tuple[int, int, str]:
    """Split 'HH:MM' 24h into (hour12, minute, AM/PM) for pre-filling the boxes."""
    h, m = map(int, time_str.split(":"))
    period = "AM" if h < 12 else "PM"
    h12 = h % 12 or 12
    return h12, m, period


# ---------------------------------------------------------------------------
# Initialise session state once
# Streamlit re-runs the entire script on every button click or widget change.
# session_state is the only storage that survives across those re-runs.
# ---------------------------------------------------------------------------
if "owner" not in st.session_state:
    st.session_state.owner = None
if "pets" not in st.session_state:
    st.session_state.pets = []
if "plan" not in st.session_state:
    st.session_state.plan = None
if "editing_task" not in st.session_state:
    st.session_state.editing_task = None  # (pet_index, task_index) of the row being edited


# ---------------------------------------------------------------------------
# Section 1 — Owner info
# ---------------------------------------------------------------------------
st.subheader("Owner Info")

with st.form("owner_form"):
    owner_name   = st.text_input("Your name", value="Jordan")
    avail_mins   = st.number_input("Available time today (minutes)", min_value=10, max_value=480, value=120)
    preferences  = st.text_input("Any preferences? (optional)")
    if st.form_submit_button("Save Owner"):
        st.session_state.owner = Owner(
            name=owner_name,
            available_minutes=int(avail_mins),
            preferences=preferences,
        )

if st.session_state.owner:
    o = st.session_state.owner
    st.caption(f"Saved: **{o.name}** — {o.available_minutes} min available")


# ---------------------------------------------------------------------------
# Section 2 — Pets
# ---------------------------------------------------------------------------
st.divider()
st.subheader("Pets")

with st.form("add_pet_form"):
    pet_name = st.text_input("Pet name", value="Bella")
    species  = st.selectbox("Species", ["dog", "cat", "other"])
    # Always rendered (not conditional on species) — widgets inside a form don't
    # rerun the script on change, so `if species == "other"` here would still be
    # reflecting last run's selection.
    custom_species = st.text_input("If Other, please specify")
    age      = st.number_input("Age (years)", min_value=0, max_value=30, value=3)
    breed    = st.text_input("Breed (optional)")
    if st.form_submit_button("Add Pet"):
        final_species = custom_species.strip() if species == "other" and custom_species.strip() else species
        st.session_state.pets.append(
            Pet(name=pet_name, species=final_species, age=int(age), breed=breed)
        )

if st.session_state.pets:
    for i, pet in enumerate(st.session_state.pets):
        col1, col2 = st.columns([5, 1])
        with col1:
            st.write(f"**{pet.name}** ({pet.species}, age {pet.age}) — {len(pet.tasks)} task(s)")
        with col2:
            if st.button("Remove", key=f"remove_pet_{i}"):
                st.session_state.pets.pop(i)
                st.session_state.plan = None   # plan is stale without this pet
                st.rerun()                     # needed so the loop re-renders with correct indices
else:
    st.info("No pets yet. Add one above.")


# ---------------------------------------------------------------------------
# Section 3 — Tasks
# ---------------------------------------------------------------------------
st.divider()
st.subheader("Tasks")

if not st.session_state.pets:
    st.info("Add a pet first.")
else:
    pet_names = [p.name for p in st.session_state.pets]

    with st.form("add_task_form"):
        selected_pet_name = st.selectbox("Add task to", pet_names)
        col1, col2, col3 = st.columns(3)
        with col1:
            task_title = st.text_input("Task title", value="Morning walk")
        with col2:
            duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
        with col3:
            priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
        owner_required = st.checkbox("Requires owner's presence", value=True)

        has_anchor = st.checkbox("Anchor to a specific time (e.g. medication with breakfast)", value=True)
        # Checked by default — the boxes below are always visible, so defaulting to
        # anchored avoids silently discarding a time the owner just filled in.
        # Not `disabled=not has_anchor` — widgets inside a form don't rerun on change,
        # so the disabled state would reflect last run's checkbox value, not this one.
        st.caption("Preferred time (uncheck the box above for flexible timing instead)")
        h_col, m_col, ap_col = st.columns(3)
        with h_col:
            anchor_hour = st.number_input("Hour", min_value=1, max_value=12, value=8, step=1, format="%02d")
        with m_col:
            anchor_minute = st.number_input("Minute", min_value=0, max_value=59, value=0, step=1, format="%02d")
        with ap_col:
            anchor_period = st.radio("AM/PM", ["AM", "PM"], horizontal=True)

        if st.form_submit_button("Add Task"):
            target_pet = next(p for p in st.session_state.pets if p.name == selected_pet_name)
            target_pet.add_task(                      # calls Pet.add_task() from backend
                Task(
                    title=task_title,
                    duration_minutes=int(duration),
                    priority=priority,
                    owner_required=owner_required,
                    preferred_time=_to_24h(anchor_hour, anchor_minute, anchor_period) if has_anchor else None,
                )
            )
            st.session_state.plan = None   # plan is stale without this task

    # Display current tasks per pet, with inline edit/remove before scheduling
    for pi, pet in enumerate(st.session_state.pets):
        if not pet.tasks:
            continue
        st.markdown(f"**{pet.name}'s tasks:**")
        for ti, task in enumerate(pet.tasks):
            if st.session_state.editing_task == (pi, ti):
                with st.container(border=True):
                    e_title = st.text_input("Task title", value=task.title, key=f"edit_title_{pi}_{ti}")
                    e_col1, e_col2 = st.columns(2)
                    with e_col1:
                        e_duration = st.number_input(
                            "Duration (min)", min_value=1, max_value=240,
                            value=task.duration_minutes, key=f"edit_duration_{pi}_{ti}",
                        )
                    with e_col2:
                        e_priority = st.selectbox(
                            "Priority", ["low", "medium", "high"],
                            index=["low", "medium", "high"].index(task.priority),
                            key=f"edit_priority_{pi}_{ti}",
                        )
                    e_owner_required = st.checkbox(
                        "Requires owner's presence", value=task.owner_required,
                        key=f"edit_owner_required_{pi}_{ti}",
                    )
                    e_has_anchor = st.checkbox(
                        "Anchor to a specific time", value=task.preferred_time is not None,
                        key=f"edit_has_anchor_{pi}_{ti}",
                    )
                    if task.preferred_time:
                        default_hour, default_minute, default_period = _from_24h(task.preferred_time)
                    else:
                        default_hour, default_minute, default_period = 8, 0, "AM"
                    st.caption("Preferred time (used only if anchored, above)")
                    e_h_col, e_m_col, e_ap_col = st.columns(3)
                    with e_h_col:
                        e_hour = st.number_input(
                            "Hour", min_value=1, max_value=12, value=default_hour, step=1,
                            format="%02d", key=f"edit_hour_{pi}_{ti}",
                        )
                    with e_m_col:
                        e_minute = st.number_input(
                            "Minute", min_value=0, max_value=59, value=default_minute, step=1,
                            format="%02d", key=f"edit_minute_{pi}_{ti}",
                        )
                    with e_ap_col:
                        e_period = st.radio(
                            "AM/PM", ["AM", "PM"], index=["AM", "PM"].index(default_period),
                            horizontal=True, key=f"edit_period_{pi}_{ti}",
                        )
                    save_col, cancel_col = st.columns(2)
                    with save_col:
                        if st.button("Save", key=f"save_task_{pi}_{ti}"):
                            task.apply_edit(
                                title=e_title,
                                duration_minutes=int(e_duration),
                                priority=e_priority,
                                owner_required=e_owner_required,
                                preferred_time=_to_24h(e_hour, e_minute, e_period) if e_has_anchor else None,
                            )
                            st.session_state.editing_task = None
                            st.session_state.plan = None
                            st.rerun()
                    with cancel_col:
                        if st.button("Cancel", key=f"cancel_task_{pi}_{ti}"):
                            st.session_state.editing_task = None
                            st.rerun()
            else:
                if task.preferred_time:
                    end_time = compute_end_time(task.preferred_time, task.duration_minutes)
                    time_tag = f"  *({_to_12h(task.preferred_time)} – {_to_12h(end_time)})*"
                else:
                    time_tag = ""
                row_col, edit_col, remove_col = st.columns([6, 1, 1])
                with row_col:
                    st.write(f"  • {task.title} — {task.duration_minutes} min [{task.priority}]{'  *(bg)*' if not task.owner_required else ''}{time_tag}")
                with edit_col:
                    if st.button("Edit", key=f"edit_task_{pi}_{ti}"):
                        st.session_state.editing_task = (pi, ti)
                        st.rerun()
                with remove_col:
                    if st.button("Remove", key=f"remove_task_{pi}_{ti}"):
                        pet.tasks.pop(ti)
                        st.session_state.editing_task = None  # index may now be stale
                        st.session_state.plan = None
                        st.rerun()


# ---------------------------------------------------------------------------
# Section 4 — Generate schedule
# ---------------------------------------------------------------------------
st.divider()
st.subheader("Generate Schedule")

pet_tasks = [(pet, pet.tasks) for pet in st.session_state.pets if pet.tasks]
has_tasks = bool(pet_tasks)
pending_conflicts = find_time_conflicts(pet_tasks) if has_tasks else []

if pending_conflicts:
    st.warning("Some tasks share the same preferred time. Resolve these before generating a schedule:")
    for group in pending_conflicts:
        time_str = group[0][1].preferred_time
        # A task joining an already-confirmed group (e.g. it silently inherited a
        # time it wasn't meant to share) needs different, more pointed wording than
        # a brand-new pairing — otherwise it's easy to reflexively click "Yes" and
        # sweep an unintended task into an existing simultaneous block.
        confirmed = [(pet, task) for pet, task in group if task.concurrent_group == time_str]
        new_members = [(pet, task) for pet, task in group if task.concurrent_group != time_str]
        new_names = ", ".join(f"{pet.name}'s “{task.title}”" for pet, task in new_members)

        if confirmed:
            confirmed_names = ", ".join(f"{pet.name}'s “{task.title}”" for pet, task in confirmed)
            st.write(
                f"**{_to_12h(time_str)}** — {new_names} also wants this time, "
                f"same as your already-confirmed {confirmed_names}."
            )
            yes_label = f"Yes, include {new_names} too"
            no_caption = f"If No: use Edit above to change {new_names}'s preferred time."
        else:
            all_names = ", ".join(f"{pet.name}'s “{task.title}”" for pet, task in group)
            st.write(f"**{_to_12h(time_str)}** — {all_names}")
            yes_label = f"Yes, all {len(group)} at the same time" if len(group) > 2 else "Yes, same time"
            no_caption = "If No: use Edit above to change one of these tasks' preferred time."

        yes_col, no_col = st.columns(2)
        with yes_col:
            if st.button(yes_label, key=f"conflict_yes_{time_str}"):
                confirm_concurrent_group(group)
                st.session_state.plan = None
                st.rerun()
        with no_col:
            if st.button("No, different times", key=f"conflict_no_{time_str}"):
                st.rerun()
        st.caption(no_caption)

can_generate = st.session_state.owner is not None and has_tasks and not pending_conflicts

if not can_generate and not pending_conflicts:
    st.caption("Save an owner and add at least one pet with a task to continue.")

if st.button("Generate schedule", disabled=not can_generate):
    # Clear stale checkbox state from any previous plan
    for key in list(st.session_state.keys()):
        if key.startswith("done_"):
            del st.session_state[key]

    scheduler = MultiPetScheduler(owner=st.session_state.owner, pet_tasks=pet_tasks)
    st.session_state.plan = scheduler.generate_plan()


# ---------------------------------------------------------------------------
# Section 5 — Display plan with completion checkboxes
# ---------------------------------------------------------------------------
if st.session_state.plan:
    plan  = st.session_state.plan
    owner = st.session_state.owner

    st.markdown(f"### Daily Plan — {owner.name}")

    if not plan.scheduled_slots:
        st.warning("No tasks fit within the available time.")
    else:
        slots = sorted(plan.scheduled_slots, key=lambda s: (s[0], s[3]))  # time, bg last

        for i, (time, pet, task, is_bg) in enumerate(slots):
            col1, col2 = st.columns([1, 6])
            with col1:
                done = st.checkbox("", value=task.completed, key=f"done_{i}")
                if done:
                    task.mark_complete()        # stamps last_completed_date for is_due()
                else:
                    task.completed = False
            with col2:
                bg_tag = " *(bg)*" if is_bg else ""
                line = f"**{_to_12h(time)}** — [{pet.name}] {task.title}{bg_tag} ({task.duration_minutes} min)"
                st.markdown(f"~~{line}~~" if task.completed else line)

        completed_count = sum(1 for _, _, t, _ in slots if t.completed)
        st.caption(f"Progress: {completed_count}/{len(slots)} tasks done  |  Owner time: {plan.total_owner_minutes} min")

        if any(s[3] for s in slots):
            st.caption("*(bg) = runs in background, no owner needed*")

        if plan.unscheduled:
            st.warning(
                "Not scheduled today (ran out of owner time): "
                + ", ".join(f"{task.title} ({pet.name})" for pet, task in plan.unscheduled)
            )

        if plan.missed_anchors:
            st.info(
                "Missed preferred time: "
                + ", ".join(
                    f"{task.title} ({pet.name}) wanted {_to_12h(task.preferred_time)}"
                    for pet, task in plan.missed_anchors
                )
            )

        with st.expander("Why was this plan chosen?"):
            for _, pet, task, is_bg in slots:
                bg_note = " — no owner needed" if is_bg else ""
                st.write(f"• **{task.title}** [{pet.name}] — {task.priority} priority{bg_note}")
