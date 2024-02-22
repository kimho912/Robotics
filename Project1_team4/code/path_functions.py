def locate_row(grid, char):
	row = 0
	for i in grid:
		row+=1
		col = 0
		for k in i:
			col+=1
			if k == char:
				return row-1

def locate_col(grid, char):
	row = 0
	for i in grid:
		row+=1
		col = 0
		for k in i:
			col+=1
			if k == char:
				return col-1

def gen_coord(grid, char):
	coord = []
	coord.append(locate_row(grid, char))
	coord.append(locate_col(grid, char))
	return coord

def gen_goal_room(room, start, goal):
	goal_room = [row[:] for row in room]
	goal_room[start[0]][start[1]] = 0
	goal_room[goal[0]][goal[1]] = 3
	return goal_room
