from pawpal_system import Task, Pet, Owner, Scheduler
from datetime import date, timedelta


def test_mark_complete():
    task = Task("Walk", "08:00", 20, "high")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_count():
    pet = Pet("Mochi", "dog")
    assert len(pet.get_tasks()) == 0
    pet.add_task(Task("Walk", "08:00", 20, "high"))
    assert len(pet.get_tasks()) == 1
    pet.add_task(Task("Feed", "12:00", 10, "medium"))
    assert len(pet.get_tasks()) == 2
