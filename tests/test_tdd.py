import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from tasks import (
    load_tasks, 
    save_tasks, 
    filter_tasks_by_priority, 
    filter_tasks_by_category, 
    filter_tasks_by_completion, 
    search_tasks, 
    get_overdue_tasks, 
    generate_unique_id   # <-- Add this
)

def test_generate_unique_id_when_tasks_empty():
    tasks = []
    assert generate_unique_id(tasks) == 1

def test_generate_unique_id_when_tasks_exist():
    tasks = [{"id": 1}, {"id": 5}, {"id": 3}]
    assert generate_unique_id(tasks) == 6
