from datetime import datetime as tm
from tabulate import tabulate as tb
from enum import Enum
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
     # open archive json
    def load_data(self):
        try:
              with open(self.archive, 'r', encoding='utf-8') as file:
                   data = json.load(file)
                   self.dict_task = {int(k): v for k, v in data.get('dict_task', {}).items()}
                   self.id_task = data.get('id_task', 1)
                   self.free_id = data.get('free_id',[])
                   self.deleted_tasks = {int(k): v for k, v in data.get('deleted_tasks', {}).items()}
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"File not load: {e}")

    def save_data(self):
        try:
              with open(self.archive, 'w', encoding='utf-8') as file:
                   json.dump({
                        'dict_task': self.dict_task,
                        'id_task': self.id_task,
                        'free_id': self.free_id,
                        'deleted_tasks': self.deleted_tasks

                   }, file, indent=4, ensure_ascii=False)
        except Exception as e:
             print(f"File not save: {e}")


class TaskManager():
       
    def __init__(self):
        self.id_task = 1
        self.dict_task = {}
        self.free_id = []
        self.deleted_tasks = {}
        self.archive = "taskTracker.json"
        self.load_data()
    
    @staticmethod
    def validate_status(value: str):
        try:
              return Status(value).value
        except ValueError:
             raise ValueError("Invalid status")
        
    def show_menu(self):
         print("\n---Task Manager CLI---")
         print(f"[{MenuOption.ADD.value}] Add")
         print(f"[{MenuOption.UPDATE.value}] Update")
         print(f"[{MenuOption.DELETE.value}] Delete")
         print(f"[{MenuOption.LIST.value}] List")
         print(f"[{MenuOption.EXIT.value}] Exit")
         print("What do you want?")
    # add
    def add(self, description_input, status):
        createdAt = tm.now().strftime(DATETIME_FMT)
        task_id = self.free_id.pop(0) if self.free_id else self.id_task
        
        try:
            self.dict_task[task_id] = {
                    'description': description_input, 
                    'status': status,
                    'createdAt' : createdAt,
                    'updateAt' : None
                    }
            
                
            if not self.free_id:
                 self.id_task += 1
            self.save_data()

        except ValueError:
             print("Invalid status. Try again.")
             return        
        except Exception as e:
             print(f"You receive the error {e}")

# update
    def update_description(self, id_choice, new_update):
        
        updateAt = tm.now().strftime(DATETIME_FMT)
        try:
                self.dict_task[id_choice]['description'] =  new_update
                self.dict_task[id_choice]['updateAt'] = updateAt                              
                self.save_data()

        except KeyError:
            print("Key not found")

    def update_status(self,id_choice, status):
            
            updateAt = tm.now().strftime(DATETIME_FMT)
            try:
                  self.dict_task[id_choice]['status'] = status
                  self.dict_task[id_choice]['updateAt'] = updateAt 
                  self.save_data()

            except KeyError:
                  print("Invalid status")
# delete
    def delete_task(self, choice_delete):
        try:
            
            if choice_delete in self.dict_task:
                # Move the task fot deleted_tasks
                self.deleted_tasks[choice_delete] = self.dict_task[choice_delete]
                del self.dict_task[choice_delete] 
                self.free_id.append(choice_delete)
                self.free_id.sort()
                self.save_data()
                print(f"Task {choice_delete} was deleted from program, you can see the task in taskTracker.json")
            else: 
                print("Id not found")
        except Exception as e:
             print(f"You receive the error {e}")
    
    def list_task(self):

        if self.dict_task:
            # list all task
            # k is id v is the task data(values) **v unpacks the task data into the dictionary, the function combines the id with the 
            # task data into one dictionary
            print(tb([{'id': k, **v} for k, v in sorted(self.dict_task.items())], headers= 'keys', tablefmt='github'),'\n')
            self.save_data()
        else:
             print("Task Empty")

    def list_task_filtered(self, choice_list_task):
        
            # lista all  done
        if choice_list_task == '1':
                status_filter = Status.DONE.value
                
            # list all in progress
        elif choice_list_task == '2':
                status_filter = Status.PROGRESS.value 
                
            # list all not done
        elif choice_list_task == '3':
                status_filter = Status.TODO.value
                
        else:
             print("Choice not found")
             return
        
        filtered = [{'id':k, **v} for k, v in sorted(self.dict_task.items()) if v['status'] == status_filter]
        print(tb(filtered, headers='keys', tablefmt='github'),'\n')


class TaskCli():
    def run(self):   
        while True:
            # menu de escolhas   
            menu = '''
--- Task Manager CLI ---
[1] Add
[2] Update
[3] Delete
[4] List 
[5] Sair
What do you want?
            '''
            # cliente
            
            print(menu)
            self.show_menu()
            user_choice = input('').strip()

            if user_choice == MenuOption.ADD.value:
                description_input = input('Input your task:\n')
                status_input = input("How is your task going?(todo, progress, done):\n")
                try: 
                    status = TaskManager.validate_status(status_input) 
                    self.add(description_input, status)
                    self.list_task()
                except ValueError as e:
                     print(e)

            elif user_choice == MenuOption.UPDATE.value:
                self.list_task()
                menu_update = '''
--- Update ---
[1] Update description
[2] Update status
Choose what you want
        '''
                
                print(menu_update)
                id_choice = int(input('What is the id:\n').strip())
                if id_choice == '1':
                    new_update = input('New description\n')
                    self.update_description(id_choice, new_update)

                elif id_choice == '2':
                     status = TaskManager.validate_status(new_update) 
                     new_update = input('New status (todo, progress, done):\n')
                     self.update_status(id_choice, status)
                else:
                     print('Invalid update choice')
                     return
                
                

            elif user_choice == MenuOption.DELETE.value:
                self.list_task()
                choice_delete = int(input("What is the id:\n").strip())
                self.delete_task(choice_delete)

            elif user_choice == MenuOption.LIST.value:
                menu_list_filtered = '''
--- List Task Filtered ---
[1] List all done
[2] List all progress
[3] List all todo
What do you want to see
        '''
                print(menu_list_filtered)
                choice_list_task = input('').strip()
                self.list_task_filtered(choice_list_task)

            elif user_choice == MenuOption.EXIT.value:
                break

            else:
                print("Invalid option. Try again")


if __name__ == "__main__":
     cli = TaskCli()
     cli.run()

