from Parameters import *
import numpy as np
from math import atan, acos, floor
from random import random, choice, randint

def nearestIndex(self,L): #return closest being in list L from self
    x,y=self.position
    cible=-1
    dMin=xSize+ySize
    for i in range(len(L)):
        if L[i]!=self:
            u,v=L[i].position
            d=((x-u)**2+(y-v)**2)**0.5
            if d<dMin:
                cible=i
                dMin=d
    return(cible)

def cellsOnLine(x1,y1,x2,y2): #return the list of the cells between 2 points
    if x1>x2:
        x1,y1,x2,y2=x2,y2,x1,y1 #x1<=x2

    if floor(x1)==floor(x2):
        ym,yM=min(y1,y2), max(y1,y2)
        return([(floor(x1),y) for y in range(floor(ym),floor(yM)+(1-(yM%1==0)))])
    if y1==y2:
        return([(x,floor(y1)) for x in range(floor(x1),floor(x2)+1-(x2%1==0))])

    reverse=False
    if y1>y2:
        reverse=True
        y2=2*y1-y2 #x1<x2 and y1<y2

    L=[(floor(x1),floor(y1))]

    a=(y2-y1)/(x2-x1) #y=ax +y1
    x,y=x1,y1

    if x2%1==0:
        cond1=lambda x: abs(x-x2)>10**-10 and floor(x)!=floor(x2)
    else:
        cond1=lambda x: floor(x)!=floor(x2)

    if y2%1==0:
        cond2=lambda y: abs(y-y2)>10**-10 and floor(y)!=floor(y2)
    else:
        cond2=lambda y: floor(y)!=floor(y2)

    while cond1(x) or cond2(y):
       xNew=floor(x)+1
       yNew=y+a*(xNew-x)
       if yNew<floor(y)+1: #we didnt cross the top frontier of the cell
           x,y=xNew,yNew
           L.append((xNew,floor(y)))
       else: #we crossed the top frontier of the cell
           yNew=floor(y)+1
           xNew=x+(yNew-y)/a
           x,y=xNew,yNew
           L.append((floor(xNew),y))

    if reverse:
        L=[(x,2*int(y1)-y-1) for x,y in L]
    if x2%1==0 or y2%1==0:
        L.pop()
    return(L)
    #return([(int(x),int(y)) for x,y in L])

