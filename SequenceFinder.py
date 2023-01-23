import pygame
import numpy as np
from queue import PriorityQueue

#Generate a 2 dimentional matrix that by traversing through the file
with open('maze.txt') as f:
    lines = f.readlines()

maze=[["X"]*(len(lines)+2)]
for i in range(len(lines)):
    if i==len(lines)-1:
        maze.append(["X"]+list(lines[i])+["X"])
    else:
        maze.append(["X"]+list(lines[i][:-1])+["X"])
maze.append(["X"]*(len(lines)+2))
maze=np.array(maze)
maze=maze.transpose()   ## we do just to visualize with pygame that is fliping the visuals.


##########################################
RES = WIDTH, HEIGHT = 840, 840
TILE = 40
cols, rows = WIDTH // TILE, HEIGHT // TILE

pygame.init()
sc= pygame.display.set_mode(RES)
clock=pygame.time.Clock()



wall = pygame.image.load("brick.png").convert()
wall = pygame.transform.scale(wall, (40, 40))

drone_location=[]
##Class to draw the pygame
class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y


    def draw(self):
        possiblepath=0
        x1, y1 = self.x*TILE, self.y*TILE
        if maze[self.x][self.y]=="X":
            sc.blit(wall, (x1, y1))
            # pygame.draw.rect(sc, pygame.Color('brown'), (x1, y1,TILE, TILE))

        if maze[self.x][self.y]=="_":
            pygame.draw.rect(sc, pygame.Color('darkgrey'), (x1, y1,TILE, TILE))

        if (self.x,self.y) in drone_location:    
            pygame.draw.rect(sc, pygame.Color('orange'), (x1, y1,TILE, TILE))
            possiblepath=1

#Calculate the heuristic for the astar path algorithm
def h(p1, p2):
	return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
#Check and return neighbors for the astar path algorithm
def check_neighbors(x,y):
    neighbors=[]
    if maze[x+1][y]!="X": 
        neighbors.append((x+1,y))
    if maze[x][y+1]!="X":
        neighbors.append((x,y+1))
    if maze[x-1][y]!="X":
        neighbors.append((x-1,y))
    if maze[x][y-1]!="X":
        neighbors.append((x,y-1))
    return neighbors
#take current and next move as input and send back
def find_direction(ghost_drone,next):
    x,y=ghost_drone
    x1,y1=next
    if x1>x:
        return "RIGHT"
    if x1<x:
        return "LEFT"
    if y1>y:
        return "DOWN"
    if y1<y:
        return "UP"

#######for priority queue A star path. Same as project 1
def astarsearch(start,end):
    count=0
    PQ = PriorityQueue()
    PQ.put((0, count, start))
    came_from = {}
    g = {(col, row): float("inf") for row in range(len(maze)) for col in range(len(maze))}
    g[start] = 0
    f = {(col, row): float("inf") for row in range(len(maze)) for col in range(len(maze))}
    f[start] = h(start, end)
    PQ_list = {start}
    while True:
        current = PQ.get()[2]
        PQ_list.remove(current)
        Cell(current[0],current[1]).visited = True
        if current == end:
            l=0
            patha=[]
            while current in came_from:
                current = came_from[current]
                patha.append(current)
                l=l+1
            patha.insert(0,end)
            patha=patha[:-1]
            return patha

        for neighbor in check_neighbors(current[0],current[1]):
            temp_g = g[current] + 1
            if temp_g < g[neighbor]:
                came_from[neighbor] = current
                g[neighbor] = temp_g
                f[neighbor] = temp_g + h(neighbor, end)
                if neighbor not in PQ_list:
                    count += 1
                    PQ.put((f[neighbor], count, neighbor))
                    PQ_list.add(neighbor)
            
        if len(PQ_list)==0:
            return "no possible path"

#get different quadarant or local blocks so we can solve
def get_quadrant_drones(drone_location):
    Quadrant_point=[(8,8),(19,11),(8,15),(19,19)]#[(8,8),(11,19),(15,8),(19,19)]
    dq1,dq2,dq3,dq4=([],[],[],[])
    drone_location=sorted(drone_location)
    for i in drone_location:
        dist_from_q1=len(astarsearch(i,Quadrant_point[0]))
        dist_from_q2=len(astarsearch(i,Quadrant_point[1]))
        dist_from_q3=len(astarsearch(i,Quadrant_point[2]))
        dist_from_q4=len(astarsearch(i,Quadrant_point[3]))
        all_dist=[dist_from_q1,dist_from_q2,dist_from_q3,dist_from_q4]
        min_dist=all_dist.index(min(all_dist))
        if min_dist==0:
            dq1.append(i)
        elif min_dist==1:
            dq2.append(i)
        elif min_dist==2:
            dq3.append(i)
        else:
            dq4.append(i)
    return dq1,dq2,dq3,dq4

