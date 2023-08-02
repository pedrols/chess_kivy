from kivy.app import App
from kivy.uix.gridlayout import GridLayout
# from kivy.uix.button import Button
# from kivy.uix.image import Image
from kivy.utils import rgba
from kivy.lang import Builder

# a posição das peças só ficou correta interpretando diretamente da linguagem kivy
chess_button = """
Button:
    background_normal: ""
    Image:
        source: ""
        center_x: self.parent.center_x
        center_y: self.parent.center_y
        allow_stretch: True 
        keep_ratio: True
        width: 50
        height: 50
"""

base_pieces_dir = "./JohnPablok Cburnett Chess set/PNGs/With shadow/1x/"
pieces_names = {'p': 'pawn', 'n': 'knight', 'k': 'king', 'q': 'queen', 'r': 'rook', 'b':'bishop'}

class Theme:
    COR_ESCURA_TABULEIRO = rgba('#5bbdff')
    COR_CLARA_TABULEIRO = rgba('#e6e6ff')
    # COR_PECA_SELECIOANDA =  

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

                self.quadros[row][col] = Builder.load_string(chess_button)
                self.quadros[row][col].background_color = cor

                self.add_widget(self.quadros[row][col])
        
        self.tabuleiro_matriz()
        self.fill_initial_board()

    def tabuleiro_matriz(self):
        qmat = [['.' for _ in range(8)] for _ in range(8)]
        # peças brancas
        qmat[0] = [c for c in 'rnbqkbnr']
        qmat[1] = ['p' for _ in range(8)]
        # peças pretas
        qmat[-2] = ['P' for _ in range(8)]
        qmat[-1] = [c for c in 'rnbqkbnr'.upper()]

        self.qmat = qmat

        def printar_tabuleiro(tabuleiro):
            for row in tabuleiro:
                print(row)

        printar_tabuleiro(qmat)
    
    def format_piece_names(self, c):
        return base_pieces_dir + f"{'w' if c.isupper() else 'b'}_{pieces_names[c.lower()]}_1x.png"

    def fill_initial_board(self):
        for row in range(8):
            for col in range(8):
                if self.qmat[row][col] != '.':
                    self.quadros[row][col].children[0].source = self.format_piece_names(self.qmat[row][col])
                else:
                    self.quadros[row][col].children[0].opacity = 0



class MyApp(App):
    def build(self):
        return Tabuleiro()

if __name__ == '__main__':
    MyApp().run()
    
