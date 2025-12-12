def decision_engine(player_cash, property_cost, property_type, game_stage):
    """
    Evaluates whether a player should purchase a property when they land on it.
    
    Args:
        player_cash(int): the player's current cash amount.
        property_cost(int): the cost of the property being considered.
        property_type(str): the name of the property.
        game_stage(str): current game stage - "early", "mid", or "late". 
    
    Returns:
        dict: A dictionary containing:
            - "decision"(str): "buy", "skip", or "risky"
            - "confidence"(int): confidence percentage from 0-100
            - "reason"(str): explanation for the decision
            - "affordability_ratio"(float): ratio of property cost to player cash
            - "remaining_cash"(int): cash left after potential purchase
            - "risk_score"(int): number of risk factors identified (0-3)
    
    Side Effects:
        None. This is a pure function that does not modify any external state.
    """
    affordability = property_cost /  player_cash
    remaining_cash =  player_cash - property_cost
        
    if player_cash == 0 or property_cost > player_cash:
        decision = "skip"
        confidence = 100
        reason = f"""No cash or too expensive, property cost: {property_cost}, player cash: {player_cash}"""
        
    if game_stage == "early":
        safe_reserve = 200
    elif game_stage == "mid":
        safe_reserve = 400
    else:
        safe_reserve = 600
        
    #calculate risk factors
    risk_factor = []
    if remaining_cash  < safe_reserve:
        risk_factor.append("low cash")
    if affordability > 0.7:
        risk_factor.append("high cost")
    if game_stage == "late" and remaining_cash < 500:
        risk_factor.append("late game")
        
    risk_score = 0
    for factor in risk_factor:
        risk_score+=1
        
    #uses risk factors to make decision
    if risk_score >=3:
        decision = "skip"
        confidence = 80
        reason = f"""Too risky: {risk_factor}"""
        
    elif risk_score == 2:
        decision = "risky"
        confidence = 50
        reason = f"""Moderate risk: {risk_factor}"""
        
    elif affordability <= 0.3:
        decision = "buy"
        confidence = 90
        reason = f"""Affordable: {affordability}"""
    
    elif remaining_cash >= safe_reserve *1.5:
        decision = "buy"
        confidence = 75
        reason = f"""safe purchase with good cash reserve:: {remaining_cash}"""
        
    else:
        decision ="buy"
        confidence = 60
        reason = f"""Acceptable purchase: {remaining_cash}"""
        
    return {
        "decision": decision,
        "confidence": confidence,
        "reason": reason,
        "affordability_ratio": round(affordability, 2),
        "remaining_cash": remaining_cash,
        "risk_score": risk_score
    }

if __name__ == "__main__":
    print("Test 1: Affordable purchase")
    result1 = decision_engine(1000, 200, "McKeldin", "mid")
    print(f"Decision: {result1['decision']}")
    print(f"Confidence: {result1['confidence']}%")
    print(f"Reason: {result1['reason']}\n")
 
    print("Test 2: Expensive property")
    result2 = decision_engine(500, 450, "Stamp", "late")
    print(f"Decision: {result2['decision']}")
    print(f"Confidence: {result2['confidence']}%")
    print(f"Reason: {result2['reason']}\n")
   
    print("Test 3: Risky purchase")
    result3 = decision_engine(600, 350, "Eppley", "mid")
    print(f"Decision: {result3['decision']}")
    print(f"Confidence: {result3['confidence']}%")
    print(f"Reason: {result3['reason']}\n")