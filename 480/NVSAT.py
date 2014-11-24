import sys

global found
"""
#is useless... thought of this completely wrong, checks to see if a line has all 1's and another line has all 0's
def checkUnsat(expr):
    all_clause = False
    for clause in expr:
        temp = set(clause)
        if '-' in temp:
            temp.remove('-') # remove the minuses and check if len temp is still 1
        if len(temp) == 1: # if all are same element check positions of this clause w/ others
            for clause2 in [x for x in expr if x != clause]:
                checkFor = '0' if list(temp)[0] == '1' else '1' 
                strikes = 0
                for idx in range(0, len(clause)):
                    if (clause2[idx] == checkFor and clause[idx] == list(temp)[0]) or (clause[idx] == '-' and clause2[idx] == '-'):
                        strikes += 1
                if strikes == len(clause):
                    return True
    return False
"""

#early termination
def clauseCheck(clause, model):
    minusLocations = []
    #print("Clause Checking...: ", model)
    for lit in range(0, len(clause)):
        if clause[lit] != '-':
            if clause[lit] == '1' and model[lit][1] == 'True':
                return True
            if clause[lit] == '0' and model[lit][1] == 'False':
                return True
        else:
            minusLocations.append(lit)
    if len(set(clause)) == 1 and clause[0] == '-':
        return True
    #Check the Non-Minus'd areas to see if elements are matching an unknown before returning False
    for lit in [x for x in range(0, len(clause)) if x not in minusLocations]:
        if model[lit][1] == 'None':
            #print("Returning Unknown.?")
            return "Unknown"
    #print("Returning False.?")
    return False

#unit propogation/clause
def setPropogation(expr, symbols):
    for clause in expr:
        if clause.count('-') == (len(clause) - 1):
            for count in [x for x in range(0, len(clause)) if x in symbols]:
                if clause[count] != '-':
                    #print("Prop Setting :", count, ("True" if clause[count] == '1' else "False" ))
                    return (count, ("True" if clause[count] == '1' else "False" ))       
    return (-1, None)

#pure-symbol heuristic  
def setPurity(expr, symbols):
    for count in range(0, len(expr[0])):
        pure = True
        symbol = expr[0][count]
        for clause in expr:
            if symbol == '-':
                symbol = clause[count]
            if symbol != clause[count] and symbol != '-' and clause[count] != '-':
                pure = False
        if pure and count in symbols:
            return (count, ("True" if symbol == '1' else "False" ))
    return (-1, None)

def printCorrectModel(model):
    for lit in model:
        if lit[1] != "None" and lit != model[-1]:
            print("X" + str(lit[0] + 1), "=", lit[1], end=", ")
        elif lit == model[-1] and lit[1] != "None":
            print("X" + str(lit[0] + 1), "=", lit[1], end="")
    #print()

def DPLL(clauses, symbols, model):
    global found
    if found == False:
        sat = True
        for clause in clauses:
            result = clauseCheck(clause, model)
            if result == False:
                return False
            elif result == "Unknown":
                sat = False
                break
        if sat:
            #print("Found correct model? ", model)
            found = True
            #print(model)
            printCorrectModel(model)
            return True
        (p, value) = setPurity(clauses, symbols)
        if value is not None:     
            symbols = [x for x in symbols if x != p]
            model[p] =(p, value)
            DPLL(clauses, symbols, model)
        (p, value) = setPropogation(clauses, symbols)
        if value is not None:
            symbols = [x for x in symbols if x != p]
            model[p] =(p, value)
            DPLL(clauses, symbols, model)
        if len(symbols) > 0:
            p = symbols[0]
        else:
            return False
        symbols = [x for x in symbols if x != p]
        model[p] = (p, "True")
        return DPLL(clauses, symbols, model)
        model[p] = (p, "False")
        return DPLL(clauses, symbols, model)

def main(input_file):
    expr = []
    global found
    found = False
    with open (input_file, 'r') as infile:
        for line in infile:
            line = line.strip()
            clause = []
            if len(line) > 0 and line[0] != '#':
                clause = [x for x in line.replace(' #', '#').split('#')[0].split(' ')]
                expr.append(clause)
    lit_ct = len(expr[0])
    model = []
    symbols = []
    for count in range(0, lit_ct):
        model.append((count, "None"))
        symbols.append(count)  
    DPLL(expr, symbols, model)
    if not found:
        print("unsatisfiable")

