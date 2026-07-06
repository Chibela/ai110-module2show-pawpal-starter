from pawpal_system import Pet, Task


def test_task_starts_incomplete_and_marks_complete():
    """A new task should be incomplete; mark_complete() should flip it to done."""
    task = Task(title="Morning walk", duration_minutes=30, priority="high")

    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count():
    """Adding a task to a pet should increase its task list by exactly one."""
    pet = Pet(name="Bella", species="dog", age=4)
    initial_count = len(pet.tasks)

    pet.add_task(Task(title="Feed breakfast", duration_minutes=10, priority="high"))

    assert len(pet.tasks) == initial_count + 1
