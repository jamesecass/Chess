import pygame
import copy
import os

WIDTH = 800
HEIGHT = 800
FPS = 60
H_WHITE = (247, 247, 105)
H_GREEN = (187, 203, 43)
WHITE = (238, 238, 210)
GREEN = (118, 150, 86)

display = pygame.display.set_mode((800,800))

pygame.display.set_caption("Chess")

programIcon = pygame.image.load('Images/bp.png')
pygame.display.set_icon(programIcon)

class Board():
    def __init__(self):
        self.board = [
            ['br', 'bn', 'bb', 'bq', 'bk', 'bb', 'bn', 'br'], 
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'], 
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],  
            ['wr', 'wn', 'wb', 'wq', 'wk', 'wb', 'wn', 'wr'],  
        ]
        self.white_king_moved = False
        self.black_king_moved = False
        self.white_rook_a_moved = False
        self.white_rook_h_moved = False 
        self.black_rook_a_moved = False 
        self.black_rook_h_moved = False 

        self.en_passant_target = None

class Square():
    def __init__(self):
        self.height = 100
        self.width = 100

    def drawPattern(self,x,y,rep): 
            if rep == 0:
                return pygame.draw.rect(display,H_WHITE,(x, y, self.width, self.height))
            elif rep == 1:
                return pygame.draw.rect(display,H_GREEN,(x, y, self.width, self.height))
            elif rep == 2:
                return pygame.draw.rect(display,WHITE,(x, y, self.width, self.height))
            elif rep == 3:
                return pygame.draw.rect(display,GREEN,(x, y, self.width, self.height))
      
    def drawImage(self,x,y,piece):
        if piece in IMAGES:
            display.blit(IMAGES[piece], (x, y))

def long_range_recursion(start, row, column, dirx, diry):
    c_row = row + dirx
    c_col = column + diry
    moves = []

    if c_row < 0 or c_row > 7 or c_col < 0 or c_col > 7:
        return moves

    start_piece = board.board[start[0]][start[1]]
    c_piece = board.board[c_row][c_col]

    if c_piece == ' ':
        moves.append([c_row, c_col])
        moves += long_range_recursion(start, c_row, c_col, dirx, diry)
        return moves

    if c_piece[0] == start_piece[0]:
        return moves

    if c_piece[0] != start_piece[0]:
        moves.append([c_row, c_col])
        return moves
  
def execute_move(start,end):
    moving_piece = board.board[start[0]][start[1]]
    
    if moving_piece[1] == 'p' and start[1] != end[1] and board.board[end[0]][end[1]] == ' ':
        board.board[start[0]][end[1]] = ' ' 

    if moving_piece == 'wk' and abs(start[1] - end[1]) == 2:
        if end[1] == 6: # King Side White
            board.board[7][5] = 'wr'; board.board[7][7] = ' '
        elif end[1] == 2: # Queen Side White
            board.board[7][3] = 'wr'; board.board[7][0] = ' '
            
    if moving_piece == 'bk' and abs(start[1] - end[1]) == 2:
        if end[1] == 6: 
            board.board[0][5] = 'br'; board.board[0][7] = ' '
        elif end[1] == 2: 
            board.board[0][3] = 'br'; board.board[0][0] = ' '

    if moving_piece[1] == 'p' and abs(start[0] - end[0]) == 2:
        board.en_passant_target = [end[0], end[1]] 
    else:
        board.en_passant_target = None

    if moving_piece == 'wk': board.white_king_moved = True
    if moving_piece == 'bk': board.black_king_moved = True
    if start == [7,0]: board.white_rook_a_moved = True
    if start == [7,7]: board.white_rook_h_moved = True
    if start == [0,0]: board.black_rook_a_moved = True
    if start == [0,7]: board.black_rook_h_moved = True

    if end[0] == 0 and moving_piece == 'wp': moving_piece = 'wq'
    if end[0] == 7 and moving_piece == 'bp': moving_piece = 'bq'                 

    board.board[end[0]][end[1]] = moving_piece
    board.board[start[0]][start[1]] = ' '

