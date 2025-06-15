from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.properties import ObjectProperty
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.clock import Clock


class Tabs(TabbedPanel):
    def on_current_tab(self, instance, value):
        print("Current tab label:", value.text)
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

    def add_item1(self):
        #print(self.give_current_tab_name())
        # always prints Default Tab
        if self.inputcontent1.text != "":
            # Get correct tab
            formatted = f'\n -{self.inputcontent1.text}'
            self.outputcontent1.items.append(formatted)
            self.outputcontent1.update()
            self.inputcontent1.text = ""

    def add_item2(self):
        #print(self.give_current_tab_name())
        # always prints Default Tab
        if self.inputcontent2.text != "":
            # Get correct tab
            formatted = f'\n {self.inputcontent2.text}'
            self.outputcontent2.items.append(formatted)
            self.outputcontent2.update()
            self.inputcontent2.text = ""
            
    def add_item3(self):
        #print(self.give_current_tab_name())
        # always prints Default Tab
        if self.inputcontent3.text != "":
            # Get correct tab
            formatted = f'\n -{self.inputcontent3.text}'
            self.outputcontent3.items.append(formatted)
            self.outputcontent3.update()
            self.inputcontent3.text = ""

    # Remove item        

class MyfullApp(App):
    def build(self):
        tp = Tabs()
        tp.bind(current_tab=tp.on_current_tab)
        return RootWidget()
    

MyfullApp().run()