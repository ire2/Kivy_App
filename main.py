# # '''
# # 3D Rotating Monkey Head
# # ========================

# # This example demonstrates using OpenGL to display a rotating monkey head. This
# # includes loading a Blender OBJ file, shaders written in OpenGL's Shading
# # Language (GLSL), and using scheduled callbacks.

# # The monkey.obj file is an OBJ file output from the Blender free 3D creation
# # software. The file is text, listing vertices and faces and is loaded
# # using a class in the file objloader.py. The file simple.glsl is
# # a simple vertex and fragment shader written in GLSL.
# # '''

# # from kivy.app import App
# # from kivy.clock import Clock
# # from kivy.core.window import Window
# # from kivy.uix.widget import Widget
# # from kivy.resources import resource_find
# # from kivy.graphics.transformation import Matrix
# # from kivy.graphics.opengl import glEnable, glDisable, GL_DEPTH_TEST
# # from kivy.graphics import RenderContext, Callback, PushMatrix, PopMatrix, \
# #     Color, Translate, Rotate, Mesh, UpdateNormalMatrix
# # from objloader import ObjFile


# # class Renderer(Widget):
# #     def __init__(self, **kwargs):
# #         self.canvas = RenderContext(compute_normal_mat=True)
# #         self.canvas.shader.source = resource_find('simple.glsl')
# #         self.scene = ObjFile(resource_find("monkey.obj"))
# #         super(Renderer, self).__init__(**kwargs)
# #         with self.canvas:
# #             self.cb = Callback(self.setup_gl_context)
# #             PushMatrix()
# #             self.setup_scene()
# #             PopMatrix()
# #             self.cb = Callback(self.reset_gl_context)
# #         Clock.schedule_interval(self.update_glsl, 1 / 60.)

# #     def setup_gl_context(self, *args):
# #         glEnable(GL_DEPTH_TEST)

# #     def reset_gl_context(self, *args):
# #         glDisable(GL_DEPTH_TEST)

# #     def update_glsl(self, delta):
# #         asp = self.width / float(self.height)
# #         proj = Matrix().view_clip(-asp, asp, -1, 1, 1, 100, 1)
# #         self.canvas['projection_mat'] = proj
# #         self.canvas['diffuse_light'] = (1.0, 1.0, 0.8)
# #         self.canvas['ambient_light'] = (0.1, 0.1, 0.1)
# #         self.rot.angle += delta * 100

# #     def setup_scene(self):
# #         Color(1, 1, 1, 1)
# #         PushMatrix()
# #         Translate(0, 0, -3)
# #         self.rot = Rotate(1, 0, 1, 0)
# #         m = list(self.scene.objects.values())[0]
# #         UpdateNormalMatrix()
# #         self.mesh = Mesh(
# #             vertices=m.vertices,
# #             indices=m.indices,
# #             fmt=m.vertex_format,
# #             mode='triangles',
# #         )
# #         PopMatrix()


# # class RendererApp(App):
# #     def build(self):
# #         return Renderer()


# # if __name__ == "__main__":
# #     RendererApp().run()
# #!/usr/bin/env python3
# from objloader import ObjFile
# from kivy.graphics import (
#     RenderContext, Callback,
#     PushMatrix, PopMatrix,
#     Color, Translate, Rotate,
#     Mesh, UpdateNormalMatrix
# )
# from kivy.graphics.opengl import glEnable, glDisable, GL_DEPTH_TEST
# from kivy.graphics.transformation import Matrix
# from kivy.resources import resource_find
# from kivy.uix.widget import Widget
# from kivy.core.window import Window
# from kivy.clock import Clock
# from kivy.app import App
# import os
# from kivy.config import Config
# # ─ disable multisampling so GL_DEPTH_TEST behaves predictably
# Config.set('graphics', 'multisamples', '0')


# # ─ force window to show on top
# Window.raise_window()
# Window.show()


# class Renderer(Widget):
#     def __init__(self, **kwargs):
#         # 1) Let the base Widget set up its canvas stack…
#         super().__init__(**kwargs)

#         # 2) Then replace it with a RenderContext so we can pass uniforms
#         self.canvas = RenderContext(compute_normal_mat=True)

#         # 3) Find our files relative to this script
#         here = os.path.dirname(__file__)
#         shader_path = resource_find(os.path.join(here, 'simple.glsl'))
#         obj_path = resource_find(os.path.join(here, 'monkey.obj'))
#         if not shader_path or not obj_path:
#             raise RuntimeError(
#                 f"Could not find simple.glsl or monkey.obj in {here}")

#         self.canvas.shader.source = shader_path
#         self.scene = ObjFile(obj_path)

#         # 4) Build the scene graph
#         with self.canvas:
#             # turn on depth testing
#             Callback(self._setup_gl)
#             PushMatrix()
#             # center back a bit
#             Translate(0, 0, -3)
#             # initial rotation
#             self.rot = Rotate(angle=0, axis=(0, 1, 0))
#             # load the first mesh in the OBJ
#             m = next(iter(self.scene.objects.values()))
#             UpdateNormalMatrix()
#             Mesh(
#                 vertices=m.vertices,
#                 indices=m.indices,
#                 fmt=m.vertex_format,
#                 mode='triangles',
#             )
#             PopMatrix()
#             # turn depth testing off for any 2D overlays
#             Callback(self._reset_gl)

#         # 5) animate at 60 Hz
#         Clock.schedule_interval(self.update_glsl, 1 / 60.)

#     def _setup_gl(self, *l):
#         glEnable(GL_DEPTH_TEST)

#     def _reset_gl(self, *l):
#         glDisable(GL_DEPTH_TEST)

