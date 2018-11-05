#!.venv/bin/python

# Life rules
# 1. There is one type of dots 1 (next: two types of dots: blue (B), red (R))
# 2. If one is touching to atleast three and more than same - becomes other
# 3. If there is three same kind touching by border (form of L) in any direction -> new appears in corner, other splits diagonaly
# 4. After a turn on border line of planet one dies

# Test PR

import time
from enum import Enum

class MateOrientation(Enum):
    south_west = 1
    north_west = 2
    north_east = 3
    south_east = 4

class LifeForm:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.alive = True

# Planet setup
width, height = 20, 20
life_forms = []
life_forms.append(LifeForm(5,5))
life_forms.append(LifeForm(5,6))
life_forms.append(LifeForm(6,5))

def creature_at(x, y, life_forms: [LifeForm]) -> LifeForm:
    for creature in life_forms:
        if creature.x == x and creature.y == y and creature.alive:
            return creature
    return None

def find_creature_mates(creature: LifeForm, life_forms: [LifeForm]):
    creature_in_south = creature_at(creature.x, creature.y - 1, life_forms)
    creature_in_west = creature_at(creature.x - 1, creature.y, life_forms)
    
    if creature_in_south != None and creature_in_west != None:
        return creature_in_south, creature_in_west, MateOrientation.south_west
    
    creature_in_north = creature_at(creature.x, creature.y + 1, life_forms)
    if creature_in_west != None and creature_in_north != None: 
        return creature_in_west, creature_in_north, MateOrientation.north_west

    creature_in_east = creature_at(creature.x + 1, creature.y, life_forms)
    if creature_in_north != None and creature_in_east != None:
        return creature_in_north, creature_in_east, MateOrientation.north_east

    if creature_in_east != None and creature_in_south != None:
        return creature_in_east, creature_in_south, MateOrientation.south_east

    return None

def creatures_after_mating(mother_creature: LifeForm, mate_orientation: MateOrientation):
    
    if (mate_orientation == MateOrientation.south_west):
        creatures = [LifeForm(mother_creature.x - 1, mother_creature.y - 1), 
                    LifeForm(mother_creature.x - 2, mother_creature.y - 2)]
    elif (mate_orientation == MateOrientation.north_west):
        creatures = [LifeForm(mother_creature.x - 1, mother_creature.y + 1), 
                    LifeForm(mother_creature.x - 2, mother_creature.y + 2)]
    elif (mate_orientation == MateOrientation.north_east):
        creatures = [LifeForm(mother_creature.x + 1, mother_creature.y + 1), 
                    LifeForm(mother_creature.x + 2, mother_creature.y + 2)]
    else:
        creatures = [LifeForm(mother_creature.x + 1, mother_creature.y - 1), 
                    LifeForm(mother_creature.x + 2, mother_creature.y - 2)]

    return creatures

def apply_survival_rules(life_forms: [LifeForm]):
    next_iteration = []
    for creature in life_forms:
        # mates
        creature_mates = find_creature_mates(creature, life_forms)
        if creature_mates != None:
            new_creatures = creatures_after_mating(creature, creature_mates[2])
            next_iteration.extend(new_creatures)
            creature.alive = False

        if creature.alive:
            next_iteration.append(creature)

    return next_iteration

def print_creatures(life_forms: [LifeForm]):
    for life_form in life_forms:
        print("{},{}".format(life_form.x, life_form.y))

print("Initial forms:")
print_creatures(life_forms)

while True:

    print("Life forms after cycle:")
    life_forms = apply_survival_rules(life_forms)
    print_creatures(life_forms)

    time.sleep(2)
    
