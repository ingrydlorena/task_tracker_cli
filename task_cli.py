from datetime import datetime as tm
from tabulate import tabulate as tb
from enum import Enum
import json
DATETIME_FMT = "%d/%m/%y %H:%M"
class Status(Enum):
         TODO = 'todo'
         PROGRESS = 'progress'
         DONE = 'done'

class TaskCli():
       
    def __init__(self):
        self.id_task = 1
        self.dict_task = {}
        self.free_id = []
        self.deleted_tasks = {}
        self.archive = "taskTracker.json"
        self.load_data()
    
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

    # add
    def add(self):
        createdAt = tm.now().strftime(DATETIME_FMT)
        task_id = self.free_id.pop(0) if self.free_id else self.id_task
        description_input = input('input your task:\n')
        status_input = input('how is your task going?\n')
        try:
            status = Status(status_input).value
        
            self.dict_task[task_id] = {
                    'description': description_input, 
                    'status': status,
                    'createdAt' : createdAt,
                    'updateAt' : None
                    }
            
                
            if not self.free_id:
                 self.id_task += 1
                
        except ValueError:
             print("Invalid status. Try again.")
             return        
        except Exception as e:
             print(f"You receive the error {e}")



# update
    def update(self):
        menu_update = '''
--- Update ---
[1] Update description
[2] Update status
Choose what you want
        '''
        updateAt = tm.now().strftime(DATETIME_FMT)
        try:
            print(menu_update)
            update_choice = input('').strip()
            id_choice = int(input('What is the id:\n').strip())

        except ValueError:
             print("Invalid ID")
             return
        
        if update_choice == '1':
            try:
                self.dict_task[id_choice]['description'] =  input('New description\n')
                self.dict_task[id_choice]['updateAt'] = updateAt                              
                self.save_data()

            except KeyError:
                print("Key not found")
        elif update_choice == '2':
            try:
                  status_update = input('New status\n')
                  status = Status(status_update).value
                  self.dict_task[id_choice]['status'] = status
                  self.dict_task[id_choice]['updateAt'] = updateAt 
                  self.save_data()

            except KeyError:
                  print("Invalid status")

# delete
    def delete_task(self):
        try:
            choice_delete = int(input("What is the id:\n").strip())
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

    def list_task_filtered(self):
        menu_list_filtered = '''
--- List Task Filtered ---
[1] List all done
[2] List all progress
[3] List all todo
What do you want to see
        '''
        print(menu_list_filtered)
        
        choice_list_task = input('').strip()
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
            user_choice = input('').strip()
            if user_choice == "1":
                self.add()
                self.list_task()
            elif user_choice == "2":
                self.list_task()
                self.update()

            elif user_choice == "3":
                self.list_task()
                self.delete_task()

            elif user_choice == "4":
                self.list_task_filtered()

            elif user_choice == "5":
                break

            else:
                print("Invalid option. Try again")


if __name__ == "__main__":
     cli = TaskCli()
     cli.run()

