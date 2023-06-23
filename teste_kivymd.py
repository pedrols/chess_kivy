# from kivy.app import App
from kivymd.app import MDApp
# from kivy.uix.gridlayout import GridLayout
# from kivy.uix.button import Button
from kivy.utils import rgba
from kivy.lang import Builder
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.button import MDIconButton, MDRectangleFlatIconButton

class Theme:
    COR_ESCURA_TABULEIRO = rgba('#5bbdff')
    COR_CLARA_TABULEIRO = rgba('#e6e6ff')

ik = """
BoxLayout:
    background_color: 1,0,0,1
    MDIconButton:
        icon: "chess-rook"
        user_font_size: "600sp"
        pos_hint: {"center_x": .5, "center_y": .5}
        theme_text_color: "Custom"
        text_color: 0,0,0,1
"""

# class Tabuleiro(GridLayout):
class Tabuleiro(MDGridLayout):

    def __init__(self, **kwargs):
        super(Tabuleiro, self).__init__(**kwargs)
        self.cols = 8  # Define o número de colunas do grid
        self.adaptive_height = True
        self.adaptive_width = True
        self.adaptive_size = True

        # Adiciona botões ao grid
        count = 0
        self.quadros = [[[] for _ in range(8)] for _ in range(8)]
        for row in range(8):
            for col in range(8):
                count += 1
                if (row + col) % 2 == 0:
                    cor = Theme.COR_CLARA_TABULEIRO
                else:
                    cor  = Theme.COR_ESCURA_TABULEIRO
                # self.quadros[row][col] = Button(background_normal="", background_color=cor, color=(0,0,0,1),
                #                                 size_hint=(1,1), text=str(count))

                # self.quadros[row][col] = MDIconButton(
                #     icon="chess-rook", pos_hint={"center_x": .5, "center_y": .5},
                #     theme_text_color= "Custom",
                #     text_color = (1,1,0,1),
                #     md_bg_color = cor,
                #     rounded_button = True
                # )
                                         
                self.quadros[row][col] = Builder.load_string(ik)
                #
                self.add_widget(self.quadros[row][col])
        
        # self.tabuleiro_matriz()

    def tabuleiro_matriz(self):
        qmat = [['.' for _ in range(8)] for _ in range(8)]
        # peças brancas
        qmat[0] = [c for c in 'rnbqkbnr']
        qmat[1] = ['p' for _ in range(8)]
        # peças pretas
        qmat[-2] = ['P' for _ in range(8)]
        qmat[-1] = [c for c in 'rnbqkbnr'.upper()]

        for row in range(8):
            for col in range(8):
                self.quadros[row][col].text = qmat[row][col]

        def printar_tabuleiro(tabuleiro):
            for row in tabuleiro:
                print(row)

        printar_tabuleiro(qmat)



class MyApp(MDApp):
    def build(self):
        return Tabuleiro()

if __name__ == '__main__':
    MyApp().run()
    
