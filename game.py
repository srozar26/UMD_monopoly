from random import randint
from UMD_player import Player
from UMD_property import UMDProperty
from board import MakeBoard
from decision_engine import decision_engine
from event_generator import event_generator
from save import save_game



class Game:
    def __init__(self, mode="pvc"):
        self.board = MakeBoard()
        
        # player setup

        if mode == "pvc":
            self.player = Player("Player 1", "@")
            self.cpu = Player("CPU", "#")
            self.cpu_enabled = True
        else:
            self.player = Player("Player 1", "@")
            self.cpu = Player("Player 2", "#")
            self.cpu_enabled = False

        # Register both tokens on board
        self.board.players = {
            self.player.token: self.player.position,
            self.cpu.token: self.cpu.position
        }

        # Property list from UMD_property.py
        self.all_properties = UMDProperty.create_UMD_board()

        # Create mapping from board symbols to properties
        self.board.prop_mapping = {}
        for prop in self.all_properties:
            symbol = prop.code[0]
            if symbol not in self.board.prop_mapping:
                self.board.prop_mapping[symbol] = []
            self.board.prop_mapping[symbol].append(prop)

        self.turn_count = 0
        self.current_player = "player"
        
   
    def get_property_from_symbol(self, symbol):
        # maps the board symbols to the umd properties
        mapping = self.board.prop_mapping

        if symbol not in mapping:
            return None  # event, jail, rent, etc.

        # return first unowned, otherwise first in group
        for p in mapping[symbol]:
            if p.owner is None:
                return p

        return mapping[symbol][0]
    

   
    def take_turn(self):
        current = self.player
        print("\nTurn:", self.turn_count + 1)

        roll = randint(1, 6)
        print("You rolled a", roll)

        # Move player and update board
        current.move(roll, 40)  # 40 because 11+11+9+9 for perimeter of board
        self.board.players[current.token] = current.position
        self.board.display_board()

        # Tile symbol
        tile_symbol = self.board.get_tile(current.position)
        print("You landed on:", tile_symbol)

        # Handle tile
        self.handle_tile(current, tile_symbol)
        
        # code for if a player is out of money (game over)

        if current.cash <= 0:
            print("You are out of money. Game over.")
            return False

        return True
    

 
    def cpu_take_turn(self):
        roll = randint(1, 6)
        current = self.cpu
        if self.cpu_enabled:
            print("\nCPU TURN:")
            print("CPU rolled:", roll)
        else:
            print(f"\n{current.name}'s TURN:")
            print(f"{current.name} rolled:", roll)

        current.move(roll, 40)
        self.board.players[current.token] = current.position
        self.board.display_board()

        tile_symbol = self.board.get_tile(current.position)
        print("CPU landed on:", tile_symbol)

        self.handle_tile(current, tile_symbol)

        if current.cash <= 0:
            if self.cpu_enabled:
                print("CPU is out of money. You win!")
            else:
                print(f"{current.name} is out of money. Game over!")
            return False


        return True
    

  
    def handle_tile(self, player, tile_symbol):

        # Event tile
        if tile_symbol == "E":
            print(player.name, "triggered an EVENT!")
            event_generator()
            return

        # Jail tile
        if tile_symbol == "J":
            print(player.name, "is just visiting jail.")
            return

        # Scooter rental
        if tile_symbol == "R":
            rent = randint(1, 6) * 20
            print(player.name, "paid scooter rent:", rent)
            player.cash -= rent
            return

        # Property tile
        prop = self.get_property_from_symbol(tile_symbol)
        if prop is None:
            print("Blank or unsupported tile.")
            return

        print(player.name, "landed on property:", prop.name)

        # If unowned 
        if prop.owner is None:
            self.buy_logic(player, prop)
        else:
            self.rent_logic(player, prop)


    def buy_logic(self, player, prop):
        """Buy decision for human and CPU"""

        cost = prop.cost

        # CPU logic
        if player.name == "CPU":
            result = decision_engine(player.cash, cost, prop.code, "mid")
            print("CPU decision:", result["decision"])

            if result["decision"] == "buy":
                player.buy_property(prop)
            else:
                print("CPU skipped buying.")
            return

        # Human player logic
        print("Property cost:", cost)
        choice = input("Buy it? (y/n): ")

        if choice.lower() == "y":
            player.buy_property(prop)
        else:
            print("You skipped buying.")


   
    def rent_logic(self, player, prop):
        owner = prop.owner

        if owner == player:
            print("You already own this property.")
            return

        # Monopoly logic
        monopoly = owner.has_monopoly(prop.group)

        rent = prop.calculate_rent(owner_has_monopoly=monopoly)
        print(f"{player.name} owes ${rent} to {owner.name}")

        player.pay_rent(rent, owner)


   
    def turn(self):
        #this code will decide whos turn it is and take it
        #if we decide to implement player vs player we can add to this code
        
        self.turn_count += 1

        if self.current_player == "player":
            alive = self.take_turn()
            self.current_player = "cpu"
        else:
            # CPU may also be Player 2 if PvP
            alive = self.cpu_take_turn()
            self.current_player = "player"

        return alive
        
        
        
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

            
   
    def __str__ (self):
        "Gives an update of the board and whos turn it is"
        "Will need the board for this to work"
        "Can implement after each turn "
        return f"Current Player:{self.current_player}\nBoard:{self.board}"
    
    
    def run(self):
        print("Game Started!")

        while True:
            alive = self.turn()
            if not alive:
                self.end_game()
                break



if __name__ == "__main__":
    print("Select game mode:")
    print("1. Player vs CPU")
    print("2. Player vs Player")
    
    choice = input("Enter 1 or 2: ")

    mode = "pvc" if choice == "1" else "pvp"

    game = Game(mode)
    game.run()
