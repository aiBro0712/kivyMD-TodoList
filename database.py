import sqlite3

class Database():
    def __init__(self) -> None:
        self.con = sqlite3.connect("task_database.db")
        self.cursor =self.con.cursor() 
        self.create_task_table()

    def create_task_table(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS TASKS(id integer PRIMARY KEY AUTOINCREMENT,task varchar(50)NOT NULL, due_date varchar(50),completed BOOLEAN NOT NULL CHECK(completed IN(0,1)) )")
        self.con.commit()

    #creating task
    def create_task(self,task,due_date):
        self.cursor.execute("insert into tasks(task,due_date, completed) values(?,?,?)",(task,due_date,0))
        self.con.commit()

        #getting the last entered item so we can add it t the task list 
        created_task = self .cursor.execute("select id ,task,due_date from tasks where task =? and completed =0",(task,)).fetchall()
        return created_task[-1]
   
    #get the task  completed or incomplted
    def get_tasks(self):
        #incompleted tasks
        incompleted_tasks = self.cursor.execute("select id ,task,due_date from tasks where completed=0").fetchall()
        
        #completed tasks
        completed_tasks = self.cursor.execute("select id ,task,due_date from tasks where completed =1").fetchall()
        return incompleted_tasks,completed_tasks
    
    #updating tasks
    def mark_task_as_completed(self,taskid):
        '''mark task as completed'''
        self.cursor.execute("update tasks set set completed = 1 where id = ?",(taskid,))
        self.con.commit()
    
    def mark_task_as_incompleted(self,taskid):
        """ mark task as incompleted"""
        self.cursor.execute("update tasks set set completed = 0 where id = ?",(taskid,))
        self.con.commit()

        #return task text 
        task_text = self.cursor.execute("select tasks from task where id =?",(taskid,)).fetchall()

        return task_text[0][0]
    
    #deleting task 
    def delete_task(self,taskid):
        '''deleting a task'''
        self.cursor.execute("delete from tasks where id =?",(taskid,))
        self.con.commit()

    def close_connnection(self):
        self.con.close()



    