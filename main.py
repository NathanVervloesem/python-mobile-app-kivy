from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Rectangle, Line
from kivy.uix.widget import Widget


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
        
        return MyWidget()
    
if __name__ == '__main__':
    MyApp().run()