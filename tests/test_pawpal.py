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


def test_sort_by_time():
    owner = Owner("Test")
    pet = Pet("Buddy", "dog")
    owner.add_pet(pet)
    pet.add_task(Task("Evening walk", "18:00", 30, "high"))
    pet.add_task(Task("Breakfast", "07:00", 10, "medium"))
    pet.add_task(Task("Lunch med", "12:00", 5, "high"))

    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_by_time()
    times = [t.time for t in sorted_tasks]
    assert times == ["07:00", "12:00", "18:00"]


def test_sort_by_priority():
    owner = Owner("Test")
    pet = Pet("Buddy", "dog")
    owner.add_pet(pet)
    pet.add_task(Task("Play", "09:00", 20, "low"))
    pet.add_task(Task("Meds", "08:00", 5, "high"))
    pet.add_task(Task("Brush", "10:00", 15, "medium"))

    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_by_priority()
    priorities = [t.priority for t in sorted_tasks]
    assert priorities == ["high", "medium", "low"]


def test_daily_generates_6_months():
    pet = Pet("Buddy", "dog")
    today = date.today()
    pet.add_task(Task("Walk", "08:00", 20, "high", frequency="daily", date=today))

    end_date = today + timedelta(days=180)
    expected_count = (end_date - today).days + 1  # today + 180 days
    assert len(pet.get_tasks()) == expected_count

    # First task is today, last is ~6 months out
    dates = sorted(t.date for t in pet.get_tasks())
    assert dates[0] == today
    assert dates[-1] == end_date


def test_weekly_generates_6_months():
    pet = Pet("Buddy", "dog")
    today = date.today()
    pet.add_task(Task("Grooming", "10:00", 60, "medium", frequency="weekly", date=today))

    tasks = pet.get_tasks()
    assert len(tasks) > 25  # at least 26 weeks
    dates = sorted(t.date for t in tasks)
    assert dates[0] == today
    assert dates[1] == today + timedelta(weeks=1)


def test_once_does_not_generate_extra():
    pet = Pet("Buddy", "dog")
    pet.add_task(Task("Vet visit", "14:00", 60, "high", frequency="once"))
    assert len(pet.get_tasks()) == 1


def test_complete_daily_next_day_exists():
    owner = Owner("Test")
    pet = Pet("Buddy", "dog")
    owner.add_pet(pet)
    today = date.today()
    pet.add_task(Task("Walk", "08:00", 20, "high", frequency="daily", date=today))

    scheduler = Scheduler(owner)
    today_task = [t for t in pet.get_tasks() if t.date == today][0]
    scheduler.mark_task_complete(today_task)

    assert today_task.completed is True
    tomorrow_tasks = [t for t in pet.get_tasks() if t.date == today + timedelta(days=1)]
    assert len(tomorrow_tasks) == 1
    assert tomorrow_tasks[0].completed is False


def test_conflict_blocks_addition():
    pet = Pet("Buddy", "dog")
    assert pet.add_task(Task("Walk", "09:00", 30, "high")) is None
    conflict = pet.add_task(Task("Vet", "09:00", 60, "high"))
    assert conflict is not None
    assert "Walk" in conflict
    assert len(pet.get_tasks()) == 1


def test_overlap_blocks_addition():
    pet = Pet("Buddy", "dog")
    assert pet.add_task(Task("Walk", "09:00", 30, "high")) is None
    # 09:15 falls within 09:00-09:30
    conflict = pet.add_task(Task("Vet", "09:15", 60, "high"))
    assert conflict is not None
    assert "Walk" in conflict
    assert len(pet.get_tasks()) == 1


def test_no_overlap_adjacent_tasks():
    pet = Pet("Buddy", "dog")
    # 09:00-09:30 and 09:30-10:30 — adjacent, not overlapping
    assert pet.add_task(Task("Walk", "09:00", 30, "high")) is None
    assert pet.add_task(Task("Vet", "09:30", 60, "high")) is None
    assert len(pet.get_tasks()) == 2


def test_no_conflict_different_times():
    owner = Owner("Test")
    pet = Pet("Buddy", "dog")
    owner.add_pet(pet)
    pet.add_task(Task("Walk", "08:00", 30, "high"))
    pet.add_task(Task("Vet", "09:00", 60, "high"))

    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()
    assert len(conflicts) == 0


