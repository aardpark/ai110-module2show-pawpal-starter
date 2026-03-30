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
        pass


@dataclass
class Pet:
    name: str
    species: str
    tasks: list = field(default_factory=list)

    def add_task(self, task: Task):
        """Add a task to this pet's task list."""
        pass

    def get_tasks(self) -> list:
        """Return all tasks for this pet."""
        pass


@dataclass
class Owner:
    name: str
    pets: list = field(default_factory=list)

    def add_pet(self, pet: Pet):
        """Add a pet to this owner."""
        pass

    def get_pet(self, name: str) -> Optional[Pet]:
        """Find a pet by name."""
        pass

    def get_all_tasks(self) -> list:
        """Return all tasks across all pets."""
        pass


class Scheduler:
    def __init__(self, owner: Owner):
        """Initialize scheduler with an owner."""
        pass

    def sort_by_time(self, tasks: list = None) -> list:
        """Sort tasks by their scheduled time (HH:MM)."""
        pass

    def filter_tasks(self, pet_name: str = None, completed: bool = None) -> list:
        """Filter tasks by pet name and/or completion status."""
        pass

    def detect_conflicts(self) -> list:
        """Detect tasks scheduled at the same time for the same pet."""
        pass

    def mark_task_complete(self, task: Task):
        """Mark a task complete; if recurring, create next occurrence."""
        pass

    def get_daily_schedule(self, target_date: date = None) -> list:
        """Get all tasks for a given date, sorted by time."""
        pass
