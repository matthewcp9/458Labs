import sys

class Person:
	def __init__(self, name):
		self.name = name
		self.hierarchy = {}

def GrandChild(gchild, gparent):
	gptree = gparent.hierarchy
	ctree = gchild.hierarchy 

	try: 
		for parent in ctree["Parent"]:
			for grandparent in parent.hierarchy["Parent"]:
				if grandparent.name == gparent.name:
					return True
	except Exception as e: 
		print("Exception Happened: %s" % str(e))
		return True
	
	return False


def GreatGrandParent(ggparent, ggchild): #Pass in objects
	ctree = ggchild.hierarchy 

	try: 
		for parent in ctree["Parent"]:
			for grandparent in parent.hierarchy["Parent"]:
				for greatgrandparent in grandparent.hierarchy["Parent"]:
					if greatgrandparent.name == ggparent.name:
						return True
	except Exception as e: 
		print("Exception Happened: %s" % str(e))
		return False
	
	return False
	

def Ancestor(ancest, child):
	ctree = child.hierarchy
	recursive_tree = {}
	recursive_tree["Parent"] = []
	recursive_tree["Parent"] += ctree["Parent"]

	while len(recursive_tree["Parent"]) != 0:
		temp = []
		for parent in recursive_tree["Parent"]:	
			if parent.name == ancest.name:
				return True
			temp += parent.hierarchy["Parent"]
		recursive_tree["Parent"] = temp
	return False

def Brother(bro, child):
	ctree = child.hierarchy
	try:
		for parent in ctree["Parent"]:
			for sibling in parent.hierarchy["Child"]:
				if sibling.name != child.name and bro.name == sibling.name and sibling.gender == "Male":
					return True 
	except Exception as e: 
		print("Exception Happened: %s" % str(e))
		return False
	
	return False

def Sister(sis, child):
	ctree = child.hierarchy
	try:
		for parent in ctree["Parent"]:
			for sibling in parent.hierarchy["Child"]:
				if sibling.name != child.name and sis.name == sibling.name and sibling.gender == "Female":
					return True 
	except Exception as e: 
		print("Exception Happened: %s" % str(e))
		return False
	
	return False

def Daughter(daug, parent):
	ptree = parent.hierarchy
	try:
		for child in ptree["Child"]:
			if child.gender == "Female" and child.name == daug.name:
				return True
	except Exception as e: 
		print("Exception Happened: %s" % str(e))
		return False
	return False

def Son(son, parent):
	ptree = parent.hierarchy
	try:
		for child in ptree["Child"]:
			if child.gender == "Male" and child.name == son.name:
				return True
	except Exception as e: 
		print("Exception Happened: %s" % str(e))
		return False
	return False

def FirstCousin(cous, child):
	ctree = child.hierarchy
	cous_tree = cous.hierarchy

	try:
		child_grandparents = []
		cous_grandparents = []
		for parent in ctree["Parent"]:
			child_grandparents += parent.hierarchy["Parent"]
		for parent in cous_tree["Parent"]:
			cous_grandparents += parent.hierarchy["Parent"]
		
		for gp1 in child_grandparents:
			for gp2 in cous_grandparents:
				if gp1.name == gp2.name:
					return True
	except Exception as e: 
		print("Exception Happened: %s" % str(e))
		return False
	return False
	
def BrotherInLaw(bil, child):
	ctree = child.hierarchy
	try:
		for spouse in ctree["Spouse"]:
			for parent in spouse.hierarchy["Parent"]:
				for sibling in parent.hierarchy["Child"]:
					if spouse.name != sibling.name and sibling.name != child.name and bil.name == sibling.name and sibling.gender == "Male":
						return True
	except Exception as e: 
		print("Exception Happened: %s" % str(e))
		return False
	
	return False

def SisterInLaw(sil, child):
	ctree = child.hierarchy
	try:
		for spouse in ctree["Spouse"]:
			for parent in spouse.hierarchy["Parent"]:
				for sibling in parent.hierarchy["Child"]:
					if spouse.name != sibling.name and sibling.name != child.name and sil.name == sibling.name and sibling.gender == "Male":
						return True
	except Exception as e: 
		print("Exception Happened: %s" % str(e))
		return False
	
	return False

