from stockfish import Stockfish
from itertools import product
from collections import defaultdict
import copy
stockfish = Stockfish(path="C:/Users/Maria Luiza/OneDrive/Documentos/Python Scripts/stockfish-windows-2022-x86-64-avx2.exe")

"""
Regras de movimento para implementar:
roque (movimento especial do rei). 
promoção de peão. Notação: a7a8=Q

regras do castle:
o rei se move 2 casas para um dos lados e a torre assume a posição ao lado
nenhuma das peças envolvidas pode ter se mexido
não pode haver peças no caminho
o rei não pode estar em cheque
o rei não pode se mover sobre uma posição que está em ataque (1 ou 2 casas)
Notação O-O (king side) O-O-O (queen side) ou 0-0 0-0-0

colocar posição inicial nas peças
substituir letras por objetos

"""

class ChessEngine:
    
    def __init__(self):

        # defining initial character board
        board_pieces = [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
        ]

        # # defining initial character board
        # board_pieces = [
        #     ['.', '.', '.', '.', '.', '.', '.', '.'],
        #     ['.', '.', '.', '.', '.', '.', '.', '.'],
        #     ['.', '.', '.', '.', '.', '.', '.', '.'],
        #     ['.', '.', '.', '.', '.', '.', '.', '.'],
        #     ['.', '.', '.', '.', '.', '.', '.', '.'],
        #     ['.', '.', '.', '.', '.', '.', '.', '.'],
        #     ['.', '.', '.', '.', '.', '.', '.', '.'],
        #     ['r', '.', '.', '.', 'K', '.', '.', '.'],
        # ]


        self.board_pieces = board_pieces

        # traditional chess coordinates matrix
        self.board_coords = [[a+str(b) for a in 'abcdefgh'] for b in range(8,0,-1)]

        # actual indexes matrix
        self.board_inds = [[(r, c) for c in range(8)] for r in range(8)]

        # dict with coords to index equivalences
        self.coords_dict =  {c+str(r): (ir,ic) for ir,r in enumerate(range(8,0,-1)) for ic,c in enumerate(list('abcdefgh'))}

        self.pieces_and_classes = {'k':self.King, 'q':self.Queen, 'r':self.Rook, 'n':self.Knight, 'b':self.Bishop, 'p':self.Pawn}

        # piece objects board
        self.pieces_obj = [[[] for _ in range(8)] for _ in range(8)]

        # filling the board
        for row in range(8):
            for col in range(8):
                ch = board_pieces[row][col]
                if ch != '.':
                    self.pieces_obj[row][col] = self.pieces_and_classes[ch.lower()](ch, (row,col))

        # captured pieces
        self.captured = {'w': [], 'b': []}

        # moves in the game
        self.history = []

        self.turn_number = 0

    def whos_turn(self):
        return 'w' if (self.turn_number % 2) == 0 else 'b'

    def draw_board_inds(self):
       for row in self.board_inds:
           print(row)

    @staticmethod
    def draw_board(board):
        azul = lambda s: f"\033[34m{s}\033[0m"
        for n, row in zip(range(8,0,-1), board):
            print(azul(n), '|', *row)
        print(' ' * 4 + ' '.join(azul(e) for e in 'abcdefgh') + '\n')

    def print_current_board(self, board=None):
        if board is None:
            board = self.pieces_obj
        lboard = [[piece.letter if (piece:=board[r][c]) else '.' for c in range(8)] for r in range(8)]
        self.draw_board(lboard)

    def coord2inds(self, st):
        return self.coords_dict[st]

    def inds2coord(self, coord1, coord2):
        return next((key for key, val in self.coords_dict.items() if val == (coord1, coord2)), None)

    def mov_inds2coords(self, cstart, cend):
        return self.inds2coord(cstart[0], cstart[1]) + self.inds2coord(cend[0], cend[1])

    def mov_coords2inds(self, sstart, send):
        return self.coord2inds(sstart), self.coord2inds(send)

    @staticmethod
    def find_team_coords(board, team):
        return [(r, c) for r in range(8) for c in range(8)
                if (piece := board[r][c]) and (piece.team == team)]

    @staticmethod
    def move_obj_in_board(piece, r2, c2, board):
        # initial coords
        r1, c1 = piece.pos
        # removing piece from last position
        board[r1][c1] = []
        # assigning new position
        board[r2][c2] = piece
        return board

    @staticmethod
    def capture_piece(piece, board):
        r, c = piece.pos
        # delete from board
        board[r][c] = []
        return board

    def calc_all_possible_moves(self, board=None, team=None):
        """
        if function is called with one parameter triggers one level recursion 
        necessary to calculate if any move would result in check
        """
        if board is None:
            # if no parameter passed, calculates possible enemy moves for each move
            board = self.pieces_obj
            repeat = True
        else:
            repeat = False
        if team is None:
            team = self.whos_turn()

        # allied piece coordinates
        piece_coords = self.find_team_coords(board, team)
        # store results
        all_moves = defaultdict(list)
        for pc in piece_coords:
            piece = board[pc[0]][pc[1]]
            # possible moves and captures (positions only)
            moves, captures = piece.move_fnc(self, board, piece)

            # # debugging
            # tabb = '' if repeat else '     '
            # print(tabb,str(piece).split('\n')[0])
            # print(tabb,str(piece).split('\n')[1])
            # print(tabb, moves, captures)
            # print()

            # if no moves for that piece, skip to next piece
            if not moves:
                continue
            for move, cap in zip(moves, captures):
                # capture piece obj if any
                # creating a copy to not interfere in the original board matrix
                res_board = copy.deepcopy(board)
                captured_piece = res_board[cap[0]][cap[1]] if cap else None
                # capture piece
                if captured_piece is not None:
                    res_board = self.capture_piece(captured_piece, res_board)
                # move piece in board
                res_board = self.move_obj_in_board(piece, move[0], move[1], res_board)

                if repeat:
                    # debugging
                    # print(tabb, 'testing move', move)
                    next_turn_moves = self.calc_all_possible_moves(res_board, 'w' if team=='b' else 'b')
                    # if move results in check do not allow it
                    if any(next_turn_moves['is_check']):
                        continue

                all_moves['move_inds'].append((pc, move))
                all_moves['move'].append(self.mov_inds2coords(pc, move))
                all_moves['piece'].append(piece)
                all_moves['captured'].append(captured_piece)
                all_moves['is_check'].append(True if (captured_piece) and (captured_piece.letter.lower() == 'k') else False)
                all_moves['resulting_board'].append(res_board)

        return all_moves

    def move_piece(self, move):
        # FIXME checar stale mate and check mate se não tiver jogadas válidas
        # FIXME criar excessão para roque

        possible_moves = self.calc_all_possible_moves()

        if not possible_moves:
            # test for check mate or stale mate (draw)
            return

        if move not in possible_moves['move']:
            print("Movimento inválido!")
            return

        # index in possible moves
        index = possible_moves["move"].index(move)

        board = possible_moves['resulting_board'][index]
        piece =  possible_moves['piece'][index]
        captured_piece = possible_moves['captured'][index]

        # updating board
        self.pieces_obj = board

        # updating capture list
        if captured_piece is not None:
            captured_piece.pos = None
            captured_piece.is_captured = True
            self.captured[self.whos_turn()].append(captured_piece)

        # updating piece params
        piece.pos = possible_moves["move_inds"][index][1]
        piece.n_moves += 1
            
        # updating turn params
        self.history.append(move)
        self.turn_number += 1

    @staticmethod
    def is_poss_move_has_enemy(board, cpos, team):
        if not ((0 <= cpos[0] <= 7) and (0 <= cpos[1] <= 7)):
            return False, False
        if board[cpos[0]][cpos[1]]:
            if (board[cpos[0]][cpos[1]].team != team):
                return True, True
            else:
                return False, False
        else:
            return True, False


    def calc_possible_moves(self, board, piece):
        # returns coordinates
        poss_moves = []
        captures = []
        for d in piece.base_directions:
            cpos = piece.pos
            f = 0
            cont = True
            while cont:
                if piece.unlimited:
                    f += 1
                else:
                    f = 1
                    cont = False
                cpos = (piece.pos[0] + d[0] * f, piece.pos[1] + d[1] * f)
                is_valid, is_capture =  self.is_poss_move_has_enemy(board, cpos, piece.team)
                if not is_valid:
                    break
                poss_moves.append(cpos)
                captures.append(cpos if is_capture else None)
                if is_valid and is_capture:
                    break

        return poss_moves, captures

    def calc_possible_moves_king(self, board, piece):
        # FIXME add castling

        poss_moves, captures = self.calc_possible_moves(self, board, piece)

        # conditions for castling 

        # king hasnt moved 
        if piece.n_moves == 0:
            pos = piece.pos

            # on the 0 side
            for corner in [0,7]:

                # test if hook hasnt moved
                cond1 = (h:=board[pos[0]][corner]) and isinstance(h, self.Hook) and (h.n_moves == 0)

                # test for empty squares between hook and king
                if corner == 0:
                    inbetween = list(range(1, pos[1]))
                if corner == 7:
                    inbetween = list(range(pos[1]+1, 7))
                cond2 = not any(board[pos[0]][inbetween])

                # test if any square is under attack
                cond3 = True
                for n in inbetween:
                    res_board = copy.deepcopy(board)
                    res_board = self.move_obj_in_board(piece, pos[0], n, res_board)
                    next_turn_moves = self.calc_all_possible_moves(res_board, 'w' if piece.team=='b' else 'b')
                    if any(next_turn_moves['is_check']):
                        cond3 = False
            
                if cond1 and cond2 and cond3:
                    poss_moves.append((pos[0], pos[1] + 2 * (1 if corner == 7 else -1)))
                    captures.append(None)


    def calc_possible_moves_pawn(self, board, piece):
        poss_moves = []
        captures = []

        # mov direction, initial pos, en passant pos, promotion pos
        opts = {'w': (-1, 6, 3, 0), 'b': (1, 1, 4, 7)}

        # one square mov.
        cpos = (piece.pos[0] + opts[piece.team][0],  piece.pos[1])
        is_valid, is_capture = self.is_poss_move_has_enemy(board, cpos, piece.team)
        cond1 = is_valid and not is_capture
        if cond1:
            poss_moves += [cpos]
            captures += [None]

        # two square mov.
        if piece.n_moves == 0:
            cpos = (piece.pos[0] + 2 * opts[piece.team][0],  piece.pos[1])
            is_valid, is_capture = self.is_poss_move_has_enemy(board, cpos, piece.team)
            cond2 = is_valid and not is_capture
            if cond1 and cond2:
                poss_moves += [cpos]
                captures += [None]

        # capture
        for diag_dir in [-1, 1]:
            cpos = (piece.pos[0] + opts[piece.team][0] , piece.pos[1] + diag_dir)
            is_valid, is_capture = self.is_poss_move_has_enemy(board, cpos, piece.team)
            if is_valid and is_capture:
                poss_moves += [cpos]
                captures += [cpos]
            else:
                # testing for enpassant capture
                enpos = (piece.pos[0],cpos[1])
                _ , is_capture_enp = self.is_poss_move_has_enemy(board, enpos, piece.team)
                # if is enemy, is pawn, has moved only once, moved on previous turn
                if is_capture_enp and isinstance(epiece:=board[enpos[0]][enpos[1]], self.Pawn) \
                    and (epiece.n_moves == 1) and (self.coord2inds(self.history[-1][2:]) == enpos):
                    poss_moves += [cpos]
                    captures += [enpos]

        return poss_moves, captures

    class Piece:
        def __init__(self, character, pos):
            self.team = 'w' if character.isupper() else 'b'
            self.letter = character
            self.pos = pos
            self.is_captured = False
            self.n_moves = 0
            self.move_fnc = ChessEngine.calc_possible_moves

        def __str__(self):
            return f"Piece: {'Black' if self.team=='b' else 'White'} {self.piece_name} \n" + \
                f"Position: {self.pos}"

    class Queen(Piece):
        def __init__(self, character, pos):
            super().__init__(character, pos)
            self.piece_name = 'Queen'
            self.base_directions = list(product([0,1,-1], repeat=2))
            self.base_directions.remove((0,0))
            self.unlimited = True

    class King(Piece):
        def __init__(self, character, pos):
            super().__init__(character, pos)
            self.piece_name = 'King'
            self.base_directions = list(product([0,1,-1], repeat=2))
            self.base_directions.remove((0,0))
            self.unlimited = False

    class Rook(Piece):
        def __init__(self, character, pos):
            super().__init__(character, pos)
            self.piece_name = 'Rook'
            self.base_directions = [(1,0), (0,1), (-1,0), (0,-1)]
            self.unlimited = True
        
    class Knight(Piece):
        def __init__(self, character, pos):
            super().__init__(character, pos)
            self.piece_name = 'Knight'
            self.base_directions = [(2,1), (2,-1), (-2,1), (-2,-1), (1,-2), (-1,-2), (1,2), (-1,2)]
            self.unlimited = False

    class Bishop(Piece):
        def __init__(self, character, pos):
            super().__init__(character, pos)
            self.piece_name = 'Bishop'
            self.base_directions = [(1,1), (-1,1), (1,-1), (-1,-1)]
            self.unlimited = True

    class Pawn(Piece):
        def __init__(self, character, pos):
            super().__init__(character, pos)
            self.piece_name = 'Pawn'
            self.move_fnc = ChessEngine.calc_possible_moves_pawn


if __name__ == '__main__':
    chess = ChessEngine()

    chess.print_current_board()
    print(chess.calc_all_possible_moves()["move"])

    # # enpassant 
    # moves = ['a2a4', 'h7h5', 'a4a5', 'b7b5', 'a5b6']
    # for m in moves:
    #     chess.move_piece(m)
    #     chess.print_current_board()

    # # teste en passant
    # enpassant = ['a7a5', 'b2b4', 'b4b5', 'b5a6']
    # # enpassant = ['a7a5', 'b2b4', 'b4a5']
    # for en in enpassant:
    #     chess.move_piece(en)
    #     chess.draw_board()
    # print(chess.captured)

    # for _ in range(10):
    #     move = stockfish.get_best_move()
    #     stockfish.make_moves_from_current_position([move])
    #     chess.move_piece(move)

    # chess.draw_board()


    