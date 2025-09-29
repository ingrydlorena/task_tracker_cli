from datetime import datetime as tm
from tabulate import tabulate as tb
import json

class TaskCli():
    def __init__(self):
        self.id_task = 1
        self.dict_task = {}
        self.free_id = []
        self.deleted_tasks = {}
        self.status = ['todo', 'progress', 'done']
        self.time = tm.today().strftime("%d/%m/%y %H:%M")
        self.archive = "taskTracker.json"
        self.load_data()
    
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
        try:
            
            if self.free_id:
                self.reused_id = self.free_id.pop(0)
                self.dict_task[self.reused_id] = {
                'description': input('input your task:\n'), 
                'status': input('how is going your task?\n'),
                'createdAt' : self.time,
                'updateAt' : None
                }
                self.save_data()
                return self.save_data()
                
            else:
                self.dict_task[self.id_task] = {
                    'description': input('input your task:\n'), 
                    'status': input('how is going your task?\n'),
                    'createdAt' : self.time,
                    'updateAt' : None
                    }
                self.id_task += 1
                self.save_data
                return self.save_data()
                
        except:
             print("Try again")



# update
    def update(self):
        self.menu_update = '''
        [1] Update description
        [2] Update status

        Choose what you want
        '''
        print(self.menu_update)
        self.update_choice = input('')
        self.id_choice = int(input('What is the id:\n'))

        if self.update_choice == '1':
            try:
                self.dict_task[self.id_choice]['description'] =  input('New description\n')
                self.dict_task[self.id_choice]['updateAt'] = self.time                                
                self.save_data()

            except KeyError:
                print("Key not found")
        elif self.update_choice == '2':
            try:
                  self.dict_task[self.id_choice]['status'] = input("New status\n")
                  self.dict_task[self.id_choice]['updateAt'] =self.time  
                  self.save_data()

            except KeyError:
                  print("Key not found")

# delete
    def delete_task(self):
        self.choice_delete = int(input("What is the id:\n"))
        if self.choice_delete in self.dict_task:
            # Move the task fot deleted_tasks
            self.deleted_tasks[self.choice_delete] = self.dict_task[self.choice_delete]
            del self.dict_task[self.choice_delete] 
            self.free_id.append(self.choice_delete)
            self.free_id.sort()
            self.save_data()
            print(f"Task {self.choice_delete} was deleted from program, you can see the task in taskTracker.json")
        else: 
             print("Id not found")
        

    def appearance(self):

        if self.dict_task:
            # list all task
            # k is id v is the task data(values) **v unpacks the task data into the dictionary, the function combines the id with the 
            # task data into one dictionary
            print(tb([{'id': k, **v} for k, v in sorted(self.dict_task.items())], headers= 'keys', tablefmt='github'),'\n')
            self.save_data()
        else:
             print("Task Empty")

    def appearance_filtered(self):
        self.menu_appearance = print('''
        [1] List all complete
        [2] List all progress
        [3] List all not complete
        What do you want to see
        ''')

        self.choice_appearance = input('')
            # lista all  done
        if self.choice_appearance == '1':
                print(tb([{'id': k, **v} for k, v in sorted(self.dict_task.items()) if v['status'] == 'done'], headers='keys', tablefmt='github'), '\n')
            # list all in progress
        elif self.choice_appearance == '2':
                print(tb([{'id': k, **v} for k, v in sorted(self.dict_task.items()) if v['status'] == 'progress'], headers='keys', tablefmt='github'), '\n')
            # list all not done
        elif self.choice_appearance == '3':
                print(tb([{'id': k, **v} for k, v in sorted(self.dict_task.items()) if v['status'] == 'todo'], headers='keys', tablefmt='github'), '\n')
        
            
# loop
task_cli = TaskCli()

while True:
    # menu de escolhas   
    menu = '''
    [1] Add
    [2] Update
    [3] Delete
    [4] List 
    [5] Sair
    What do you want?
    '''
    # cliente
    task_cli.appearance()
    print(menu)
    escolha_cliente = input('')
    if escolha_cliente == "1":
        task_cli.appearance()
        task_cli.add()
        

    elif escolha_cliente == "2":
        task_cli.appearance()
        task_cli.update()

    elif escolha_cliente == "3":
        task_cli.appearance()
        task_cli.delete_task()

    elif escolha_cliente == "4":
        task_cli.appearance_filtered()

    elif escolha_cliente == "5":
        break

    else:
         break