def Aunt(aunt, child):
	ctree = child.hierarchy
	parents = []
	try:
		for parent in ctree["Parent"]:
			parents.append(parent.name)
		for parent in ctree["Parent"]:
			for grandparent in parent.hierarchy["Parent"]:
				for sibling in grandparent.hierarchy["Child"]:
					if sibling.name not in parents and aunt.name == sibling.name and sibling.gender == "Female":
						return True
					for spouse in sibling.hierarchy["Spouse"]:
						if spouse.name not in parents and aunt.name == spouse.name and spouse.gender == "Female":
							return True

	except Exception as e: 
		print("Exception Happened: %s" % str(e))
		return False
	
	return False

def Uncle(unc, child):
	ctree = child.hierarchy
	parents = []
	try:
		for parent in ctree["Parent"]:
			parents.append(parent.name)
		for parent in ctree["Parent"]:
			for grandparent in parent.hierarchy["Parent"]:
				for sibling in grandparent.hierarchy["Child"]:
					if sibling.name not in parents and unc.name == sibling.name and sibling.gender == "Male":
						return True
					for spouse in sibling.hierarchy["Spouse"]:
						if spouse.name not in parents and unc.name == spouse.name and spouse.gender == "Male":
							return True
	except Exception as e: 
		print("Exception Happened: %s" % str(e))
		return False
	
	return False

def mth_Cousin_ntimes_Removed(m, n, cous, child):
	ctree = child.hierarchy

	#deepcopy the ctree
	parentList = []
	parentList.append(child)

	if True:
		# n generation removed
		for count in range(0, n):	
			temp = parentList
			parentList = []
			for parent in temp:
				parentList += parent.hierarchy["Parent"]
		
		## --- Remove duplicates in list -- ##
		parent_name_list = [] #stores the nth removed generation parents names for later on
		temp = []
		for parent in parentList:
			if not parent.name in parent_name_list:
				parent_name_list.append(parent.name)
				temp.append(parent)
		parentList = temp
		# mth cousin's parent using the parentList holding the nth generation
		mthCousinParentList = parentList

		for count in range(0, m + 1):
			temp = mthCousinParentList
			mthCousinParentList = []
			for parent in temp:
				mthCousinParentList += parent.hierarchy["Parent"]
		cousinList = []
		for parent in mthCousinParentList:
			cousinList += parent.hierarchy["Child"]
		

		## --- Remove duplicates in list -- ##
		name_list = []
		temp = []
		for parent in cousinList:
			if not parent.name in name_list:
				name_list.append(parent.name)
				temp.append(parent)
		cousinList = temp

		#for parent in parentList:
			#print("Name", parent.name)
		#Now have the set parents that they may have shared
		#check the cousin's mth grandparent
		cous_parentList = []
		cous_parentList.append(cous)
		for count in range(0, m + 1):
			temp = cous_parentList
			cous_parentList = []
			for parent in temp:
				cous_parentList += parent.hierarchy["Parent"]
		#Now Check the two lists if they share the same name
		for mparent in mthCousinParentList:
			for mcous_parent in cous_parentList:
				if mparent.name == mcous_parent.name and cous.name not in parent_name_list :
					return True
	return False