def valid_moves(start,piece):
    moves = []

    if piece == 'bn' or piece == 'wn': # KNIGHT LOGIC  
        offsets = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (-1, 2), (1, -2), (-1, -2)
        ]
        
        for dr, dc in offsets:
            r, c = start[0] + dr, start[1] + dc
            
            if 0 <= r <= 7 and 0 <= c <= 7:
                target_piece = board.board[r][c]
                
                if target_piece == ' ' or piece[0] != target_piece[0]:
                    moves.append([r, c])

        return moves
    
    elif piece == 'bp': # BLACK PAWN LOGIC
        if start[0] != 7:
            if board.board[start[0] + 1][start[1]] == ' ':
                moves.append([start[0] + 1,start[1]])
                
                if start[0] == 1 and board.board[2][start[1]] == ' ' and board.board[3][start[1]] == ' ':
                    moves.append([start[0] + 2,start[1]])

        if start[1] > 0:
            if (board.board[start[0] + 1][start[1] - 1])[0] == 'w': # PAWN CAPTURING
                moves.append([start[0] + 1,start[1] - 1])
        if start[1] < 7:
            if (board.board[start[0] + 1][start[1] + 1])[0] == 'w': # PAWN CAPTURING
                moves.append([start[0] + 1,start[1] + 1])

        if start[0] == 4 and board.en_passant_target:
           
            if start[1] > 0 and board.en_passant_target == [4, start[1] - 1]:
                moves.append([5, start[1] - 1])
    
            if start[1] < 7 and board.en_passant_target == [4, start[1] + 1]:
                moves.append([5, start[1] + 1])
    
        return moves
            
    elif piece == 'wp': # WHITE PAWN LOGIC
        if board.board[start[0] - 1][start[1]] == ' ':
            moves.append([start[0] - 1,start[1]])
            
            if start[0] == 6 and board.board[5][start[1]] == ' ' and board.board[4][start[1]] == ' ':
                moves.append([start[0] - 2,start[1]])

        if start[1] > 0:
            if (board.board[start[0] - 1][start[1] - 1])[0] == 'b': # PAWN CAPTURING
                moves.append([start[0] - 1,start[1] - 1])
        if start[1] < 7:
            if (board.board[start[0] - 1][start[1] + 1])[0] == 'b': # PAWN CAPTURING
                moves.append([start[0] - 1,start[1] + 1])

        if start[0] == 3 and board.en_passant_target:

            if start[1] > 0 and board.en_passant_target == [3, start[1] - 1]:
                moves.append([2, start[1] - 1])

            if start[1] < 7 and board.en_passant_target == [3, start[1] + 1]: 
                moves.append([2, start[1] + 1])

        return moves

    elif piece == 'br' or piece == 'wr': # ROOK LOGIC
        directions = [(0,1),(1,0),(0,-1),(-1,0)]
        for dx, dy in directions:
            moves += long_range_recursion(start,start[0],start[1],dx,dy)

        return moves

    elif piece == 'bb' or piece == 'wb': # BISHOP LOGIC 
        directions = [(1,1),(-1,-1),(1,-1),(-1,1)]

        for dx, dy in directions:
            moves += long_range_recursion(start,start[0],start[1],dx,dy)
        
        return moves

    elif piece == 'bq' or piece == 'wq': # QUEEN LOGIC
        directions = [(1,1),(-1,-1),(1,-1),(-1,1),(0,1),(1,0),(0,-1),(-1,0)]

        for dx, dy in directions:
            moves += long_range_recursion(start,start[0],start[1],dx,dy)
        
        return moves

    elif piece == 'bk' or piece == 'wk': # KING LOGIC
        directions = [(1,1),(-1,-1),(1,-1),(-1,1),(0,1),(1,0),(0,-1),(-1,0)]

        for dx, dy in directions:
            r = start[0] + dx
            c = start[1] + dy

            if 0 <= r <= 7 and 0 <= c <= 7:
                target_piece = board.board[r][c]

                if target_piece[0] != piece[0]:
                    moves.append([r,c])

        if piece == 'wk' and not board.white_king_moved and not is_in_check('w'):

            if not board.white_rook_h_moved and board.board[7][5] == ' ' and board.board[7][6] == ' ':

                if not is_square_attacked_by_color([7, 5], 'b') and not is_square_attacked_by_color([7, 6], 'b'):
                    moves.append([7, 6])

            if not board.white_rook_a_moved and board.board[7][1] == ' ' and board.board[7][2] == ' ' and board.board[7][3] == ' ':
                if not is_square_attacked_by_color([7, 2], 'b') and not is_square_attacked_by_color([7, 3], 'b'):
                    moves.append([7, 2])

        elif piece == 'bk' and not board.black_king_moved and not is_in_check('b'):
            if not board.black_rook_h_moved and board.board[0][5] == ' ' and board.board[0][6] == ' ':
                if not is_square_attacked_by_color([0, 5], 'w') and not is_square_attacked_by_color([0, 6], 'w'):
                    moves.append([0, 6])

            if not board.black_rook_a_moved and board.board[0][1] == ' ' and board.board[0][2] == ' ' and board.board[0][3] == ' ':
                if not is_square_attacked_by_color([0, 2], 'w') and not is_square_attacked_by_color([0, 3], 'w'):
                    moves.append([0, 2])
        return moves

def find_king(colour,custom_board=None):
    target_board = custom_board if custom_board else board.board
    for r in range(8):
        for c in range(8):
            if target_board[r][c] == colour + 'k':
                return [r,c]

def is_in_check(colour,custom_board=None):
    target_board = custom_board if custom_board else board.board
    king_pos = find_king(colour, target_board)
    if not king_pos:
        return False

    enemy_moves = []
    
    opponent_color = 'b' if colour == 'w' else 'w'

    for r in range(8):
        for c in range(8):
            piece = target_board[r][c]
            if piece != ' ' and piece[0] == opponent_color:

                if piece[1] == 'k':
                    if abs(king_pos[0] - r) <= 1 and abs(king_pos[1] - c) <= 1:
                        return True
                    continue

                enemy_moves += valid_moves_for_board([r,c],piece,target_board)
                if king_pos in enemy_moves:
                    return True
    return False