"""   
class MyTest(unittest.TestCase):
    def testClauseCheck(self):
        self.assertEqual(clauseCheck(['1', '0', '1'], ["True", "False", "True"]), True)
        self.assertEqual(clauseCheck(['1', '1', '1'], ["True", "False", "True"]), True)
        self.assertEqual(clauseCheck(['1', '1', '1'], ["True", "True", "True"]), True)
        self.assertEqual(clauseCheck(['1', '1', '-'], ["True", "True", "None"]), True)
        self.assertEqual(clauseCheck(['0', '1', '-'], ["False", "False", "None"]), True)
        self.assertEqual(clauseCheck(['0', '1', '1'], ["None", "True", "True"]), True)
        self.assertEqual(clauseCheck(['1', '-', '-'], ["False", "None", "True"]), False)
        self.assertEqual(clauseCheck(['1', '-', '-'], ["None", "False", "True"]), "Unknown")
        self.assertEqual(clauseCheck(['-', '0', '1'], ["None", "True", "None"]), "Unknown")
        self.assertEqual(clauseCheck(['0', '1', '1'], ["None", "False", "False"]), "Unknown")
        self.assertEqual(clauseCheck(['1', '1', '1'], ["False", "False", "False"]), False)
        self.assertEqual(clauseCheck(['0', '0', '1'], ["True", "True", "False"]), False)
        self.assertEqual(clauseCheck(['-', '-', '-'], ["None", "None", "None"]), True)
        self.assertEqual(clauseCheck(['-', '-', '-'], ["True", "None", "None"]), True)
    def testSetPurity(self):
        expr = [['0', '1', '0'], ['1', '0', '-'], ['1', '1', '-'], ['0', '0', '0'], ['-', '-', '0']]
        symbols = ["None", "None", "None"]
        self.assertEqual(setPurity(expr, symbols), (2, "False"))
        expr = [['0', '1', '1'], ['1', '0', '-'], ['1', '1', '-'], ['0', '0', '0'], ['-', '-', '0']]
        symbols = ["None", "None", "None"]
        self.assertEqual(setPurity(expr, symbols), (-1, None))
        expr = [['1', '1', '1'], ['1', '1', '-'], ['1', '1', '-'], ['1', '1', '0'], ['-', '-', '0']]
        symbols = [1]
        self.assertEqual(setPurity(expr, symbols), (1, "True"))
    def testSetPropagation(self):
        expr = [['0', '1', '0'], ['1', '0', '-'], ['1', '-', '-']]
        symbols = ["None", "None", "None"]
        self.assertEqual(setPropogation(expr, symbols), (0, "True"))
    def testUnsat(self):
        expr = [['1', '1', '1'], ['0', '0', '0']]
        self.assertEqual(checkUnsat(expr), True)
        expr = [['1', '1', '0'], ['0', '0', '0']]
        self.assertEqual(checkUnsat(expr), False)
        expr = [['1', '1', '1', '-', '-', '1'], ['0', '0', '0', '-', '-', '0']]
        self.assertEqual(checkUnsat(expr), True)
        expr = [['1', '-', '-', '-', '-', '-'], ['0', '-', '-', '-', '-', '-']]
        self.assertEqual(checkUnsat(expr), True)
        expr = [['-', '-', '-', '-', '-', '-'], ['-', '1', '-', '-', '-', '-']]
        self.assertEqual(checkUnsat(expr), False)
        expr = [['-', '1', '1', '1', '1', '1'], ['-', '1', '1', '1', '1', '1']]
        self.assertEqual(checkUnsat(expr), False)
        expr = [['-', '1', '0', '1', '0', '1'], ['-', '0', '1', '0', '0', '1']]
        self.assertEqual(checkUnsat(expr), False)
        print("end of sat")
"""   
#mt = MyTest()
#mt.testClauseCheck()
#mt.testSetPurity()
#mt.testSetPropagation()
#mt.testUnsat()
#print("End of tests")
if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    print("No input file specified")
main(filename)
