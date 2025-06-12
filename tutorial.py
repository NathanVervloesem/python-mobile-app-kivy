from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty

class MyBox(Widget):
    myInput = ObjectProperty(None)

    def printOut(self):
        print(self.myInput.text)

class MyApp(App):
    def build(self):
        return MyBox()
    

if __name__ == '__main__':
    MyApp().run()