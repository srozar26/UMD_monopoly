from typing import List, Dict, Optional, Set
from datetime import datetime
from UMD_property import UMDProperty

class Player:
    """
    Represents a player in UMD-themed Monopoly.
    """
    
    def __init__(self, name: str, token: str = "@", cash: int = 1500, position: int = 0):
        """
        Initialize a new player.
        
        Args:
            name: Player's name
            token: Board token symbol (default "@")
            cash: Starting cash (default 1500)
            position: Starting board position (default 0)
        """
        self.name = name
        self.token = token
        self.cash = cash
        self.position = position
        self.properties = []  # Composition with Property objects
        self.in_jail = False
        self.jail_turns = 0
        self.get_out_of_jail_cards = 0
        self.bankrupt = False
        
        # Track owned property groups
        self.owned_groups: Dict[str, List[str]] = {}
        self.monopolies: Set[str] = set()
        
        # Player statistics
        self.turns_played = 0
        self.total_moves = 0
        self.properties_bought = 0
        
    def __str__(self):
        """String representation of player."""
        jail_status = " (IN JAIL)" if self.in_jail else ""
        bankrupt_status = " (BANKRUPT)" if self.bankrupt else ""
        # f-string containing expression
        property_count = len(self.properties)
        return f"Player {self.name}: ${self.cash}, {property_count} properties{jail_status}{bankrupt_status}"
    
    def __repr__(self):
        """Detailed representation."""
        return f"Player(name='{self.name}', cash={self.cash}, position={self.position})"
    
    def move(self, spaces: int, board_size: int = 40):
        """
        Move player around the board.
        
        Primary Author: [Your Name Here]
        Technique: f-strings containing expressions
        """
        old_position = self.position
        self.position = (self.position + spaces) % board_size
        self.total_moves += 1
        
        # Check if player passed GO (position 0)
        if (old_position + spaces) >= board_size:
            self.cash += 200
            # f-string containing expression here
            print(f"{self.name} passed GO! Collected $200. Total: ${self.cash}")
        
        return self.position
    
    def buy_property(self, property_obj, property_cost: Optional[int] = None):
        """
        Attempt to buy a property.
        
        Args:
            property_obj: Property object to buy
            property_cost: Optional custom price
            
        Returns:
            True if purchase successful
        """
        cost = property_cost if property_cost is not None else property_obj.cost
        
        # Conditional expression used here
        can_afford = True if self.cash >= cost else False
        
        if not can_afford:
            print(f"{self.name} cannot afford {property_obj.name} (${cost}). Cash: ${self.cash}")
            return False
        
        if property_obj.owner is not None:
            print(f"{property_obj.name} is already owned by {property_obj.owner}")
            return False
        
        # to make purchases
        self.cash -= cost
        property_obj.set_owner(self)
        self.properties.append(property_obj)
        self.properties_bought += 1
        
        # Update group tracking
        if property_obj.group:
            if property_obj.group not in self.owned_groups:
                self.owned_groups[property_obj.group] = []
            self.owned_groups[property_obj.group].append(property_obj.code)
            
            # Check for monopoly
            self._check_monopoly(property_obj.group)
        
        print(f"{self.name} bought {property_obj.name} for ${cost}. Cash remaining: ${self.cash}")
        return True
    
    def _check_monopoly(self, group_name):
        """
        Check if player has monopoly on a property group.
        
        Returns:
            True if monopoly achieved
        """
        
        if group_name not in self.owned_groups:
            return False
    
        owned_count = len(self.owned_groups[group_name])
        group_info = UMDProperty.PROPERTY_GROUPS.get(group_name, {})
        required_count = group_info.get("full_set_count", 3)
    
        if owned_count >= required_count:
            self.monopolies.add(group_name)
            print(f" {self.name} achieved MONOPOLY on {group_name}!")
            return True
    
        return False
    
    def pay_rent(self, amount: int, to_player):
        """
        Pay rent to another player.
        
        Args:
            amount: Rent amount
            to_player: Player receiving payment
            
        Returns:
            True if payment successful, False if bankrupt
        """
        if self.cash >= amount:
            self.cash -= amount
            to_player.cash += amount
            print(f"{self.name} paid ${amount} rent to {to_player.name}. Cash remaining for {self.name}: ${self.cash}")
            return True
        else:
            # Player goes bankrupt!
            self.bankrupt = True
            self.cash = 0
            
            # Transfer properties to the player receiving rent
            for prop in self.properties:
                prop.owner = to_player
                to_player.properties.append(prop)
            
            self.properties.clear()
            print(f"{self.name} cannot pay ${amount} rent and goes bankrupt!")
            return False
        
    
    def has_monopoly(self, group_name: str):
        """Check if player has monopoly in specific group."""
        return group_name in self.monopolies
    
    def to_dict(self):
        """
        Convert player data to dictionary for saving.
        Here I am using composition with Property objects.
        """
        property_data = []
        for prop in self.properties:
            prop_dict = {
                "code": prop.code,
                "name": prop.name,
                "position": prop.position,
                "group": prop.group
            }
            property_data.append(prop_dict)
        
        return {
            "name": self.name,
            "token": self.token,
            "cash": self.cash,
            "position": self.position,
            "in_jail": self.in_jail,
            "jail_turns": self.jail_turns,
            "get_out_of_jail_cards": self.get_out_of_jail_cards,
            "bankrupt": self.bankrupt,
            "properties": property_data,
            "monopolies": list(self.monopolies),
            "turns_played": self.turns_played,
            "total_moves": self.total_moves,
            "properties_bought": self.properties_bought,
            "timestamp": datetime.now().isoformat()
        }
    
