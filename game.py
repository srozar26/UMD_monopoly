from Random import randint
# still need board, player, and property import
from event_generator import event_generator
from decision_engine import decision_engine
from save import save_game




class game:
   def__init__(self):
       self.event = event_generator()
       #add board and player attributes here
       self.cpu = decision_engine()
       self.save = save_game()
       
      
      
       self.turn_count = 0
       
      
   def take_turn(self):
      
       self.turn_count += 1
       print("\nTurn,", self.turn_count)
      
       roll = randint(1,6)
       print("\nYou rolled a", roll)
      
       """
       the 2 lines below may need to be changed depending on what the code for the player and board files have for names.
       For right now, this is what i put to deal with a player moving x amount of spaces depending on roll and where they will land in respect to the board
       """
       self.player.move(roll, self.board.size())
       tile = self.board.get_tile(self.player.position)
      
       # make code for if the space is the starting spot
      
       # make code for if the space has an event
      
       # make code for if the space has a property
      
       # make code if the space has not be claimed by a player or the cpu yet. We can just make this to determine whether or not the cpu buys it
      
       #  then make code for if you already own the property and then must pay rent
      
      
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
      
  
    if __name__ =="__main__":
   #code here should be to run the game and then once done just type in terminal 'python game.py'
    

