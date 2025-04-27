import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from tasks import filter_tasks_by_priority
import pytest

@pytest.mark.parametrize("priority,expected_count", [
    ("High", 1),
    ("Medium", 0),
    ("Low", 1),
])
def test_priority_filtering(priority, expected_count):
    tasks = [{"priority": "High"}, {"priority": "Low"}]
    filtered = filter_tasks_by_priority(tasks, priority)
    assert len(filtered) == expected_count
