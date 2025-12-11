from random import randint
from UMD_player import Player
from UMD_property import UMDProperty
from board import MakeBoard
from decision_engine import decision_engine
from event_generator import event_generator
from save import save_game


class Game:
    def __init__(self, mode="player_vs_cpu", p1="Player 1", p2="Player 2"):
        self.board = MakeBoard()

        # player setup
        if mode == "player_vs_cpu":
            self.player = Player(p1, "@")   # Use actual name for player 1
            self.cpu = Player("CPU", "#")
            self.cpu_enabled = True
        else:
            self.player = Player(p1, "@")
            self.cpu = Player(p2, "#")      # if pvp add player 2 instead of cpu
            self.cpu_enabled = False

        # Register both tokens on board which will then give them their position
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
        self.max_turns = 150
        self.current_player = "player"

    def get_property_from_symbol(self, symbol):
        # maps the board symbols to the umd properties
        mapping = self.board.prop_mapping

        if symbol not in mapping:
            return None  # event, jail, rent, etc.

        # First check if any property with this symbol is owned (for rent)
        for p in mapping[symbol]:
            if p.owner is not None:
                return p

        # If none owned, return first unowned (for buying)
        for p in mapping[symbol]:
            if p.owner is None:
                return p

        return mapping[symbol][0]

    def take_turn(self):
        current = self.player
        print("\nTurn:", self.turn_count + 1)

        roll = randint(1, 6)
        print(f"{current.name} rolled a {roll}")
        

        # Move player and update board
        current.move(roll, 40)
        self.board.players[current.token] = current.position
        self.board.display_board()

        # Tile symbol
        tile_symbol = self.board.get_tile(current.position)
        print(f"{current.name} landed on: {tile_symbol}")

        # Handle tile
        self.handle_tile(current, tile_symbol)

        # Player loses
        if current.cash <= 0:
            print(f"{current.name} is out of money. Game over.")
            return False

        return True

    def cpu_take_turn(self):
        roll = randint(1, 6)
        current = self.cpu  # Could be CPU or Player 2 depending on what user selected

        if self.cpu_enabled:
            print("\nCPU TURN:")
            print("CPU rolled:", roll)
        else:
            print(f"\n{current.name}'s TURN:")
            print(f"{current.name} rolled: {roll}")

        current.move(roll, 40)
        self.board.players[current.token] = current.position
        self.board.display_board()

        tile_symbol = self.board.get_tile(current.position)

        if self.cpu_enabled:
            print("CPU landed on:", tile_symbol)
        else:
            print(f"{current.name} landed on:", tile_symbol)

        self.handle_tile(current, tile_symbol)

        if current.cash <= 0:
            if self.cpu_enabled:
                print("CPU is out of money. YOU WIN!")
            else:
                print(f"{current.name} is out of money. GAME OVER!")
            return False

        return True

    def handle_tile(self, player, tile_symbol):

        # Event tile
        if tile_symbol == "E":
            print(player.name, "triggered an Event!")   
            event_generator()
            return

        # Jail tile
        if tile_symbol == "J":
            print(player.name, "is in jail.")
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

        if prop.owner is None:
            self.buy_logic(player, prop)
        else:
            self.rent_logic(player, prop)

    def buy_logic(self, player, prop):
        """Buy decisions for human and CPU"""

        cost = prop.cost
        player_properties = []
        # CPU logic
        if player.name == "CPU":
            result = decision_engine(player.cash, cost, prop.code, "mid")
            print("CPU decision:", result["decision"])

            if result["decision"] == "buy":
                player.buy_property(prop)
                player_properties.append(prop.name)
            else:
                print("CPU skipped buying.")
            return

        # Human player logic
        print("Property cost:", cost)

        while True:
            choice = input("Buy it? (y/n): ").strip().lower()

            if choice == "y":
                player.buy_property(prop)
                player_properties.append(prop.name)
                break
            elif choice == "n":
                print(f"{player.name} skipped buying.")
                break
            else:
                print("Invalid input. Please enter 'y' or 'n'.")
        print(f"{player.name} now owns: {', '.join(player_properties)}")
    def rent_logic(self, player, prop):
        owner = prop.owner

        if owner == player:
            print(f"{player.name} already owns this property.")
            return
        elif owner !=player and owner:
            print(f"{prop.name} is owned by {owner.name}.")

        # Monopoly logic
        monopoly = owner.has_monopoly(prop.group)

        rent = prop.calculate_rent(owner_has_monopoly=monopoly)
        rent *= 7 # Speed up game
        print(f"{player.name} owes ${rent} to {owner.name}")

        player.pay_rent(rent, owner)

    def turn(self):
        # Game ends at turn limit
        if self.turn_count >= self.max_turns:
            print("\nReached turn limit. Ending game...")
            return False

        self.turn_count += 1

        if self.current_player == "player":
            alive = self.take_turn()
            self.current_player = "cpu"
        else:
            alive = self.cpu_take_turn()
            self.current_player = "player"
        print(self)
        return alive

    def end_game(self):
        print("\nGame over!")

        # this will give the data for not just player 1 but also player 2. before we only had player 1 save data
        player1_data = {
        "name": self.player.name,
        "cash": self.player.cash,
        "properties": [prop.to_dict() for prop in self.player.properties]
        }

        player2_data = {
        "name": self.cpu.name,
        "cash": self.cpu.cash,
        "properties": [prop.to_dict() for prop in self.cpu.properties]
        }

        # Full saved game state
        game_state = {
        "turns_played": self.turn_count,
        "players": [player1_data, player2_data]
        }

        save_game(game_state)


    def __str__(self):
        player_props = "None"
        cpu_props = "None"

        if self.player.properties:
            player_props = ",".join([prop.name for prop in self.player.properties])
        if self.cpu.properties:
            cpu_props = ",".join([prop.name for prop in self.cpu.properties])

        return (
            f"Properties\n"
            f"{self.player.name} owns:{player_props}\n"
            f"{self.cpu.name} owns:{cpu_props}"
        )


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
    mode = "player_vs_cpu" if choice == "1" else "pvp"
    if choice == "1":
        print("Player1 position on the board is @")
        print("CPU position on the board is #")
    else:
        print("Player1 position on the board is @")
        print("Player2 position on the board is #")

    # Ask for Player 1 name
    
    p1 = input("\nEnter Player 1 name: ").strip()
    if p1 == "":
        p1 = "Player 1"

    # PvP: ask for Player 2 name
    
    if mode == "pvp":
        
        p2 = input("Enter Player 2 name: ").strip()
        if p2 == "":
            p2 = "Player 2"
    else:
        p2 = "CPU"

    # Start game with names
    game = Game(mode, p1=p1, p2=p2)
    game.run()