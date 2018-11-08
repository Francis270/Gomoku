import random
import pisqpipe as pp
from pisqpipe import DEBUG_EVAL, DEBUG

pp.infotext = 'name="pbrain-bordeaux-francois.caicedo", author="François Caïcedo and Pierre-Laurent Vergnaud", version="1.0", country="France", www="https://github.com/Francis270/gomoku"'

DEBUG_LOGFILE = "C:\\Users\\Francis\\Documents\\GitHub\\Gomoku\\debug.txt"

MAX_BOARD = 100
board = [[0 for i in range(MAX_BOARD)] for j in range(MAX_BOARD)]
my_brain = {
	"ite": 0,
	"last": [0, 0],
	"dir": "north"
}

def brain_init():
	if pp.width < 5 or pp.height < 5:
		pp.pipeOut("ERROR size of the board")
		return
	if pp.width > MAX_BOARD or pp.height > MAX_BOARD:
		pp.pipeOut("ERROR Maximal board size is {}".format(MAX_BOARD))
		return
	pp.pipeOut("OK")

def brain_restart():
	for x in range(pp.width):
		for y in range(pp.height):
			board[x][y] = 0
	my_brain["ite"] = 0
	pp.pipeOut("OK")

def isValidPos(x, y, to_search):
	return x >= 0 and y >= 0 and x < pp.width and y < pp.height and board[x][y] == to_search

def isFree(x, y):
	return x >= 0 and y >= 0 and x < pp.width and y < pp.height and board[x][y] == 0

def brain_my(x, y):
	if isFree(x,y):
		board[x][y] = 1
	else:
		pp.pipeOut("ERROR my move [{},{}]".format(x, y))

def brain_opponents(x, y):
	if isFree(x,y):
		board[x][y] = 2
	else:
		pp.pipeOut("ERROR opponents's move [{},{}]".format(x, y))

def brain_block(x, y):
	if isFree(x,y):
		board[x][y] = 3
	else:
		pp.pipeOut("ERROR winning move [{},{}]".format(x, y))

def brain_takeback(x, y):
	if x >= 0 and y >= 0 and x < pp.width and y < pp.height and board[x][y] != 0:
		board[x][y] = 0
		return 0
	return 2

def make_random_move():
	while True:
		my_brain["last"][0] = random.randint(0, pp.width)
		my_brain["last"][1] = random.randint(0, pp.height)
		if isFree(my_brain["last"][0], my_brain["last"][1]):
			break
	pp.do_mymove(my_brain["last"][0], my_brain["last"][1])

def init_node_params(node, dir, head, tail, add_head, add_tail):
	ret = {
		"node": node,
		"dir": dir,
		"head": head,
		"tail": tail,
		"add_head": add_head,
		"add_tail": add_tail
	}
	return ret

def init_node():
	ret = {
		"node": [
		],
		"dir": "none",
		"head": [0, 0],
		"tail": [0, 0],
		"add_head": [0, 0],
		"add_tail": [0, 0]
	}
	return ret

