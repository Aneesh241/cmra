import sys

PRECEDENCE = {
    "<": 0, 
    ">": 0, 
    "<=": 0, 
    ">=": 0, 
    "==": 0,
    "+": 1, 
    "-": 1, 
    "*": 2, 
    "/": 2}

VARIABLES = {}

DIRECTION = 1

def evaluate(line):
    values = []
    operators = []

    for token in line:
        if type(token) == float:
            values.append(token)
        elif token in PRECEDENCE:
            if len(operators) == 0:
                operators.append(token)
                continue
        
            current_operator = token
            # IF previous operator has HIGHER precedence
            prev_operator = operators[-1]
            if PRECEDENCE[prev_operator] >= PRECEDENCE[current_operator]:
                op = operators.pop()
                value_2 = values.pop()
                value_1 = values.pop()
                result = eval(f"{value_1} {op} {value_2}")
                values.append(result)

            operators.append(token)
        else:
            # variable, take value out
            value = VARIABLES[token]
            values.append(value)

    while len(operators) > 0:
        op = operators.pop()
        value_2 = values.pop()
        value_1 = values.pop()
        result = eval(f"{value_1} {op} {value_2}")
        values.append(result)

    return values[0]

def run(line):
    if len(line) == 0:
        pass
    elif line[0] == "murmur":
        pass
    elif line[0] == "roar":
        value = line[1:]
        print(evaluate(value))
    elif len(line) >= 2 and line[1] == "bind":
        # assignment
        variable = line[0]
        value = evaluate(line[2:])
        VARIABLES[variable] = value
    elif line[0] == "sniff":
        # conditional
        colon_index = line.index(":")
        condition = line[1:colon_index]
        statement = line[colon_index+1:]

        if evaluate(condition):
            run(statement)
    elif line[0] == "soar":
        global DIRECTION
        DIRECTION = -1
    elif line[0] == "dive":
        DIRECTION = 1

def main():
    filepath = sys.argv[1]

    with open(filepath) as file:
        lines = file.readlines() 
        lines = [tokenize(line) for line in lines]
    
    line_index = 0
    while line_index >= 0 and line_index < len(lines):
        line = lines[line_index]
        run(line)
        line_index += DIRECTION



def tokenize(line):
    items = line.split()
    tokens = []
    for item in items:
        try:
            token = float(item)
        except:
            token = item

        tokens.append(token)
        

    return tokens

main()