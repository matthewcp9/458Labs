import sys, unittest

initialKB = {}
goalKB = {}

class Block:
	def __init__(self, name):
		self.name = name
		self.clear = None
		self.on = None

def Move(block1, block2):
	if not block1.clear or not block2.clear:
		return "Bad Move"

	block2.clear = False
	if not block1.on == "Table":
		initialKB[block1.on].clear = True
	block1.on = block2.name
	return "Good Move"

def MoveToTable(block1):
	if block1.clear != False:
		initialKB[block1.on].clear = True
		block1.on = "Table"
		return "Good Move"
	else:
		return "Bad Move"

def main():
	global initialKB, goalKB
	
	filename = sys.argv[1]
	with open(filename, 'r') as infile:
		KB = initialKB
		for line in infile:
			text = line.strip().split()
			if text[0] == "ON": 
				if text[1] not in KB: #make new Variable
					KB[text[1]] = Block(text[1])
				KB[text[1]].on = text[2]
				
				if text[2] == "Table":
					MoveToTable(KB[text[1]])
				else:
					if text[2] not in KB: #make new Variable
						KB[text[2]] = Block(text[2])
					Move(KB[text[1]], KB[text[2]])
			elif text[0] == "CLEAR":
				if text[1] not in KB: #make new Variable
					KB[text[1]] = Block(text[1])
				KB[text[1]].clear = True
			elif text[0] == "GOAL":
				KB = goalKB #switch to the goal KB
			else: #comment line
				continue 
	#print(initialKB)
	#print("--------------------------------------------------------")
	#print(goalKB)

def verifyKBisatGoal(myKB, goalKB):
	for var, block in goalKB.items():
		if var in myKB:
			if myKB[var].on != myKB[var].on
				return False
		else:
			return False
	return True

class BlockTest(unittest.TestCase):
	def TestInit(self):
		main()
		self.assertEquals(initialKB["A"].on, "Table")
		self.assertEquals(initialKB["B"].on, "Table")
		self.assertEquals(initialKB["C"].on, "A")
		self.assertEquals(initialKB["C"].clear, True)
		self.assertEquals(initialKB["B"].clear, True)
		self.assertEquals(initialKB["A"].clear, False)
		self.assertEquals(goalKB["A"].on, "B")
		self.assertEquals(goalKB["B"].on, "C")
	def TestMove(self):
		global initialKB

		temp = initialKB
		initialKB = {}
		b1 = Block("A")
		b1.clear = False
		b1.on = "Table"
		initialKB["A"] = b1

		b2 = Block("B")
		b2.clear = True
		b2.on = "A"
		initialKB["B"] = b2

		b3 = Block("C")
		b3.clear = True
		b3.on = "Table"
		initialKB["C"] = b3

		self.assertEquals(Move(b3, b1), "Bad Move")
		Move(b3, b2)
		self.assertEquals(b3.clear, True)
		self.assertEquals(b3.on, "B")
		self.assertEquals(b1.clear, False)
		initialKB = temp #rebuild init KB

	def TestMoveToTable(self):
		global initialKB

		temp = initialKB
		initialKB = {}
		b1 = Block("A")
		b1.clear = False
		b1.on = "Table"
		initialKB["A"] = b1

		b2 = Block("B")
		b2.clear = True
		b2.on = "A"
		initialKB["B"] = b2

		b3 = Block("C")
		b3.clear = True
		b3.on = "Table"
		initialKB["C"] = b3

		self.assertEquals(MoveToTable(b1), "Bad Move")
		self.assertEquals(MoveToTable(b2), "Good Move")
		self.assertEquals(b2.on, "Table")
		self.assertEquals(b1.clear, True)


t = BlockTest()
t.TestInit()
t.TestMove()