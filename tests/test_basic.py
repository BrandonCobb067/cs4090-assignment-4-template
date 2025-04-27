import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from tasks import load_tasks, save_tasks, filter_tasks_by_priority, filter_tasks_by_category, filter_tasks_by_completion, search_tasks, get_overdue_tasks


def test_save_and_load_tasks(tmp_path):
    file = tmp_path / "tasks.json"
    tasks = [{"id": 1, "title": "Test Task", "completed": False}]
    save_tasks(tasks, file)
    loaded = load_tasks(file)
    assert loaded == tasks

def test_load_tasks_file_not_found(tmp_path):
    file = tmp_path / "non_existent.json"
    tasks = load_tasks(file)
    assert tasks == []

def test_load_tasks_bad_json(tmp_path):
    bad_file = tmp_path / "bad_tasks.json"
    bad_file.write_text("not json")
    tasks = load_tasks(bad_file)
    assert tasks == []

def test_filter_by_priority_found():
    tasks = [{"priority": "High"}, {"priority": "Low"}]
    result = filter_tasks_by_priority(tasks, "High")
    assert len(result) == 1
    assert result[0]["priority"] == "High"

def test_filter_by_priority_not_found():
    tasks = [{"priority": "Low"}]
    result = filter_tasks_by_priority(tasks, "High")
    assert result == []

def test_filter_by_category_found():
    tasks = [{"category": "School"}, {"category": "Work"}]
    result = filter_tasks_by_category(tasks, "School")
    assert len(result) == 1
    assert result[0]["category"] == "School"

def test_filter_by_category_not_found():
    tasks = [{"category": "Work"}]
    result = filter_tasks_by_category(tasks, "School")
    assert result == []

def test_search_tasks_found():
    tasks = [{"title": "Buy milk", "description": "Go to store"}]
    result = search_tasks(tasks, "milk")
    assert len(result) == 1

def test_search_tasks_not_found():
    tasks = [{"title": "Buy milk", "description": "Go to store"}]
    result = search_tasks(tasks, "homework")
    assert result == []

def test_get_overdue_tasks_found():
    tasks = [{"due_date": "2000-01-01", "completed": False}]
    result = get_overdue_tasks(tasks)
    assert len(result) == 1

def test_get_overdue_tasks_not_found():
    tasks = [{"due_date": "2999-01-01", "completed": False}]
    result = get_overdue_tasks(tasks)
    assert result == []