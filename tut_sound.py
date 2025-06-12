from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.uix.boxlayout import BoxLayout

class SoundPlayer(BoxLayout):
    def play_sound(self):
        sound = SoundLoader.load('progressieve_relaxatie_1_lange_training.mp3') # file needs to be in same directory

        if sound:
            sound.volume = 0.1
            sound.play()

class MySoundApp(App):
    def build(self):
        return SoundPlayer()
    
MySoundApp().run()