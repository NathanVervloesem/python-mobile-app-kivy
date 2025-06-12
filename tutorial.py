from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.image import Image
from kivy.uix.image import AsyncImage

class MyImage(AsyncImage):
    pass

class MyBox(Widget):
    myInput = ObjectProperty(None)

    def printOut(self):
        print(self.myInput.text)

class MyApp(App):
    def build(self):
        return MyImage()
    

if __name__ == '__main__':
    MyApp().run()