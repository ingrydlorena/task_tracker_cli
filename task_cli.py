from datetime import datetime as tm
class TaskCli():
    def __init__(self):
        self.id_task = 1
        self.dict_task = {}
        self.free_id = []
        self.status = ['todo', 'in-progress', 'done']
        
    # add
    def add(self):
        if self.free_id:
             self.reused_id = self.free_id.pop(0)
             self.dict_task[self.reused_id] = {
            'description': input('input your task:\n'), 
            'status': input('how is going your task?\n'),
            'createdAt' : tm.today().strftime("%d/%m/%y %H:%M"),
            'updateAt' : None
            }
        else:
            self.dict_task[self.id_task] = {
                'description': input('input your task:\n'), 
                'status': input('how is going your task?\n'),
                'createdAt' : tm.today().strftime("%d/%m/%y %H:%M"),
                'updateAt' : None
                }
            self.id_task += 1
        print(self.dict_task)


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
                self.dict_task[self.id_choice]['updateAt'] = tm.today().strftime("%d/%m/%y %H:%M")                                

            except KeyError:
                print("Key not found")
        elif self.update_choice == '2':
            try:
                  self.dict_task[self.id_choice]['status'] = input("New status\n")
                  self.dict_task[self.id_choice]['updateAt'] = tm.today().strftime("%d/%m/%y %H:%M")  
            except KeyError:
                  print("Key not found")

# delete
    def delete_task(self):
        self.choice_delete = int(input("What is the id:\n"))
        if self.choice_delete in self.dict_task:
            del self.dict_task[self.choice_delete]
            self.free_id.append(self.choice_delete)
            self.free_id.sort()
        else: 
             print("Id not found")
        print(self.dict_task)

# list all task

# lista all  done

# list all not done

# list all in progress

# loop
task_cli = TaskCli()

while True:
    # menu de escolhas   
    menu = '''
    [1] Add
    [2] Update
    [3] Delete
    [4] Sair
    What do you want?
    '''
    # cliente
    print(menu)
    escolha_cliente = input('')
    if escolha_cliente == "1":
        task_cli.add()
        print('Task add with success')
    elif escolha_cliente == "2":
        task_cli.update()
    elif escolha_cliente == "3":
        task_cli.delete_task()
    elif escolha_cliente == "4":
            break
    else:
         break
