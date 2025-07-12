import sys
sys.path.insert(0, '../')
from planet_wars import issue_order


def attack_weakest_enemy_planet(state):
    # (1) If we currently have a fleet in flight, abort plan.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (3) Find the weakest enemy planet.
    weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)


def spread_to_weakest_neutral_planet(state):
    # (1) If we currently have a fleet in flight, just do nothing.
    if len(state.my_fleets()) >= 1:
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


def attack_closest_enemy_planet(state):
    # (1) If we already have a fleet in flight, skip this behavior.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Get all our planets and enemy planets.
    my_planets = state.my_planets()
    enemy_planets = state.enemy_planets()

    # (3) If either list is empty, there's nothing to attack or attack from.
    if not my_planets or not enemy_planets:
        return False

    # (4) Initialize variables to track the closest source-target pair.
    best_source, best_target = None, None
    min_distance = float('inf')  # Start with an infinitely large distance.

    # (5) Check every pair of our planets and enemy planets.
    for src in my_planets:
        for tgt in enemy_planets:
            dist = state.distance(src.ID, tgt.ID)  # Compute distance between the pair.

            # (6) Only consider attacking if our source planet has more than 10 ships.
            if dist < min_distance and src.num_ships > 10:
                # (7) Update the closest valid attack pair found so far.
                best_source = src
                best_target = tgt
                min_distance = dist

    # (8) If we found a valid pair, send half the ships to attack the closest enemy.
    if best_source and best_target:
        return issue_order(state, best_source.ID, best_target.ID, best_source.num_ships / 2)

    # (9) If no suitable target found, skip this behavior.
    return False
