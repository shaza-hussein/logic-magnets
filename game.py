
from tkinter import *
import random
import time
from tkinter import messagebox
from collections import deque



window = Tk()
window.title('Logic Magnets')



n = 4
cell_size = 60
colors = ["gray", "purple", "red", "green"]



empty_cells = []
pieces = {}
green_cells = []
active_piece = None




class Node:
    def __init__(self, state, parent=None, action=None):
        self.state = state
        self.parent = parent
        self.action = action

    def get_path(self):
        path = []
        node = self
        while node:
            path.append(node.state)
            node = node.parent
        return path[::-1]  





def encode_state(pieces, empty_cells):
    return tuple(sorted(pieces.items())), tuple(sorted(empty_cells))

def decode_state(state):
    pieces, empty_cells = dict(state[0]), list(state[1])
    return pieces, empty_cells





def bfs(start_state):
    queue = deque([Node(start_state)])
    visited = set()
    visited.add(start_state)

    while queue:
        current_node = queue.popleft()
        if is_goal_state(current_node.state):
            return current_node.get_path() 

        for new_state in generate_possible_states(current_node.state):
            if new_state not in visited:
                visited.add(new_state)
                queue.append(Node(new_state, parent=current_node))
    return None  





def dfs(start_state):
    stack = [Node(start_state)]
    visited = set()
    visited.add(start_state)

    while stack:
        current_node = stack.pop()
        if is_goal_state(current_node.state):
            return current_node.get_path()  

            

        for new_state in generate_possible_states(current_node.state):
            if new_state not in visited:
                visited.add(new_state)
                stack.append(Node(new_state, parent=current_node))
                
    return None  




def is_goal_state(state):
    pieces, _ = decode_state(state)
    return all(cell in pieces for cell in green_cells)






def generate_possible_states(state):
    pieces, empty_cells = decode_state(state)
    possible_states = []

    for (row, col), color in pieces.items():
        if color in ["red", "purple"]:  
            for d_row, d_col in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  
                new_row, new_col = row + d_row, col + d_col
                if 0 <= new_row < n and 0 <= new_col < n and (new_row, new_col) in empty_cells:
                
                    new_pieces = pieces.copy()
                    new_pieces[(new_row, new_col)] = new_pieces.pop((row, col))
                    new_empty_cells = empty_cells.copy()
                    new_empty_cells.remove((new_row, new_col))
                    new_empty_cells.append((row, col))

                    
                    if color == "red":
                        new_pieces, new_empty_cells = attract_pieces_in_state(new_row, new_col, new_pieces, new_empty_cells)
                    elif color == "purple":
                        new_pieces, new_empty_cells = repel_pieces_in_state(new_row, new_col, new_pieces, new_empty_cells)

                    new_state = encode_state(new_pieces, new_empty_cells)
                    possible_states.append(new_state)

    return possible_states



def attract_pieces_in_state(row, col, pieces, empty_cells):
    for r in range(n):
        if (r, col) in pieces and pieces[(r, col)] in ["gray", "purple"]:
            pieces, empty_cells = move_piece_towards_in_state(r, col, row, col, pieces, empty_cells)
    
    for c in range(n):
        if (row, c) in pieces and pieces[(row, c)] in ["gray", "purple"]:
            pieces, empty_cells = move_piece_towards_in_state(row, c, row, col, pieces, empty_cells)

    return pieces, empty_cells




def move_piece_towards_in_state(from_row, from_col, to_row, to_col, pieces, empty_cells):
    new_row, new_col = from_row, from_col
    if from_row < to_row:
        new_row += 1
    elif from_row > to_row:
        new_row -= 1
    if from_col < to_col:
        new_col += 1
    elif from_col > to_col:
        new_col -= 1
    
    if (new_row, new_col) in empty_cells:
        pieces[(new_row, new_col)] = pieces[(from_row, from_col)]
        del pieces[(from_row, from_col)]
        empty_cells.append((from_row, from_col))
        empty_cells.remove((new_row, new_col))

    return pieces, empty_cells




def repel_pieces_in_state(row, col, pieces, empty_cells):
    for r in range(n):
        if (r, col) in pieces and pieces[(r, col)] in ["gray", "red"]:
            pieces, empty_cells = move_piece_away_in_state(r, col, row, col, pieces, empty_cells)

    for c in range(n):
        if (row, c) in pieces and pieces[(row, c)] in ["gray", "red"]:
            pieces, empty_cells = move_piece_away_in_state(row, c, row, col, pieces, empty_cells)

    return pieces, empty_cells





def move_piece_away_in_state(from_row, from_col, away_row, away_col, pieces, empty_cells):
    new_row, new_col = from_row, from_col
    if from_row < away_row and new_row > 0:
        new_row -= 1
    elif from_row > away_row and new_row < n - 1:
        new_row += 1
    if from_col < away_col and new_col > 0:
        new_col -= 1
    elif from_col > away_col and new_col < n - 1:
        new_col += 1
    
    if (new_row, new_col) in empty_cells:
        pieces[(new_row, new_col)] = pieces[(from_row, from_col)]
        del pieces[(from_row, from_col)]
        empty_cells.append((from_row, from_col))
        empty_cells.remove((new_row, new_col))

    return pieces, empty_cells






def select_piece(event, row, col):
    global active_piece
    if pieces.get((row, col)) in ["red", "purple"]:
        active_piece = (row, col)

def move_to_empty_cell(event, target_row, target_col):
    global active_piece, empty_cells, pieces

    if active_piece and (target_row, target_col) in empty_cells:
        piece_color = pieces[active_piece]
        pieces[(target_row, target_col)] = piece_color
        del pieces[active_piece]

        empty_cells.append(active_piece)
        empty_cells.remove((target_row, target_col))

        if piece_color == "red":
            attract_pieces(target_row, target_col)
        elif piece_color == "purple":
            repel_pieces(target_row, target_col)

        draw_board()
        check_win_condition()
        active_piece = None

