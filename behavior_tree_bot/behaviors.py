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
    # If no planets or only one planet, skip
    my_planets = state.my_planets()
    if len(my_planets) < 2 or len(state.my_fleets()) >= 1:
        return False

    # Find weakest and strongest planets
    weakest = min(my_planets, key=lambda p: p.num_ships, default=None)
    strongest = max(my_planets, key=lambda p: p.num_ships, default=None)

    if weakest.ID == strongest.ID or strongest.num_ships < 20:
        return False  # nothing to reinforce or too few ships to help

    # Send 1/3 of ships to weakest planet
    num_to_send = strongest.num_ships // 3
    return issue_order(state, strongest.ID, weakest.ID, num_to_send)
