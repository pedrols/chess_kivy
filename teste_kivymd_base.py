from kivymd.app import MDApp
from kivy.lang import Builder


ik = """
MDFloatLayout:
    mg_bg_color: 0,0,0,0
    MDIconButton:
        icon: "chess-rook"
        user_font_size: "150sp"
        pos_hint: {"center_x": .5, "center_y": .85}
        theme_text_color: "Custom"
        text_color: 0,0,0,1

"""

class LoginPage(MDApp):
    def build(self):
        page = Builder.load_string(ik)
        return page

if __name__ == '__main__':
    LoginPage().run()