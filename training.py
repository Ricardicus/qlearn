from util import *
from random import uniform, randint

dimension = 10
update_time = 5
rewards = {'apple': 1.0, 'death': -100.0, 'default': -0.01}
Q_vals = {}

### parameters ###
# bellman coefficient
gamma = 0.9
# learning rate
alpha = 0.80
# greedyness
epsilon = 0.001

episode_count = 1
episode_score = 0

store_every = 100
store_info_every = 1

avg_score_hundred = []
explored = []
new_states = 0

root = ""

def timerFired(data):
	global episode_count, episode_score, avg_score_hundred, explored, Q_vals, root
	# The game loop event trigger!
	if (data["isGameOver"] == False):

		# Will only process if the game is not over
		redrawAll(data)
		direct = data["direction"]
		snakeBoard = data["snakeBoard"]

		# testing all direction
		best_action = "forward"
		qval_best = -9999
		for action in ["forward", "left", "right"]:
			# Updating the Q-values for each action
			# Action is based upon arg_{max} Q(state, arg)
			# or random, based on greedyness parameter eplison
			results = next_state(data, action)
			reward = results["reward"]
			new_direction = results["newDirection"]

			if ( reward == rewards["death"]):
				key = get_key(snakeBoard, action)
				Q_vals[key] = reward
				if ( Q_vals[key] > qval_best ):
					qval_best = Q_vals[key]
					best_action = action
			else:
				# looking one step ahead to find the highest Q-value!
				# Q(s,a) = R(s,a) + gamma * [max_{a'} Q(s',a')]
				key = get_key(snakeBoard, action)
				new_snakeBoard = results["newSnakeBoard"]
				scoreTemp = data["score"]
				
				if ( reward == rewards["apple"] ):
					scoreTemp += 1
					place_food(new_snakeBoard)

				qval_highest = -9999
				for sample_action in ["forward", "left", "right"]:
					sample_data = {}
					sample_data["snakeBoard"] = new_snakeBoard
					sample_data["direction"] = new_direction
					sample_data["rewards"] = rewards

					sample_result = next_state(sample_data, sample_action)
					sample_scoreTemp = scoreTemp

					sample_snakeBoard = deepcopy(new_snakeBoard)
					if ( sample_result["reward"] == rewards["apple"] ):
						sample_scoreTemp += 1
						place_food(sample_snakeBoard)
					
					sample_key = get_key(sample_snakeBoard, sample_action)

					try:
						Q_vals[sample_key]
					except:
						Q_vals[sample_key] = 0
					if ( Q_vals[sample_key] > qval_highest ):
						qval_highest = Q_vals[sample_key]

				try:
					Q_vals[key]
				except:
					Q_vals[key] = 0
				# the highest q-value found.. 
				Q_vals[key] = ( 1 - alpha ) * Q_vals[key] + alpha * ( reward + gamma * qval_highest )
				if ( Q_vals[key] > qval_best ):
					qval_best = Q_vals[key]
					best_action = action
	
		next_action = best_action

		# act randomly, to increase state space 
		# and prevent getting stuck
		greed = uniform(0,1)
		if ( greed < epsilon ):
			moves = ["forward", "left", "right"]
			moves.remove(best_action)
			next_action = moves[randint(0,1)]
			#print "random move!"

		results = next_state(data, next_action)
		reward = results["reward"]

		if ( reward == rewards["default"] ):
			new_snakeBoard = results["newSnakeBoard"]
			new_direction = results["newDirection"]
			data["snakeBoard"] = new_snakeBoard
			data["direction"] = new_direction
		elif ( reward == rewards["death"] ):
			#print "died!!"
			data["isGameOver"] = True
		elif (reward == rewards["apple"]):
			#print "ate an apple!"
			data["score"] += 1

			new_snakeBoard = results["newSnakeBoard"]
			new_direction = results["newDirection"]
			place_food(new_snakeBoard)
			data["snakeBoard"] = new_snakeBoard
			data["direction"] = new_direction

		#print "states: ", len(Q_vals)

		# Call if the game is not over!
		data["canvas"].after(update_time, timerFired, data) # The main game-loop!
	else:
		if ( len(avg_score_hundred) >= 10000 ):
			avg_score_hundred = avg_score_hundred[1:]
		avg_score_hundred.append(data["score"])

		print "episode: ", episode_count, " score: ", data["score"], " avg score over 100: ", sum(avg_score_hundred) / (1.0*len(avg_score_hundred)), " states: ", len(Q_vals)

		if ( episode_count % store_info_every == 0):
			f = open('info.txt', "w")
			f.write("episode: " + str(episode_count) + " score: " + str(data["score"]) + " avg score over 100: " + str(sum(avg_score_hundred) / (1.0*len(avg_score_hundred))) + " states: " + str(len(Q_vals)))
			f.close()

		episode_count += 1
		start_new_episode(data)

		if (episode_count % store_every == 0):
			store_Q_vals(Q_vals)
			root.quit()
		else:
			data["canvas"].after(update_time, timerFired, data)

def game_on():
	global root, Q_vals

	root = Tk()
	margin = 3
	cellSize = 15
	canvasWidth = 2*margin + dimension*cellSize
	canvasHeight = 2*margin + dimension*cellSize
	canvas = Canvas(root, width=canvasWidth, height=canvasHeight)
	canvas.pack()
	root.resizable(width=0, height=0)
	# Stores canvas in root and in itself for callbacks. (Not original idea.. found help online)
	root.canvas = canvas.canvas = canvas
	# Setting up the canvas and the dictionary containg data of the game in canvas.
	data = {}
	data["canvas"] = canvas
	data["margin"] = margin
	data["cellSize"] = cellSize
	data["canvasWidth"] = canvasWidth
	data["canvasHeight"] = canvasHeight
	data["points"] = 0
	data["rewards"] = rewards

	data["isGameOver"] = False
	data["training"] = False
	data["dimension"] = dimension
	snakeBoard = []

	for r in range(0,dimension):
		snakeBoard.append([])
		for c in range(0, dimension):
			snakeBoard[r].append(0)

	data["snakeBoard"] = snakeBoard
	# set up events
#	root.bind("<Button-1>", mousePressed)
#	root.bind("<Key>", keyPressed)
	start_new_episode(data)

	Q_vals = load_Q_vals()
	print len(Q_vals), " states loaded."

	timerFired(data)

	# and launch the app
	root.mainloop() 

if __name__ == "__main__":
	game_on()
