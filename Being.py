q# -*- coding: utf-8 -*-
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
    def __init__(self,position,speed,vision,hearing,strength,agility):
        self.position=position      # (x,y) for position in pixels
        self.cell=(int(position[0]),int(position[1]))                  # The cell the being is in
        self.speed=speed                # (vr,vteta) vr is the norm and vteta the angle of the speed
        self.vision=vision              #vision distance
        self.hearing=hearing                    #hearing threshold
        self.strength=strength              #physical trait (don't change)
        self.agilty=agility                 #agility trait (don't change)
        self.stop=0                         #countdown when the entity stop moving
    
    def move(self,t):
        if self.stop==0:                                                            #verif that the entity can move
            self.position[0]+=t*self.speed[0]*np.cos(self.speed[1])                  #new position of the being
            self.position[1]+=t*self.speed[0]*np.sin(self.speed[1])
            self.cell=self.master.which_cell(self.position[0],self.position[1])
        else:                                                                       #decrease by one the countdown
            self.stop-=1

class Zombie(Being):
    def __init__(self,master,position,speed):
        Being.__init__(self,master,position,speed,z_vision,z_hearing,z_strength,z_agility)
        self.lifespan=z_lifespan

    def death(self):
        Zombies.remove(self)

    def detectSound(G,x,y,R):
    u,v=0,0
    for i in range(x-R,x+R+1):
        for j in range(y-R,y+R+1):
            r=((i-x)**2+(j-y)**2)**(1/2)
            if r<=R and r!=0:
                volume=G[i][j].sound
                u+=volume*(i-x)/r
                v+=volume*(j-y)/r
    return (u,v)

class Human(Being):
    def __init__(self,master,position,speed,vision,hearing,strength,agility,morality,cold_blood,behavior):
        Being.__init__(self,master,position,speed,h_vision,h_hearing,strength,agility)
        self.morality=morality              #define the morality of the human
        self.cold_blood=cold_blood          #define how the human endure the stress
        self.behavior=behavior              #define the type of survival (hide,flee,fight,...)
        self.hunger=100                  #hunger (decrease by time) 0=death
        self.energy=100                  #energy (decrease by time) 0=death
        self.stress=0                  #quantity of stress (determine the quality of the decisions)
        self.stamina=100                #stamina (decrease when running) 0=no more running
        self.knowing=False                  #knowing the zombie invasion

    def detectSound(G,x,y,R):
    u,v=0,0
    for i in range(x-R,x+R+1):
        for j in range(y-R,y+R+1):
            r=((i-x)**2+(j-y)**2)**(1/2)
            if r<=R and r!=0:
                volume=G[i][j].sound
                u+=volume*(i-x)/r
                v+=volume*(j-y)/r
    return (u,v)

    def zombification(self):
        time.sleep(z_incubation_time*dt)                #waiting for the human to turn into a zombie
        Humans.remove(self)              #removing the entity from class human
        Zombies.add(Zombie(self.master,self.position,0))             #creating a new zombie
    
    def eaten(self):
        time.sleep(z_incubation_time*dt)                #waiting for the human to turn into a zombie
        Humans.remove(self)
    
    def fight(self,Zincell):
        Zstrength=0
        genSound(self.cell[0],self.cell[1],)
        for Z in Zincell:
            Zstrength+=Z.stength
        proba=rd.random()                                          #fight system: uniform law.
        if 1-self.strength/(2*(Zstrength+self.strength))>=proba:          #zombie(s) stronger than human

            if proba_zombie>=rd.random():           #2 cases: eaten or transformed
                self.zombification()
            else:
                self.eaten()
        elif self.strength/(2*(Zstrength+self.strength))<=proba:        #human stronger than zombie(s)
            for Z in Zincell:
                Z.death()
        else:                                       #human and zombie(s) as strong: human manage to get away
            for Z in Zincell:
                Z.stop=2
