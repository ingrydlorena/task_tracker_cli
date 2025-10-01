# task_tracker_cli
Task Tracker is a project designed to help you track and manage your tasks. This simple command-line interface (CLI) allows you to track what you need to do, what you are currently working on, and what you have completed.

## Tecnology
- Python 3
- Libraries:<br>
  1.[`tabulate`](https://pypi.org/project/tabulate/) formats lists or tables into nicely printed, readable tabular text in various styles.<br>
  2.[`datetime`](https://docs.python.org/3/library/datetime.html) provides classes to work with dates and times—allowing you to create, manipulate, format, and perform arithmetic with dates, times, and timestamps.<br>
  3.[`enum`](https://docs.python.org/3/library/enum.html) defines a set of named constant values (enumerations), making your code more readable and helping avoid arbitrary literals.<br>
  4.[`json`](https://docs.python.org/3/library/json.html) encodes (serializes) Python objects into JSON strings and decodes (parses) JSON strings back into Python objects, enabling easy data interchange with web APIs and storage.

## Installation
1. Clone this repository:
```bash
git clone https://github.com/ingrydlorena/task_tracker_cli.git
```
2. Navigate to the project folder:  
```bash
cd task_tracker_cli
```
3. Install the dependencies:  
```bash
pip install -r requirements.txt
```
## Usage
Run the CLI tool with:  
```bash
python task_cli.py
```
## Funcionality
-  `add` tasks with description, status, creation date, and last update datee
-  `update` task description or status
-  `delete` tasks (tasks are archived in JSON)
-  `list all` tasks or filter by status
-  Tasks are stored persistently in a JSON file

## Task_properties
- `id`: unique identifier for the task
- `description`: brief description of the task
- `status`: task status (`todo`, `progress`, `done`)
- `created_at`: date and time the task was created
- `update_at`: date and time the task was last updated

## Project
This is a project from [roadmap](https://roadmap.sh/). You can see it here: [Task Tracker project](https://roadmap.sh/projects/task-tracker)

> Feel free to contribute or raise issues!
