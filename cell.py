from tkinter import Button, Label, messagebox
import random
import settings
import sys


class Cell:
    all = []
    cell_count = settings.CELL_COUNT
    cell_count_label_object = None

    def __init__(self, x, y, is_mine=False):
        self.is_mine = is_mine
        self.is_opened = False
        self.cell_btn_object = None
        self.is_mine_candidate = False
        self.x = x
        self.y = y

        # Append the object to the Cell.all list.
        Cell.all.append(self)

    def create_btn_object(self, location):
        btn = Button(
            location,
            width=12,
            height=4,
        )
        btn.bind('<Button-1>', self.left_click_actions)     # Left Click
        btn.bind('<Button-3>', self.right_click_actions)    # Right Click
        self.cell_btn_object = btn

    @staticmethod
    def create_cell_count_label(location):
        # pass
        lbl = Label(
            location,
            bg='grey',
            fg='white',
            text=f'Cell Left:{settings.CELL_COUNT}',
            font=('', 36)
        )
        Cell.cell_count_label_object = lbl

    def left_click_actions(self, event):
        if self.is_mine:
            self.show_mine()
        else:
            if self.surrounded_cells_is_mine_length == 0:
                for cell_obj in self.surrounded_cells:
                    cell_obj.show_cell()
            self.show_cell()

        # If Mine count is equal to Cell count left, player won
        if Cell.cell_count == settings.MINES_COUNT:
            messagebox.showinfo('Gamer Over', 'You Won!!')
            sys.exit('You Won!!')
        # Cancel Left and Right click events if cell is already opened:
        self.cell_btn_object.unbind('<Button-1>')
        self.cell_btn_object.unbind('<Button-3>')

    def get_cell_by_axis(self, x, y):
        # Return a cell object based on value of x, y
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell

    @property
    def surrounded_cells(self):
        cells = [
            self.get_cell_by_axis(self.x - 1, self.y - 1),
            self.get_cell_by_axis(self.x, self.y - 1),
            self.get_cell_by_axis(self.x + 1, self.y - 1),
            self.get_cell_by_axis(self.x + 1, self.y),
            self.get_cell_by_axis(self.x + 1, self.y + 1),
            self.get_cell_by_axis(self.x, self.y + 1),
            self.get_cell_by_axis(self.x - 1, self.y + 1),
            self.get_cell_by_axis(self.x - 1, self.y)
        ]
        cells = [cell for cell in cells if cell is not None]
        return cells

    @property
    def surrounded_cells_is_mine_length(self):
        count = 0
        for cell in self.surrounded_cells:
            if cell.is_mine:
                count += 1
        return count

    def show_cell(self):
        if not self.is_opened:
            Cell.cell_count -= 1
            self.cell_btn_object.configure(text=self.surrounded_cells_is_mine_length)
            # Replace the text of cell count label with the newer count
            if Cell.cell_count_label_object:
                Cell.cell_count_label_object.configure(
                    text=f'Cells Left: {Cell.cell_count}'
                )
            # If this was mine candidate, then for safety.we should
            # configure the background to original color
            self.cell_btn_object.configure(
                bg='gray85'
            )
            # Mark the cell as opened (Use it as the last line of this method)
            self.is_opened = True

    def show_mine(self):
        # A logic to interrupt the game and display a message that Player lost!
        self.cell_btn_object.configure(bg='red')
        messagebox.showinfo('Game Over', 'You Lost')
        sys.exit('Game Over,You Lost')

    def right_click_actions(self, event):
        if not self.is_mine_candidate:
            self.cell_btn_object.configure(
                bg='Orange'
            )
            self.is_mine_candidate = True
        else:
            self.cell_btn_object.configure(
                bg='gray85'
            )
            self.is_mine_candidate = False

    @staticmethod
    def randomize_mines():
        picked_cells = random.sample(
            Cell.all,
            settings.MINES_COUNT
        )
        for picked_cell in picked_cells:
            picked_cell.is_mine = True

    def __repr__(self):
        return f'Cell({self.y}, {self.x})'
