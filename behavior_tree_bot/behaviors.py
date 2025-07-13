import sys
sys.path.insert(0, '../')
from planet_wars import issue_order


def attack_weakest_enemy_planet(state): #provided functionality
    # Don't wait for fleets - be aggressive like successful bots!
    if len(state.my_fleets()) >= 3:
        return False
    # Find our strongest planet
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)
    
    # Find weakest enemy planet not already being attacked
    enemy_planets = [t for t in state.enemy_planets() 
                    if not any(fleet.destination_planet == t.ID for fleet in state.my_fleets())]
    
    if not strongest_planet or not enemy_planets:
        return False
    else:
        weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)


def spread_to_weakest_neutral_planet(state):#provided functionality
    # Allow multiple fleets for rapid expansion
    if len(state.my_fleets()) >= 2:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (3) Find the weakest neutral planet.
    weakest_planet = min(state.neutral_planets(), key=lambda p: p.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)
    
def spread_to_nearest_weak_planet(state):
    if len(state.my_fleets()) >= 5:
        return False

    my_planets = state.my_planets()
    targets = state.not_my_planets()

    if not my_planets or not targets:
        return False

    best_src = None
    best_tgt = None
    best_score = float('-inf')

    for src in my_planets:
        if src.num_ships <= 15:
            continue
        for tgt in targets:
            if tgt.num_ships >= src.num_ships:
                continue

            distance = state.distance(src.ID, tgt.ID)
            # NEW: prioritize growth rate more heavily
            score = (src.num_ships - tgt.num_ships) + (tgt.growth_rate * 2) - (distance)

            if score > best_score:
                best_src = src
                best_tgt = tgt
                best_score = score

    if best_src and best_tgt:
        ships_to_send = min(tgt.num_ships + 1, src.num_ships - 1)
        return issue_order(state, best_src.ID, best_tgt.ID, ships_to_send)

    return False


def reinforce_weakest_my_planet(state):
    my_planets = state.my_planets() # Get a list of all our planets

    # Only reinforce if we have at least 2 planets and no fleet already in flight
    if len(my_planets) < 2 or len(state.my_fleets()) >= 1:
        return False

    # Find weakest and strongest planets
    weakest_planet = min(my_planets, key=lambda p: p.num_ships, default=None)
    strongest_planet = max(my_planets, key=lambda p: p.num_ships, default=None)

    # Don't reinforce the same planet or if we don't have enough ships
    if weakest_planet.ID == strongest_planet.ID or strongest_planet.num_ships < 20:
        return False

    # Send 1/3 of ships from strongest to weakest planet
    num_to_send = strongest_planet.num_ships // 3
    return issue_order(state, strongest_planet.ID, weakest_planet.ID, num_to_send)


def attack_closest_enemy_planet(state): #needs improvement but is currently ok :)
    # Allow some fleets for opportunistic attacks
    if len(state.my_fleets()) >= 2:
        return False

    my_planets = state.my_planets()
    enemy_planets = state.enemy_planets()

    if not my_planets or not enemy_planets:
        return False

    best_source, best_target = None, None
    best_score = -1

    # Look for good attack opportunities
    for src in my_planets:
        if src.num_ships <= 12:  # Need enough ships to attack
            continue
            
        for tgt in enemy_planets:
            # Only attack if we can win
            if tgt.num_ships >= src.num_ships - 5:
                continue
                
            distance = state.distance(src.ID, tgt.ID)
            # Prefer close, weak targets
            score = (src.num_ships - tgt.num_ships) / (distance + 1)
            
            if score > best_score:
                best_source = src
                best_target = tgt
                best_score = score

    # Attack with optimal force
    if best_source and best_target:
        ships_needed = best_target.num_ships + 4
        ships_to_send = min(ships_needed, best_source.num_ships - 4)
        if ships_to_send > 0:
            return issue_order(state, best_source.ID, best_target.ID, ships_to_send)

    return False
