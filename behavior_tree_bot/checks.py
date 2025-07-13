

def if_neutral_planet_available(state):
    return any(state.neutral_planets())

#checks for fleet majority
def have_larger_fleet(state):
    my_fleet = sum(planet.num_ships for planet in state.my_planets())\
        + sum(fleet.num_ships for fleet in state.my_fleets())
    enemy_fleet = sum(planet.num_ships for planet in state.enemy_planets())\
        + sum(fleet.num_ships for fleet in state.enemy_fleets())
    if my_fleet >= enemy_fleet * 0.7:
        return True
