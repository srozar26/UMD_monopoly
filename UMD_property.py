import json
import re
from typing import Dict, List, Optional  # Removed problematic imports
from datetime import datetime


class PropertyType:
    """Types of properties on UMD campus."""
    HOUSING = "Housing"
    DINING = "Dining"
    ACADEMIC = "Academic"
    RECREATION = "Recreation"
    ADMIN = "Administrative"
    SPECIAL = "Special"


class UMDProperty:
    """
    Represents a property on UMD-themed Monopoly board.
    
    Primary Author: [Your Name Here]
    Techniques claimed:
    1. Magic methods other than __init__()
    2. Set operations
    3. Key function with sorted()
    4. Optional parameters
    """
    
    # UMD campus property groups with realistic data
    PROPERTY_GROUPS = {
        "North Campus": {
            "type": PropertyType.HOUSING,
            "color": "Red", 
            "properties": {
                "C": "Cambridge Community",
                "C2": "Cambridge Hall",
                "C3": "Cambridge Commons"
            },
            "full_set_count": 3,
            "base_rent": 20,
            "house_rents": [50, 150, 450, 625, 750],
            "house_cost": 100
        },
        "South Campus": {
            "type": PropertyType.HOUSING,
            "color": "Teal",
            "properties": {
                "T": "T-Row Apartments",
                "T2": "Terrapin Row",
                "T3": "Towers"
            },
            "full_set_count": 3,
            "base_rent": 25,
            "house_rents": [60, 180, 500, 700, 900],
            "house_cost": 120
        },
        "Academic Core": {
            "type": PropertyType.ACADEMIC,
            "color": "Blue",
            "properties": {
                "M": "McKeldin Library",
                "H": "Hornbake Library",
                "U": "Stamp Student Union"
            },
            "full_set_count": 3,
            "base_rent": 30,
            "house_rents": [70, 200, 550, 750, 950],
            "house_cost": 150
        },
        "Dining Halls": {
            "type": PropertyType.DINING,
            "color": "Green",  
            "properties": {
                "D1": "South Campus Dining",
                "D2": "251 North",
                "D3": "The Diner"
            },
            "full_set_count": 3,
            "base_rent": 15,
            "house_rents": [40, 100, 300, 450, 600],
            "house_cost": 80
        },
        "Athletics": {
            "type": PropertyType.RECREATION,
            "color": "Yellow", 
            "properties": {
                "V": "Varsity Team House",
                "X": "Xfinity Center",
                "S": "SECU Stadium"
            },
            "full_set_count": 3,
            "base_rent": 35,
            "house_rents": [80, 220, 600, 800, 1000],
            "house_cost": 180
        }
    }
    
    # Special Unuiversity of Maryland properties
    SPECIAL_PROPERTIES = {
        "GO": {"name": "START / GO", "action": "Collect $200 when passing"},
        "J": {"name": "Jail / Just Visiting", "action": "Lose turn or pay $50"},
        "E": {"name": "Event Space", "action": "Draw event card"},
        "P": {"name": "Free Parking", "action": "Collect accumulated fees"},
        "R": {"name": "Rent-A-Scooter", "action": "Variable rent based on dice roll"}
    }
    
    def __init__(self, code: str, name: str, position: int, 
                 cost: Optional[int] = None, group: Optional[str] = None,
                 base_rent: Optional[int] = None):
        """
        Initialize a UMD property.
        
        Args:
            code: Board code (C1, T2, M, etc.)
            name: Full property name
            position: Board position (0-39)
            cost: Optional purchase cost (uses group default if None)
            group: Optional property group (auto-detected from code if None)
            base_rent: Optional base rent (uses group default if None)
        """
        
        self.code = code
        self.name = name
        self.position = position
        self.group = group or self._detect_group_from_code(code)
        self.owner = None
        self.mortgaged = False
        self.houses = 0  # 0-4 houses
        self.hotels = 0 # 5 is hotel
        
        # Set costs based on group or provided values
        self._initialize_costs(cost, base_rent)
        
        # Track transaction history
        self.purchase_history = []
        self.rent_history = []
    
    def _detect_group_from_code(self, code: str):
        """Detect which group this property belongs to based on code."""
        for group_name, group_info in self.PROPERTY_GROUPS.items():
            if code in group_info["properties"]:
                return group_name
        
        # Check for special properties
        if code in self.SPECIAL_PROPERTIES:
            return "Special"
        
        return "Unknown"
    
    def _initialize_costs(self, cost: Optional[int], base_rent: Optional[int]):
        """Initialize cost and rent based on group defaults or provided values."""
        if self.group in self.PROPERTY_GROUPS:
            group_info = self.PROPERTY_GROUPS[self.group]
            
            # Set cost
            if cost is not None:
                self.cost = cost
            else:
                # Calculate cost based on group and property code
                base_cost = group_info.get("base_cost", 200)
                if self.code.endswith("2"):
                    self.cost = base_cost + 50
                elif self.code.endswith("3"):
                    self.cost = base_cost + 100
                else:
                    self.cost = base_cost
            
            # Set base rent
            if base_rent is not None:
                self.base_rent = base_rent
            else:
                self.base_rent = group_info.get("base_rent", 20)
        else:
            # Special properties
            self.cost = 0
            self.base_rent = 0
    
    # Magic methods
    def __str__(self):
        """String representation."""
        owner_str = f" (Owned by {self.owner})" if self.owner else " (Unowned)"
        mortgage_str = " [MORTGAGED]" if self.mortgaged else ""
        houses_str = f" [{self.houses} houses]" if self.houses > 0 else ""
        hotels_str = f" [{self.hotels} hotel]" if self.hotels > 0 else ""
        return f"{self.name} (${self.cost}){owner_str}{mortgage_str}{houses_str}{hotels_str}"
    
    def __repr__(self):
        """Detailed representation."""
        return f"UMDProperty(code='{self.code}', name='{self.name}', position={self.position})"
    
    def __eq__(self, other):
        """Equality comparison."""
        if not isinstance(other, UMDProperty):
            return False
        return self.code == other.code and self.position == other.position
    
    def __hash__(self):
        """Hash function."""
        return hash((self.code, self.position))
    
    def __lt__(self, other):
        """Less than comparison for sorting by position."""
        return self.position < other.position
    
    def __contains__(self, item: str):
        """Check if property contains string in name or code."""
        return item.lower() in self.name.lower() or item.lower() in self.code.lower()
    
    def set_owner(self, player):
        """Set property owner."""
        self.owner = player
        self.purchase_history.append({
            "timestamp": datetime.now().isoformat(),
            "owner": player.name if hasattr(player, 'name') else str(player),
            "price": self.cost
        })
    
    def remove_owner(self):
        """Remove property owner (for selling/bankruptcy)."""
        self.owner = None
    
    def calculate_rent(self, dice_roll: int = 0, owner_has_monopoly: bool = False):
        """
        TO calculate the rent of property based on various factors.
        
        Primary Author: [Your Name Here]
        Technique: Optional parameters
        """
        if self.mortgaged or not self.owner:
            return 0
        
        # Special property: Rent-A-Scooter
        if self.code == "R":
            return dice_roll * 25
        
        rent = self.base_rent
        
        # Apply house/hotel multipliers
        if self.houses > 0:
            group_info = self.PROPERTY_GROUPS.get(self.group, {})
            house_rents = group_info.get("house_rents", [])
            if self.houses <= len(house_rents):
                rent = house_rents[self.houses - 1]
        
        if self.hotels > 0:
            group_info = self.PROPERTY_GROUPS.get(self.group, {})
            house_rents = group_info.get("house_rents", [])
            if len(house_rents) >= 5:
                rent = house_rents[4]  # Hotel rent
        
        # Double rent for monopoly
        if owner_has_monopoly and self.houses == 0 and self.hotels == 0:
            rent *= 2
        
        self.rent_history.append({
            "timestamp": datetime.now().isoformat(),
            "amount": rent,
            "dice_roll": dice_roll,
            "monopoly": owner_has_monopoly
        })
        
        return rent
    
    def calculate_value(self):
        """Calculate current property value."""
        value = self.cost // 2 if self.mortgaged else self.cost
        
        # Add value of improvements
        value += self.houses * (self._get_house_cost() // 2)
        value += self.hotels * (self._get_house_cost() * 2)
        
        return value
    
    def calculate_roi(self):
        """Calculate return on investment."""
        if self.cost == 0:
            return 0.0
        
        total_rent = sum(entry["amount"] for entry in self.rent_history)
        return total_rent / self.cost
    
    def _get_house_cost(self):
        """Get cost to build a house on this property."""
        if self.group in self.PROPERTY_GROUPS:
            return self.PROPERTY_GROUPS[self.group].get("house_cost", 100)
        return 100
    
    def add_house(self):
        """Add a house to the property."""
        if self.houses >= 4:
            return False
        
        self.houses += 1
        return True
    
    def add_hotel(self):
        """Add a hotel to the property (replaces 4 houses)."""
        if self.houses < 4:
            return False
        
        self.houses = 0
        self.hotels += 1
        return True
    
    
    
    @classmethod
    def find_best_investment(cls, properties: List['UMDProperty'], 
                           budget: int, owned_codes: set = None):
        """
        Find the best property investment based on budget and existing portfolio.
        Uses key function with sorted().
        
        Primary Author: [Your Name Here]
        Technique: Key function with sorted()
        Original algorithm for investment scoring
        """
        if owned_codes is None:
            owned_codes = set()
        
        # Filter affordable and available properties
        available = [p for p in properties if p.cost <= budget and not p.owner]
        
        if not available:
            return None
        
        def investment_score(prop: 'UMDProperty'):
            """
            Original algorithm for calculating investment score.
            Combines multiple factors into a single score.
            """
            score = 0.0
            
            # Factor 1: Base ROI (30% weight)
            base_roi = prop.base_rent / max(prop.cost, 1)
            score += base_roi * 0.3
            
            # Factor 2: Group completion bonus (40% weight)
            if prop.group in cls.PROPERTY_GROUPS:
                group_codes = set(cls.PROPERTY_GROUPS[prop.group]["properties"].keys())
                owned_in_group = owned_codes.intersection(group_codes)
                
                # Calculate completion percentage
                total_in_group = len(group_codes)
                owned_count = len(owned_in_group)
                completion_ratio = (owned_count + 1) / total_in_group  # +1 for this property
                
                # Exponential bonus for near-completion
                if completion_ratio >= 0.67:  # 2/3 complete
                    score += 0.4 * (completion_ratio ** 2)
                else:
                    score += 0.4 * completion_ratio
            
            # Factor 3: Position advantage (15% weight)
            # Properties closer to GO are more valuable
            position_score = 1 - (prop.position / 40)
            score += position_score * 0.15
            
            # Factor 4: Affordability (15% weight)
            affordability = 1 - (prop.cost / max(budget, 1))
            score += affordability * 0.15
            
            return score
        
        # Sort by investment score
        sorted_props = sorted(available, key=investment_score, reverse=True)
        return sorted_props[0] if sorted_props else None
    
    def analyze_name(self) :
        """Analyze property name using regular expressions."""
        analysis = {
            "name": self.name,
            "word_count": len(re.findall(r'\b\w+\b', self.name)),
            "contains_umd": bool(re.search(r'\bUMD\b', self.name, re.IGNORECASE)),
            "contains_terp": bool(re.search(r'\bterp\b', self.name, re.IGNORECASE)),
            "contains_maryland": bool(re.search(r'\bmaryland\b', self.name, re.IGNORECASE)),
            "acronyms": re.findall(r'\b[A-Z]{2,}\b', self.name),
            "building_numbers": re.findall(r'\b\d+\b', self.name)
        }
        return analysis
    
    def to_dict(self):
        """Convert property to dictionary."""
        owner_name = None
        if self.owner:
            if hasattr(self.owner, 'name'):
                owner_name = self.owner.name
            else:
                owner_name = str(self.owner)
                
        return {
            "code": self.code,
            "name": self.name,
            "position": self.position,
            "group": self.group,
            "cost": self.cost,
            "base_rent": self.base_rent,
            "owner": owner_name,
            "mortgaged": self.mortgaged,
            "houses": self.houses,
            "hotels": self.hotels,
            "current_value": self.calculate_value(),
            "total_rent_collected": sum(entry["amount"] for entry in self.rent_history)
        }
    
    def to_json(self, indent: Optional[int] = 2):
        """Convert property to JSON string."""
        data = self.to_dict()
        data["analysis"] = self.analyze_name()
        data["timestamp"] = datetime.now().isoformat()
        
        return json.dumps(data, indent=indent)
    
    @classmethod
    def create_UMD_board(cls) :
        """Create all properties for UMD Monopoly board."""
        properties = []
        
        # Create properties from groups
        position = 0
        
        for group_name, group_info in cls.PROPERTY_GROUPS.items():
            for code, name in group_info["properties"].items():
                prop = cls(
                    code=code,
                    name=name,
                    position=position,
                    group=group_name
                )
                properties.append(prop)
                position += 3  # Space them out on board
        
        # Add special properties
        special_positions = [0, 10, 20, 30, 5, 15, 25, 35]
        for i, (code, info) in enumerate(cls.SPECIAL_PROPERTIES.items()):
            pos = special_positions[i] if i < len(special_positions) else 38
            prop = cls(
                code=code,
                name=info["name"],
                position=pos,
                group="Special"
            )
            properties.append(prop)
        
        # Sort by position
        properties.sort(key=lambda p: p.position)
        return properties