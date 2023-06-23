from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.utils import rgba
from kivy.lang import Builder

# peca_png = "JohnPablok Cburnett Chess set/PNGs/With shadow/1x/b_rook_1x.png"
peca_png = "JohnPablok Cburnett Chess set/PNGs/With shadow/1x/w_rook_1x.png"
# peca_png = "Chess_bdt60.png"

kv = """
Button:
    background_normal: ""
    Image:
        source: "./JohnPablok Cburnett Chess set/PNGs/With shadow/1x/b_rook_1x.png"
        center_x: self.parent.center_x
        center_y: self.parent.center_y
        allow_stretch: True 
        keep_ratio: True
        width: 50
        height: 50
"""

# pieces_names = {
#     'p':
# }


class Theme:
    COR_ESCURA_TABULEIRO = rgba('#5bbdff')
    COR_CLARA_TABULEIRO = rgba('#e6e6ff')
    # COR_ESCURA_TABULEIRO = (0,0,0,1)
    # COR_CLARA_TABULEIRO = (1,1,1,1)

class Tabuleiro(GridLayout):

    def __init__(self, **kwargs):
        super(Tabuleiro, self).__init__(**kwargs)
        self.cols = 8  # Define o número de colunas do grid

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

                # self.quadros[row][col] = Button(background_normal=peca_png,
                #                                 background_color= (1,1,1,1),
                #                                 size_hint=(1,1))

                # image = Image(source=peca_png, size_hint=(0.1,0.1))
                # self.quadros[row][col].add_widget(image)

                # self.add_widget(self.quadros[row][col])

                # button = Button(background_normal="",
                #                 background_color=cor,
                #                 size_hint=(1,1))

                # image = Image(source=peca_png, size_hint=(0.1,0.1))
                # button.add_widget(image)

                # self.quadros[row][col] = ChessButton(cor)


                # self.quadros[row][col]  = Button(background_normal="",
                #                 background_color=cor,
                #                 size_hint=(1,1))
                # button = Button(background_normal="", size_hint=(1,1))
                # image = Image(source="./JohnPablok Cburnett Chess set/PNGs/With shadow/1x/b_rook_1x.png",
                #             #   pos=button.pos, size_hint=(None,None), size=(50,50),
                #               pos_hint={'center_x': 0.5, 'center_y': 0.5}, size_hint=(0.5, 0.5),
                #               allow_stretch=True, keep_ratio=True,
                #               )
                # button.add_widget(image)
                # self.add_widget(button)

                self.quadros[row][col] = Builder.load_string(kv)
                self.quadros[row][col].background_color = cor
                self.quadros[row][col].children[0].source = peca_png
                # self.quadros[row][col].children[0].source = ""
                self.quadros[row][col].children[0].opacity = 0

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

class ChessButton(Button):
    def __init__(self, background_color, **kwargs):
        super().__init__(**kwargs)

        self.background_normal = ''  # Remove o fundo padrão do botão
        self.background_color = background_color  # Define a cor de fundo preta
        
        self.image = Image(source=peca_png,
                           center_x=self.center_x, center_y=self.center_y,
                           width=50, height=50,
                           allow_stretch=True,
                           )
        self.add_widget(self.image)
    
# class ImagemPequena(Image):


class MyApp(App):
    def build(self):
        return Tabuleiro()

if __name__ == '__main__':
    MyApp().run()
    
