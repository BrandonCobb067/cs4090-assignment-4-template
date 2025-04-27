Feature: To-Do List Management

  Scenario: Adding a new task successfully
    Given the to-do list is empty
    When I add a task titled "Finish Assignment" with description "Finish CS4090 assignment" and category "School"
    Then the to-do list should contain a task titled "Finish Assignment"

  Scenario: Adding multiple tasks
    Given the to-do list is empty
    When I add a task titled "Buy groceries" with description "Milk, Bread, Eggs" and category "Personal"
    And I add a task titled "Workout" with description "Go to the gym" and category "Health"
    Then the to-do list should contain tasks titled "Buy groceries" and "Workout"

  Scenario: Searching for a task
    Given the to-do list contains a task titled "Call mom"
    When I search for "mom"
    Then the search results should contain "Call mom"

  Scenario: Filtering tasks by category
    Given the to-do list contains tasks with categories "Work" and "Personal"
    When I filter tasks by category "Work"
    Then I should only see tasks in the "Work" category

  Scenario: Marking a task as completed
    Given the to-do list contains a task titled "Submit taxes"
    When I mark the task "Submit taxes" as completed
    Then the task "Submit taxes" should be marked as completed
