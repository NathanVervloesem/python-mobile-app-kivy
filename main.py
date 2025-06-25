# Kivy imports
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.utils import platform
from plyer import filechooser


# Function from other files
from backend.backend_interaction import add_to_backend, clear_tab_backend, deploy_changes_wrapper, load_items, remove_item_in_backend, replace_item_in_backend
from backend.localstorage_interaction import add_to_local_cart, load_local_cart, clear_local_cart, add_receipt_data, load_local_expenses, remove_item_local_expenses
from utils.data_utils import get_input, get_itemlist, increase_amount, convert_expenses_data, get_expense_id
from utils.ai_utils import analyze_receipt_image, get_receipt_data


# External imports
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai
import json
import os
from pathlib import Path
from PIL import Image
import requests
import shutil

# Define tab labels
tab_labels = ['Lidl', 'Aldi', 'Carrefour', 'Moemoe']

# Define local file names
DATA_FILE_ITEMS = 'items.json'
DATA_FILE_CHANGES = 'changes.json'
DATA_FILE_CART = 'cart.json'
DATA_FILE_EXPENSES = 'expenses.json'

ORIGINAL_CWD = Path().absolute()

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("API_KEY")

if not GOOGLE_API_KEY:
    print("Error: Google API key not found.   Please set the GOOGLE_API_KEY environment variable.")
    exit()

genai.configure(api_key=GOOGLE_API_KEY)



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
    pass

class SelectableBoxThirdScreen(RecycleDataViewBehavior, BoxLayout):
    text = StringProperty("")
    
    def on_expense_click(self):
        # Get id
        id = get_expense_id(self.text)
        
        # Get item from expenses.json
        with open(myapp.path_expenses,"r") as f:
            expenses = json.load(f)
        for item in expenses:
            if str(item["id"]) == id:
                render_item = item

        # Render on the fifth page - #TODO 
        myapp.fifth_screen.company_name = 'Store: ' + render_item["merchant_name"]
        myapp.fifth_screen.date_of_purchase = 'Date: ' + render_item["date_of_purchase"]
        myapp.fifth_screen.total_amount = 'Total amount:  ' +str(render_item["total_amount"]) + ' euro'

        myapp.fifth_screen.receiptitems.items = render_item["items_purchased"]
        #print(render_item["items_purchased"])
        myapp.fifth_screen.receiptitems.update()

    def on_remove_expense(self):
        '''
        Remove an expense from the expense list
        '''

        exp = myapp.third_screen.expensescontent
        exp.items.remove(self.text)
        exp.update()

        # Update expenses file
        remove_item_local_expenses(myapp, self.text)


        

class SelectableBoxFifthScreen(RecycleDataViewBehavior, BoxLayout):
    name = StringProperty("")
    quantity = StringProperty("")
    price = StringProperty("")

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

class ListWidget3C(RecycleView):
    def update(self):
        self.data = [{'name': '  '+str(item['item']) , 'quantity': str(item['quantity']), 'price': str(item['price'])}for item in self.items]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.items = []
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

    def on_clear_cart_click(self):
        # Remove on screen
        itemlist = myapp.second_screen.outputcontent
        itemlist.items = [] 
        itemlist.update()  

        # Remove out local storage
        clear_local_cart(myapp)

class ThirdScreen(Screen):
    expensescontent = ObjectProperty(None)


    def on_kv_post(self, base_widget):
        myapp.third_screen = self
        
        # Load expenses   # use insert to put the newest items in front
        load_local_expenses(myapp)

class FourthScreen(Screen):
    def on_kv_post(self, base_widget):
        myapp.fourth_screen = self


    def select_file(self, *args):
        filechooser.open_file(
            title="Pick an Image",
            filters=[("Image files", "*.jpg;*.jpeg;*.png")],
            on_selection=self.file_selected
        )

    def file_selected(self, selection):
        # Restore original working dir
        os.chdir(ORIGINAL_CWD)

        if selection:
            original_path = selection[0]
            app = App.get_running_app()

            # Create a photos directory inside app's private storage
            if platform == 'android':
                save_dir = os.path.join(app.user_data_dir, "photos")
            else:
                save_dir = "photos"

            os.makedirs(save_dir, exist_ok=True)

            # Unique filename (timestamp-based)
            ext = os.path.splitext(original_path)[1]
            filename = f"photo_{datetime.now().strftime('%Y%m%d_%H%M%S')}{ext}"
            new_path = os.path.join(save_dir, filename)

            # Copy file
            shutil.copy(original_path, new_path)

            print(f"Copied image to: {new_path}")

            self.img.source = new_path
            self.img.reload()

    def analyze_photo(self):  
        # Here the code with the LLM
        if self.img.source:
            analysis_result = analyze_receipt_image(self.img.source)

            # Organise in data
            data = get_receipt_data(analysis_result)

            # Generate new id
            exp = myapp.third_screen.expensescontent
            with open(myapp.path_expenses,"r") as f:
                expenses = json.load(f) 
    
            if len(expenses) > 0:
                last_item = expenses[-1]
                new_id = last_item["id"] + 1
            else:
                new_id = 1
            
            data["id"] = new_id
    
            # Render on expenses screen
            data_string = convert_expenses_data(data)        
            exp.items.append(data_string)
            exp.update()

            # Save in local expenses file
            add_receipt_data(myapp, data)


class FifthScreen(Screen):
    company_name = StringProperty("")
    date_of_purchase = StringProperty("")
    total_amount = StringProperty("")
    receiptitems = ObjectProperty(None)

    def on_kv_post(self, base_widget):
        myapp.fifth_screen = self

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
        self.path_expenses = get_item_file_path(DATA_FILE_EXPENSES)

        print(f'Path of item file: {self.path_items}')
        print(f'Path of changes file: {self.path_changes}')
        print(f'Path of changes file: {self.path_cart}')
        print(f'Path of expenses file: {self.path_expenses}')

        # Ensure the file exists
        check_file_existence(self.path_items)
        check_file_existence(self.path_changes)
        check_file_existence(self.path_cart)
        check_file_existence(self.path_expenses)

        # Initialize tabs
        tp = Tabs()
        tp.bind(current_tab=tp.on_current_tab)
        self.tp = tp
        self.curr_tab = tp.current_tab

        # Initialize selectable box
        sb = SelectableBox()
        self.sb = sb

        # Screenmanager
        sm = MyScreenManager(transition=SlideTransition(duration=0.3))

        return sm
    
myapp = MyshoppingApp()
#myapp.build()
myapp.run()