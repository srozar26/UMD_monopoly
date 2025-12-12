from typing import List, Dict

"""
T=T-row
V=Varsity
U=Union
H= Hub
C= Towers
J=jail
E = event
M= McKeldin
D= Dining hall
R = Rent a house

"""
class MakeBoard:
    def __init__(self):
        self.board_layout = [
            "C V M U U H D1 V X M E",
            "T                   M",
            "T3                   U",
            "U                   T2",
            "H                   J",
            "S                   V",
            "E                   E",
            "C                   V",
            "C                   V",
            "M                   M",
            "J D3 C E T H R R D2 H E",
        ]
        
        
        self.players = {
            "@": 0,  # Player 1 starts at bottom right
            "#": 20  # Player 2 starts top left
        }
        
        self.size = 11  # Board is 11x11
    
    def display_board(self):
        """Show current board with player positions"""
        #build grid
        grid = []
        for i in range(self.size):
            if i == 0:
                grid.append(self.board_layout[0].split())
            elif i == self.size - 1:
                grid.append(self.board_layout[-1].split())
            else:
                row = [""] * self.size
                parts = self.board_layout[i].split()
                row[0] = parts[0]
                row[-1] = parts[-1]
                grid.append(row)
        
        #find where each player is
        player_cells = {}
        for player_char, pos in self.players.items():
            #calculate grid position from the position number
            if pos < self.size: 
                row = self.size - 1
                col = self.size - 1 - pos
            elif pos < self.size + (self.size - 2): 
                row = self.size - 2 - (pos - self.size)
                col = 0
            elif pos < 2 * self.size + (self.size - 2):
                row = 0
                col = pos - (self.size + (self.size - 2))
            else: 
                row = pos - (2 * self.size + (self.size - 2)) + 1
                col = self.size - 1
            
            player_cells[(row, col)] = player_char
        
        #make board
        border = "+" + ("---+" * self.size)
        print(border)
        
        for row in range(self.size):
            line = "|"
            for col in range(self.size):
                cell = grid[row][col] if grid[row][col] else " "
                
                #add player if at this cell
                if (row, col) in player_cells:
                    cell = f"{cell}{player_cells[(row, col)]}"
                
                line += cell.center(3) + "|"
            print(line)
            print(border)
            
    def get_tile(self, position):
        bottom = self.board_layout[-1].split()
        top = self.board_layout[0].split()
        left = [self.board_layout[i].split()[0] for i in range(9, 0, -1)]
        right = [self.board_layout[i].split()[-1] for i in range(1, 10)]
        
        all_tiles = bottom[::-1] + left + top + right
        return all_tiles[position % 40]


if __name__ == "__main__":
    game = MakeBoard()
    game.display_board()
