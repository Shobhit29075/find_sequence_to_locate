import pygame
import numpy as np
from queue import PriorityQueue

#Generate True and False with a probablity of 28:72
with open('maze.txt') as f:
    lines = f.readlines()

maze=[["X","X","X","X","X","X","X","X","X","X","X","X","X","X","X","X","X","X","X","X","X"]]
for i in range(len(lines)):
    if i==18:
        maze.append(["X"]+list(lines[i])+["X"])
    else:
        maze.append(["X"]+list(lines[i][:-1])+["X"])
maze.append(["X","X","X","X","X","X","X","X","X","X","X","X","X","X","X","X","X","X","X","X","X"])
maze=np.array(maze)
maze=maze.transpose()

##########################################
RES = WIDTH, HEIGHT = 840, 840
TILE = 40
cols, rows = WIDTH // TILE, HEIGHT // TILE

pygame.init()
sc= pygame.display.set_mode(RES)
clock=pygame.time.Clock()

# ghost = pygame.image.load("ghost.png").convert()
# ghost = pygame.transform.scale(ghost, (16, 16))

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

  
    def draw_current_cell(self):
        x1,y1=self.x*TILE,self.y*TILE
        if maze[self.x][self.y]=="O":
            pygame.draw.rect(sc, pygame.Color('brown'), (x1, y1,TILE, TILE))
        elif maze[self.x][self.y]=="_":
            pygame.draw.rect(sc, pygame.Color('darkgrey'), (x1, y1,TILE, TILE))


def h(p1, p2):
	return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

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


def get_quadrant_drones(drone_location):
    Quadrant_point=[(8,8),(11,19),(15,8),(19,19)]
    dq1,dq2,dq3,dq4=([],[],[],[])
    for i in drone_location:
        if i[0]<=13 and i[1]<=8:
            dq1.append(i)
        elif i[0]<=11 and i[1]<=19:
            dq2.append(i)
        elif i[0]<=19 and i[1]<=8:
            dq3.append(i)
        else:
            dq4.append(i)
    return dq1,dq2,dq3,dq4


#######for priority queue A star path
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
    # print(PQ_list)
    while True:
        current = PQ.get()[2]
        # print(current)
        PQ_list.remove(current)
        # Cell(current[0],current[1]).visited = True
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