def attract_pieces(row, col):
    global empty_cells, pieces

    for r in range(n):
        if (r, col) in pieces and pieces[(r, col)] == "gray":
            move_piece_towards(r, col, row, col)
    
    for c in range(n):
        if (row, c) in pieces and pieces[(row, c)] == "gray":
            move_piece_towards(row, c, row, col)

def move_piece_towards(from_row, from_col, to_row, to_col):
    global empty_cells, pieces
    
    new_row, new_col = from_row, from_col
    if from_row < to_row:
        new_row += 1
    elif from_row > to_row:
        new_row -= 1
    if from_col < to_col:
        new_col += 1
    elif from_col > to_col:
        new_col -= 1
    
    if (new_row, new_col) in empty_cells:
        pieces[(new_row, new_col)] = pieces[(from_row, from_col)]
        del pieces[(from_row, from_col)]
        empty_cells.append((from_row, from_col))
        empty_cells.remove((new_row, new_col))

def repel_pieces(row, col):
    global empty_cells, pieces

    for r in range(n):
        if (r, col) in pieces and pieces[(r, col)] == "gray":
            move_piece_away(r, col, row, col)

    for c in range(n):
        if (row, c) in pieces and pieces[(row, c)] == "gray":
            move_piece_away(row, c, row, col)

def move_piece_away(from_row, from_col, away_row, away_col):
    global empty_cells, pieces

    new_row, new_col = from_row, from_col
    if from_row < away_row and new_row > 0:
        new_row -= 1
    elif from_row > away_row and new_row < n - 1:
        new_row += 1
    if from_col < away_col and new_col > 0:
        new_col -= 1
    elif from_col > away_col and new_col < n - 1:
        new_col += 1
    
    if (new_row, new_col) in empty_cells:
        pieces[(new_row, new_col)] = pieces[(from_row, from_col)]
        del pieces[(from_row, from_col)]
        empty_cells.append((from_row, from_col))
        empty_cells.remove((new_row, new_col))

def create_board():
    global empty_cells, pieces, green_cells
    
    num_green_cells = random.randint(3, 8)
    green_cells = random.sample([(i, j) for i in range(n) for j in range(n)], num_green_cells)

    num_colored_pieces = len(green_cells)
    special_positions = random.sample([(i, j) for i in range(n) for j in range(n) if (i, j) not in green_cells], num_colored_pieces // 2)
    gray_positions = random.sample([(i, j) for i in range(n) for j in range(n) if (i, j) not in green_cells and (i, j) not in special_positions], num_colored_pieces - len(special_positions))

    for row in range(n):
        for col in range(n):
            if (row, col) in special_positions:
                color = random.choice(["purple", "red"])
                pieces[(row, col)] = color
            
            elif (row, col) in gray_positions:
                pieces[(row, col)] = "gray"
            
            elif (row, col) in green_cells:
                empty_cells.append((row, col))
                
            else:
                empty_cells.append((row, col))

def check_win_condition():
    if all(cell in pieces for cell in green_cells):
        messagebox.showinfo("Congratulations!", "You have won the game!")
        reset_board()

def reset_board():
    global empty_cells, pieces, green_cells
    empty_cells.clear()
    pieces.clear()
    green_cells.clear()
    create_board()
    draw_board()

def draw_board():
    for widget in window.winfo_children():
        widget.destroy()

    for row in range(n):
        for col in range(n):
            bg_color = "green" if (row, col) in green_cells else "white"
            cell = Frame(window, width=cell_size, height=cell_size, bg=bg_color, highlightbackground="black", highlightthickness=1)
            cell.grid(row=row, column=col)
            
            if (row, col) in pieces:
                color = pieces[(row, col)]
                piece_canvas = Canvas(cell, width=cell_size, height=cell_size, bg=bg_color, highlightthickness=0)
                radius = cell_size // 2 - 5
                x0, y0 = (cell_size - radius * 2) // 2, (cell_size - radius * 2) // 2
                piece_canvas.create_oval(x0, y0, x0 + radius * 2, y0 + radius * 2, fill=color, outline="")  # Draw piece
                piece_canvas.pack()

                if color in ["red", "purple"]:
                    piece_canvas.bind("<Button-1>", lambda event, r=row, c=col: select_piece(event, r, c))
            
            else:
                cell.bind("<Button-1>", lambda event, r=row, c=col: move_to_empty_cell(event, r, c))

def animate_solution(solution_path):
    for state in solution_path:
        global pieces, empty_cells
        pieces, empty_cells = decode_state(state)
        draw_board()
        window.update() 
        time.sleep(0.5)  
    

    messagebox.showinfo("Congratulations!", "Solution found and completed!")



def solve_with_bfs():
    start_state = encode_state(pieces, empty_cells)
    solution = bfs(start_state)
    if solution:
        animate_solution(solution)
    else:
        messagebox.showinfo("No Solution", "No solution found using BFS.")



def solve_with_dfs():
    start_state = encode_state(pieces, empty_cells)
    solution = dfs(start_state)
    if solution:
        animate_solution(solution)
    else:
        messagebox.showinfo("No Solution", "No solution found using DFS.")

create_board()
draw_board()


solve_button_bfs = Button(window, text="Solve with BFS", command=solve_with_bfs)
solve_button_bfs.grid(row=n, column=0, columnspan=n)

solve_button_dfs = Button(window, text="Solve with DFS", command=solve_with_dfs)
solve_button_dfs.grid(row=n+1, column=0, columnspan=n)  

window.mainloop()
