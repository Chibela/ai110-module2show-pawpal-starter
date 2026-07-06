from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# Data classes — pure data holders, no scheduling logic
# ---------------------------------------------------------------------------

@dataclass
class Pet:
    name: str
    species: str          # "dog", "cat", "other"
    age: int
    breed: str = ""
    special_needs: str = ""


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str         # "low", "medium", "high"
    recurrence: str = "daily"   # "daily", "weekly", "once"
    notes: str = ""

    def is_high_priority(self) -> bool:
        pass


@dataclass
class Owner:
    name: str
    available_minutes: int
    preferences: str = ""

    def get_available_minutes(self) -> int:
        pass


# ---------------------------------------------------------------------------
# Scheduler — core logic engine
# ---------------------------------------------------------------------------

class Scheduler:
    def __init__(self, owner: Owner, pet: Pet, tasks: list[Task]) -> None:
        self.owner = owner
        self.pet = pet
        self.tasks = tasks

    def sort_tasks(self) -> list[Task]:
        """Return tasks ordered by priority (high → medium → low)."""
        pass

    def filter_by_time(self, available_minutes: int) -> list[Task]:
        """Return only tasks that fit within the available time budget."""
        pass

    def generate_plan(self) -> "DailyPlan":
        """Sort, filter, assign time slots, and return a DailyPlan."""
        pass


# ---------------------------------------------------------------------------
# DailyPlan — the output produced by Scheduler
# ---------------------------------------------------------------------------

class DailyPlan:
    def __init__(self) -> None:
        self.scheduled_slots: list[tuple[str, Task]] = []  # (start_time, task)
        self.total_minutes_used: int = 0
        self.reasoning: list[str] = []

    def add_slot(self, time: str, task: Task) -> None:
        """Add a (time, task) pair and update total_minutes_used."""
        pass

    def display(self) -> str:
        """Return a formatted string of the plan for the Streamlit UI."""
        pass

    def get_summary(self) -> str:
        """Return a one-paragraph plain-English explanation of the plan."""
        pass
