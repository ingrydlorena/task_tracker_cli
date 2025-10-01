'''
Melhorias a ser feita
[x] Criar docstring
[x] Arrumar identação
[] Tratar erros genericos
[] Separar a apresentação da lógica (MVC)
[] Melhorar nomeclaturas
[] Teste automatizado
[] Criar readme

'''
from datetime import datetime 
from tabulate import tabulate 
from enum import Enum
from typing import Union
import json

DATETIME_FMT = "%d/%m/%y %H:%M"

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
    
    def load_data(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.dict_task = {int(k): v for k, v in data.get('dict_task', {}).items()}
                self.id_task_json = data.get('id_task', 1)
                self.available_ids = data.get('free_id',[])
                self.deleted_tasks = {int(k): v for k, v in data.get('deleted_tasks', {}).items()}
        
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Failed to load file: {e}")
            raise

    def save_data(self):
        try:
            with open(self.file_path, 'w', encoding='utf-8') as file:
                json.dump({
                    'dict_task': self.dict_task,
                    'id_task': self.id_task_json,
                    'free_id': self.available_ids,
                    'deleted_tasks': self.deleted_tasks

                }, file, indent=4, ensure_ascii=False)
        except Exception as e:
             print(f"Failed to save file: {e}")
             raise


class TaskManager(TaskStorage):
       
    def __init__(self):
        self.id_count = 1
        self.dict_task = {}
        self.available_ids = []
        self.deleted_tasks = {}
        self.file_path = "taskTracker.json"
        self.load_data()
    
    @staticmethod
    def validate_status(value: str) -> str:
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
    
    def add(self, description_input = str, status = str) -> str: 
        '''Adds a new task using a free ID if available, or generates a new one.'''
        created_at = datetime.now().strftime(DATETIME_FMT)
        task_id = self.available_ids.pop(0) if self.available_ids else self.id_task_json
        
        try:
            self.dict_task[task_id] = {
                'description': description_input, 
                'status': status,
                'createdAt' : created_at,
                'updateAt' : None
                }
                
            if not self.available_ids:
                self.id_count += 1
            self.save_data()

        except ValueError:
            print("Invalid status. Please enter todo, progress, or done.")
            return        
        except Exception as e:
            print(f"An error occurred: {e}")
            raise


    def update_description(self, id_update = int, new_value = str) -> [int, str]: 
        '''Updates the description of an existing task if the ID is valid.'''
        update_at =datetime.now().strftime(DATETIME_FMT)
        try:
            self.dict_task[id_update]['description'] =  new_value
            self.dict_task[id_update]['updateAt'] = update_at                              
            self.save_data()

        except KeyError:
            print("Task ID not found.")

    def update_status(self,id_update = int, status = str):
        '''Updates the status of a task given a valid ID and new status.'''
        update_at = datetime.now().strftime(DATETIME_FMT)
        try:
            self.dict_task[id_update]['status'] = status
            self.dict_task[id_update]['updateAt'] = update_at
            self.save_data()

        except KeyError:
            print("Invalid status. Please enter todo, progress, or done.")

    def delete_task(self, id_delete = int):
        '''Deletes a task and moves it to the archive. Frees the task ID for reuse.'''
        try:
            
            if id_delete in self.dict_task:
                
                self.deleted_tasks[id_delete] = self.dict_task[id_delete]
                del self.dict_task[id_delete] 
                self.available_ids.append(id_delete)
                self.available_ids.sort()
                self.save_data()
                print(f"Task {id_delete} deleted. It has been archived in 'taskTracker.json'.")
            else: 
                print("Id not found")
        except Exception as e:
            print(f"An error occurred: {e}")
            raise
    
    def list_task(self):
        '''Displays all current tasks in a formatted table.'''
        if self.dict_task:
            # k is id v is the task data(values) **v unpacks the task data into the dictionary, the function combines the id with the 
            # task data into one dictionary
            print(tabulate([{'id': k, **v} for k, v in sorted(self.dict_task.items())], headers= 'keys', tablefmt='github'),'\n')
            self.save_data()
        else:
            print("Task list is empty.")

    def list_task_filtered(self, input_filter_list = str):
        '''Displays tasks filtered by their status (todo, progress, or done).'''
        if input_filter_list == '1':
            status_filter = Status.DONE.value
            
        elif input_filter_list == '2':
            status_filter = Status.PROGRESS.value 

        elif input_filter_list == '3':
            status_filter = Status.TODO.value
                
        else:
            print("Choice not found")
            return
        
        filtered = [{'id':k, **v} for k, v in sorted(self.dict_task.items()) if v['status'] == status_filter]
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
    def handle_add(self):
        '''Handles the process of adding a task, including input and status validation.'''
        description_input = TaskManager.get_user_input("Describe your task:\n")
        try: 
            status = TaskManager.prompt_for_status()
            self.add(description_input, status)
            self.list_task()
        except ValueError as e:
            print(e)
    
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
            new_value = TaskManager.get_user_input("New description:\n")
            self.update_description(id_update, new_value)

        elif update_choice == '2':
            status = TaskManager.prompt_for_status()
            self.update_status(id_update, status)
        else:
            print('Invalid update choice')
            return
        
    def handle_delete(self):
        self.list_task()
        valid_ids = list(self.dict_task.keys())
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
        input_filter_list = TaskManager.get_user_input('', valid_options=['1','2','3'])
        self.list_task_filtered(input_filter_list)


if __name__ == "__main__":
     cli = TaskCli()
     cli.run()