#     def update_glsl(self, dt):
#         # update the projection matrix and rotate
#         asp = self.width / float(self.height)
#         proj = Matrix().view_clip(-asp, asp, -1, 1, 1, 100, 1)
#         self.canvas['projection_mat'] = proj
#         # light settings
#         self.canvas['diffuse_light'] = (1.0, 1.0, 0.8)
#         self.canvas['ambient_light'] = (0.1, 0.1, 0.1)
#         # spin!
#         self.rot.angle += dt * 100


# class RendererApp(App):
#     def build(self):
#         return Renderer()


# if __name__ == "__main__":
#     RendererApp().run()
#!/usr/bin/env python3
from kivymd.app import MDApp
from odrive.enums import AXIS_STATE_CLOSED_LOOP_CONTROL
import odrive
from objloader import ObjFile
from kivy.graphics import (
    RenderContext, Callback, PushMatrix, PopMatrix,
    Color, Translate, Rotate, Mesh, UpdateNormalMatrix
)
from kivy.graphics.opengl import glEnable, glDisable, GL_DEPTH_TEST
from kivy.graphics.transformation import Matrix
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.resources import resource_find
from kivy.properties import NumericProperty
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.app import App
import os
from kivy.config import Config
# Disable MSAA so depth works predictably
Config.set('graphics', 'multisamples', '0')


# Force window on top
Window.raise_window()
Window.show()

KV = '''
ScreenManager:
    LoadingScreen:
        name: 'load'
    MainScreen:
        name: 'main'

<LoadingScreen>:
    Robot3D:

<MainScreen>:
    speed: speed_slider.value
    MDBoxLayout:
        orientation: 'vertical'
        padding: dp(10)
        spacing: dp(10)

        MDToolbar:
            title: 'Smart Cart Control'
            md_bg_color: app.theme_cls.primary_color
            left_action_items: [['help', lambda x: app.show_help()]]

        MDBoxLayout:
            size_hint_y: None
            height: dp(150)
            spacing: dp(10)

            MDRaisedButton:
                text: 'Backward'
                on_release: app.on_direction('backward')
            MDRaisedButton:
                text: 'Stop'
                on_release: app.on_direction('stop')
            MDRaisedButton:
                text: 'Forward'
                on_release: app.on_direction('forward')

        MDLabel:
            id: status_label
            text: 'Status: Stopped'
            halign: 'center'

        MDBoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: dp(100)
            MDLabel:
                text: 'Speed: ' + '{:.2f}'.format(root.speed)
                halign: 'center'
            MDSlider:
                id: speed_slider
                min: 0
                max: 5
                value: 0
                step: 0.01

<HelpScreen@Screen>:
    MDBoxLayout:
        orientation: 'vertical'
        MDToolbar:
            title: 'Help'
            md_bg_color: app.theme_cls.primary_color
            left_action_items: [['arrow-left', lambda x: app.go_back()]]
        ScrollView:
            MDBoxLayout:
                padding: dp(10)
                size_hint_y: None
                height: self.minimum_height
                spacing: dp(5)
                MDLabel:
                    text: 'Use this app to control the smart cart via ODrive.'
                    font_style: 'Subtitle1'
                MDLabel:
                    text: '• Tap Forward or Backward to move.'
                MDLabel:
                    text: '• Adjust the slider to set speed.'
                MDLabel:
                    text: '• Press Stop to halt.'
'''


class LoadingScreen(Screen):
    pass


class MainScreen(Screen):
    speed = NumericProperty(0)


class Robot3D(RenderContext):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.compute_normal_mat = True
        # Load shader + OBJ
        here = os.path.dirname(__file__)
        shader = resource_find(os.path.join(here, 'simple.glsl'))
        objf = resource_find(os.path.join(here, 'monkey.obj'))
        if not shader or not objf:
            raise IOError("simple.glsl or robot.obj not found")

        self.shader.source = shader
        scene = ObjFile(objf)

        with self:
            Callback(lambda *a: glEnable(GL_DEPTH_TEST))
            PushMatrix()
            Translate(0, 0, -3)
            self.rot = Rotate(angle=0, axis=(0, 1, 0))
            m = next(iter(scene.objects.values()))
            UpdateNormalMatrix()
            Mesh(vertices=m.vertices,
                 indices=m.indices,
                 fmt=m.vertex_format,
                 mode='triangles')
            PopMatrix()
            Callback(lambda *a: glDisable(GL_DEPTH_TEST))

        Clock.schedule_interval(self.animate, 1/60.)

    def animate(self, dt):
        # update projection
        aspect = self.width / float(self.height)
        proj = Matrix().view_clip(-aspect, aspect, -1, 1, 1, 100, 1)
        self['projection_mat'] = proj
        self['diffuse_light'] = (1, 1, 0.8)
        self['ambient_light'] = (0.1, 0.1, 0.1)
        # spin
        self.rot.angle += dt * 90


class CartApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = 'Blue'
        self.theme_cls.accent_palette = 'Amber'
        sm = Builder.load_string(KV)
        # after 3 s switch from loading to main
        Clock.schedule_once(lambda dt: setattr(sm, 'current', 'main'), 3)
        # connect ODrive early
        self.odrv = odrive.find_any()
        self.odrv.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
        return sm

    def on_direction(self, d):
        speed = self.root.get_screen('main').speed
        if d == 'forward':
            v = +speed
        elif d == 'backward':
            v = -speed
        else:
            v = 0
        try:
            self.odrv.axis0.controller.input_vel = v
            status = f"{d.capitalize()} @ {speed:.2f}"
        except Exception as e:
            status = f"Error: {e}"
        self.root.get_screen(
            'main').ids.status_label.text = 'Status: ' + status

    def show_help(self):
        self.root.current = 'help'

    def go_back(self):
        self.root.current = 'main'


if __name__ == '__main__':
    CartApp().run()
