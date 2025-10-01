'''
Melhorias a ser feita
[x] Criar docstring
[x] Arrumar identação
[x] Tratar erros genericos
[x] Separar a apresentação da lógica (MVC)
[x] Melhorar nomeclaturas
[] Teste automatizado
[] Criar readme

'''
from datetime import datetime 
from tabulate import tabulate 
from enum import Enum
import json

DATETIME_FMT = "%d/%m/%y %H:%M"

def handle_errors(func):
    '''Decorator to catch and handle common errors. 
    Can be used in any method that requires protection.'''
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as key:
            print(f"[ERROR] Id not found: {key}")
        except ValueError as value:
            print(f"[ERROR] Invalid value: {value}")
        except FileNotFoundError:
            print(f"[ERROR] File not found")
        except json.JSONDecodeError:
            print(f"[ERROR] Corrupt or invalid file ")
        except Exception as e:
            print(f"[ERROR] Unexpected error: {e}")
    return wrapper

class Status(Enum):
    TODO = 'todo'
    PROGRESS = 'progress'
    DONE = 'done'
class MenuOption(Enum):
    ADD = '1'
    UPDATE = '2'
    DELETE = '3'
    LIST = '4'
    EXIT = '5'


class TaskStorage():

    @handle_errors
    def load_data(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            self.task = {int(k): v for k, v in data.get('task', {}).items()}
            self.next_id = data.get('id_task', 1)
            self.available_ids = data.get('free_id',[])
            self.deleted_tasks = {int(k): v for k, v in data.get('deleted_tasks', {}).items()}
    
    @handle_errors
    def save_data(self):
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump({
                'task': self.task,
                'id_task': self.next_id,
                'free_id': self.available_ids,
                'deleted_tasks': self.deleted_tasks
                }, file, indent=4, ensure_ascii=False)

class TaskManager(TaskStorage):
       
    def __init__(self):
        self.next_id = 1
        self.task = {}
        self.available_ids = []
        self.deleted_tasks = {}
        self.file_path = "taskTracker.json"
        self.load_data()
    
    @staticmethod
    def validate_status(value: str):
        '''Validates the user input by checking if it matches a valid Status value.'''
        try:
            return Status(value).value
        except ValueError:
            raise ValueError("Invalid status")
        
    @staticmethod
    def prompt_for_status():
        '''Prompts the user to enter a task status and validates it using the Status enum.'''
        while True:
            status_input = input("Enter task status (todo, progress, done):\n")
            try:
                return TaskManager.validate_status(status_input)
            except ValueError:
                print("Invalid input. Valid statuses: todo, progress, done")

    @staticmethod    
    def get_user_input(prompt, valid_options=None, expected_type=str):
        '''Receives user input, validates it, and converts it to the expected type.'''
        while True:
            user_input = input(prompt).strip()
            try:
                if expected_type == int:
                    user_input = int(user_input)
                elif expected_type == float:
                    user_input = float(user_input)
                if valid_options and user_input not in valid_options:
                    print(f"Select one of: {valid_options}")
                    continue
                
                return user_input
            except ValueError:
                print(f"Please enter a valid {expected_type.__name__}")

    def show_menu(self):
        print("\n---Task Manager CLI---")
        print(f"[{MenuOption.ADD.value}] Add")
        print(f"[{MenuOption.UPDATE.value}] Update")
        print(f"[{MenuOption.DELETE.value}] Delete")
        print(f"[{MenuOption.LIST.value}] List")
        print(f"[{MenuOption.EXIT.value}] Exit")
        print("Select an option:")
    
    @handle_errors
    def add(self, description_input, status) : 
        '''Adds a new task using a free ID if available, or generates a new one.'''
        created_at = datetime.now().strftime(DATETIME_FMT)
        task_id = self.available_ids.pop(0) if self.available_ids else self.next_id
        self.task[task_id] = {
            'description': description_input, 
            'status': status,
            'createdAt' : created_at,
            'updateAt' : None
            }
                
        if not self.available_ids:
            self.next_id += 1
        self.save_data()

    @handle_errors
    def update_description(self, id_update, new_description): 
        '''Updates the description of an existing task if the ID is valid.'''
        update_at =datetime.now().strftime(DATETIME_FMT)

        self.task[id_update]['description'] =  new_description
        self.task[id_update]['updateAt'] = update_at                              
        self.save_data()

    @handle_errors
    def update_status(self,id_update, status):
        '''Updates the status of a task given a valid ID and new status.'''
        update_at = datetime.now().strftime(DATETIME_FMT)
        self.task[id_update]['status'] = status
        self.task[id_update]['updateAt'] = update_at
        self.save_data()

    @handle_errors
    def delete_task(self, id_delete):
        '''Deletes a task and moves it to the archive. Frees the task ID for reuse.'''      
        if id_delete in self.task:
                
            self.deleted_tasks[id_delete] = self.task[id_delete]
            del self.task[id_delete] 
            self.available_ids.append(id_delete)
            self.available_ids.sort()
            self.save_data()
            print(f"Task {id_delete} deleted. It has been archived in 'taskTracker.json'.")
        else: 
            print("Id not found")
 
    
    def list_task(self):
        '''Displays all current tasks in a formatted table.'''
        if self.task:
            # k is id v is the task data(values) **v unpacks the task data into the dictionary, the function combines the id with the 
            # task data into one dictionary
            print(tabulate([{'id': k, **v} for k, v in sorted(self.task.items())], headers= 'keys', tablefmt='github'),'\n')
        else:
            print("Task list is empty.")

    def list_task_filtered(self, filter_option = str):
        '''Displays tasks filtered by their status (todo, progress, or done).'''
        if filter_option == '1':
            status_filter = Status.DONE.value
            
        elif filter_option == '2':
            status_filter = Status.PROGRESS.value 

        elif filter_option == '3':
            status_filter = Status.TODO.value
                
        else:
            print("Choice not found")
            return
        
        filtered = [{'id':k, **v} for k, v in sorted(self.task.items()) if v['status'] == status_filter]
        print(tabulate(filtered, headers='keys', tablefmt='github'),'\n')


class TaskCli(TaskManager):
    def run(self):   
        '''Runs the main loop of the CLI, handling user interactions.'''
        while True:     
            self.show_menu()
            user_filter = TaskManager.get_user_input('', valid_options=['1','2','3','4','5'])

            if user_filter == MenuOption.ADD.value:
                self.handle_add()
            elif user_filter == MenuOption.UPDATE.value:
                self.handle_update()
            elif user_filter == MenuOption.DELETE.value:
                self.handle_delete()
            elif user_filter == MenuOption.LIST.value:
                self.handle_list()
            elif user_filter == MenuOption.EXIT.value:
                break

            else:
                print("Invalid option. Try again")
    
    @handle_errors
    def handle_add(self):
        '''Handles the process of adding a task, including input and status validation.'''
        description_input = TaskManager.get_user_input("Describe your task:\n") 
        status = TaskManager.prompt_for_status()
        self.add(description_input, status)
        self.list_task()
    
    
    def handle_update(self):
        '''Handles task updates, calling either the description or status update function based on user choice.'''
        self.list_task()
        menu_update = '''
--- Update ---
[1] Update description
[2] Update status
Select an update option:
        '''
                
        print(menu_update)
        update_choice = TaskManager.get_user_input('', valid_options=['1','2'])
        id_update = TaskManager.get_user_input("What's the id:\n", expected_type=int)

        if update_choice == '1':
            new_description = TaskManager.get_user_input("New description:\n")
            self.update_description(id_update, new_description)

        elif update_choice == '2':
            status = TaskManager.prompt_for_status()
            self.update_status(id_update, status)
        else:
            print('Invalid update choice')
            return
        
    def handle_delete(self):
        self.list_task()
        valid_ids = list(self.task.keys())
        id_delete = TaskManager.get_user_input("What's the id:\n", valid_options=valid_ids, expected_type=int)
        self.delete_task(id_delete)
    
    def handle_list(self):
        menu_list_filtered = '''
--- List Task Filtered ---
[1] List all done
[2] List all progress
[3] List all todo
Select a filter option:        
'''
        print(menu_list_filtered)
        filter_option = TaskManager.get_user_input('', valid_options=['1','2','3'])
        self.list_task_filtered(filter_option)


if __name__ == "__main__":
     cli = TaskCli()
     cli.run()