####To run the agent multiple times and store the result in pandas dataframe


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
#ins=['up', 'up', 'up', 'up', 'up', 'up', 'up', 'up', 'up', 'up', 'up', 'up', 'up', 'up', 'up', 'up', 'up', 'up', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'down', 'down', 'down', 'down', 'down', 'down', 'down', 'down', 'down', 'down', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'down', 'down', 'down', 'down', 'down', 'down', 'down', 'up', 'right', 'right', 'down', 'down', 'down', 'left', 'left', 'left', 'left', 'left', 'up', 'up', 'up', 'up', 'up', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'down', 'down', 'down', 'down', 'down', 'down', 'down', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'down', 'down', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'down', 'down', 'down', 'down', 'down', 'down', 'down', 'down', 'down', 'right', 'up', 'left', 'left', 'down', 'left', 'left', 'up', 'left', 'left', 'left', 'up', 'up', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'down', 'down', 'down', 'down', 'down', 'down', 'down', 'down', 'down', 'right', 'left', 'down', 'down', 'right', 'down', 'down', 'right', 'right', 'right', 'right', 'up', 'up', 'up', 'up', 'up', 'up', 'up', 'right', 'right', 'down', 'right', 'right', 'down', 'down', 'right', 'right', 'down', 'down', 'down', 'down', 'right', 'up', 'up', 'up', 'left', 'left', 'left', 'left', 'left', 'up', 'up', 'left', 'left', 'down', 'down', 'down', 'down', 'down', 'down', 'down', 'down', 'down', 'down', 'down', 'down', 'down', 'down', 'down', 'down', 'down', 'down', 'right', 'right', 'up', 'up', 'up', 'up', 'up', 'up', 'up', 'right', 'right', 'down', 'right', 'right', 'down', 'down', 'right', 'right', 'down', 'down', 'down', 'down', 'right', 'up', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'down', 'down', 'down', 'down', 'down', 'down', 'down', 'down', 'down', 'right', 'right', 'up', 'up', 'up', 'up', 'up', 'up', 'up', 'right', 'right', 'down', 'right', 'right', 'down', 'down', 'right', 'right', 'down', 'down', 'down', 'down', 'right']
ins=['up', 'up', 'up', 'up', 'up', 'up', 'up', 'up', 'up', 'up', 'up', 'up', 'up', 'up', 'up', 'up', 'up', 'up', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'down', 'down', 'down', 'down', 'down', 'down', 'down', 'down', 'down', 'down', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'down', 'down', 'down', 'down', 'down', 'down', 'down', 'up', 'right', 'right', 'down', 'down', 'down', 'left', 'left', 'left', 'left', 'left', 'up', 'up', 'up', 'up', 'up', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'down', 'down', 'down', 'down', 'down', 'down', 'down', 'up', 'left', 'left', 'down', 'left', 'left', 'up', 'left', 'left', 'left', 'up', 'up', 'up', 'up', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'up', 'up', 'left', 'left', 'left', 'down', 'down', 'down', 'down', 'down', 'right', 'right', 'right', 'right', 'right', 'down', 'down', 'down', 'up', 'up', 'left', 'up', 'up', 'right', 'down', 'down', 'down', 'down', 'left', 'left', 'left', 'left', 'up', 'up', 'left', 'up', 'up', 'right', 'right', 'right', 'right', 'right', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'down', 'down', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'down', 'down', 'down', 'down', 'down', 'down', 'down', 'down', 'down', 'right', 'right', 'up', 'up', 'up', 'up', 'up', 'up', 'up', 'right', 'right', 'down', 'right', 'right', 'down', 'down', 'right', 'right', 'down', 'down', 'down', 'down', 'right', 'left', 'down', 'down', 'right', 'down', 'down', 'right', 'right', 'right', 'right', 'up', 'up', 'up', 'up', 'up', 'up', 'up', 'right', 'right', 'down', 'right', 'right', 'down', 'down', 'right', 'right', 'down', 'down', 'down', 'down', 'right', 'up', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'down', 'down', 'down', 'down', 'down', 'down', 'down', 'down', 'down', 'right', 'right', 'up', 'up', 'up', 'up', 'up', 'up', 'up', 'right', 'right', 'down', 'right', 'right', 'down', 'down', 'right', 'right', 'down', 'down', 'down', 'down', 'right']
while run:#len(drone_location)>1:    #####number of simulations for each number of ghosts
    sc.fill(pygame.Color("black"))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False
    for i in range(21):
        for j in range(21):
            Cell(i,j).draw()

    drone_location_next=[]
    if index<len(ins):
        if ins[index] == "down":
            instruct.append("down")
            # print(len(instruct),drone_location)
            for pos in drone_location:
                if maze[pos[0]][pos[1]+1]=="X":
                    drone_location_next.append((pos[0],pos[1]))
                else:
                    if (pos[0],pos[1]+1) not in drone_location_next:
                        drone_location_next.append((pos[0],pos[1]+1))

        
        if ins[index] == "right":
            instruct.append("right")
            print("right")
            # print(len(instruct),drone_location)
            for pos in drone_location:
                if maze[pos[0]+1][pos[1]]=="X":
                    drone_location_next.append((pos[0],pos[1]))
                else:
                    if (pos[0]+1,pos[1]) not in drone_location_next:
                        drone_location_next.append((pos[0]+1,pos[1]))
            print(drone_location)
            print(drone_location_next)
            exit

        if ins[index] == "left":
            instruct.append("left")
            # print(len(instruct),drone_location)
            for pos in drone_location:
                if maze[pos[0]-1][pos[1]]=="X":
                    drone_location_next.append((pos[0],pos[1]))
                else:
                    if (pos[0]-1,pos[1]) not in drone_location_next:
                        drone_location_next.append((pos[0]-1,pos[1]))
            
        if ins[index] == "up":
            instruct.append("up")
            # print("up")
            # print(len(instruct),drone_location)
            for pos in drone_location:
                if maze[pos[0]][pos[1]-1]=="X":
                    drone_location_next.append((pos[0],pos[1]))
                else:
                    if (pos[0],pos[1]-1) not in drone_location_next:
                        drone_location_next.append((pos[0],pos[1]-1))
            # print(len(drone_location),len(drone_location_next))
        drone_location=drone_location_next.copy()
  

    # else:
    #     run=False




    index+=1
    pygame.display.flip()
    clock.tick(10)

print(instruct,len(instruct))


# print(time.time()-start_time)