def valid_moves_for_board(start,piece,temporary_board_matrix):
    global board

    original_board = board.board
    board.board = temporary_board_matrix

    moves = valid_moves(start,piece)

    board.board = original_board

    return moves

def get_legal_moves(start,piece):
    pseudo_moves = valid_moves(start, piece)
    legal_moves = []

    for moves in pseudo_moves:
        sim_board = copy.deepcopy(board.board)

        sim_board[moves[0]][moves[1]] = sim_board[start[0]][start[1]]
        sim_board[start[0]][start[1]] = ' '

        if not is_in_check(piece[0],custom_board=sim_board):
            legal_moves.append(moves)
    return legal_moves

def has_any_legal_moves(color):
    for r in range(8):
        for c in range(8):
            piece = board.board[r][c]
            if piece != ' ' and piece[0] == color:
                if get_legal_moves([r, c], piece):
                    return True
    return False

def is_insufficient_material():
    all_pieces = []

    for r in board.board:
        for c in r:
            if c != ' ':
                all_pieces.append({'type': piece, 'row': r, 'col': c})

    if len(all_pieces) == 2:
        return True
    
    if len(all_pieces) == 3:
        minor_piece = [p['type'] for p in all_pieces if p['type'][1 != 'k']][0]
        if minor_piece[1] in ['b','n']:
            return True
        
    if len(all_pieces) == 4:
        white_pieces = [p for p in all_pieces if p['type'][0] == 'w']
        black_pieces = [p for p in all_pieces if p['type'][0] == 'b']
        
        if len(white_pieces) == 2 and len(black_pieces) == 2:
            w_minor = [p for p in white_pieces if p['type'][1] == 'b']
            b_minor = [p for p in black_pieces if p['type'][1] == 'b']
            
            if w_minor and b_minor:
                w_bishop_color = (w_minor[0]['row'] + w_minor[0]['col']) % 2
                b_bishop_color = (b_minor[0]['row'] + b_minor[0]['col']) % 2
                
                if w_bishop_color == b_bishop_color:
                    return True
    return False

def is_square_attacked_by_color(square,attacker_colour):
    sim_board = copy.deepcopy(board.board)
    sim_board[square[0]][square[1]] = attacker_colour + 'k'
    return is_in_check(attacker_colour, custom_board=sim_board)

board = Board()
current_turn = 'w'

FOLDER_NAME = "Images" 

IMAGES = {}
pieces = ['br', 'bn', 'bb', 'bq', 'bk', 'bp', 'wr', 'wn', 'wb', 'wq', 'wk', 'wp']

for piece in pieces:
    path = f"{FOLDER_NAME}/{piece}.png"
    if os.path.exists(path):
        img = pygame.image.load(path)
        IMAGES[piece] = pygame.transform.scale(img, (100, 100))
    else:
        print(f"Warning: Missing image file at {path}")

square = Square()

clicked_square = [10,10]
selected_square = None

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            x = pos[0]
            y = pos[1]
            
            clicked_square = [y // 100,x // 100]

            if selected_square is None:
            
                row = clicked_square[0]
                col = clicked_square[1]
                clicked_piece = board.board[row][col]
            
                
                if clicked_piece != ' ' and clicked_piece[0] == current_turn:
                    selected_square = clicked_square

            elif selected_square == clicked_square:
                selected_square = None
            else:
                moves = get_legal_moves(selected_square,board.board[selected_square[0]][selected_square[1]])
                if not moves:
                    clicked_square = None
                    selected_square = None
                    continue

                if clicked_square in moves:
                    execute_move(selected_square,clicked_square)

                    current_turn = 'w' if current_turn == 'b' else 'b'

                    if is_in_check(current_turn):
                        if not has_any_legal_moves(current_turn):
                            print("Checkmate")
                            running = False
                            current_turn = 'White' if current_turn == 'b' else 'Black'
                            print(f"{current_turn} team won")
                        else:
                            print("Check")
                    else:
                        if not has_any_legal_moves(current_turn):
                            print("Stalemate")
                            running = False
                            print("Draw")
                        if is_insufficient_material():
                            print("Draw")

                clicked_square = None
                selected_square = None

    display.fill((40,40,40))  
    
    x , y = 0, 0
    
    for row in range(8):
            for column in range(8):
                if (row + column) % 2 == 0 and [row, column] == clicked_square and board.board[row][column] != ' ':
                    square.drawPattern(column * 100 , row * 100, 0)
                elif (row + column) % 2 == 1 and [row, column] == clicked_square and board.board[row][column] != ' ':
                    square.drawPattern(column * 100 , row * 100, 1)
                elif (row + column) % 2 == 0:
                    square.drawPattern(column * 100 , row * 100, 2)
                else:
                    square.drawPattern(column * 100 , row * 100, 3)
    
                square.drawImage(x, y, board.board[row][column])
                x += 100
            x = 0
            y += 100

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
