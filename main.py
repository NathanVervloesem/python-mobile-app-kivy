from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.properties import ObjectProperty
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.clock import Clock
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition

import os
import json
import requests

DATA_FILE_ITEMS = 'items.json'
#Ensure the file exists
if not os.path.exists(DATA_FILE_ITEMS):
    with open(DATA_FILE_ITEMS, "w") as f:
        json.dump([], f)

# with open('items.json', 'w') as f:
#     json.dump([], f)

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

        itemlist = myapp.rw.get_itemlist()      
        
        itemlist.items.remove(self.text)
        itemlist.update()

        print(f"Button clicked of item: {self.text}")

        # Communicate with backend to remove the item
        self.remove_item_in_backend(myapp.curr_tab)


    def remove_item_in_backend(self, curr_tab):
        # Try to communicate with backend
        status = myapp.rw.ids.connection_status.text
        if status == 'Connected':
            item_formatted = self.text
            item_name = item_formatted#[2:]
            try:
                url = myapp.url + "items/remove"
                response = requests.post(url, json={"name": item_name, "store": curr_tab})
                print("Server response:", response.json())
            except Exception as e:
                print("Error sending data:", e)
            finally:
                
                # Save changes locally
                myapp.rw.save_local_all()

        elif status == "No Connection":
            pass #TODO 


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

    
    def check_connection(self, dt):
        try:
            # Ping a lightweight endpoint from your FastAPI (e.g., GET /ping)
            response = requests.get(myapp.url + "ping", timeout=2)
            if response.status_code == 200:
                self.ids.connection_status.text = "Connected"
                self.ids.connection_status.color = (0, 1, 0, 1)  # green
            else:
                self.ids.connection_status.text = "Unreachable"
                self.ids.connection_status.color = (1, 0.5, 0, 1)  # orange
        except Exception:
            self.ids.connection_status.text = "No Connection"
            self.ids.connection_status.color = (1, 0, 0, 1)  # red

        # TODO: if connected => deploy changes if changes has content

    def on_kv_post(self, base_widget):
        myapp.rw = self
        self.load_items()

    def load_items(self):

        # Doing check on outputcontent
        if not self.outputcontent1:
            print("WARNING: outputcontent1 is None — probably called too early.")

        # GET from backend
        url = myapp.url + "items/"
        
        # Try to request data from backend
        try:
            response = requests.get(url)
 
            try:
                # Get the data from json
                data = response.json()
                   
            except Exception as e:
                print(f"JSON decode error: {e}")

                # If decoding error, load locally
                data = self.load_local()


            finally:

                # Get the data in the correct format
                self.convert_data(data)
                       
                # update
                self.outputcontent1.update()
                self.outputcontent2.update()
                self.outputcontent3.update()
                self.outputcontent4.update()


                # Save locally 
                self.save_local_all()
                        
            
        except Exception as e:
            print(f"Error Unexpected status code: {e}")

            # If connection error, load locally
            data = self.load_local()

            # Gives error that self.outputcontent1.items does not exist
            self.convert_data(data)

            # print(data)
 
            # Get the data in the correct format
            #self.convert_data(data)

            # update
            self.outputcontent1.update()
            self.outputcontent2.update()
            self.outputcontent3.update()
            self.outputcontent4.update()
   
        

    def convert_data(self, data):
        for item in data:
            formatted = item['name']
            store = item['store']
            if store == 'Lidl':
                self.outputcontent1.items.append(formatted)
            elif store == 'Aldi':
                self.outputcontent2.items.append(formatted)
            elif store == 'Carrefour':
                self.outputcontent3.items.append(formatted)         
            elif store == 'Allerlei':
                self.outputcontent4.items.append(formatted) 

    def send_to_backend(self, ct, itemname):
        url = myapp.url + "items/add"
        data = { 
            'name': str(itemname),
            'store': ct
            }
        try:
            response = requests.post(url, json=data)
            print("Server response:", response.json())
        except Exception as e:
            print("Error sending data:", e)
        finally:
            # pass
            # Save locally
            self.save_local_all()

    def add_item(self):
        #print(self.give_current_tab_name())
        # always prints Default Tab
        ct = myapp.curr_tab
        print(f'Current tab: {ct}')
        if ct == 'Lidl':
            itemlist = self.outputcontent1
            input = self.inputcontent1
        elif ct == 'Aldi':
            itemlist = self.outputcontent2
            input = self.inputcontent2
        elif ct == 'Carrefour':
            itemlist = self.outputcontent3 
            input = self.inputcontent3
        elif ct == 'Allerlei':
            itemlist = self.outputcontent4
            input = self.inputcontent4
        print('Current tab: ',ct)

        if input.text != "":
            # Save item
            item = input.text
            # Get correct tab
            print( itemlist.items)
            formatted = f'{item}'
            itemlist.items.append(formatted)
            itemlist.update()
            input.text = ""

            # and send it to the backend
            self.send_to_backend(ct,item)
    
    def clear_tab(self):

        itemlist = self.get_itemlist() 

        itemlist.items = [] 
        itemlist.update()   

        # Send this to backend
        self.clear_tab_backend(myapp.curr_tab)   
    
    def clear_tab_backend(self, ct):
        try:
            url = myapp.url + "items/clear_tab"
            response = requests.post(url, json={"name": "item", "store": ct})
            print("Server response:", response.json())
        except Exception as e:
            print("Error sending data:", e)   
        finally:
            # pass
            # Save locally
            self.save_local_all()


    def save_local_all(self):
            
        # Save all items to JSON file, inefficient but fine for now
        with open(DATA_FILE_ITEMS, "r") as f:
            #items = [json.load(f)]
            items = []
            for i in self.outputcontent1.items:
                item = { 
                    'name': str(i),
                    'store': 'Lidl'
                }                 
                items.append(item)
            for i in self.outputcontent2.items:
                item = { 
                    'name': str(i),
                    'store': 'Aldi'
                }                 
                items.append(item) 
            for i in self.outputcontent3.items:
                item = { 
                    'name': str(i),
                    'store': 'Carrefour'
                }                 
                items.append(item)
            for i in self.outputcontent4.items:
                item = { 
                    'name': str(i),
                    'store': 'Allerlei'
                }                 
                items.append(item)
        with open(DATA_FILE_ITEMS, "w") as f:
            json.dump(items, f, indent=2)
            print('Saved to local file')
    
    def load_local(self):
        with open(DATA_FILE_ITEMS, "r") as f:
            data = json.load(f)
            print('Loading local data')
        
        return data

    def get_itemlist(self):
        ct = myapp.curr_tab
        if ct == 'Lidl':
            itemlist = myapp.rw.outputcontent1
        elif ct == 'Aldi':
            itemlist = myapp.rw.outputcontent2
        elif ct == 'Carrefour':
            itemlist = myapp.rw.outputcontent3 
        elif ct == 'Allerlei':
            itemlist = myapp.rw.outputcontent4 
        else:
            print('Error: tab not found')


        return itemlist

class MyshoppingApp(App):
    def __init__(self):
        super().__init__()
        self.curr_tab = 'Lidl'
        self.url = 'https://fastapi-shopping-1.onrender.com/'
        #self.url = 'http://127.0.0.1:8080/'

    def build(self):
        # Initialize Rootwidget
        rw = RootWidget()

        # Initialize tabs
        tp = Tabs()
        tp.bind(current_tab=tp.on_current_tab)
        self.tp = tp
        self.curr_tab = tp.current_tab
        self.curr_tab = 'Lidl'
        return rw
    
myapp = MyshoppingApp()
#myapp.build()
myapp.run()