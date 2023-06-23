from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.utils import rgba


class Theme:
    COR_ESCURA_TABULEIRO = rgba('#5bbdff')
    COR_CLARA_TABULEIRO = rgba('#e6e6ff')

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
                self.quadros[row][col] = Button(background_normal="", background_color=cor, color=(0,0,0,1),
                                                size_hint=(1,1), text=str(count))
                                         
                self.add_widget(self.quadros[row][col])
        
        self.tabuleiro_matriz()

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
    
