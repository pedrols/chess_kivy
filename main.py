from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import rgba

# from kivy.uix.widget import Widget
# from kivy.uix.label import Label
# from kivy.uix.gridlayout import GridLayout

KV = """
FloatLayout:
    BoxLayout:
        id: tabuleiro
        orientation: "vertical"
"""

class Theme:
    COR_ESCURA_TABULEIRO = rgba('#5bbdff')
    COR_CLARA_TABULEIRO = rgba('#e6e6ff')

    # "tabuleiro_claro": (0.9, 0.9, 0.9, 1),  # cor clara para células
    # "tabuleiro_escuro =": (0.4, 0.4, 0.4, 1)  # cor escura para células
    
class Xadrez(App):
    def build(self):
        # instancia de tabuleiro (widget) sendo retornada como a raiz da interface de usuário
        return Builder.load_string(KV)

    def on_start(self):
        tabuleiro = self.root.ids.tabuleiro
        for n in range(8):
            linha = BoxLayout(orientation="horizontal")
            for m in range(8):
                if (n+m) % 2 == 0:
                    cor = Theme.COR_CLARA_TABULEIRO
                else:
                    cor = Theme.COR_ESCURA_TABULEIRO
                linha.add_widget(Button(background_normal="", background_color=cor, size_hint=(1,1)))
            tabuleiro.add_widget(linha)


if __name__ == '__main__':
    Xadrez().run()
