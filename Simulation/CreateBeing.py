from random import random, randint
from Parameters import *
from Being import *

def create_zombie(Master):
    x,y=randint(0, xSize-1), randint(0, ySize-1)
    while Master.Map[x][y].content!=0 or Master.Map[x][y].idBuilding!=0:
        x,y=randint(0, xSize-1), randint(0, ySize-1)

    return(Zombie(Master, (x,y)))

def create_human(Master):
    ability=random()
    if ability<=pAbilities[0]:
        ability=weak
    elif ability<=pAbilities[1]+pAbilities[0]:
        ability=casual
    else:
        ability=strong

    morality=random()
    if morality<=pMoralities[0]:
        morality=evil
    elif morality<=pMoralities[1]+pMoralities[0]:
        morality=neutral
    else:
        morality=hero

    behavior=random()
    if behavior<=pBehaviors[0]:
        behavior=flee
    elif behavior<=pBehaviors[1]+pBehaviors[0]:
        behavior=hide
    else:
        behavior=fight

    coldblood=random()
    if coldblood<=pStress[0]:
        coldblood=zen
    elif coldblood<=pStress[1]+pStress[0]:
        coldblood=stable
    else:
        coldblood=stressed

    x,y=randint(0, xSize-1), randint(0, ySize-1)
    while Master.Map[x][y].content!=0:
        x,y=randint(0, xSize-1), randint(0, ySize-1)

    return(Human(Master, (x,y),ability[0], ability[1], ability[2], coldblood, morality, behavior))