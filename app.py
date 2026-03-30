import streamlit as st
from datetime import date
from pawpal_system import Task, Pet, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# --- Session State: single source of truth ---
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="")
    st.session_state.scheduler = Scheduler(st.session_state.owner)

owner = st.session_state.owner
scheduler = st.session_state.scheduler

st.title("🐾 PawPal+")

# --- Owner Setup ---
if not owner.name:
    st.subheader("Welcome! What's your name?")
    name_input = st.text_input("Owner name")
    if st.button("Set name") and name_input:
        owner.name = name_input
        st.rerun()
    st.stop()

# Show owner name with edit option
col_name, col_edit = st.columns([4, 1])
with col_name:
    st.caption(f"Logged in as **{owner.name}**")
with col_edit:
    if st.button("Edit name", type="secondary"):
        owner.name = ""
        st.rerun()

# --- Add a Pet ---
st.divider()
with st.expander("Add a Pet", expanded=not owner.pets):
    col1, col2 = st.columns(2)
    with col1:
        new_pet_name = st.text_input("Pet name", key="new_pet_name")
    with col2:
        new_pet_species = st.selectbox("Species", ["dog", "cat", "other"], key="new_pet_species")

    if st.button("Add pet"):
        if new_pet_name and not owner.get_pet(new_pet_name):
            owner.add_pet(Pet(name=new_pet_name, species=new_pet_species))
            st.rerun()
        elif not new_pet_name:
            st.warning("Please enter a pet name.")
        else:
            st.warning(f"You already have a pet named '{new_pet_name}'.")

if owner.pets:
    st.markdown(f"**{owner.name}'s pets:**")
    for pet in owner.pets:
        col_pet, col_remove = st.columns([4, 1])
        with col_pet:
            st.write(f"{pet.name} ({pet.species})")
        with col_remove:
            if st.button("Remove", key=f"remove_{pet.name}"):
                owner.remove_pet(pet.name)
                st.rerun()

# --- Add Tasks ---
if owner.pets:
    st.divider()
    st.subheader("Add a Task")

    col1, col2 = st.columns(2)
    with col1:
        task_pet = st.selectbox("For which pet?", [p.name for p in owner.pets])
        task_desc = st.text_input("Task description", value="Morning walk")
        task_time = st.text_input("Time (HH:MM)", value="08:00")
    with col2:
        task_duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        task_priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
        task_frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])

    if st.button("Add task"):
        pet = owner.get_pet(task_pet)
        if pet:
            conflict = pet.add_task(Task(
                description=task_desc,
                time=task_time,
                duration_minutes=int(task_duration),
                priority=task_priority,
                frequency=task_frequency,
            ))
            if conflict:
                st.error(conflict)
            else:
                st.rerun()

# --- Daily Schedule ---
st.divider()
st.subheader(f"Today's Schedule for {owner.name}")

if st.button("Generate schedule") or owner.get_all_tasks():
    schedule = scheduler.get_daily_schedule()

    if schedule:
        rows = []
        for t in schedule:
            rows.append({
                "Time": t.time,
                "Pet": t.pet_name,
                "Task": t.description,
                "Duration": f"{t.duration_minutes}min",
                "Priority": t.priority.upper(),
                "Freq": t.frequency,
            })
        st.table(rows)
    else:
        st.info("No tasks scheduled for today.")

    # Conflict warnings
    conflicts = scheduler.detect_conflicts()
    for warning in conflicts:
        st.warning(warning)
