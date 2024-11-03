
from tkinter import *
import random
from tkinter import messagebox

window = Tk()
window.title('Logic Magnets')

n = 5
cell_size = 60
colors = ["gray", "purple", "red", "green"]

empty_cells = []
pieces = {}
green_cells = []
active_piece = None




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
        if (r, col) in pieces and pieces[(r, col)] in ["gray", "purple"]:
            move_piece_towards(r, col, row, col)
    
    for c in range(n):
        if (row, c) in pieces and pieces[(row, c)] in ["gray", "purple"]:
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
        if (r, col) in pieces and pieces[(r, col)] in ["gray", "red"]:
            move_piece_away(r, col, row, col)

    for c in range(n):
        if (row, c) in pieces and pieces[(row, c)] in ["gray", "red"]:
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
                piece_canvas.create_oval(x0, y0, x0 + radius * 2, y0 + radius * 2, fill=color, outline="")
                piece_canvas.pack()

                if color in ["red", "purple"]:
                    piece_canvas.bind("<Button-1>", lambda event, r=row, c=col: select_piece(event, r, c))
            
            else:
                cell.bind("<Button-1>", lambda event, r=row, c=col: move_to_empty_cell(event, r, c))

create_board()
draw_board()

window.mainloop()