import os
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, NumericProperty, BooleanProperty, ListProperty
from kivy.uix.widget import Widget

class MainScreen(Screen):
    direction_text = StringProperty("Direction: Center")
    speed = NumericProperty(2.0)
    speed_text = StringProperty("Speed: 2.00 mph")
    full_throttle = BooleanProperty(False)

class HelpScreen(Screen):
    pass

class JoystickWidget(Widget):
    x_norm = NumericProperty(0)
    y_norm = NumericProperty(0)
    knob_size = ListProperty([0,0])
    knob_pos  = ListProperty([0,0])
    # … (same implementation as before) …

class CartApp(App):
    def build(self):
        # load our two KV files from the style/ folder
        style = os.path.join(os.path.dirname(__file__), 'style')
        Builder.load_file(os.path.join(style, 'help.kv'))
        return Builder.load_file(os.path.join(style, 'main.kv'))

    def on_joy(self, x, y):
        root = self.root.get_screen('main')
        # … update root.direction_text and root.speed_text …

    def on_speed(self, val):
        root = self.root.get_screen('main')
        # … update root.speed and root.speed_text …

if __name__ == '__main__':
    CartApp().run()