import streamlit as st
import pandas as pd
from datetime import datetime
from tasks import load_tasks, save_tasks, filter_tasks_by_priority, filter_tasks_by_category
import subprocess

def main():
    st.title("To-Do Application")
    
    # Load existing tasks
    tasks = load_tasks()
    
    # Sidebar for adding new tasks
    st.sidebar.header("Add New Task")
    
    # Task creation form
    with st.sidebar.form("new_task_form"):
        task_title = st.text_input("Task Title")
        task_description = st.text_area("Description")
        task_priority = st.selectbox("Priority", ["Low", "Medium", "High"])
        task_category = st.selectbox("Category", ["Work", "Personal", "School", "Other"])
        task_due_date = st.date_input("Due Date")
        submit_button = st.form_submit_button("Add Task")
        
        if submit_button and task_title:
            new_task = {
                "id": len(tasks) + 1,
                "title": task_title,
                "description": task_description,
                "priority": task_priority,
                "category": task_category,
                "due_date": task_due_date.strftime("%Y-%m-%d"),
                "completed": False,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            tasks.append(new_task)
            save_tasks(tasks)
            st.sidebar.success("Task added successfully!")
    
    # Main area to display tasks
    st.header("Your Tasks")
    
    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        filter_category = st.selectbox("Filter by Category", ["All"] + list(set([task.get("category", "Unknown") for task in tasks])))
    with col2:
        filter_priority = st.selectbox("Filter by Priority", ["All", "High", "Medium", "Low"])
    
    show_completed = st.checkbox("Show Completed Tasks")
    
    # Apply filters
    filtered_tasks = tasks.copy()
    if filter_category != "All":
        filtered_tasks = filter_tasks_by_category(filtered_tasks, filter_category)
    if filter_priority != "All":
        filtered_tasks = filter_tasks_by_priority(filtered_tasks, filter_priority)
    if not show_completed:
        filtered_tasks = [task for task in filtered_tasks if not task["completed"]]
    
    # Display tasks
    for task in filtered_tasks:
        col1, col2 = st.columns([4, 1])
        with col1:
            if task["completed"]:
                st.markdown(f"~~**{task['title']}**~~")
            else:
                st.markdown(f"**{task['title']}**")
            st.write(task.get("description", ""))
            st.caption(
                f"Due: {task.get('due_date', 'Unknown')} | "
                f"Priority: {task.get('priority', 'Unknown')} | "
                f"Category: {task.get('category', 'Unknown')}"
            )
        with col2:
            if st.button("Complete" if not task["completed"] else "Undo", key=f"complete_{task['id']}"):
                for t in tasks:
                    if t["id"] == task["id"]:
                        t["completed"] = not t["completed"]
                        save_tasks(tasks)
                        st.rerun()
            if st.button("Delete", key=f"delete_{task['id']}"):
                tasks = [t for t in tasks if t["id"] != task["id"]]
                save_tasks(tasks)
                st.rerun()


    st.sidebar.header("Testing Suite")

    if st.sidebar.button("Run Unit Tests"):
        with st.spinner("Running unit tests..."):
            result = subprocess.run(
                ["pytest", "tests/test_basic.py", "-v"],
                capture_output=True, text=True
            )
            st.code(result.stdout)

    if st.sidebar.button("Run Parameterized Tests"):
        with st.spinner("Running parameterized tests..."):
            result = subprocess.run(
                ["pytest", "tests/test_advanced.py", "-v"],
                capture_output=True, text=True
            )
            st.code(result.stdout)

    if st.sidebar.button("Run Full Coverage Report"):
        with st.spinner("Running tests and coverage..."):
            result = subprocess.run(
                ["pytest", "tests/", "--cov=tasks", "--cov-report=term-missing", "--cov-report=html:coverage_html"],
                capture_output=True, text=True
            )
            st.subheader("Test and Coverage Output:")
            st.code(result.stdout if result.stdout else result.stderr)
            st.success("✅ HTML coverage report generated at coverage_html/index.html!")

    if st.sidebar.button("Run TDD Tests"):
        with st.spinner("Running TDD tests..."):
            result = subprocess.run(
                ["pytest", "tests/test_tdd.py", "-v"],
                capture_output=True, text=True
            )
            st.code(result.stdout)

    if st.sidebar.button("Run BDD Tests"):
        with st.spinner("Running BDD feature tests..."):
            result = subprocess.run(
                ["pytest", "tests/feature", "-v"],  # <-- fixed: no "s"
                capture_output=True, text=True
            )
            st.code(result.stdout)


if __name__ == "__main__":
    main()