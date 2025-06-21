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
from backend.backend_interaction import add_to_backend, clear_tab_backend, deploy_changes_wrapper, load_items, remove_item_in_backend, replace_item_in_backend
from backend.localstorage_interaction import add_to_local_cart, load_local_cart
from utils.data_utils import get_input, get_itemlist, increase_amount


# External imports
import json
import os
import requests

DATA_FILE_ITEMS = 'items.json'
DATA_FILE_CHANGES = 'changes.json'
DATA_FILE_CART = 'cart.json'
tab_labels = ['Lidl', 'Aldi', 'Carrefour', 'Moemoe']

def get_item_file_path(filename):
    if platform == 'android':
        return os.path.join(App.get_running_app().user_data_dir, filename)
    else:
        return filename
    
def check_file_existence(filename):
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            json.dump([], f)

class MyScreenManager(ScreenManager):
    pass


class SelectableBox(RecycleDataViewBehavior, BoxLayout):
    text = StringProperty("")

    def on_remove_button_click(self):
        '''
            Remove an item from the shopping list with x button
        '''
        print('Current tab remove: ',myapp.curr_tab)

        itemlist = get_itemlist(myapp,myapp.curr_tab)      
        
        itemlist.items.remove(self.text)
        itemlist.update()

        print(f"Button clicked of item: {self.text}")

        # Communicate with backend to remove the item
        remove_item_in_backend(myapp,myapp.curr_tab,self.text)

    def on_multiple_button_click(self):
        '''
            Increase the amount of an item by replace the name.
            PROBLEM: the item is moved to the end of the list at load_items()
        '''

        print('Pushed + button')
        itemlist = get_itemlist(myapp,myapp.curr_tab)

        itemlist = get_itemlist(myapp,myapp.curr_tab)
        target_index = itemlist.items.index(self.text)

        # Increase amount
        new_text = increase_amount(self.text)
        itemlist.items[target_index] = new_text
        itemlist.update()
            
        # Communicate with backend to replace the item
        replace_item_in_backend(myapp,myapp.curr_tab,self.text, new_text)

    def on_cart_button_click(self):
        # Remove from shopping list
        self.on_remove_button_click()

        # Add in cart list
        text = self.text + ' (' + myapp.curr_tab + ')'
        itemlist = myapp.second_screen.outputcontent
        itemlist.items.append(text)
        itemlist.update()

        # Add to cart (cart.json) #TODO
        add_to_local_cart(myapp,text)



class SelectableBoxSecondScreen(RecycleDataViewBehavior, BoxLayout):
    text = StringProperty("")

class Tabs(TabbedPanel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_current_tab(self, instance, value):
        self.curr_tab = value.text
        if not value.text:
            print('check')
            value.text = tab_labels[0]
        print
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

class FirstScreen(Screen):
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

    def on_kv_post(self, base_widget):
        myapp.rw = self
        
        # Define number of tabs and labels
        myapp.rw.number_of_tabs = len(tab_labels)
        myapp.rw.set_labels(tab_labels)

        # Load items
        load_items(myapp)

    def set_labels(self, tab_labels):
        for i in range(1,myapp.rw.number_of_tabs+1):
            outputcontent = getattr(myapp.rw, f'outputcontent{i}')
            outputcontent.label = tab_labels[i-1]
    
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
            print(f'add_item: Itemslist before append: {itemlist.items}')
            itemlist.items.append(item)
            itemlist.update()
            input.text = ""

            # Send item to the backend
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


class SecondScreen(Screen):
    outputcontent = ObjectProperty(None)

    def on_kv_post(self, base_widget):
        myapp.second_screen = self
        
        # Load cart items from local storage
        load_local_cart(myapp)


class MyshoppingApp(App):
    def __init__(self):
        super().__init__()
        self.url = 'https://fastapi-shopping-1.onrender.com/'
        #self.url = 'http://127.0.0.1:8080/'  # For local testing
        self.screen_manager = ScreenManager()

    def build(self):
        # Initialize data files
        # Path for Android application
        self.path_items = get_item_file_path(DATA_FILE_ITEMS)
        self.path_changes = get_item_file_path(DATA_FILE_CHANGES)
        self.path_cart = get_item_file_path(DATA_FILE_CART)

        print(f'Path of item file: {self.path_items}')
        print(f'Path of changes file: {self.path_changes}')
        print(f'Path of changes file: {self.path_cart}')

        # Ensure the file exists
        check_file_existence(self.path_items)
        check_file_existence(self.path_changes)
        check_file_existence(self.path_cart)

        # Initialize tabs
        tp = Tabs()
        tp.bind(current_tab=tp.on_current_tab)
        self.tp = tp
        self.curr_tab = tp.current_tab

        # Initialize selectable box
        sb = SelectableBox()
        self.sb = sb

        # Screenmanage
        sm = MyScreenManager(transition=SlideTransition(duration=0.3))

        return sm
    
myapp = MyshoppingApp()
#myapp.build()
myapp.run()