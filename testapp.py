from kivy.app import App
from kivy.uix.recycleview import RecycleView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import StringProperty
from kivy.lang import Builder

Builder.load_string('''
<SelectableBox>:
    orientation: 'horizontal'
    size_hint_y: None
    height: 40
    Label:
        text: root.text
    Button:
        text: "Click me"
        on_press: root.on_button_click()

<RV>:
    viewclass: 'SelectableBox'
    RecycleBoxLayout:
        default_size: None, dp(48)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
''')

class SelectableBox(RecycleDataViewBehavior, BoxLayout):
    text = StringProperty("")

    def on_button_click(self):
        print(f"Button clicked in row: {self.text}")

class RV(RecycleView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = [{'text': f'Item {i}'} for i in range(10)]

class TestApp(App):
    def build(self):
        return RV()

if __name__ == '__main__':
    TestApp().run()
