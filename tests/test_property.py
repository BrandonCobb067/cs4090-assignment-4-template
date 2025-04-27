import pytest
import hypothesis.strategies as st
from hypothesis import given
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from tasks import filter_tasks_by_completion

@given(st.lists(st.dictionaries(keys=st.just("completed"), values=st.booleans())))
def test_filter_tasks_by_completion_property(tasks):
    completed_tasks = filter_tasks_by_completion(tasks, completed=True)
    for task in completed_tasks:
        assert task["completed"] == True