class Being:
    def __init__(self,Master,position,maxspeed,vision,hearing,strength,agility):
        self.Master=Master
        self.position=position      # [x,y] for position in pixels
        self.cell=[int(position[0]),int(position[1])]                  # The cell the being is in
        self.speed=[0,0]                # vx and vy speeds in direction x and y
        self.vision=vision              #vision distance
        self.hearing=hearing                    #hearing threshold
        self.strength=strength              #physical trait (don't change)
        self.agilty=agility                 #agility trait (don't change)
        self.stop=0                         #countdown when the entity stop moving
        self.maxspeed=maxspeed              #maximal speed
        self.fighting=False                 #Shows whether or not the being is fighting this turn

    def move(self,t,volume):
        if self.stop==0:                                                            #verif that the entity can move
            x=self.position[0]+t*self.speed[0]*self.maxspeed                 #new position of the being
            y=self.position[1]+t*self.speed[1]*self.maxspeed
            if x>=0 and x<xSize and y>=0 and y<ySize and not(self.Master.Map[int(x)][int(y)].content in [1,2]):
                self.position=[x,y]
                self.cell=[int(x),int(y)]
                if volume>0:
                    self.Master.genSound(self.cell[0], self.cell[1], volume)
        else:                                                                       #decrease by one the countdown
            self.stop-=1

    def zProximity(self):
        x,y=self.position
        vx,vy=self.speed
        L=[]
        for Z in self.Master.Zombies:
            xz,yz=Z.position
            u,v=xz-x,yz-y
            if u==0 and v==0:
                L.append(Z)
            #elif ((x-xz)**2+(y-yz)**2)**0.5<=self.vision and ((vx==0 and vy==0) or abs(acos((vx*u+vy*v)/((vx**2+vy**2)*(u**2+v**2))**0.5))<=visionAngle/2):
            elif ((x-xz)**2+(y-yz)**2)**0.5<=self.vision:
                cells=cellsOnLine(x,y,xz,yz)
                visible=True
                for xc,yc in cells:
                    if self.Master.Map[xc][yc].content in [1,2]:
                        visible=False
                        break
                if visible:
                    L.append(Z)
        return(L)

    def hProximity(self):
        x,y=self.position
        L=[]
        for H in self.Master.Humans:
            xh,yh=H.position
            u,v=xh-x,yh-y
            if u==0 and v==0:
                L.append(H)
            elif ((x-xh)**2+(y-yh)**2)**0.5<=self.vision:
                cells=cellsOnLine(x,y,xh,yh)
                visible=True
                for xc,yc in cells:
                    if self.Master.Map[xc][yc].content in [1,2]:
                        visible=False
                        break
                if visible:
                    L.append(H)
        return(L)

    def hInSight(self):
        x,y=self.position
        vx,vy=self.speed
        proxi=self.hProximity()
        L=[]
        for H in proxi:
            xh,yh=H.position
            ux,uy=xh-x,yh-y
            if (ux==0 and uy==0) or (vx==0 and vy==0):
                L.append(H)
            elif (vx*ux+vy*uy)/((vx**2+vy**2)*(ux**2+uy**2))**0.5>=cosVisionAngle:
                L.append(H)
        return(L)

    def zInSight(self):
        x,y=self.position
        vx,vy=self.speed
        proxi=self.zProximity()
        L=[]
        for Z in proxi:
            xz,yz=Z.position
            ux,uy=xz-x,yz-y
            if (ux==0 and uy==0) or (vx==0 and vy==0):
                L.append(Z)
            elif (vx*ux+vy*uy)/((vx**2+vy**2)*(ux**2+uy**2))**0.5>=cosVisionAngle:
                L.append(Z)
        return(L)


    def detectSound(self):
        x,y=self.cell
        u,v=0,0
        if x>0:
            u-=self.Master.Map[x-1][y].sound
            if y>0:
                u-=self.Master.Map[x-1][y-1].sound/2**0.5
            if y<ySize-1:
                u-=self.Master.Map[x-1][y+1].sound/2**0.5

        if x<xSize-1:
            u+=self.Master.Map[x+1][y].sound
            if y>0:
                u-=self.Master.Map[x+1][y-1].sound/2**0.5
            if y<ySize-1:
                u-=self.Master.Map[x+1][y+1].sound/2**0.5

        if y>0:
            v-=self.Master.Map[x][y-1].sound
        if y<ySize-1:
            v+=self.Master.Map[x][y+1].sound

        return(u,v)
        # sound in (x,y) not added

class Zombie(Being):
    def __init__(self,Master,position):
        Being.__init__(self,Master,position,zMaxspeed,zVision,zHearing,zStrength,zAgility)
        self.lifespan=zLifespan

    def info(self):
        x,y=self.position
        vx,vy=self.speed
        print("Race: Zombie, case: x={}, y={}".format(x,y))
        print("vx={}, vy={}".format(vx,vy))

    def addLifespan(self, s):
        self.lifespan+=s
        if self.lifespan<=0:
            self.death()

    def action(self):
        x,y=self.position

        hVision=self.hInSight()
        cible=nearestIndex(self,hVision)
        if cible!=-1:
            xh,yh=hVision[cible].position
            r=((x-xh)**2+(y-yh)**2)**0.5
            if r==0:
                self.speed=[0,0]
                return("human on position")
            if r<self.maxspeed*dt:
                r=self.maxspeed*dt
            self.speed=[(xh-x)/r,(yh-y)/r]
            self.move(dt, shoutVolume)
            return("human in sight")

        xSound, ySound=self.detectSound()
        r=(xSound**2+ySound**2)**0.5
        if r>self.hearing:
            self.speed=[xSound/r, ySound/r]
            self.move(dt,0)
            return("sound heard")

        """zVision=self.zInSight()
        cible=nearestIndex(self, zVision)
        if cible!=-1:
            xz,yz=zVision[cible].position
            r=((x-xz)**2+(y-yz)**2)**0.5
            if r==0:
                self.speed=[0,0]
                return("zombie on position")
            if r<self.maxspeed*dt:
                r=self.maxspeed*dt
            self.speed=[(xz-x)/r,(yz-y)/r]
            self.move(dt,0)
            return("zombie in sight")"""

        return("nothing detected")

    def death(self):
        print("A zombie is dead, the minions of hell grow weaker.")
        self.Master.Zombies.remove(self)