def Ask(string, target_name, name_list, familyTree):
	if True:
		return_names = []
		target_person = familyTree[target_name]
		if string == "Grandchild":
			for name in [x for x in name_list if x != target_name]:
				query_person = familyTree[name]
				if GrandChild(query_person, target_person):
					return_names.append(query_person.name)
		elif string == "Greatgrandparent":
			for name in [x for x in name_list if x != target_name]:
				query_person = familyTree[name]
				if GreatGrandParent(query_person, target_person):
					return_names.append(query_person.name)
		elif string == "Ancestor":
			for name in [x for x in name_list if x != target_name]:
				query_person = familyTree[name]
				if Ancestor(query_person, target_person):
					return_names.append(query_person.name)
		elif string == "Brother":
			for name in [x for x in name_list if x != target_name]:
				query_person = familyTree[name]
				if Brother(query_person, target_person):
					return_names.append(query_person.name)
		elif string == "Sister":
			for name in [x for x in name_list if x != target_name]:
				query_person = familyTree[name]
				if Sister(query_person, target_person):
					return_names.append(query_person.name)								
		elif string == "Daughter":
			for name in [x for x in name_list if x != target_name]:
				query_person = familyTree[name]
				if Daughter(query_person, target_person):
					return_names.append(query_person.name)		
		elif string == "Son":
			for name in [x for x in name_list if x != target_name]:
				query_person = familyTree[name]
				if Son(query_person, target_person):
					return_names.append(query_person.name)
		elif string == "FirstCousin":
			for name in [x for x in name_list if x != target_name]:
				query_person = familyTree[name]
				if FirstCousin(query_person, target_person):
					return_names.append(query_person.name)
		elif string == "BrotherInLaw":
			for name in [x for x in name_list if x != target_name]:
				query_person = familyTree[name]
				if BrotherInLaw(query_person, target_person):
					return_names.append(query_person.name)
		elif string == "SisterInLaw":
			for name in [x for x in name_list if x != target_name]:
				query_person = familyTree[name]
				if SisterInLaw(query_person, target_person):
					return_names.append(query_person.name)
		elif string == "Aunt":
			for name in [x for x in name_list if x != target_name]:
				query_person = familyTree[name]
				if Aunt(query_person, target_person):
					return_names.append(query_person.name)
		elif string == "Uncle":
			for name in [x for x in name_list if x != target_name]:
				query_person = familyTree[name]
				if Uncle(query_person, target_person):
					return_names.append(query_person.name)
		elif string =="MthCousinNthTimesRemoved":
			m = int(input("Enter the m variable: "))
			n = int(input("Enter the n variable: "))
			for name in [x for x in name_list if x != target_name]:
				query_person = familyTree[name]
				if mth_Cousin_ntimes_Removed(m, n, query_person, target_person):
					return_names.append(query_person.name)
		else:
			print("invalid_query")
	#except Exception as e: 
		#print("Exception Happened: %s" % str(e))
		#return return_names	
	return return_names
				
#File content order	:
#Name   Spouse    Children    Parents   Gender			
def main():
	filename = sys.argv[1]
	familyTree = {}
	nameList = []
	# Read from input file and fill in the "Family Tree" with known facts
	with open(filename, "r") as infile:
		for line in infile:
			if(line[0] != '#'): #skip comments
				output = line.split('(')
				if(output[0] == "Person"):
					txt = output[1].strip()[:-1]
					p = Person(txt)
					p.hierarchy["Parent"] = []
					p.hierarchy["Child"] = []
					p.hierarchy["Spouse"] = []
					familyTree[txt] = p
					nameList.append(txt)
	with open(filename, "r") as infile:
		for line in infile:
			if(line[0] != '#'): #skip comments
				output = line.split('(')
				if output[0] == "Gender":
					txt = output[1].strip()[:-1]
					txtOutput = txt.split(',')
					familyTree[txtOutput[0]].gender = txtOutput[1].strip()
				elif output[0] == "Child":
					txt = output[1].strip()[:-1]
					txtOutput = txt.split(',')
					param1 = txtOutput[0].strip()
					param2 = txtOutput[1].strip()
					person = familyTree[param2]
					person.hierarchy["Child"].append(familyTree[param1])
				elif output[0] == "Parent":
					txt = output[1].strip()[:-1]
					txtOutput = txt.split(',')
					param1 = txtOutput[0].strip()
					param2 = txtOutput[1].strip()
					person = familyTree[param2]
					person.hierarchy["Parent"].append(familyTree[param1])
				elif output[0] == "Spouse":
					txt = output[1].strip()[:-1]
					txtOutput = txt.split(',')
					param1 = txtOutput[0].strip()
					param2 = txtOutput[1].strip()
					person = familyTree[param2]
					person.hierarchy["Spouse"].append(familyTree[param1])
				elif output[0] == "Ask":
					relation = output[1].strip().split('(')[0].strip()
					name = output[2].strip().split(')')[0].strip()
					print(Ask(relation, name, nameList, familyTree))

	#print(Ask("FirstCousin", "William", nameList, familyTree))
	#print(Ask("Grandchild", "Elizabeth", nameList, familyTree))
	#print(Ask("BrotherInLaw", "Diana", nameList, familyTree))
	#print(Ask("Greatgrandparent", "Zara", nameList, familyTree))
	#print(Ask("Ancestor", "Eugenie", nameList, familyTree))
	#print(Brother(familyTree["Andrew"], familyTree["Charles"]))
	#print(BrotherInLaw(familyTree["Andrew"], familyTree["Diana"]))
	#print(BrotherInLaw(familyTree["Mark"], familyTree["Diana"]))
	#print(GreatGrandParent(familyTree["George"], familyTree["William"]))

main()