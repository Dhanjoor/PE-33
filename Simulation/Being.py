# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 14:38:58 2018

@author: Nicolas
"""

from tkinter import *
from Entities import *
import numpy as np
import random as rd
import time

class Being:
    def __init__(self,master,postion,cell,speed,vision,hearing,strength,agility,mental):
        self.master=master
        self.postion=postion      # (x,y) for position in pixels
        self.cell=(int(position[0]),int(position[1]))                  # The cell the being is in
        self.speed=speed                # (vr,vteta) vr is the norm and vteta the angle of the speed
        self.vision=vision              #vision distance
        self.hearing=hearing                    #hearing threshold
        self.strength=strength              #physical trait (don't change)
        self.agilty=agility                 #agility trait (don't change)
        self.mental=mental                  #mental trait (don't change)
    
    def move(self,t):
        self.postion[0]+=t*self.speed[0]*np.cos(self.speed[1])                  #new position of the being
        self.postion[1]+=t*self.speed[0]*np.sin(self.speed[1])
        self.cell=self.master.which_cell(self.postion[0],self.postion[1])
    
class Zombie(Being):
    def __init__(self,master,postion,cell,speed):
        zombie_vision=
        zombie_hearing=
        zombie_strength=
        zombie_agility=
        zombie_mental=
        zombie_lifespan=
        Being.__init__(self,master,postion,cell,speed,zombie_vision,zombie_hearing,zombie_strength,zombie_agility,zombie_mental)
        self.lifespan=zombie_lifespan

    def death(self):
        self.master.zombies.remove(self)
    
    def stop(self):

class Human(Being):
    def __init__(self,master,postion,cell,speed,vision,hearing,strength,agility,mental,morality,survival,hunger,energy,stress,stamina):
        Being.__init__(self,master,postion,cell,speed,vision,hearing,strength,agility,mental)
        self.morality=morality              #define the morality of the human
        self.survival=survival              #define the type of survival (hide,flee,fight,...)
        self.hunger=hunger                  #hunger (decrease by time) 0=death
        self.energy=energy                  #energy (decrease by time) 0=death
        self.stress=stress                  #quantity of stress (determine the quality of the decisions)
        self.stamina=stamina                #stamina (decrease when running) 0=no more running
        self.knowing=False                  #knowing the zombie invasion
    
    def zombification(self):
        time.sleep(zombie_incubationtime*dt)                #waiting for the human to turn into a zombie
        self.master.humans.remove(self)              #removing the entity from class human
        self.master.zombies.add(Zombie(self.master,self.postion,self.cell,0))             #creating a new zombie
    
    def eaten(self):
        self.master.humans.remove(self)
    
    def fight(H,Z):
        proba=rd.random()*200-100                   #fight system: uniform law
        if H.strength-Z.strength<=proba-5:          #zombie stronger than human
            if proba_zombie>=rd.random():           #2 cases: eaten or transformed
                H.zombification()
            else:
                H.eaten()
        elif H.strength-Z.strength>=proba+5:        #human stronger than zombie
            Z.death()
        else:                                       #human and zombie as strong: human manage to get away
            Z.stop()