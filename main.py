from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Rectangle, Line
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition


class MyBox(Widget):
    pass

class FirstPage(Button):
    def __init__(self):
        super().__init__()
        self.text = 'hi'
        self.bind(on_press=self.switch)

    def switch(self,item):
        myapp.screen_manager.transition = SlideTransition(direction='left')
        myapp.screen_manager.current = 'Second'

class SecondPage(Button):
    def __init__(self):
        super().__init__()
        self.text = 'hi there'
        self.bind(on_press=self.switch)

    def switch(self,item):
        myapp.screen_manager.transition = SlideTransition(direction='right')
        myapp.screen_manager.current = 'First'

class MyWidget(Widget):
    def on_touch_down(self, touch):
        touch.ud['line'] = Line(points=(touch.x,touch.y))
        self.canvas.add(touch.ud['line'])
        

    def on_touch_move(self, touch):
        touch.ud['line'].points += [touch.x,touch.y]
    



class MyLabel(Label):
    def __init__(self, text):
        super().__init__()
        self.text = text

    def on_touch_down(self, touch):
        print('DOWN', touch)
        #return super().on_touch_down(touch)
    def on_touch_up(self, touch):
        print('UP',touch)
    def on_touch_move(self, touch):
        print('MOVE',touch)
        

class MyLayout(BoxLayout):
    def __init__(self):
        super().__init__()
        self.button = Button(text='Press me')
        self.button.bind(on_press=self.new_label)

        self.add_widget(self.button)

    def new_label(self, button):
        self.label = Label(text='my new label')
        self.add_widget(self.label)
        self.remove_widget(button)


class MyApp(App):
    def build(self):
        self.screen_manager = ScreenManager()

        # First page
        self.firstpage = FirstPage()
        screen = Screen(name='First')
        screen.add_widget(self.firstpage)
        self.screen_manager.add_widget(screen)

        # Second page
        self.secondpage = SecondPage()
        screen = Screen(name='Second')
        screen.add_widget(self.secondpage)
        self.screen_manager.add_widget(screen)
        
        return self.screen_manager


myapp = MyApp()
myapp.run()
