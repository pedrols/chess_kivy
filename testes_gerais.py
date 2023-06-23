# %%
tabuleiro = [['.' for _ in range(8)] for _ in range(8)]

tabuleiro[0] = [c for c in 'rnbqkbnr']
tabuleiro[1] = ['p' for _ in range(8)]

tabuleiro[-2] = ['P' for _ in range(8)]
tabuleiro[-1] = [c for c in 'rnbqkbnr'.upper()]

def printar_tabuleiro(tabuleiro):
    for row in tabuleiro:
        print(row)

printar_tabuleiro(tabuleiro)

# %%
# testes com fontawesome

import fontawesome as fa

nomes_pecas = ['rook', 'knight', 'bishop', 'queen', 'king', 'pawn']

print(fa.icons['thumbs-up'])

#%%

base_pieces_dir = "./JohnPablok Cburnett Chess set/PNGs/With shadow/1x/"
pieces_names = {'p': 'pawn', 'n': 'knight', 'k': 'king', 'q': 'queen', 'r': 'rook'}

def format_piece_names(c):
    return base_pieces_dir + f"{'w' if c.isupper() else 'b'}_{pieces_names[c.lower()]}_1x.png"

#%%

format_piece_names('P')