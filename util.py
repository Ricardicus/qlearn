from random import *
from copy import deepcopy
from Tkinter import *

# row, col
directions = [[1,0],[0,1], [-1,0], [0,-1]]
dimension = 10

def store_Q_vals(Q_vals):
	f = open("learning/Qvals", "w")
	for key in Q_vals:
		f.write(key + '@' + str(Q_vals[key]) + '\n')
	f.close()

def load_Q_vals():
	Q_vals = {}

	try:
		f = open("learning/Qvals", "r")
		for line in f:
			key = line.split('@')[0]
			value = float(line.split('@')[1])
			Q_vals[key] = value
		f.close()
	except:
		pass
	return Q_vals


def next_state(data, action):
	snakeBoard = deepcopy(data["snakeBoard"])
	direction = data["direction"]
	rewards = data["rewards"]

	if action == "left":
		direction = (direction + 1) % len(directions)
	elif action == "right":
		direction = (len(directions) + direction - 1) % len(directions)

	dRow = directions[direction][0]
	dCol = directions[direction][1]

	headRow = 0
	headCol = 0

	# finding the head of the snake
	max = 0
	for r in range(0,dimension):
		for c in range(0,dimension):
			if ( snakeBoard[r][c] > max):
				max = snakeBoard[r][c]
				headRow = r
				headCol = c

	newHeadRow = headRow + dRow
	newHeadCol = headCol + dCol

	result = {'newHeadRow': newHeadRow, 'newHeadCol': newHeadCol, 'newDirection': direction}

	result["reward"] = rewards["default"]

	if newHeadCol == 0 or newHeadCol == dimension - 1:
		# signaling that the snake dies
		result["reward"] = rewards["death"]	
		return result
	if newHeadRow == 0 or newHeadRow == dimension - 1:
		# singlaing that the snake dies
		result["reward"] = rewards["death"]	
		return result
	if snakeBoard[newHeadRow][newHeadCol] > 0:
		# singlaing that the snake dies
		result["reward"] = rewards["death"]	
		return result

	if snakeBoard[newHeadRow][newHeadCol] == -1:
		# signaling apple found
		result["reward"] = rewards["apple"]

	continuing(snakeBoard, result["reward"] == rewards["apple"], newHeadRow, newHeadCol)
	result["newSnakeBoard"] = snakeBoard

	return result

def continuing(snakeBoard, apple, newHeadRow, newHeadCol):
	
	max = 0
	for r in range(0,dimension):
		for c in range(0,dimension):
			if ( snakeBoard[r][c] > max):
				max = snakeBoard[r][c]

		# continuing
	snakeBoard[newHeadRow][newHeadCol] = max + 1

	if (not apple):
		for r in range(0,dimension):
			for c in range(0,dimension):
				if snakeBoard[r][c] > 0:
					snakeBoard[r][c] -= 1


def place_food(snakeBoard):
	# new apple start location
	ar = randint(1,dimension-2)
	ac = randint(1,dimension-2)

	while ( snakeBoard[ar][ac] > 0):
		ar = randint(1,dimension-2)
		ac = randint(1,dimension-2)

	snakeBoard[ar][ac] = -1

def start_new_episode(data):
	data["isGameOver"] = False
	snakeBoard = data["snakeBoard"]
	data["score"] = 0

	for r in range(0,dimension):
		for c in range(0,dimension):
			snakeBoard[r][c] = 0

	# new snake start location
	snakeBoard[randint(2, dimension-2)][randint(2, dimension-2)] = 1

	place_food(snakeBoard)

	data["direction"] = randint(0,3)

def reconstruct_snake_board_from_key(key):
	v = key.split('-')

	snakeBoard = []

	for r in range(0,dimension):
		snakeBoard.append([])
		for c in range(0, dimension):
			snakeBoard[r].append(0)

	for r in range(0,dimension):
		for c in range(0, dimension):
			snakeBoard[r][c] = int(v[r*dimension + c])
			apple = [r,c]

	snakeBoard[int(v[len(v) - 3])][int(v[len(v) - 2])] = -1
	direction = int(v[len(v) - 1])

	data = {}
	data["snakeBoard"] = snakeBoard
	data["direction"] = direction

	return data

def get_key(snakeBoard, direction):
#	need direcion [0,1,2,3] in directions
#	the snake board grid
#	dimension NxN

	key = ""
	apple = []

	if ( direction == "forward" ):
		direction = "f"
	elif ( direction == "left" ):
		direction = "l"
	elif ( direction == "right" ):
		direction = "r"

	first = 1
	for r in range(0,dimension):
		for c in range(0, dimension):
			if ( snakeBoard[r][c] == -1):
				apple = [r,c]
				if ( first != 1):
					key += '-'
				key += '0'
			else:
				if ( first != 1):
					key += '-'
				key += str(snakeBoard[r][c])
			first = 0

	key += "-" + str(apple[0]) + "-" + str(apple[1]) + "-" + direction

	return key

def get_number_of_states(Q_vals):
	states = 0
	for i in range(0,len(Q_vals)):
		states += len(Q_vals[i])
	return states