def test_filter_by_pet():
    owner = Owner("Test")
    dog = Pet("Buddy", "dog")
    cat = Pet("Whiskers", "cat")
    owner.add_pet(dog)
    owner.add_pet(cat)
    dog.add_task(Task("Walk", "08:00", 20, "high"))
    cat.add_task(Task("Feed", "08:00", 10, "medium"))

    scheduler = Scheduler(owner)
    buddy_tasks = scheduler.filter_tasks(pet_name="Buddy")
    assert len(buddy_tasks) == 1
    assert buddy_tasks[0].pet_name == "Buddy"


def test_filter_by_completion():
    owner = Owner("Test")
    pet = Pet("Buddy", "dog")
    owner.add_pet(pet)
    pet.add_task(Task("Walk", "08:00", 20, "high"))
    pet.add_task(Task("Feed", "12:00", 10, "medium"))
    pet.get_tasks()[0].mark_complete()

    scheduler = Scheduler(owner)
    incomplete = scheduler.filter_tasks(completed=False)
    assert len(incomplete) == 1
    assert incomplete[0].description == "Feed"


def test_pet_with_no_tasks():
    owner = Owner("Test")
    pet = Pet("Buddy", "dog")
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    assert scheduler.get_daily_schedule() == []
    assert scheduler.detect_conflicts() == []
    assert scheduler.sort_by_time() == []


def test_daily_schedule_excludes_completed():
    owner = Owner("Test")
    pet = Pet("Buddy", "dog")
    owner.add_pet(pet)
    pet.add_task(Task("Walk", "08:00", 20, "high", date=date.today()))
    pet.add_task(Task("Feed", "12:00", 10, "medium", date=date.today()))
    pet.get_tasks()[0].mark_complete()

    scheduler = Scheduler(owner)
    schedule = scheduler.get_daily_schedule()
    assert len(schedule) == 1
    assert schedule[0].description == "Feed"


def test_get_pet_not_found():
    owner = Owner("Test")
    owner.add_pet(Pet("Buddy", "dog"))
    assert owner.get_pet("NonExistent") is None


def test_add_task_stamps_pet_name():
    pet = Pet("Buddy", "dog")
    task = Task("Walk", "08:00", 20, "high")
    assert task.pet_name == ""
    pet.add_task(task)
    assert task.pet_name == "Buddy"


def test_filter_nonexistent_pet():
    owner = Owner("Test")
    owner.add_pet(Pet("Buddy", "dog"))
    scheduler = Scheduler(owner)
    assert scheduler.filter_tasks(pet_name="Ghost") == []


def test_owner_no_pets():
    owner = Owner("Test")
    scheduler = Scheduler(owner)
    assert scheduler.get_daily_schedule() == []
    assert scheduler.detect_conflicts() == []
    assert owner.get_all_tasks() == []


def test_remove_pet():
    owner = Owner("Test")
    owner.add_pet(Pet("Buddy", "dog"))
    owner.add_pet(Pet("Luna", "cat"))
    assert len(owner.pets) == 2
    assert owner.remove_pet("Buddy") is True
    assert len(owner.pets) == 1
    assert owner.get_pet("Buddy") is None


def test_remove_pet_not_found():
    owner = Owner("Test")
    owner.add_pet(Pet("Buddy", "dog"))
    assert owner.remove_pet("Ghost") is False
    assert len(owner.pets) == 1


def test_cross_pet_same_time_allowed():
    owner = Owner("Test")
    dog = Pet("Buddy", "dog")
    cat = Pet("Luna", "cat")
    owner.add_pet(dog)
    owner.add_pet(cat)
    assert dog.add_task(Task("Walk", "08:00", 20, "high")) is None
    assert cat.add_task(Task("Feed", "08:00", 10, "medium")) is None
    scheduler = Scheduler(owner)
    assert scheduler.detect_conflicts() == []


def test_conflict_allows_after_completed():
    pet = Pet("Buddy", "dog")
    pet.add_task(Task("Walk", "09:00", 30, "high"))
    pet.get_tasks()[0].mark_complete()
    # Same time should now be allowed since existing task is completed
    assert pet.add_task(Task("Vet", "09:00", 60, "high")) is None
    assert len(pet.get_tasks()) == 2