class Human(Being):
    def __init__(self,Master,position,maxspeed,strength,agility,morality,coldblood,behavior,charisma):
        Being.__init__(self,Master,position,maxspeed,hVision,hHearing,strength,agility)
        self.morality=morality              #define the morality of the human
        self.coldblood=coldblood          #define how the human endure the stress
        self.behavior=behavior              #define the type of survival (hide,flee,fight,...)
        self.charisma=charisma             #define the group behavior of the human
        self.hunger=randint(100, maxHunger)                  #hunger (decrease by time) 0=death
        self.energy=randint(100, maxEnergy)                    #energy (decrease by time) 0=death
        self.stress=0                  #quantity of stress (determine the quality of the decisions)
        self.stamina=100                #stamina (decrease when running) 0=no more running
        self.aware=False                   #aware the zombie invasion
        self.group=None                #define the social group of the human
        self.path=[]
        self.flee=False
        self.sleeping=False

    def info(self):
        x,y=self.position
        print("Race: Humain, case: x={}, y={}".format(x,y))

    def addEnergy(self,e):
        if self.energy+e<0:
            self.death("energy")
        else:
            self.energy=min(maxEnergy,self.energy+e)

    def addHunger(self,h):
        if self.hunger+h<0:
            self.death("hunger")
        else:
            self.hunger=min(maxHunger,self.hunger+h)

    def setGroup(self,newGroup):
        if self.group !=None:
            self.Master.Groups[self.group].remove(self)
        self.group=newGroup
        self.Master.Groups[newGroup].append(self)

    def followpath(self, flee=False): # when called, move the human following self.path ( on a distance maxspeed*dt/2 ),
                      # and remove the cells reached in self.path
        if flee:
            dist=self.maxspeed*dt
        else:
            dist=self.maxspeed*dt/2
        while dist>0 and self.path:
            nexttar=[self.path[0][0]+0.5,self.path[0][1]+0.5]
            dToCell=((self.position[0]-nexttar[0])**2+(self.position[1]-nexttar[1])**2)**0.5 # distance to next cell
            if dToCell > dist:
                move=[(nexttar[0]-self.position[0])/dToCell*dist,(nexttar[1]-self.position[1])/dToCell*dist]
                self.position=[self.position[0]+move[0],self.position[1]+move[1]]
                self.cell=[int(self.position[0]), int(self.position[1])]
                dist=0
            else:
                self.position=nexttar
                self.cell=[int(self.position[0]), int(self.position[1])]
                dist-=dToCell
                self.path.pop(0)

    def action(self):
        actionMade=""
        self.fighting=False
        if self.sleeping:
            self.addEnergy(10)
            if self.energy==maxEnergy:
                self.sleeping=False
                self.stop=0
                actionMade+="Wake up, "
                self.Master.Map[self.cell[0]][self.cell[1]].quantity+=1
                idBuilding=self.Master.Map[self.cell[0]][self.cell[1]].idBuilding
            else:
                actionMade+="Sleep, "
                return(actionMade)

        zVision=self.zInSight()
        if not(self.aware) and self.detectZ(zVision):
            actionMade+="Aware, "

        elif self.flee and self.path:
            self.followpath(True)
            if self.Master.Map[self.cell[0]][self.cell[1]].idBuilding!=0:
                self.flee=False
            actionMade+="Fleeing, "

        elif self.aware and zVision:
            self.stop=0
            d=self.vision
            self.addStress()
            target=None
            vx,vy=0,0
            for z in zVision:
                if d>((self.position[0]-z.position[0])**2+(self.position[1]-z.position[1])**2)**0.5:
                    target=z
                    d=((self.position[0]-z.position[0])**2+(self.position[1]-z.position[1])**2)**0.5
            if self.behavior=="fight" and target:
                self.path=[]
                vx,vy=target.position[0]-self.position[0],target.position[1]-self.position[1]
                if vx!=0 or vy!=0:
                    vx,vy=self.maxspeed*vx/((vx**2+vy**2)**0.5),self.maxspeed*vy/((vx**2+vy**2)**0.5)
                actionMade+="Zombie in sight (fight), "
                if self.stamina!=0:
                    self.speed=[vx,vy]
                else:
                    self.speed=[vx/4,vy/4]
            else:
                self.flee=True
                self.path=self.pathfinding("shelter")
                self.followpath(True)
                if self.Master.Map[self.cell[0]][self.cell[1]].idBuilding!=0:
                    self.flee=False
                actionMade+="Zombie in sight (flee), "

        elif self.stress>90:
            self.path=[]
            sx,sy=random(),random()
            if sx!=0 or sy!=0:
                sx,sy=sx/((sx**2+sy**2)**0.5),sy/((sx**2+sy**2)**0.5)
            d=self.maxspeed*random()
            sx,sy=d*sx,d*sy
            self.speed=[sx,sy]
            actionMade+="Stressed, "

        elif self.hunger<maxHunger/2 and self.Master.Map[self.cell[0]][self.cell[1]].content!=3:
            actionMade+="FindFood"
            if not(self.path):
                self.path=self.pathfinding("food")
                actionMade+="-Pathfinding"
            if self.path:
                self.followpath()
                actionMade+="-Followpath"
            actionMade+=", "

        if self.Master.Map[self.cell[0]][self.cell[1]].content==3 and self.hunger<maxHunger and self.stress<90:
            idBuilding=self.Master.Map[self.cell[0]][self.cell[1]].idBuilding
            self.addHunger(10)
            actionMade+="Eat, "
            self.eating=True
            self.Master.Map[self.cell[0]][self.cell[1]].quantity-=1
            if self.Master.Map[self.cell[0]][self.cell[1]].quantity==0:
                self.Master.Map[self.cell[0]][self.cell[1]].content=0
                self.Master.Buildings[idBuilding-1].nFoodCells-=1
        else:
            self.eating=False

        if self.energy<maxEnergy/3 and self.Master.Map[self.cell[0]][self.cell[1]].content!=4 and self.stress<90:
            actionMade+="FindRest"
            if not(self.path):
                self.path=self.pathfinding("rest")
                actionMade+="-Pathfinding"
            if self.path:
                self.followpath()
                actionMade+="-Followpath"
            actionMade+=", "

        if self.energy<maxEnergy/4 and self.stress<90:
            if self.Master.Map[self.cell[0]][self.cell[1]].content==4 and self.Master.Map[self.cell[0]][self.cell[1]].quantity>0:
                self.sleeping=True
                actionMade+="Start sleeping, "
                self.Master.Map[self.cell[0]][self.cell[1]].quantity-=1
                idBuilding=self.Master.Map[self.cell[0]][self.cell[1]].idBuilding
            elif self.Master.Map[self.cell[0]][self.cell[1]].content==4:
                actionMade+="FindRest"
                if not(self.path):
                    self.path=self.pathfinding("rest")
                    actionMade+="-Pathfinding"
                if self.path:
                    self.followpath()
                    actionMade+="-Followpath"
                actionMade+=", "

        if actionMade=="" and self.path:
            self.followpath()
            actionMade+="Followpath, "

        elif self.aware and self.Master.Map[self.cell[0]][self.cell[1]].idBuilding!=0 and self.behavior=="hide":
            self.speed=[0,0]
            actionMade+="Hide, "

