# task_tracker_cli
Task tracker is a project used to track and manage your tasks. In this task, you will build a simple command line interface (CLI) to track what you need to do, what you have done, and what you are currently working on.

## Tecnology
- Python 3
- Libraries:
    1. [`tabulate`](https://pypi.org/project/tabulate/)
    2. [`datetime`](https://docs.python.org/3/library/datetime.html)(built-in)
    3. [`enum`](https://docs.python.org/3/library/enum.html)(built-in)
    4. [`json`](https://docs.python.org/3/library/json.html)(built-in)

## Installation
1. Clone this repository
```bash
git clone https://github.com/ingrydlorena/task_tracker_cli.git
```
2. Entre na pasta do project:
```bash
cd task_tracker_cli
```
3. Instale as dependências
```bash
pip install -r requirements.txt
```
## Usage
```bash
python task_cli.py
```
## Funcionality
-  Add tasks with description, status, creation date, and last update datee
-  Update task description or status
-  Delete tasks (tasks are archived in JSON)
-  List all tasks or filter by status
-  Tasks are stored persistently in a JSON file

## Task_properties
- `id`: unique identifier for the task
- `description`: brief description of the task
- `status`: task status (`todo`, `progress`, `done`)
- `created_at`: date and time the task was created
- `update_at`: date and time the task was last updated

## Project
This is a project from [``roadmap``](https://roadmap.sh/)
