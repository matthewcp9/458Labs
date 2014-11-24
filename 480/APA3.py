import random
Trinh3Store = {}


def Trinh3(hist=[], score=[], query = False):

	def checkHistoryDifferences(Trinh3Store, hist):
		differences = -1

		if (len(Trinh3Store["myHistory"]) > 11):
			myLast10Moves = Trinh3Store["myHistory"][-11:]
			if len(hist) > 11:
				new_hist = hist[-11:]
				differences += 1
				for count in range(0, 11):
					print(count)
					if (new_hist[count] != myLast10Moves[count]):
						differences += 1
		return differences


	def checkOppRatio(hist):
		turnsPassed = len(hist)
		numCs = 0.0

		for turn in hist:
			if turn[1].upper() == 'C': 
				numCs += 1
		return numCs/turnsPassed
	   
	if query:
		return ["Sand Gambler3", "He lost all his money in Vegas so now he's gambling with sand."]
	   
	turnsPassed = len(hist)
	if not "myHistory" in Trinh3Store:
		Trinh3Store["myHistory"] = []
	
	if turnsPassed > 11:
		ratio = checkHistoryDifferences(Trinh3Store, hist) #returns higher when flip is high
		if ratio >= 0: 
			print("Ratio", ratio/11)
			turnsPassed = 1000
			print("Ratio To beat", ratio/11 + (turnsPassed * .000133))
			if random.random() >= (ratio/11 - (turnsPassed * .000133)): #if ratio of flip is high, hard to get the same val so choose opp
				Trinh3Store["myHistory"].append('D')
				return 'D'
			else:
				Trinh3Store["myHistory"].append('C')
				return 'C'
		else: #if this fails then whatever return D
			return 'D'
	else:
		print("Selecting C since less than 15 turns")
		return 'C'
Trinh3Store["myHistory"] = ["D", "D", "D", "D", "D", "D", "D", "D", "D", "D", "D", "D", "D", "D", "D", "D", "D", "D", "D", "D", "D", "D", "D", "D", "D", "D", "D", "D", "D", "D", "D"] 
print(len(["C","D","D","C","D", "D", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C"]), len(Trinh3Store["myHistory"]))
print("Selecting ", Trinh3(["C","D","D","C","D", "D", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C"], [100, 100], False))