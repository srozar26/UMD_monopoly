from random import randint


from board import MakeBoard       
from property import Property

from event_generator import event_generator
from decision_engine import decision_engine
from save import save_game




class Game:
   def __init__(self):
        self.board = MakeBoard()
        self.player = Player("Testudo")
        self.cpu = Player("CPU")  # CPU player added
        self.board.players["@"] = 0     # human player
        self.board.players["#"] = 20    # cpu 
        self.current_player = "player"
        self.turn_count = 0
        self.turn_count_max = 5  # stops infinite rolling
       
      
   def take_turn(self):
      
       self.turn_count += 1
       print("\nTurn,", self.turn_count)
      
       roll = randint(1,6)
       print("\nYou rolled a", roll)
       
         # move player along the edge path
        self.player.move(roll, 40)  # 40 because 11+11+9+9 for perimeter of board
        self.board.players["@"] = self.player.position

        # Display current board
        self.board.display_board()
        
        
        # tile the player landed on
        row, col = self.board.position_to_coords(self.player.position)
        tile_symbol = self.board.board_layout[row].split()[col]
        
         print(f"You landed on tile symbol: {tile_symbol}")
      

       # make code for if the space is the starting spot
      
       # make code for if the space has an event
      
       # make code for if the space has a property
      
       # make code if the space has not be claimed by a player or the cpu yet. We can just make this to determine whether or not the cpu buys it
      
       # then make code for if you already own the property and then must pay rent
      
      
       # code for if a player is out of money (game over)
       

    
       if self.player.cash <= 0:
           print("You hare out of money. Game over.")
           return False
       return True
   

   
    def cpu_take_turn(self):
    self.turn_count += 1
    print("\nTurn", self.turn_count)

    roll = randint(1, 6)
    print("CPU rolled a", roll)

    #will move the cpu pieve
    self.cpu.move(roll, self.board.size())

    #gets the tile for the cpu
    tile = self.board.get_tile(self.cpu.position)

    # TODO: handle events, properties, rent, etc.

       
        
   def turn(self):
       #this code will decide whos turn it is and take it
       #if we decide to implement player vs player we can add to this code
    if self.current_player == "player":
        self.take_turn()
        self.current_player = "cpu"
    else:
        self.cpu_take_turn()
        self.current_player = "player"

            
   
    def __str__ (self):
        "Gives an update of the board and whos turn it is"
        "Will need the board for this to work"
        "Can implement after each turn "
        return f"Current Player:{self.current_player}\nBoard:{self.Board}"
      
    
    def end_game(self): 
        
        """this gives each player what their cash and properties were."""
        
        print("\nGame over")
        print("Total cash:", self.player.cash)
        print("Properties owned:", self.player.properties)

        save_game({
            "cash": self.player.cash,
            "properties": self.player.properties,
            "turns": self.turn_count
        })
   
    if __name__ =="__main__":
   #code here should be to run the game and then once done just type in terminal 'python game.py'
    

