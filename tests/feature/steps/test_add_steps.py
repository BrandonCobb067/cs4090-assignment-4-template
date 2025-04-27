import pytest
from pytest_bdd import scenarios, given, when, then, parsers
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../src')))

from tasks import (
    load_tasks, 
    save_tasks, 
    search_tasks, 
    filter_tasks_by_category
)

# Where the feature file is
scenarios('../add_task.feature')

# Shared in-memory "fake" tasks list
tasks = []

@given('the to-do list is empty')
def clear_tasks():
    tasks.clear()

@when(parsers.parse('I add a task titled "{title}" with description "{description}" and category "{category}"'))
def add_task(title, description, category):
    task = {
        "id": len(tasks) + 1,
        "title": title,
        "description": description,
        "category": category,
        "completed": False
    }
    tasks.append(task)

@then(parsers.parse('the to-do list should contain a task titled "{title}"'))
def check_task_exists(title):
    assert any(task['title'] == title for task in tasks)

@when(parsers.parse('I add a task titled "{title}" with description "{description}" and category "{category}"'))
@when(parsers.parse('And I add a task titled "{title}" with description "{description}" and category "{category}"'))
def add_another_task(title, description, category):
    task = {
        "id": len(tasks) + 1,
        "title": title,
        "description": description,
        "category": category,
        "completed": False
    }
    tasks.append(task)

@then(parsers.parse('the to-do list should contain tasks titled "{title1}" and "{title2}"'))
def check_multiple_tasks_exist(title1, title2):
    titles = [task['title'] for task in tasks]
    assert title1 in titles and title2 in titles

@given(parsers.parse('the to-do list contains a task titled "{title}"'))
def prepopulate_task(title):
    tasks.append({
        "id": len(tasks) + 1,
        "title": title,
        "description": "",
        "category": "General",
        "completed": False
    })

@when(parsers.parse('I search for "{keyword}"'))
def search_for_task(keyword):
    global search_results
    search_results = search_tasks(tasks, keyword)

@then(parsers.parse('the search results should contain "{title}"'))
def verify_search_result(title):
    assert any(task['title'] == title for task in search_results)

@given('the to-do list contains tasks with categories "Work" and "Personal"')
def populate_categories():
    tasks.append({
        "id": len(tasks) + 1,
        "title": "Team Meeting",
        "description": "",
        "category": "Work",
        "completed": False
    })
    tasks.append({
        "id": len(tasks) + 1,
        "title": "Dinner with family",
        "description": "",
        "category": "Personal",
        "completed": False
    })

@when(parsers.parse('I filter tasks by category "{category}"'))
def filter_by_category(category):
    global filtered_tasks
    filtered_tasks = filter_tasks_by_category(tasks, category)

@then(parsers.parse('I should only see tasks in the "{category}" category'))
def verify_filtered_category(category):
    assert all(task['category'] == category for task in filtered_tasks)

@when(parsers.parse('I mark the task "{title}" as completed'))
def mark_task_completed(title):
    for task in tasks:
        if task['title'] == title:
            task['completed'] = True

@then(parsers.parse('the task "{title}" should be marked as completed'))
def verify_task_completed(title):
    for task in tasks:
        if task['title'] == title:
            assert task['completed'] is True
