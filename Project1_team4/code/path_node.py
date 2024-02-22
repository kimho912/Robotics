import path_functions as pf

class Node:
	def __init__(self, grid, cost, move, tileMoved, hval,parent):
		self.grid = grid
		self.cost = cost
		self.move = move
		self.tileMoved = tileMoved
		self.hval = hval
		self.parent = parent
			
	def gen_state(self, direction,parent,cost):
		deepGrid = [row[:] for row in self.grid]
		row = pf.locate_row(deepGrid, 3)
		col = pf.locate_col(deepGrid, 3)
		blank = 0
		tile = 0
		if direction == 'up':
			blank = deepGrid[row][col]
			tile = deepGrid[row-1][col]
			deepGrid[row][col] = tile
			deepGrid[row-1][col] = blank
		if direction == 'down':
			blank = deepGrid[row][col]
			tile = deepGrid[row+1][col]
			deepGrid[row][col] = tile
			deepGrid[row+1][col] = blank
		if direction == 'left':
			blank = deepGrid[row][col]
			tile = deepGrid[row][col-1]
			deepGrid[row][col] = tile
			deepGrid[row][col-1] = blank
		if direction == 'right':
			blank = deepGrid[row][col]
			tile = deepGrid[row][col+1]
			deepGrid[row][col] = tile
			deepGrid[row][col+1] = blank
		#newCost = self.cost+tile
		generatedState = Node(deepGrid, cost, direction, tile, self.hval,parent)
		return generatedState
	
	def check(self,direction):
		row = pf.locate_row(self.grid, 3)
		col = pf.locate_col(self.grid, 3)
		if direction == "up":
			if row > 0 and (self.grid[row-1][col] == 0 or self.grid[row-1][col] == 6):
				return True
			else:
				return False
		if direction == "down":
			if row < 9 and (self.grid[row+1][col] == 0 or self.grid[row+1][col] == 6):
				return True
			else:
				return False
		if direction == "left":
			if col >= 1 and (self.grid[row][col-1] == 0 or self.grid[row][col-1] == 6):
				return True
			else:
				return False
		if direction == "right":
			if col < 15 and (self.grid[row][col+1] == 0 or self.grid[row][col+1] == 6):
				return True
			else:
				return False	


	def print_node(self):
		for i in range(10):
			print(self.grid[i])
		print('\n')
