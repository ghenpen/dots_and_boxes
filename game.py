from tkinter import *
import numpy as np
from copy import deepcopy
import copy

size_of_board = 600
number_of_dots = 6
symbol_size = (size_of_board / 3 - size_of_board / 8) / 2
symbol_thickness = 50
dot_color = '#7BC043'
player1_color = '#0492CF'
player1_color_light = '#67B0CF'
player2_color = '#EE4035'
player2_color_light = '#EE7E77'
player1_score = 0
player2_score = 0
Green_color = '#7BC043'
dot_width = 0.25*size_of_board/number_of_dots
edge_width = 0.1*size_of_board/number_of_dots
distance_between_dots = size_of_board / (number_of_dots)

class GameModeSelection(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.root = root
        self.pack()
        self.create_widgets()
        
        self.master.geometry("600x600") 

    def create_widgets(self):
        self.title_label = Label(self.root, text="Dots and Boxes", font=("Comic Sans MS", 30, "bold"))
        self.title_label.pack(pady=50) 

        self.title_label = Label(self.root, text="Game Mode Selection", font=("Comic Sans MS", 20, "bold"))
        self.title_label.pack(pady=50)

        self.player_button = Button(self.root, text="Play with Another Player",font=("Comic Sans MS", 15, "bold"), command=self.play_with_player, relief="raised")
        self.player_button.pack(pady=10)

        self.computer_button = Button(self.root, text="Play with Computer",font=("Comic Sans MS", 15, "bold"), command=self.play_with_computer, relief="raised")
        self.computer_button.pack(pady=10)
        
    def play_with_player(self):
        self.master.destroy()
        game_instance = Dots_and_Boxes()
        game_instance.mainloop()

    def play_with_computer(self):
        self.master.destroy()
        game_instance = DotsAndBoxesWithComputer()
        game_instance.mainloop()

class Dots_and_Boxes():
    # ------------------------------------------------------------------
    # Initialization functions
    # ------------------------------------------------------------------
    def __init__(self):
        self.window = Tk()
        self.window.title('Dots_and_Boxes')
        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board)
        self.canvas.pack()
        self.window.bind('<Button-1>', self.click)
        self.player1_starts = True
        self.refresh_board()
        self.play_again()

    def play_again(self):
        self.refresh_board()
        self.board_status = np.zeros(shape=(number_of_dots - 1, number_of_dots - 1))
        self.last_player = np.zeros(shape=(number_of_dots - 1, number_of_dots - 1))
        self.row_status = np.zeros(shape=(number_of_dots, number_of_dots - 1))
        self.col_status = np.zeros(shape=(number_of_dots - 1, number_of_dots))
        
        # Input from user in form of clicks
        self.player1_starts = not self.player1_starts
        self.player1_turn = not self.player1_starts
        self.reset_board = False
        self.turntext_handle = []

        self.already_marked_boxes = []
        self.display_turn_text()

    def mainloop(self):
        self.window.mainloop()

    # ------------------------------------------------------------------
    # Logical Functions:
    # The modules required to carry out game logic
    # ------------------------------------------------------------------

    def is_grid_occupied(self, logical_position, type):
        r = logical_position[0]
        c = logical_position[1]
        occupied = True

        if type == 'row' and self.row_status[c][r] == 0:
            occupied = False
        if type == 'col' and self.col_status[c][r] == 0:
            occupied = False

        return occupied

    def convert_grid_to_logical_position(self, grid_position):
        grid_position = np.array(grid_position)
        position = (grid_position-distance_between_dots/4)//(distance_between_dots/2)

        type = False
        logical_position = []
        if position[1] % 2 == 0 and (position[0] - 1) % 2 == 0:
            r = int((position[0]-1)//2)
            c = int(position[1]//2)
            logical_position = [r, c]
            
            type = 'row'
            # self.row_status[c][r]=1
        elif position[0] % 2 == 0 and (position[1] - 1) % 2 == 0:
            c = int((position[1] - 1) // 2)
            r = int(position[0] // 2)
            logical_position = [r, c]
            type = 'col'

        return logical_position, type

    def mark_box(self):
        boxes = np.argwhere(self.board_status == 4)
        global player1_score, player2_score
        one_marked = False
        for box in boxes:
            if list(box) not in self.already_marked_boxes and list(box) !=[]:
                self.already_marked_boxes.append(list(box))
                if self.last_player[box[0]][box[1]] == 1:
                    color = player2_color_light
                    player2_score = player2_score + 1                    
                else:
                    color = player1_color_light
                    player1_score = player1_score + 1
                self.shade_box(box, color)
                one_marked = True
                
        if one_marked == True:
            self.player1_turn = not self.player1_turn

    def update_board(self, type, logical_position):
        r = logical_position[0]
        c = logical_position[1]
        val = 1
        player_val=1
        if self.player1_turn:
            player_val = 2

        if c < (number_of_dots-1) and r < (number_of_dots-1):
            self.board_status[c][r] += val
            self.last_player[c][r] = player_val

        if type == 'row':
            self.row_status[c][r] = 1
            if c >= 1:
                self.board_status[c-1][r] += val
                self.last_player[c-1][r] = player_val

        elif type == 'col':
            self.col_status[c][r] = 1
            if r >= 1:
                self.board_status[c][r-1] += val
                self.last_player[c][r-1] = player_val

    def is_gameover(self):
        return (self.row_status == 1).all() and (self.col_status == 1).all()

    # ------------------------------------------------------------------
    # Drawing Functions:
    # The modules required to draw required game based object on canvas
    # ------------------------------------------------------------------

    def make_edge(self, type, logical_position):
        if type == 'row':
            start_x = distance_between_dots/2 + logical_position[0]*distance_between_dots
            end_x = start_x+distance_between_dots
            start_y = distance_between_dots/2 + logical_position[1]*distance_between_dots
            end_y = start_y
        elif type == 'col':
            start_y = distance_between_dots / 2 + logical_position[1] * distance_between_dots
            end_y = start_y + distance_between_dots
            start_x = distance_between_dots / 2 + logical_position[0] * distance_between_dots
            end_x = start_x

        if self.player1_turn:
            color = player1_color
        else:
            color = player2_color
        self.canvas.create_line(start_x, start_y, end_x, end_y, fill=color, width=edge_width)

    def display_gameover(self):

        if player1_score > player2_score:
            # Player 1 wins
            text = 'Winner: Player 1 '
            color = player1_color
        elif player2_score > player1_score:
            text = 'Winner: Player 2 '
            color = player2_color
        else:
            text = 'Its a tie'
            color = 'gray'

        self.canvas.delete("all")
        self.canvas.create_text(size_of_board / 2, size_of_board / 3, font="cmr 60 bold", fill=color, text=text)

        score_text = 'Scores \n'
        self.canvas.create_text(size_of_board / 2, 5 * size_of_board / 8, font="cmr 40 bold", fill=Green_color,
                                text=score_text)

        score_text = 'Player 1 : ' + str(player1_score) + '\n'
        score_text += 'Player 2 : ' + str(player2_score) + '\n'
        # score_text += 'Tie                    : ' + str(self.tie_score)
        self.canvas.create_text(size_of_board / 2, 3 * size_of_board / 4, font="cmr 30 bold", fill=Green_color,
                                text=score_text)
        self.reset_board = True

        score_text = 'Click to play again \n'
        self.canvas.create_text(size_of_board / 2, 15 * size_of_board / 16, font="cmr 20 bold", fill="gray",
                                text=score_text)

    def refresh_board(self):
        for i in range(number_of_dots):
            x = i*distance_between_dots+distance_between_dots/2
            self.canvas.create_line(x, distance_between_dots/2, x,
                                    size_of_board-distance_between_dots/2,
                                    fill='gray', dash = (2, 2))
            self.canvas.create_line(distance_between_dots/2, x,
                                    size_of_board-distance_between_dots/2, x,
                                    fill='gray', dash=(2, 2))

        for i in range(number_of_dots):
            for j in range(number_of_dots):
                start_x = i*distance_between_dots+distance_between_dots/2
                end_x = j*distance_between_dots+distance_between_dots/2
                self.canvas.create_oval(start_x-dot_width/2, end_x-dot_width/2, start_x+dot_width/2,
                                        end_x+dot_width/2, fill=dot_color,
                                        outline=dot_color)

    def display_turn_text(self):
        text = 'Next turn: '
        if self.player1_turn:
            text += 'Player1'
            color = player1_color
        else:
            text += 'Player2'
            color = player2_color

        self.canvas.delete(self.turntext_handle)
        self.turntext_handle = self.canvas.create_text(size_of_board - 5*len(text),
                                                       size_of_board-distance_between_dots/8,
                                                       font="cmr 15 bold", text=text, fill=color)


    def shade_box(self, box, color):
        start_x = distance_between_dots / 2 + box[1] * distance_between_dots + edge_width/2
        start_y = distance_between_dots / 2 + box[0] * distance_between_dots + edge_width/2
        end_x = start_x + distance_between_dots - edge_width
        end_y = start_y + distance_between_dots - edge_width
        self.canvas.create_rectangle(start_x, start_y, end_x, end_y, fill=color, outline='')

    def display_turn_text(self):
        text = 'Next turn: '
        if self.player1_turn:
            text += 'Player1'
            color = player1_color
        else:
            text += 'Player2'
            color = player2_color

        self.canvas.delete(self.turntext_handle)
        self.turntext_handle = self.canvas.create_text(size_of_board - 5*len(text),
                                                       size_of_board-distance_between_dots/8,
                                                       font="cmr 15 bold",text=text, fill=color)

    def click(self, event):
        if not self.reset_board:
            grid_position = [event.x, event.y]
            logical_positon, valid_input = self.convert_grid_to_logical_position(grid_position)
            if valid_input and not self.is_grid_occupied(logical_positon, valid_input):
                self.update_board(valid_input, logical_positon)
                self.make_edge(valid_input, logical_positon)
                self.mark_box()
                self.refresh_board()
                self.player1_turn = not self.player1_turn
                if self.is_gameover():
                    self.display_gameover()
                else:
                    self.display_turn_text()
        else:
            self.canvas.delete("all")
            self.play_again()
            self.reset_board = False
            
            
class DotsAndBoxesWithComputer:
    def __init__(self):
        self.window = Tk()
        self.window.title('Dots_and_Boxes')
        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board)
        self.canvas.pack()
        self.window.bind('<Button-1>', self.click)
        self.player1_starts = True
        self.refresh_board()
        self.play_again()
    
    def play_again(self):
        self.refresh_board()
        self.board_status = np.zeros(shape=(number_of_dots - 1, number_of_dots - 1))
        self.last_player = np.zeros(shape=(number_of_dots - 1, number_of_dots - 1))
        self.row_status = np.zeros(shape=(number_of_dots, number_of_dots - 1))
        self.col_status = np.zeros(shape=(number_of_dots - 1, number_of_dots))
        
        # Input from user in form of clicks
        self.player1_starts = not self.player1_starts
        self.player1_turn = not self.player1_starts
        self.reset_board = False
        self.turntext_handle = []

        self.already_marked_boxes = []
        self.display_turn_text()
        
    def mainloop(self):
        self.window.mainloop()
        
    def convert_grid_to_logical_position(self, grid_position):
        grid_position = np.array(grid_position)
        position = (grid_position-distance_between_dots/4)//(distance_between_dots/2)

        type = False
        logical_position = []
        if position[1] % 2 == 0 and (position[0] - 1) % 2 == 0:
            r = int((position[0]-1)//2)
            c = int(position[1]//2)
            logical_position = [r, c]
            type = 'row'
            # self.row_status[c][r]=1
        elif position[0] % 2 == 0 and (position[1] - 1) % 2 == 0:
            c = int((position[1] - 1) // 2)
            r = int(position[0] // 2)
            logical_position = [r, c]
            type = 'col'

        return logical_position, type
    
    def is_grid_occupied(self, logical_position, type):
        r = logical_position[1]
        c = logical_position[0]
        occupied = True

        if type == 'row' and self.row_status[r][c] == 0:
            occupied = False
        if type == 'col' and self.col_status[r][c] == 0:
            occupied = False

        return occupied
        
    def display_gameover(self):

        if player1_score > player2_score:
            # Player 1 wins
            text = 'Winner: Player 1 '
            color = player1_color
        elif player2_score > player1_score:
            text = 'Winner: Computer '
            color = player2_color
        else:
            text = 'Its a tie'
            color = 'gray'

        self.canvas.delete("all")
        self.canvas.create_text(size_of_board / 2, size_of_board / 3, font="cmr 60 bold", fill=color, text=text)

        score_text = 'Scores \n'
        self.canvas.create_text(size_of_board / 2, 5 * size_of_board / 8, font="cmr 40 bold", fill=Green_color,
                                text=score_text)

        score_text = 'Player 1 : ' + str(player1_score) + '\n'
        score_text += 'Computer : ' + str(player2_score) + '\n'
        # score_text += 'Tie                    : ' + str(self.tie_score)
        self.canvas.create_text(size_of_board / 2, 3 * size_of_board / 4, font="cmr 30 bold", fill=Green_color,
                                text=score_text)
        self.reset_board = True

        score_text = 'Click to play again \n'
        self.canvas.create_text(size_of_board / 2, 15 * size_of_board / 16, font="cmr 20 bold", fill="gray",
                                text=score_text)
        
    def refresh_board(self):
        for i in range(number_of_dots):
            x = i*distance_between_dots+distance_between_dots/2
            self.canvas.create_line(x, distance_between_dots/2, x,
                                    size_of_board-distance_between_dots/2,
                                    fill='gray', dash = (2, 2))
            self.canvas.create_line(distance_between_dots/2, x,
                                    size_of_board-distance_between_dots/2, x,
                                    fill='gray', dash=(2, 2))

        for i in range(number_of_dots):
            for j in range(number_of_dots):
                start_x = i*distance_between_dots+distance_between_dots/2
                end_x = j*distance_between_dots+distance_between_dots/2
                self.canvas.create_oval(start_x-dot_width/2, end_x-dot_width/2, start_x+dot_width/2,
                                        end_x+dot_width/2, fill=dot_color,
                                        outline=dot_color)
                
    def display_turn_text(self):
        text = 'Next turn: '
        if self.player1_turn:
            text += 'Player1'
            color = player1_color
        else:
            text += 'Computer'
            color = player2_color
            

        self.canvas.delete(self.turntext_handle)
        self.turntext_handle = self.canvas.create_text(size_of_board - 5*len(text),
                                                       size_of_board-distance_between_dots/8,
                                                       font="cmr 15 bold",text=text, fill=color)

        if self.player1_turn == False:
            self.AI_Move()

    def make_edge(self, type, logical_position):
        if type == 'row':
            start_x = distance_between_dots/2 + logical_position[0]*distance_between_dots
            end_x = start_x+distance_between_dots
            start_y = distance_between_dots/2 + logical_position[1]*distance_between_dots
            end_y = start_y
        elif type == 'col':
            start_y = distance_between_dots / 2 + logical_position[1] * distance_between_dots
            end_y = start_y + distance_between_dots
            start_x = distance_between_dots / 2 + logical_position[0] * distance_between_dots
            end_x = start_x

        if self.player1_turn:
            color = player1_color
        else:
            color = player2_color
        self.canvas.create_line(start_x, start_y, end_x, end_y, fill=color, width=edge_width)  
        
    def shade_box(self, box, color):
        start_x = distance_between_dots / 2 + box[1] * distance_between_dots + edge_width/2
        start_y = distance_between_dots / 2 + box[0] * distance_between_dots + edge_width/2
        end_x = start_x + distance_between_dots - edge_width
        end_y = start_y + distance_between_dots - edge_width
        self.canvas.create_rectangle(start_x, start_y, end_x, end_y, fill=color, outline='')
        
    def update_board(self, type, logical_position):
        r = logical_position[1]
        c = logical_position[0]
        val = 1
        player_val=1
        if self.player1_turn:
            player_val = 2

        if c < (number_of_dots-1) and r < (number_of_dots-1):
            self.board_status[r][c] += val
            self.last_player[r][c] = player_val

        if type == 'row':
            self.row_status[r][c] = 1
            if r >= 1:
                self.board_status[r-1][c] += val
                self.last_player[r-1][c] = player_val

        elif type == 'col':
            self.col_status[r][c] = 1
            if c >= 1:
                self.board_status[r][c-1] += val
                self.last_player[r][c-1] = player_val
                
    def mark_box(self):
        boxes = np.argwhere(self.board_status == 4)
        global player1_score, player2_score
        one_marked = False
        for box in boxes:
            if list(box) not in self.already_marked_boxes and list(box) !=[]:
                self.already_marked_boxes.append(list(box))
                if self.last_player[box[0]][box[1]] == 1:
                    color = player2_color_light
                    player2_score = player2_score + 1                    
                else:
                    color = player1_color_light
                    player1_score = player1_score + 1
                self.shade_box(box, color)
                one_marked = True
                
        if one_marked == True:
            self.player1_turn = not self.player1_turn
    def is_gameover(self):
        return (self.row_status == 1).all() and (self.col_status == 1).all()
    
    def make_computer_move(self):
        #print(self.row_status)
        #print(self.col_status)
        #print(self.board_status)
        #print(self.last_player)
        best_move_result = self.minimax((self.row_status, self.col_status, self.board_status, self.last_player), 2, True)
        best_move = best_move_result[1]
        #print(best_move)

        return best_move
        # Verifică dacă există o mișcare validă
        '''
        if best_move is not None:
            self.update_board(best_move[0], best_move[1])
            self.make_edge(best_move[0], best_move[1])
            self.mark_box()
            self.refresh_board()
            if self.is_gameover():
                self.display_gameover()
            else:
                self.display_turn_text()
        '''
            
    def minimax(self, board, depth, maximizing_player):

        if depth == 0 or self.is_gameover():
            return self.evaluate(board[2],board[3]), None

        if maximizing_player:
            max_eval = float('-inf')
            best_move = (None, None)
            for move in self.get_possible_moves(board):
               # print(f"depth: {depth} , move: -> {move}")
                new_board, simulation_result = self.simulate_move(board, move, 1) # vezi daca s a facut box de la functia simulate_move, daca da atunci minimax cu True, altfel cu False cum e acum
                if simulation_result == False:
                    eval = self.minimax(copy.deepcopy(new_board), depth - 1, False)[0]
                else:
                    eval = self.minimax(copy.deepcopy(new_board), depth - 1, True)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                #print(board)
               # print(board[1])
                #print(f"indice x: {best_move[1][0]}, indice y: {best_move[1][1]}, valoare: {board[1][best_move[1][0]][best_move[1][1]]}")
                pass

            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = (None, None)
            for move in self.get_possible_moves(board):
                new_board, simulation_result = self.simulate_move(board, move, 2)
                if simulation_result == False:
                    eval = self.minimax(copy.deepcopy(new_board), depth - 1, True)[0]
                else:
                    eval = self.minimax(copy.deepcopy(new_board), depth - 1, False)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
            return min_eval, best_move
 
    def evaluate(self, board, last_turn):   ## Euristica gresita --> trb refacuta
        MAX_score = 0
        MIN_score = 0
    
        # Numărul de cutii capturate de fiecare jucător
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == 4:
                    if last_turn[i][j] == 1:
                        MAX_score += 2
                    else:
                        MIN_score += 2
    
        # Diferența de scor între jucători
        score_difference = MAX_score - MIN_score
    
        return score_difference
        # Returnează o valoare mai mare dacă jucătorul curent este în avantaj
        #if self.player1_turn:
         #   return score_difference
        #else:
         #   return -score_difference

    def get_possible_moves(self, board):
        possible_moves = []
        row_status = board[0]
        col_status = board[1]

        # Verifică fiecare punct pentru a vedea dacă poate fi conectat pentru a forma o cutie
        for i in range(len(row_status)):
            for j in range(len(row_status[0])):
                  if row_status[i][j] >  0-0.0001 and row_status[i][j] < 0 + 0.0001:
                        possible_moves.append(('row',(i,j)))
                        #rows
                       # if j>0 and self.row_status[i][j-1] == 0:
                       #     possible_moves.append(('row',(i,j-1)))
                       #  if j < len(self.row_status[0]) - 1 and self.row_status[i][j+1] == 0:
                       #     possible_moves.append(('row'),(i,j+1))
                        # cols
                        #if col_status[i][j] == 0:
                        #    possible_moves.append(('col',(i,j)))
                        #if i>0 and col_status[i-1][j] == 0:
                        #    possible_moves.append(('col',(i-1,j)))
                        #if j < len(row_status[0]) - 1 and col_status[i][j+1] == 0 :
                         #   possible_moves.append(('col',(i,j+1)))
                        #if i>0 and j < len(row_status[0]) - 1 and col_status[i-1][j+1] == 0:
                         #   possible_moves.append(('col',(i-1,j+1)))

        for i in range(len(col_status)):
            for j in range(len(col_status[0])):
                if col_status[i][j] == 0:
                    possible_moves.append(('col',(i,j)))
                    #rows
                    #if row_status[i][j] == 0:
                     #   possible_moves.append(('row',(i,j)))
                    #if i > 0 and row_status[i-1][j] == 0:
                     #   possible_moves.append(('row',(i-1,j)))
                    #if j > 0 and row_status[i][j-1] == 0:
                     #   possible_moves.append(('row',(i,j-1)))
                    #if i > 0 and j > 0 and row_status[i-1][j-1] == 0:
                     #   possible_moves.append(('row',(i-1,j-1))) 
        return possible_moves
        
        
        '''
        for i in range(len(board)):
            for j in range(len(board[0])):
                print(board[i][j])
                if i % 2 == 0 and j % 2 == 1 and board[i][j] == ' ':
                    if j > 0 and board[i][j - 1] == '-':
                        possible_moves.append(('row',(i, j))) 
                    if j < len(board[0]) - 1 and board[i][j + 1] == '-':
                        possible_moves.append(('row',(i, j)))
                elif i % 2 == 1 and j % 2 == 0 and board[i][j] == ' ':
                    if i > 0 and board[i - 1][j] == '|':
                        possible_moves.append(('col',(i, j)))
                    if i < len(board) - 1 and board[i + 1][j] == '|':
                        possible_moves.append(('col',(i, j)))
        '''
    
    def simulate_move(self, board, move, turn):
        #new_board = [row[:] for row in board]  # Crează o copie a tablei de joc pentru a nu o modifica direct
        row_status = board[0]
        col_status = board[1]
        board_status = board[2]
        last_player = board[3]

        new_row_status = copy.deepcopy(row_status)
        new_col_status = copy.deepcopy(col_status)
        new_board_status = copy.deepcopy(board_status)
        new_last_player = copy.deepcopy(last_player)

        r = move[1][0]
        c = move[1][1]
        #if move[0] == 'row':
            #print(f"input AI: --> x: {r}, y: {c} --> {new_row_status[r][c]}")
        val = 1
        player_val = turn
        box_completed = False
        type_ = move[0]

        if c < (number_of_dots-1) and r < (number_of_dots-1):
            new_board_status[r][c] += val
            new_last_player[r][c] = player_val

            if new_board_status[r][c] == 4:
                box_completed = True

        if type_ == 'row':
            new_row_status[r][c] = 1
            if r >= 1:
                new_board_status[r-1][c] += val
                new_last_player[r-1][c] = player_val
                if new_board_status[r-1][c] == 4:
                    box_completed = True

        elif type_ == 'col':
            new_col_status[r][c] = 1
            if c >= 1:
                new_board_status[r][c-1] += val
                new_last_player[r][c-1] = player_val
                if new_board_status[r][c-1] == 4:
                    box_completed = True

        new_board = (new_row_status, new_col_status, new_board_status, new_last_player)

        return new_board, box_completed

        '''
        if i % 2 == 0 and j % 2 == 1:
            # Se trasează o linie orizontală
            new_board[i][j] = '-'
            # Verifică dacă se completează o cutie
            if i > 0 and new_board[i - 1][j] == '|' and new_board[i - 1][j - 1] == '-' and new_board[i - 1][j + 1] == '-':
                new_board[i - 1][j] = 'Player2' if self.player1_turn else 'Player1'
        elif i % 2 == 1 and j % 2 == 0:
            # Se trasează o linie verticală
            new_board[i][j] = '|'
            # Verifică dacă se completează o cutie
            if j > 0 and new_board[i][j - 1] == '-' and new_board[i - 1][j - 1] == '|' and new_board[i + 1][j - 1] == '|':
                new_board[i][j - 1] = 'Player2' if self.player1_turn else 'Player1'
        '''


        
    def click(self, event, virtual_event = False, x = None, y = None):
        if not self.reset_board:
            if virtual_event == False:
                grid_position = [event.x, event.y]
                logical_position, valid_input = self.convert_grid_to_logical_position(grid_position)
            else:
                valid_input = x 
                logical_position = (y[1],y[0])
            if valid_input and not self.is_grid_occupied(logical_position, valid_input):
                self.update_board(valid_input, logical_position)
                self.make_edge(valid_input, logical_position)
                self.mark_box()
                self.refresh_board()
                self.player1_turn = not self.player1_turn
                if self.is_gameover():
                    self.display_gameover()
                else:
                    self.display_turn_text()
        else:
            self.canvas.delete("all")
            self.play_again()
            self.reset_board = False

    def AI_Move(self):
        help = self.make_computer_move()  
        self.click(None, True, help[0], help[1])
       # self.refresh_board()
       # self.display_turn_text()

root = Tk()
game_mode_selection = GameModeSelection(master=root)
game_mode_selection.mainloop()
