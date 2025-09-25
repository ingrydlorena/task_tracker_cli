from datetime import datetime as tm
class TaskCli():
    def __init__(self):
        self.id_task = 1
        self.dict_task = {}
        self.status = ['todo', 'in-progress', 'done']

     # menu de escolhas   
        self.menu = '''
                [1] Add
                [2] Update
                [3] Delete
                [4] Sair
                What do you want?
                '''
        # cliente
        print(self.menu)
        self.escolha_cliente = input('')

    # add
    def add(self):
        
        self.dict_task[self.id_task] = {
            'description:': input('input your task:\n'), 
            'status': input('how is going your task?\n'),
            'createdAt' : tm.today().strftime("%d/%m/%y %H:%M"),
            'updateAt' : None
            }
        self.id_task += 1


# update
    def update(self):
        self.menu_update = '''
        [1] Update description
        [2] Update status

        Choose what you want
        '''
        print(self.menu_update)
        self.update_choice = input('')
        self.id_choice = input('What is the id:\n')

        if self.id_choice in self.dict_task[self.id_task]:
            self.dict_task['description'] = input('New description:\n')
            print(self.dict_task)
        else:
            print("Key not found")
                


# delete

# list all task

# lista all  done

# list all not done

# list all in progress

# loop
task_cli = TaskCli()

match task_cli.escolha_cliente:
    case "1":
        task_cli.add()
    case "2":
        task_cli.update()
    
