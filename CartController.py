#!/usr/bin/env python3
from kivy.utils import get_color_from_hex
from odrive.enums import AXIS_STATE_CLOSED_LOOP_CONTROL
import odrive
from kivymd.app import MDApp
from kivy.properties import NumericProperty
from kivy.lang import Builder
from kivy.core.window import Window
import os
# ───— disable file logging ─────────────────────────────────────────────
os.environ['KIVY_NO_FILELOG'] = '1'

# ───— force window to show/raise ──────────────────────────────────────
Window.raise_window()
Window.show()


KV = r'''
ScreenManager:
    MainScreen:
        name: "main"
    HelpScreen:
        name: "help"

<MainScreen>:
    speed: speed_slider.value
    MDBoxLayout:
        orientation: "vertical"
        spacing: dp(10)
        padding: dp(10)

        MDToolbar:
            title: "Smart Cart Control"
            md_bg_color: get_color_from_hex("#455A64")
            left_action_items: [["help", lambda x: app.show_help()]]
            specific_text_color: 1,1,1,1

        MDBoxLayout:
            size_hint_y: None
            height: dp(150)
            spacing: dp(10)

            MDRaisedButton:
                text: "Backward"
                md_bg_color: get_color_from_hex("#EF5350")
                text_color: 1,1,1,1
                on_release: app.on_direction("backward")

            MDRaisedButton:
                text: "Stop"
                md_bg_color: get_color_from_hex("#607D8B")
                text_color: 1,1,1,1
                on_release: app.on_direction("stop")

            MDRaisedButton:
                text: "Forward"
                md_bg_color: get_color_from_hex("#8BC34A")
                text_color: 1,1,1,1
                on_release: app.on_direction("forward")

        MDLabel:
            id: status_label
            text: "Status: Stopped"
            halign: "center"
            font_style: "H6"

        BoxLayout:
            orientation: "vertical"
            size_hint_y: None
            height: dp(100)

            MDLabel:
                text: "Speed: " + "{:.2f}".format(root.speed)
                halign: "center"
                font_style: "Body1"

            MDSlider:
                id: speed_slider
                min: 0
                max: 5
                value: 0
                step: 0.01

        Widget:

<HelpScreen>:
    MDBoxLayout:
        orientation: "vertical"

        MDToolbar:
            title: "Help"
            md_bg_color: get_color_from_hex("#455A64")
            left_action_items: [["arrow-left", lambda x: app.go_back()]]
            specific_text_color: 1,1,1,1

        ScrollView:
            MDBoxLayout:
                orientation: "vertical"
                size_hint_y: None
                height: self.minimum_height
                padding: dp(10)
                spacing: dp(5)

                MDLabel:
                    text: "Use this app to control the smart cart via ODrive."
                    font_style: "Subtitle1"

                MDLabel:
                    text: "• Tap Forward or Backward to move."
                    font_style: "Body1"

                MDLabel:
                    text: "• Adjust the slider to set speed."
                    font_style: "Body1"

                MDLabel:
                    text: "• Press Stop to halt."
                    font_style: "Body1"

                MDLabel:
                    text: "Ensure ODrive is connected and calibrated."
                    font_style: "Caption"
'''


class MainScreen(Builder.get_class('MainScreen') or object):
    speed = NumericProperty(0)


class HelpScreen(Builder.get_class('HelpScreen') or object):
    pass


class CartApp(MDApp):
    def build(self):
        # — theme setup
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.primary_hue = "500"
        self.theme_cls.accent_palette = "Amber"
        self.theme_cls.accent_hue = "500"

        # — hook up the ODrive
        print("Finding ODrive…")
        self.odrv0 = odrive.find_any()
        print("Entering closed-loop control")
        self.odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

        return Builder.load_string(KV)

    def on_direction(self, direction):
        speed = self.root.get_screen("main").speed
        if direction == "forward":
            vel = speed
        elif direction == "backward":
            vel = -speed
        else:
            vel = 0

        try:
            self.odrv0.axis0.controller.input_vel = vel
            status = f"{direction.capitalize()} @ {speed:.2f}"
        except Exception as e:
            status = f"Error: {e!r}"

        self.root.get_screen(
            "main").ids.status_label.text = "Status: " + status

    def show_help(self):
        self.root.current = "help"

    def go_back(self):
        self.root.current = "main"


if __name__ == "__main__":
    CartApp().run()
