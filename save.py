import json
from datetime import datetime

def save_game(game_state, filename=None):
    """The save game function will save current game to a JSON file.

    Args:
        game_state (dict): The dict holds the entire game state data
        filename (str, optional): Customized filename to save file.

    Returns:
        str: The filename where the game will be saved, otherwise None if save failed
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d, %H:%M:%S")
        filename = f"umd_monopoly_{timestamp}.json"
        
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(game_state, file, indent=2)
            
        print(f"Game saved successfully to {filename}")
        return filename
    
    except Exception as e:
        print(f"Error saving game: {e}")
        return None
    
    
    #Mock trial of function with sample data
if __name__ == "__main__":
    sample_game = {
        "players": [
            {
                "name": "Testudo", 
                "cash": 1500,
                "position": 0,
                "properties_owned": ["McKeldin Library"]
            }
        ],
        "properties": {
            "McKeldin Library": {
                    "base_rent": 50,
                    "group": "North Campus",
                    "owner": "Testudo"
            }
        },
        "current_player": 0,
        "turn_count":5
    }
    #with an automated file name
    result = save_game(sample_game)
    
    #with custom
    result2 = save_game(sample_game, "test_save.json")
    
    if result and result2:
        print("The Save Function works well!")