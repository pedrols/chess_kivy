from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.utils import rgba
from kivy.lang import Builder

# NÃO FUNCIONOU
# ValueError: the given link did not return a correct status code

import kivysome
from kivysome import FontGroup

# kivysome.enable(kivysome.latest, group=kivysome.fontgroup.regular)

kivysome.enable(
        "https://kit.fontawesome.com/ca2efa7b5c.js",
        group=FontGroup.SOLID,
        font_folder="../fonts",
    )

kv_button = """
Button:
    markup: True
    size_hint: (1,1)
    text: "%s"%(icon('chess-rook', 32))

"""

class Theme:
    COR_ESCURA_TABULEIRO = rgba('#5bbdff')
    COR_CLARA_TABULEIRO = rgba('#e6e6ff')

class Tabuleiro(GridLayout):

    def __init__(self, **kwargs):
        super(Tabuleiro, self).__init__(**kwargs)
        self.cols = 8  # Define o número de colunas do grid

        # EXEMPLO DE BOTÃO COM KIVYSOME

        # Adiciona botões ao grid
        count = 0
        # self.quadros = [[Button(size_hint=(1,1)) for _ in range(8)] for _ in range(8)]
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
                self.quadros[row][col] = Builder.load_string(kv_button)
                                         
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



class MyApp(App):
    def build(self):
        return Tabuleiro()

if __name__ == '__main__':
    MyApp().run()
    
