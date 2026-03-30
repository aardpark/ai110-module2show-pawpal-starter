from pawpal_system import Task, Pet, Owner, Scheduler
from datetime import date

# --- Setup ---
owner = Owner(name="Jordan")

mochi = Pet(name="Mochi", species="dog")
luna = Pet(name="Luna", species="cat")
owner.add_pet(mochi)
owner.add_pet(luna)

# Add tasks (intentionally out of order to test sorting)
mochi.add_task(Task("Evening walk", "18:00", 30, "high", "daily"))
mochi.add_task(Task("Morning walk", "07:30", 20, "high", "daily"))
mochi.add_task(Task("Flea medication", "09:00", 5, "high", "weekly"))
luna.add_task(Task("Breakfast", "08:00", 10, "medium", "daily"))
luna.add_task(Task("Play time", "15:00", 20, "low"))
luna.add_task(Task("Vet appointment", "09:00", 60, "high"))

# Attempt a conflict: Luna already has something at 09:00
conflict = luna.add_task(Task("Grooming", "09:00", 30, "medium"))
if conflict:
    print(f"⚠ Blocked: {conflict}")

scheduler = Scheduler(owner)

# --- Today's Schedule (sorted) ---
print("=" * 50)
print(f"  Today's Schedule for {owner.name} ({date.today()})")
print("=" * 50)
for task in scheduler.get_daily_schedule():
    print(f"  {task.time}  [{task.priority.upper():>6}]  {task.pet_name:>5} - {task.description} ({task.duration_minutes}min)")

# --- Conflict Detection ---
conflicts = scheduler.detect_conflicts()
if conflicts:
    print()
    print("⚠ Conflicts detected:")
    for warning in conflicts:
        print(f"  {warning}")

# --- Filtering ---
print()
print("-- Mochi's tasks only --")
for task in scheduler.filter_tasks(pet_name="Mochi"):
    print(f"  {task.time}  {task.description}")

# --- Sort by Priority ---
print()
print("-- All tasks sorted by priority --")
for task in scheduler.sort_by_priority():
    print(f"  [{task.priority.upper():>6}]  {task.time}  {task.pet_name:>5} - {task.description}")

# --- Recurring Task Demo ---
print()
print("-- Completing Mochi's morning walk (daily) --")
morning_walk = mochi.get_tasks()[1]  # "Morning walk"
new_task = scheduler.mark_task_complete(morning_walk)
print(f"  Completed: {morning_walk.description} on {morning_walk.date}")
print(f"  Created:   {new_task.description} on {new_task.date}")

# --- Updated Schedule ---
print()
print("-- Mochi's tasks after completion --")
for task in scheduler.filter_tasks(pet_name="Mochi"):
    status = "✓" if task.completed else " "
    print(f"  [{status}] {task.time} {task.description} (date: {task.date})")
