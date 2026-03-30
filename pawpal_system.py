from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Optional


@dataclass
class Task:
    description: str
    time: str  # "HH:MM" format
    duration_minutes: int
    priority: str  # "low", "medium", "high"
    frequency: str = "once"  # "once", "daily", "weekly"
    completed: bool = False
    pet_name: str = ""
    date: date = field(default_factory=date.today)

    def mark_complete(self):
        """Mark this task as completed."""
        self.completed = True


@dataclass
class Pet:
    name: str
    species: str
    tasks: list = field(default_factory=list)

    def add_task(self, task: Task) -> str | None:
        """Add a task to this pet's task list. Recurring tasks generate 6 months of occurrences."""
        for existing in self.tasks:
            if existing.time == task.time and existing.date == task.date and not existing.completed:
                return (f"Conflict: '{existing.description}' already scheduled "
                        f"at {task.time} on {task.date}")
        task.pet_name = self.name
        self.tasks.append(task)

        # Pre-generate recurring occurrences for 6 months
        if task.frequency == "daily":
            delta = timedelta(days=1)
        elif task.frequency == "weekly":
            delta = timedelta(weeks=1)
        else:
            return None

        current_date = task.date + delta
        end_date = task.date + timedelta(days=180)
        while current_date <= end_date:
            occurrence = Task(
                description=task.description,
                time=task.time,
                duration_minutes=task.duration_minutes,
                priority=task.priority,
                frequency=task.frequency,
                pet_name=self.name,
                date=current_date,
            )
            self.tasks.append(occurrence)
            current_date += delta

        return None

    def remove_task(self, task: Task):
        """Remove a task from this pet's task list."""
        if task in self.tasks:
            self.tasks.remove(task)

    def get_tasks(self) -> list:
        """Return all tasks for this pet."""
        return self.tasks


@dataclass
class Owner:
    name: str
    pets: list = field(default_factory=list)

    def add_pet(self, pet: Pet):
        """Add a pet to this owner."""
        self.pets.append(pet)

    def remove_pet(self, name: str) -> bool:
        """Remove a pet by name. Returns True if found and removed."""
        pet = self.get_pet(name)
        if pet:
            self.pets.remove(pet)
            return True
        return False

    def get_pet(self, name: str) -> Optional[Pet]:
        """Find a pet by name."""
        for pet in self.pets:
            if pet.name == name:
                return pet
        return None

    def get_all_tasks(self) -> list:
        """Return all tasks across all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


class Scheduler:
    def __init__(self, owner: Owner):
        """Initialize scheduler with an owner."""
        self.owner = owner

    def sort_by_time(self, tasks: list = None) -> list:
        """Sort tasks by their scheduled time (HH:MM)."""
        if tasks is None:
            tasks = self.owner.get_all_tasks()
        return sorted(tasks, key=lambda t: t.time)

    def sort_by_priority(self, tasks: list = None) -> list:
        """Sort tasks by priority (high first), then by time."""
        if tasks is None:
            tasks = self.owner.get_all_tasks()
        rank = {"high": 0, "medium": 1, "low": 2}
        return sorted(tasks, key=lambda t: (rank.get(t.priority, 3), t.time))

    def filter_tasks(self, pet_name: str = None, completed: bool = None) -> list:
        """Filter tasks by pet name and/or completion status."""
        tasks = self.owner.get_all_tasks()
        if pet_name is not None:
            tasks = [t for t in tasks if t.pet_name == pet_name]
        if completed is not None:
            tasks = [t for t in tasks if t.completed == completed]
        return tasks

    def detect_conflicts(self) -> list:
        """Detect tasks scheduled at the same time for the same pet."""
        warnings = []
        tasks = self.owner.get_all_tasks()
        seen = {}
        for task in tasks:
            key = (task.pet_name, task.time, task.date)
            if key in seen:
                warnings.append(
                    f"Conflict: '{task.description}' and '{seen[key].description}' "
                    f"for {task.pet_name} at {task.time} on {task.date}"
                )
            else:
                seen[key] = task
        return warnings

    def mark_task_complete(self, task: Task):
        """Mark a task complete."""
        task.mark_complete()

    def get_daily_schedule(self, target_date: date = None) -> list:
        """Get all tasks for a given date, sorted by time."""
        if target_date is None:
            target_date = date.today()
        tasks = [t for t in self.owner.get_all_tasks()
                 if t.date == target_date and not t.completed]
        return self.sort_by_time(tasks)
