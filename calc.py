op_set = {"+", "-", "/", "*", "^"}

def find_parenthesis_substring(input):
    # want to find the substring to recurse on
    s = []
    for i in range(len(input)):
        char = input[i]
        if char == "(":
            s.append(".")
        if char == ")" and len(s) > 0:
            s.pop()
        
        if(len(s) == 0):
            i += 1
            break
    
    #assume that now we have the correct substring where the substring goes from 0 to i-1, and the rest is i to the end
    return [input[1:i-1], input[i:]] #retunrs the first section without the parens and the second part 

def parse(player_text): # DOES NOT DO ERROR CHECKING OR CASE HANDLING
    #break the string up into pieces ... starting simple
    # 3 + 4
    #want a = 3, op = + and b = 4
    #print(player_text)
    #go through each character
    cur_segment = ""
    #a, b, op = 0, 0, ""
    stack = []
    num = 0 #temp variable
    i = 0
    while i < len(player_text):
        char = player_text[i]
        #print("Cur_char", char)
        if not char.isnumeric() and char not in op_set and char != "." and char != "(" and char != ")":
            i += 1
            continue
        if char in op_set: #if an operator is seen
            #need to set a = cur_segment and set the operator
            num = to_num(num, cur_segment)
            #if not num:
            #    return -1
            if num:
                stack.append(num)
            
            cur_segment = "" #reset the value of cur_segment
            op = char
            stack.append(op)
        elif char == "(":
            #push the cur_segment and start an new subarray
            if cur_segment != "":
                num = to_num(num, cur_segment)
                if not num:
                    return -1
                stack.append(num)

            # recurse into this substring between the ( and closing )
            paren_substring, rest = find_parenthesis_substring(player_text[i:])
            stack.append(parse(paren_substring))

            #now continue on with the rest portion
            i = i + len(paren_substring) + 1
            #print("Stack:", stack)
            #print("Rest:", player_text[i:])
        else: # if it is any other length character
            cur_segment += char

        i += 1

    #print("stack",stack)
    num = to_num(num, cur_segment)
    #if not num:
    #    return -1
    if num:
        stack.append(num)
    return stack

def is_float(num):
    return not num.isdigit()

def to_num(num, cur_segment): #sets the supplied variable to the correct type of number, if not a number returns -1
    #tries to set the number first to an int, if that doesn't work tries to set it to a float, and if that doesn't work returns None
    # if you try to convert a string representing a float into an int, a value error is raised due to having the "."
    try:
        num = int(cur_segment) 
    except ValueError:
        try:
            num = float(cur_segment)
        except:
            return None
    return num
    
def calculate(stack):
    # need PEMDAS to do this 
    # let's start with MDAS to keep it simple

    #case 1
    # [5, '+', 5, '*', 5] -> do the multiplation first
    # [5, '+', 25] # then the addition
    # [125] # then return the result

    #case 2
    # (5+5)*5 this should compute the 5+5 first
    # [[5, '+', 5], '*', 5] so compute the first index first

    # ((5+4)-7) * 2
    # 
    # [
    #   [
    #       [5, '+', 4]
    #       , '-', 7
    #   ]
    # , '*', 2]

    # first handle parens via recursion ... meaning if you see an index that
    #    is an array recurse until you get a result, pass this result up
    #    and replace the array with the result
    # P -> solve parenthesis
    for i in range(len(stack)):
        if isinstance(stack[i], list):
            res = calculate(stack[i])
            stack[i] = res

    while len(stack) > 1:
        # E -> solve any exponents from left to right
        i = 0
        while i+2 < len(stack):
            a, op, b = stack[i], stack[i+1], stack[i+2]
            if op == "^":
                new_val = simple_calculate(a,op,b)
                del stack[i+2]
                del stack[i+1]
                del stack[i]
                stack.insert(i, new_val)
                i = -1
            i += 1

        # MD -> solve any multiplication and division from left to right
        i = 0
        while i+2 < len(stack):
            a, op, b = stack[i], stack[i+1], stack[i+2]
            if op == "*" or op == "/":
                new_val = simple_calculate(a,op,b)
                del stack[i+2]
                del stack[i+1]
                del stack[i]
                stack.insert(i, new_val)
                i = -1
            i += 1
        
        # AS -> then do another pass solving any addition and subtraction from left to right
        i = 0
        while i+2 < len(stack):
            a, op, b = stack[i], stack[i+1], stack[i+2]
            if op == "+" or op == "-":
                new_val = simple_calculate(a,op,b)
                #print(new_val, stack)
                del stack[i+2]
                del stack[i+1]
                del stack[i]
                stack.insert(i, new_val)
                #print(new_val, i, stack)
                i = -1
            i += 1
    
    return stack[0]

def simple_calculate(a, op, b):
    if op == "+":
        return a + b
    elif op == "*":
        return a * b
    elif op == "/":
        return a/b
    elif op == "-":
        return a - b
    elif op == "^":
        return a**b
    else:
        return "ERROR, operation not supported"
    
#_________________________________________________________________________________

print("Welcome to Calculator!")

#first compute the test cases
# Case 1: 5 
# Case 2: 
# the left is the string and the right is the desired answer
tests = {
    " 5": 5,
    "5": 5, 
    "5-4": 1,
    "(5-4)": 1,
    "(5+4)-7": 2,
    "((5+4)-7)": 2,
    "(1*(2*(3*(4))))": 24,
    "((5+4)-7)*2": 4,
    "(5^2)^2": 625,
    "5^(1-1)": 1,
    "(4.5* 0.5^2)^2*2": 2.53125 
    }

def run_tests():
    i = 1
    for string, answer in tests.items():
        print("Test Case ", i)
        print("\t String: ", string)
        sample = parse(string)
        print("\t Parsed string: ", sample)
        res = calculate(sample)
        if res == answer:
            print("\t Test case passed!")
        else: 
            print("FAILED! Answer given:", res, "Actual answer: ", answer)
        i += 1

run_tests()
while True:
    print(">", end = "")
    player_text = input()
    sample = parse(player_text)

    if sample == -1:
        print("Error, invalid string.")
        continue
    
    print(sample)
    res = calculate(sample)
    print(res)
