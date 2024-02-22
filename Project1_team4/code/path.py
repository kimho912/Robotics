import math
import path_functions as pf
import path_node as pn
def findpath():
    room = [[0 for i in range(16)] for j in range(10)]

    obstacle_coord = [[4, 1], [4, 2],[4, 3],[4,4],
                    [4, 5],[7, 4], [7, 5],[7, 6],
                    [7, 7],[7, 8],[7, 9],[7, 10],[10, 3], [10, 4], [10, 5], [10, 6], [10, 7],
					[11, 3], [12, 3], [12, 4], [13, 3], [13, 4]]

    tile_obstacle = []
    for i in obstacle_coord:
    	 tile_obstacle.append([i[0],i[1]])

    for i in tile_obstacle:
        room[10 - i[1]][i[0]] = 1
        room[10 - i[1] - 1][i[0]] = 1
        room[10 - i[1]][i[0] - 1] = 1
        room[10 - i[1] - 1][i[0] - 1] = 1
    
    start = [.305,1.219]
    goal = [3.658,1.829]
        
    start_cellx = 2
    start_celly = 10 - 2
   
    goal_cellx = 13
    goal_celly = 10 - 7
        
    room[goal_celly][goal_cellx] = 6
    print(start_cellx)
    print(start_celly)
    room[start_celly][start_cellx] = 3
    
    goal = pf.gen_coord(room, 6)
    start = pf.gen_coord(room, 3)
  
    goal_room = pf.gen_goal_room(room, start, goal)
   
    start_node = pn.Node(list(room), 0, "Start", 0, 0,None)
    start_node.print_node()
    def manhattan(start,goal):
        return abs(start[0] - goal[0]) + abs(start[1] - goal[1])

    fringe = []
    closed = []

    fringe.append([start_node,manhattan(pf.gen_coord(room,3),goal)])
    while fringe:
        node_puzzle = fringe.pop(0)
        node = node_puzzle[0]

        if node.grid[goal[0]][goal[1]] == 3:    
            break

        if node.grid not in closed:
            closed.append(node.grid)
            if node.check("right"):
                right = node.gen_state("right",node,node.cost+1)
                fringe.append([right, right.cost + manhattan(pf.gen_coord(right.grid,3),goal)])
            if node.check("down"):
                down = node.gen_state("down",node,node.cost+1)
                fringe.append([down, down.cost + manhattan(pf.gen_coord(down.grid,3),goal)])
            if node.check("left"): 
                left  = node.gen_state("left",node,node.cost+1)
                fringe.append([left, left.cost + manhattan(pf.gen_coord(left.grid,3),goal)])
            if node.check("up"):
                up = node.gen_state("up",node,node.cost+1)
                fringe.append([up, up.cost + manhattan(pf.gen_coord(up.grid,3),goal)])
            
        fringe.sort(key=lambda x:x[1])

    node.print_node()
    moveList = []
    moveArr = []
    while node is not None:
        moveList.append(node.move)
        moveArr.append(node.grid)
        node = node.parent
    
    moveArr.reverse()
    moveList.reverse()
    return moveList[1:]
