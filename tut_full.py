from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.properties import ObjectProperty
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.clock import Clock
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import StringProperty
import pprint
import requests


class SelectableBox(RecycleDataViewBehavior, BoxLayout):
    text = StringProperty("")

    def on_button_click(self):
        print('Current tab remove: ',myapp.curr_tab)

        if myapp.curr_tab == 'Lidl':
            itemlist = myapp.rw.outputcontent1
        elif myapp.curr_tab == 'Aldi':
            itemlist = myapp.rw.outputcontent2
        elif myapp.curr_tab == 'Carrefour':
            itemlist = myapp.rw.outputcontent3      
        
        itemlist.items.remove(self.text)
        itemlist.update()

        print(f"Button clicked of item: {self.text}")
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

    # def get_backend_data(self):
    #     response = requests.get("http://127.0.0.1:8080/")
    #     data = response.json()
    #     print(data) 
        

    # Get the data from the backend - fastapi
    # # Backend call

    # print(outputcontent1)
    # outputcontent1.items.append(data["1"])
    # outputcontent2.items = data["2"]
    # outputcontent3.items = data["3"]
    def load_items(self):
        response = requests.get("http://127.0.0.1:8080/")
        data = response.json()
        print(data) 

        self.outputcontent1.items = data["1"]
        self.outputcontent2.items = data["2"]
        self.outputcontent3.items = data["3"]

        # update
        self.outputcontent1.update()
        self.outputcontent2.update()
        self.outputcontent3.update()

    def send_to_backend(self):
        url = "http://127.0.0.1:8080/send"
        data = {
            "one": self.outputcontent1.items,
            "two": self.outputcontent2.items,
            "three": self.outputcontent3.items
        }
        try:
            response = requests.post(url, json=data)
            print("Server response:", response.json())
        except Exception as e:
            print("Error sending data:", e)
      


    def add_item(self):
        #print(self.give_current_tab_name())
        # always prints Default Tab
        
        if myapp.curr_tab == 'Lidl':
            itemlist = self.outputcontent1
            input = self.inputcontent1
        elif myapp.curr_tab == 'Aldi':
            itemlist = self.outputcontent2
            input = self.inputcontent2
        elif myapp.curr_tab == 'Carrefour':
            itemlist = self.outputcontent3 
            input = self.inputcontent3
        print('Current tab: ',myapp.curr_tab)

        if input.text != "":
            # Get correct tab
            print( itemlist.items)
            formatted = f'\n {input.text}'
            itemlist.items.append(formatted)
            itemlist.update()
            input.text = ""

            # and send it to the backend
            self.send_to_backend()
            
      

class MyfullApp(App):
    def __init__(self):
        super().__init__()
        self.curr_tab = 'Lidl'

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