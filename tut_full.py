from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.properties import ObjectProperty
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.clock import Clock
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import StringProperty
import os
import json
import requests

DATA_FILE = 'items.json'
with open('items.json', 'w') as f:
    json.dump([], f)

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
        item_formatted = self.text
        item_name = item_formatted#[2:]
        try:
            url = myapp.url + "items/remove"
            response = requests.post(url, json={"name": item_name, "store": curr_tab})
            print("Server response:", response.json())
        except Exception as e:
            print("Error sending data:", e)

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
    inputbutton2 = ObjectProperty(None)
    inputcontent2 = ObjectProperty(None)    
    outputcontent1 = ObjectProperty(None)
    outputcontent2 = ObjectProperty(None)
    outputcontent3 = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_items()

    def load_items(self):
        url = myapp.url + "items/"
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        print(f"Raw Response: {response.text}")  # See actual cont
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(data) 

                # Get the data in the correct format
                for item in data:
                    formatted = f'{item['name']}'
                    store = item['store']
                    if store == 'Lidl':
                        self.outputcontent1.items.append(formatted)
                    elif store == 'Aldi':
                        self.outputcontent2.items.append(formatted)
                    elif store == 'Carrefour':
                        self.outputcontent3.items.append(formatted)   
                       
                # update
                self.outputcontent1.update()
                self.outputcontent2.update()
                self.outputcontent3.update()
                   
            except Exception as e:
                print(f"JSON decode error: {e}")
        else:
            print("Error Unexpected status code")


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

    def add_item(self):
        #print(self.give_current_tab_name())
        # always prints Default Tab
        ct = myapp.curr_tab
        if ct == 'Lidl':
            itemlist = self.outputcontent1
            input = self.inputcontent1
        elif ct == 'Aldi':
            itemlist = self.outputcontent2
            input = self.inputcontent2
        elif ct == 'Carrefour':
            itemlist = self.outputcontent3 
            input = self.inputcontent3
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

    def save_local(self):
            
        # Save all items to JSON file
        with open(DATA_FILE, "r") as f:
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
        with open(DATA_FILE, "w") as f:
            json.dump(items, f, indent=2)
            print('Saved to local file')



    def get_itemlist(self):
        ct = myapp.curr_tab
        if ct == 'Lidl':
            itemlist = myapp.rw.outputcontent1
        elif ct == 'Aldi':
            itemlist = myapp.rw.outputcontent2
        elif ct == 'Carrefour':
            itemlist = myapp.rw.outputcontent3    

        return itemlist

class MyfullApp(App):
    def __init__(self):
        super().__init__()
        self.curr_tab = 'Lidl'
        self.url = 'https://fastapi-shopping-1.onrender.com/'

    def build(self):
        rw = RootWidget()
        self.rw = rw
        tp = Tabs()
        tp.bind(current_tab=tp.on_current_tab)
        self.tp = tp
        self.curr_tab = tp.current_tab
        self.curr_tab = 'Lidl'

        # response = requests.get("http://127.0.0.1:8080/")
        # data = response.json()
        # print(data)

        #self.rw.outputcontent1.items = data["1"]
        #print(self.rw.outputcontent1.items)
        
        return rw
    
myapp = MyfullApp()
myapp.build()
print(myapp.rw.outputcontent1)
myapp.run()