def best_nonblock_serie(player):
	ret = init_node()
	to_search = 0
	if player == "vilain":
		to_search = 2
	elif player == "hero":
		to_search = 1
	max = 0
	for x in range(pp.width):
		for y in range(pp.height):
			if board[x][y] == to_search:

				# nord
				size = 1
				node = []
				z = y
				while isValidPos(x, z, to_search):
					if board[x][z] == to_search:
						node.append([x, z])
						size += 1
					z -= 1
				if size > max:
					if isValidPos(x, z + 1, 0) or isValidPos(x, z, 0):
						max = size
						ret = init_node_params(node, "nord", [x, y], [x, z + 1], [x, y + 1], [x, z])

				# south
				size = 1
				node = []
				z = y
				while isValidPos(x, z, to_search):
					if board[x][z] == to_search:
						node.append([x, z])
						size += 1
					z += 1
				if size > max:
					if isValidPos(x, z - 1, 0) or isValidPos(x, z, 0):
						max = size
						ret = init_node_params(node, "south", [x, y], [x, z - 1], [x, y - 1], [x, z])

				# west
				size = 1
				node = []
				z = x
				while isValidPos(z, y, to_search):
					if board[z][y] == to_search:
						node.append([z, y])
						size += 1
					z -= 1
				if size > max:
					if isValidPos(z + 1, y, 0) or isValidPos(z, y, 0):
						max = size
						ret = init_node_params(node, "west", [x, y], [z + 1, y], [x + 1, y], [z, y])

				# east
				size = 1
				node = []
				z = x
				while isValidPos(z, y, to_search):
					if board[z][y] == to_search:
						node.append([z, y])
						size += 1
					z += 1
				if size > max:
					if isValidPos(z - 1, y, 0) or isValidPos(z, y, 0):
						max = size
						ret = init_node_params(node, "east", [x, y], [z - 1, y], [x - 1, y], [z, y])

				# north west
				size = 1
				node = []
				x2 = x
				y2 = y
				while isValidPos(x2, y2, to_search):
					if board[x2][y2]:
						node.append([x2, y2])
						size += 1
					x2 -= 1
					y2 -= 1
				if size > max:
					if isValidPos(x + 1, y + 1, 0) or isValidPos(x2, y2, 0):
						max = size
						ret = init_node_params(node, "north west", [x, y], [x2 + 1, y2 + 1], [x + 1, y + 1], [x2, y2])

				# north east
				size = 1
				node = []
				x2 = x
				y2 = y
				while isValidPos(x2, y2, to_search):
					if board[x2][y2]:
						node.append([x2, y2])
						size += 1
					x2 += 1
					y2 -= 1
				if size > max:
					if isValidPos(x - 1, y + 1, 0) or isValidPos(x2, y2, 0):
						max = size
						ret = init_node_params(node, "north east", [x, y], [x2 - 1, y2 + 1], [x - 1, y + 1], [x2, y2])

	return ret

def block_node(info):
	if isValidPos(info["add_head"][0], info["add_head"][1], 0):
		pp.do_mymove(info["add_head"][0], info["add_head"][1])
	elif isValidPos(info["add_tail"][0], info["add_tail"][1], 0):
		pp.do_mymove(info["add_tail"][0], info["add_tail"][1])
	else:
		make_random_move()

def increase_node(info):
	if isValidPos(info["add_head"][0], info["add_head"][1], 0):
		pp.do_mymove(info["add_head"][0], info["add_head"][1])
	elif isValidPos(info["add_tail"][0], info["add_tail"][1], 0):
		pp.do_mymove(info["add_tail"][0], info["add_tail"][1])
	else:
		make_random_move()

def ai():
	best_vilain = best_nonblock_serie("vilain")
	best_hero = best_nonblock_serie("hero")
	if len(best_hero["node"]) > len(best_vilain["node"]):
		increase_node(best_hero)
	else:
		if len(best_vilain["node"]) >= 2:
			block_node(best_vilain)
		else:
			if len(best_hero["node"]) > 0:
				increase_node(best_hero)
			else:
				make_random_move()

def brain_turn():
	if pp.terminateAI:
		return
	try:
		ai()
	except:
		logDebug("error, doing random to save the turn")
		make_random_move()

def logDebug(msg):
	with open(DEBUG_LOGFILE, "a") as f:
		print(msg, file=f)

def brain_end():
	pass

def brain_about():
	pp.pipeOut(pp.infotext)

if DEBUG_EVAL:
	import win32gui
	def brain_eval(x, y):
		wnd = win32gui.GetForegroundWindow()
		dc = win32gui.GetDC(wnd)
		rc = win32gui.GetClientRect(wnd)
		c = str(board[x][y])
		win32gui.ExtTextOut(dc, rc[2]-15, 3, 0, None, c, ())
		win32gui.ReleaseDC(wnd, dc)

pp.brain_init = brain_init
pp.brain_restart = brain_restart
pp.brain_my = brain_my
pp.brain_opponents = brain_opponents
pp.brain_block = brain_block
pp.brain_takeback = brain_takeback
pp.brain_turn = brain_turn
pp.brain_end = brain_end
pp.brain_about = brain_about
if DEBUG_EVAL:
	pp.brain_eval = brain_eval

def main():
	pp.main()

if __name__ == "__main__":
	main()