#        elif actionMade=="" and self.aware:
#            sx,sy=random(),random()
#            sx,sy=sx/((sx**2+sy**2)**(1/2)),sy/((sx**2+sy**2)**(1/2))
#            d=self.maxspeed/2
#            sx,sy=d*sx,d*sy
#            self.speed=[sx, sy]
#            actionMade+="RandomAware, "

        elif self.aware and actionMade=="":
            self.path=self.pathfinding("shelter")
            if self.path:
                self.followpath()
                actionMade+="Pathfinding-shelter, "

        elif not(self.aware) and actionMade=="" and self.Master.Map[self.cell[0]][self.cell[1]].idBuilding!=0 and len(self.Master.Buildings)>1:
            self.path=self.pathfinding("shelter")
            if self.path:
                self.followpath()
                actionMade+="MoveNotAware, "

#        elif actionMade=="" and not(self.aware or self.path):
#            print(3)
#            sx,sy=random(),random()
#            sx,sy=sx/((sx**2+sy**2)**(1/2)),sy/((sx**2+sy**2)**(1/2))
#            d=self.maxspeed/2
#            sx,sy=d*sx,d*sy
#            self.speed=[sx, sy]
#            actionMade+='RandomNotAware, '

        elif not(self.aware) and actionMade=="" and self.Master.Map[self.cell[0]][self.cell[1]].idBuilding==0:
            self.path=self.pathfinding("shelter")
            if self.path:
                self.followpath()
                actionMade+="MoveNotAware, "

        self.addEnergy(-1)
        self.addHunger(-1)
        self.stress=min(0, self.stress-1)

        for z in self.Master.Zombies:
            xz,yz=z.position
            x,y=self.position
            if (x-xz)**2+(y-yz)**2<=dInteraction**2:
                if self.aware:
                    self.fight()
                    actionMade+="Fight, "
                else:
                    self.zombification()
            break

        if not(self.sleeping or self.eating) and self.speed!=[0,0]:
            self.move(dt,moveVolume)
            actionMade+="Move."
        return(actionMade)

    def addStress(self):
        if self.coldblood=="zen":
            self.stress+=1
        elif self.coldblood=="normal":
            self.stress+=5
        else:
            self.stress+=10


    def detectZ(self, zVision):
        if len(zVision)>=nZombieAware:
            self.aware=True
            self.stress=90
            return(True)
        for x in zVision:
            if x.fighting:
                self.aware=True
                self.stress=90
                return(True)
        return(False)

    def death(self, cause="Unknown"):
        try:
            self.Master.Humans.remove(self)
        except:
            pass

    def zombification(self):
        print("A zombie has joined the fight, the minions of hell grow stronger.")
        x,y=self.cell
        dx,dy=random(),random()
        self.Master.Zombies.append(Zombie(self.Master,[x+dx, y+dy]))             #creating a new zombie
        self.Master.Zombies[-1].stop=zIncubationTime
        self.death("zombifié, aware:"+ str(self.aware))

    def pathfinding(self,ressource):

        x,y=self.cell
        idBuilding=self.Master.Map[x][y].idBuilding

        def moveInBuilding(self, ressource, batiment, path, xnew, ynew):
            x1,y1,x2,y2=batiment.corners
            distance=xSize+ySize
            if ressource=="food" or ressource=="rest":
                if ressource=="food":
                    ressource=3
                else:
                    ressource=4
                xr,yr=-1,-1
                for x in range(min(x1,x2)+1, max(x1,x2)):
                    for y in range(min(y1,y2)+1, max(y1,y2)):
                        if self.Master.Map[x][y].content==ressource and self.Master.Map[x][y].quantity>0 and abs((x-xnew))+abs((y-ynew))<distance:
                            xr,yr=x,y
                            distance=abs((xr-xnew))+abs((yr-ynew))

            elif ressource=="shelter":
                xr,yr=(x1+x2)//2, (y1+y2)//2
            if (xr,yr)==(-1,-1):
                return([])
            if ynew<yr:
                path.extend([(xnew, y) for y in range(ynew, yr+1)])
            elif ynew>yr:
                path.extend([(xnew, y) for y in range(ynew, yr-1, -1)])
            if xnew<xr:
                path.extend([(x, yr) for x in range(xnew, xr+1)])
            elif xnew>xr:
                path.extend([(x, yr) for x in range(xnew, xr-1, -1)])

            return(path)

        #If human is already in a building
        if idBuilding!=0 and (self.aware or (not(self.aware) and ressource!="shelter")):
            batiment=self.Master.Buildings[idBuilding-1]
            path=[]
            xnew,ynew=x,y
            #If ressource needed  is in current building
            if (ressource == "food" and batiment.nFoodCells>0) or (ressource == "rest" and batiment.nRestCells>0) or ressource == "shelter":
                return(moveInBuilding(self, ressource, batiment, path, xnew, ynew))

        distance=xSize**2+ySize**2
        xd,yd=-1,-1

        if not(self.aware) and idBuilding==0 and ressource=="shelter":
            idBati=randint(1, len(self.Master.Buildings))
            batiment=self.Master.Buildings[idBati-1]
            doors=batiment.doors
            xd,yd=choice(doors)

        elif not(self.aware) and ressource=="shelter":
            idBati=idBuilding
            while idBati==idBuilding:
                idBati=randint(1, len(self.Master.Buildings))
            batiment=self.Master.Buildings[idBati-1]
            doors=batiment.doors
            xd,yd=choice(doors)
        else:
            for bati in self.Master.Buildings:
                if (ressource == "food" and bati.nFoodCells>0) or (ressource == "rest" and bati.nRestCells>0) or ressource == "shelter":
                    for door in bati.doors:
                        r=(door[0]-self.position[0])**2+(door[1]-self.position[1])**2
                        if r<distance:
                            batiment=bati
                            xd,yd=door[0],door[1]    # xd,yd position of door
                            distance=r
        if (xd,yd)==(-1,-1):
            return([])
        # We create a table of cells that can be passed through
        m=xSize**2+ySize**2
        access=[[m for _ in range(ySize)] for _ in range(xSize)]
        for i in range(xSize):
            for j in range(ySize):
                if self.Master.Map[i][j].content==1:
                    access[i][j] = -1
        if self.aware:
            for zombie in self.Master.Zombies :
                x,y=zombie.cell
                access[x][y] = -1

        # All possible Moves to a neighbor cell, list of cells to visit, final path
        moves=[(1,0),(0,1),(-1,0),(0,-1)]
        toVisit=[(self.cell[0],self.cell[1])]
        access[self.cell[0]][self.cell[1]]=0

        # BFS
        fini=False
        while toVisit and not(fini):
            x,y=toVisit.pop()
            n=access[x][y]
            for dx,dy in moves:
                x2,y2=x+dx,y+dy
                if (0<=x2 and x2<xSize and 0<=y2 and y2<ySize and access[x2][y2]>n+1):
                    toVisit.insert(0,(x2,y2))
                    access[x2][y2]=n+1
                if (x2,y2)==(xd,yd):
                    fini=True
                    break

        # Extraction of the path
        if fini:
            path,x,y,n=[(xd,yd)],xd,yd,access[xd][yd]
            while n>0:
                for dx,dy in moves:
                    if (0<=x+dx and x+dx<=xSize-1 and 0<=y+dy and y+dy<=ySize-1 and access[x+dx][y+dy]==n-1):
                        x,y,n=x+dx,y+dy,n-1
                        path.append((x,y))
                        break
            path.reverse()

            #Enter in the building
            for dx,dy in moves:
                xnew,ynew=xd+dx,yd+dy
                if self.Master.Map[xnew][ynew].idBuilding and not(self.Master.Map[xnew][ynew].content in [1,2]):
                    path.append((xnew,ynew))
                    break

            #Move to the ressource if human inside of building
            return(moveInBuilding(self, ressource, batiment, path, xnew, ynew))

        return([])

    def fight(self):
        self.Master.genSound(self.cell[0],self.cell[1], fightVolume)
        Zstrength=0
        Zbattle=[]
        for Z in self.zProximity():
            Zbattle.append(Z)
            Z.fighting=True
            Z.speed=[0,0]
            Zstrength+=Z.strength
        Hstrength=self.strength
        Hbattle=[self]
        self.fighting=True
        for H in self.hProximity():
            if H.morality=="hero": # or H.group==self.group
                Hbattle.append(H)
                Hstrength+=H.strength                                     #fight system: uniform law.
                H.fighting=True
                H.speed=[0,0]
        proba=random()
        print("fight: Humans:",Hstrength, "Zombies:", Zstrength, "proba:", proba)
        if Hstrength<Zstrength:
            L=Hstrength/(1.2*(Zstrength+Hstrength))
        else:
            L=Zstrength/(1.2*(Zstrength+Hstrength))
        if Hstrength/(Zstrength+Hstrength)+L<=proba:         #zombie(s) stronger than human
            for H in Hbattle:
                H.zombification()
        elif Hstrength/(Zstrength+Hstrength)-L>=proba:        #human stronger than zombie(s)
            for Z in Zbattle:
                Z.death()
        else:                                       #human and zombie(s) as strong: human manage to get away
            for Z in Zbattle:
                Z.stop=2
