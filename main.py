# Kivy imports
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.utils import platform

# Function from other files
from backend.backend_interaction import add_to_backend, clear_tab_backend, deploy_changes_wrapper, load_items, remove_item_in_backend
from utils.data_utils import get_input, get_itemlist


# External imports
import json
import os
import requests

DATA_FILE_ITEMS = 'items.json'
DATA_FILE_CHANGES = 'changes.json'

def get_item_file_path(filename):
    if platform == 'android':
        return os.path.join(App.get_running_app().user_data_dir, filename)
    else:
        return filename
    
def check_file_existence(filename):
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            json.dump([], f)

# class FirstPage(BoxLayout):
#     def __init__(self):
#         super().__init__()
#         self.bind(on_press=self.switch)

#     def switch(self,item):
#         myapp.screen_manager.transition = SlideTransition(direction='left')
#         myapp.screen_manager.current = 'Second'

# class SecondPage(BoxLayout):
#     def __init__(self):
#         super().__init__()
#         self.bind(on_press=self.switch)

#     def switch(self,item):
#         myapp.screen_manager.transition = SlideTransition(direction='right')
#         myapp.screen_manager.current = 'First'

class SelectableBox(RecycleDataViewBehavior, BoxLayout):
    text = StringProperty("")

    def on_button_click(self):
        print('Current tab remove: ',myapp.curr_tab)

        itemlist = get_itemlist(myapp,myapp.curr_tab)      
        
        itemlist.items.remove(self.text)
        itemlist.update()

        print(f"Button clicked of item: {self.text}")

        # Communicate with backend to remove the item
        remove_item_in_backend(myapp,myapp.curr_tab,self.text)


class Tabs(TabbedPanel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_current_tab(self, instance, value):
         self.curr_tab = value.text
         print("Current tab label:", value.text)
         myapp.curr_tab = value.text
         return value.text

class ListWidget(RecycleView):

    def update(self):
        self.data = [{'text': str(item)}for item in self.items]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.items = []
        self.label = ''

class RootWidget(BoxLayout):
    inputbutton1 = ObjectProperty(None)
    inputcontent1 = ObjectProperty(None)
    outputcontent1 = ObjectProperty(None)

    inputbutton2 = ObjectProperty(None)
    inputcontent2 = ObjectProperty(None) 
    outputcontent2 = ObjectProperty(None)  

    inputbutton3 = ObjectProperty(None)
    inputcontent3 = ObjectProperty(None)    
    outputcontent3 = ObjectProperty(None)

    inputbutton4 = ObjectProperty(None)
    inputcontent4 = ObjectProperty(None)    
    outputcontent4 = ObjectProperty(None)
    

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.check_connection, 5)  # every 5 seconds

    def set_labels(self):
        self.outputcontent1.label = 'Lidl'
        self.outputcontent2.label = 'Aldi'
        self.outputcontent3.label = 'Carrefour'
        self.outputcontent4.label = 'Allerlei'
    
    def check_connection(self, dt):
        try:
            # Ping a lightweight endpoint from your FastAPI (e.g., GET /ping)
            response = requests.get(myapp.url + "ping", timeout=2)
            if response.status_code == 200:
                self.ids.connection_status.text = "Connected"
                self.ids.connection_status.connected = True # 1 if connected, 0 if not connected
                self.ids.connection_status.color = (0, 1, 0, 1)  # green

            else:
                self.ids.connection_status.text = "Unreachable"
                self.ids.connection_status.connected = False
                self.ids.connection_status.color = (1, 0.5, 0, 1)  # orange
        except Exception:
            self.ids.connection_status.text = "No Connection"
            self.ids.connection_status.connected = False
            self.ids.connection_status.color = (1, 0, 0, 1)  # red

        # If connected, deploy changes made to backend and load items
        if self.ids.connection_status.connected:

            # Deploy changes wrapper
            deploy_changes_wrapper(myapp)
            
            # Load items
            load_items(myapp)

    def on_kv_post(self, base_widget):
        myapp.rw = self
        
        # Define number of tabs and labels
        myapp.rw.number_of_tabs = 4
        myapp.rw.set_labels()

        # Load items
        load_items(myapp)

    def add_item(self):
        '''
            Add an item in the tab
        '''

        itemlist = get_itemlist(myapp, myapp.curr_tab)
        input = get_input(myapp, myapp.curr_tab)

        if input.text != "":
            # Save item
            item = input.text
            # Get correct tab
            print( itemlist.items)
            itemlist.items.append(item)
            itemlist.update()
            input.text = ""

            # and send it to the backend
            add_to_backend(myapp,myapp.curr_tab,item)
    
    def clear_tab(self):
        '''
            Clears a tab completely
        '''

        itemlist = get_itemlist(myapp, myapp.curr_tab) 

        itemlist.items = [] 
        itemlist.update()   

        # Send this to backend
        clear_tab_backend(myapp, myapp.curr_tab)   

class MyshoppingApp(App):
    def __init__(self):
        super().__init__()
        self.curr_tab = 'Lidl'
        self.url = 'https://fastapi-shopping-1.onrender.com/'
        #self.url = 'http://127.0.0.1:8080/'

    def build(self):
        # Initialize data files
        # Path for Android application
        self.path_items = get_item_file_path(DATA_FILE_ITEMS)
        self.path_changes = get_item_file_path(DATA_FILE_CHANGES)

        print(self.path_items)
        print(self.path_changes)

        # Ensure the file exists
        check_file_existence(self.path_items)
        check_file_existence(self.path_changes)

        # Initialize Rootwidget
        rw = RootWidget()

        # Initialize tabs
        tp = Tabs()
        tp.bind(current_tab=tp.on_current_tab)
        self.tp = tp
        self.curr_tab = tp.current_tab
        self.curr_tab = 'Lidl'

        # Initialize selectable box
        sb = SelectableBox()
        self.sb = sb



        return rw
    
myapp = MyshoppingApp()
#myapp.build()
myapp.run()