####To implement each move, we just change the drone locations we are maintaining in a list. The below code does that based on the move order
ghost_drone=()
def implement_astarmove(nextset,drone_location,converge,find_min):
    global ghost_drone
    if converge in find_min and len(drone_location)>4:
        find_min.remove(converge)
    if len(nextset)==0:        ########this block check if we have some moves to complete astar or else generates a new set of moves for a different location
        ghost_drone=min(find_min)
        nextset=astarsearch(ghost_drone,converge)
        
    nextmove=find_direction(ghost_drone,nextset[-1])
    ghost_drone=nextset[-1]
    nextset=nextset[:-1]
    # print(nextmove,nextset)

    if nextmove == "DOWN":
        instruct.append("down")
        # print(len(instruct),drone_location)
        for pos in drone_location:
            if maze[pos[0]][pos[1]+1]=="X":
                if (pos[0],pos[1]) not in drone_location_next:
                    drone_location_next.append((pos[0],pos[1]))
            else:
                if (pos[0],pos[1]+1) not in drone_location_next:
                    drone_location_next.append((pos[0],pos[1]+1))

    
    if nextmove == "RIGHT":
        instruct.append("right")
        # print(len(instruct),drone_location)
        for pos in drone_location:
            if maze[pos[0]+1][pos[1]]=="X":
                if (pos[0],pos[1]) not in drone_location_next:
                    drone_location_next.append((pos[0],pos[1]))
            else:
                if (pos[0]+1,pos[1]) not in drone_location_next:
                    drone_location_next.append((pos[0]+1,pos[1]))
        
    if nextmove == "LEFT":
        instruct.append("left")
        # print(len(instruct),drone_location)
        for pos in drone_location:
            if maze[pos[0]-1][pos[1]]=="X":
                if (pos[0],pos[1]) not in drone_location_next:
                    drone_location_next.append((pos[0],pos[1]))
            else:
                if (pos[0]-1,pos[1]) not in drone_location_next:
                    drone_location_next.append((pos[0]-1,pos[1]))
        
    if nextmove == "UP":
        instruct.append("up")
        # print(len(instruct),drone_location)
        for pos in drone_location:
            if maze[pos[0]][pos[1]-1]=="X":
                if (pos[0],pos[1]) not in drone_location_next:
                    drone_location_next.append((pos[0],pos[1]))
            else:
                if (pos[0],pos[1]-1) not in drone_location_next:
                    drone_location_next.append((pos[0],pos[1]-1))

    return nextset,drone_location_next

drone_location=[]
for i in range(21):
    for j in range(21):
        if maze[i][j]=="_":
            drone_location.append((i,j))
drone_location_next=[]
oldlen=len(drone_location)
instruct=[]
direction=["UP","RIGHT","DOWN","LEFT"]
nextset=[]
nextset1=[]
index=0
c=0
run=True

while run:
    sc.fill(pygame.Color("black"))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False
    for i in range(21):
        for j in range(21):
            Cell(i,j).draw()
#####implement part 1 as explained in the report
    drone_location_next=[]
    if index<4:
        if direction[index] == "DOWN":
            instruct.append("down")
            for pos in drone_location:
                if maze[pos[0]][pos[1]+1]=="X":
                    if (pos[0],pos[1]) not in drone_location_next:
                        drone_location_next.append((pos[0],pos[1]))
                else:
                    if (pos[0],pos[1]+1) not in drone_location_next:
                        drone_location_next.append((pos[0],pos[1]+1))

        if direction[index] == "RIGHT":
            instruct.append("right")
            for pos in drone_location:
                if maze[pos[0]+1][pos[1]]=="X":
                    if (pos[0],pos[1]) not in drone_location_next:
                        drone_location_next.append((pos[0],pos[1]))
                else:
                    if (pos[0]+1,pos[1]) not in drone_location_next:
                        drone_location_next.append((pos[0]+1,pos[1]))
        if direction[index] == "LEFT":
            instruct.append("left")
            for pos in drone_location:
                if maze[pos[0]-1][pos[1]]=="X":
                    if (pos[0],pos[1]) not in drone_location_next:
                        drone_location_next.append((pos[0],pos[1]))
                else:
                    if (pos[0]-1,pos[1]) not in drone_location_next:
                        drone_location_next.append((pos[0]-1,pos[1]))
        if direction[index] == "UP":
            instruct.append("up")
            for pos in drone_location:
                if maze[pos[0]][pos[1]-1]=="X":
                    if (pos[0],pos[1]) not in drone_location_next:
                        drone_location_next.append((pos[0],pos[1]))
                else:
                    if (pos[0],pos[1]-1) not in drone_location_next:
                        drone_location_next.append((pos[0],pos[1]-1))
     
        oldlen=drone_location==drone_location_next#len(drone_location)
        drone_location=drone_location_next.copy()
##implement part2 which is local convergance as explained in the report.
    elif len(drone_location)>4:
        # print("local",len(drone_location))
        Quadrant_point=[(8,8),(19,11),(8,15),(19,19)]#[(8,8),(11,19),(15,8),(19,19)]
        dronesQ1,dronesQ2,dronesQ3,dronesQ4=get_quadrant_drones(drone_location)
        # print(drone_location)

        if len(dronesQ1)>1:
            nextset,drone_location_next=implement_astarmove(nextset,drone_location,Quadrant_point[0],dronesQ1)
        elif len(dronesQ2)>1:
            nextset,drone_location_next=implement_astarmove(nextset,drone_location,Quadrant_point[1],dronesQ2)
        elif len(dronesQ3)>1:
            nextset,drone_location_next=implement_astarmove(nextset,drone_location,Quadrant_point[2],dronesQ3)
        elif len(dronesQ4)>1:
            nextset,drone_location_next=implement_astarmove(nextset,drone_location,Quadrant_point[3],dronesQ4)
        drone_location=drone_location_next.copy()
##implement part3 which is global convergance.
    elif len(drone_location)>1:
        # print("enter elif",len(drone_location))
        nextset,drone_location_next=implement_astarmove(nextset,drone_location,(19,19),drone_location)
        drone_location=drone_location_next.copy()
#####to exit the loop if total locations of drones become 1
    else:
        print(instruct,len(instruct))
        run=False
###implement index increment to enable part 1 execution
    if oldlen:#len(drone_location_next)==oldlen and c>1:
        instruct=instruct[:-1]
        index+=1
        if(index>=4):
            oldlen=False
    pygame.display.flip()
    clock.tick(100)

# print(instruct,len(instruct))

# print(time.time()-start_time)