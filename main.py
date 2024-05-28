from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.list import TwoLineAvatarIconListItem,ILeftBody
from kivymd.uix.selectioncontrol import MDCheckbox
from datetime import datetime
#importing database class
from database import Database
#instatiating db object
db = Database()

class DialogContent(MDBoxLayout):
    #init function for   class(constructor)
    def __init__(self,**kwargs):
        super().__init__( **kwargs)
        self.ids.date_text.text = datetime.now().strftime("%A %d %B %Y")
    
    #Function for display date picker
    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()
    
    #Function will get the date and saves in a friendly form 
    def on_save(self,instance,value,date_range):
        date= value.strftime("%A %d %B %Y")
        self.ids.date_text.text = str(date)


class ListItemWithCheckbox(TwoLineAvatarIconListItem):
    def __init__(self,pk=None , **kwargs):
        super().__init__(**kwargs)
        self.pk = pk


    #marking item complted or deleting 
    def mark(self,check,the_list_item):
        if check.active == True:
            the_list_item.text = f"[s]{the_list_item.text}[/s]"
            db.mark_task_as_completed(the_list_item.pk)
        else:
            the_list_item = str(db.mark_task_as_incompleted(the_list_item.pk))

    #deleting the item 
    def delete_item(self,the_list_item):
        self.parent.remove_widget(the_list_item)
        db.delete_task(the_list_item.pk)

class LeftCheckBox(ILeftBody,MDCheckbox):
    pass



#this is main class
class MainApp(MDApp):
    task_list_dialog = None
    #this is the build function setting the theme
    def build(self):
        # self.theme_cls.primary_palette = ("Teal")
        pass
    #this is the show task function 
    def show_task_dialog(self):
        if not self.task_list_dialog:
            self.task_list_dialog= MDDialog(
                title='Create Task',
                type ="custom",
                content_cls = DialogContent()
            )
            self.task_list_dialog.open()
    
    #adding task
    def add_task(self,task,task_date):
        # print(task.text,task_date)
        created_task = db.create_task(task.text,task_date)
        print(created_task)
        self.root.ids['container'].add_widget(ListItemWithCheckbox(pk =created_task[0],
                                                                   text = "[b]"+ created_task[1]+"[/b]",
                                                                   secondary_text = created_task[2]))
        task.text = ''

    #this is close function
    def close_dialog(self,*args):
        self.task_list_dialog.dismiss()

    def on_start(self):
        '''this u=is to load the saved taska and add them into MDList widget'''
        completed_task,incompleted_task = db.get_tasks()

        if incompleted_task!=[]:
            for task in incompleted_task:
                add_task = ListItemWithCheckbox(pk =task[0],text = task[1],secondary_text =task[2])
                self.root.ids.container.add_widget(add_task)

        if completed_task!=[]:
            for task in incompleted_task:
                add_task = ListItemWithCheckbox(pk =task[0],text = ["s"]+ task[1]+["/s"],
                                                secondary_text = task[2])
                add_task.ids.check.active = True
                self.root.ids.container.add_widget(add_task)

    


if __name__=="__main__":
    MainApp().run()

