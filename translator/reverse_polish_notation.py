
def op_plus(x,y):
    return x+y
def op_minux(x,y):
    return x-y
def op_mul(x,y):
    return x*y
def op_div(x,y):
    return x//y
def op_mod(x,y):
    return x%y
def op_or(x,y):
    return x | y

def op_and(x,y):
    return x & y
def op_eq(x,y):
    return x == y
def op_neq(x,y):
    return x != y
def op_gt(x,y):
    return x > y
def op_lt(x,y):
    return x < y

OPERATORS = {"*": (4, op_mul),
             "/": (4, op_div),
             "%": (4, op_mod),
             "+": (3, op_plus),
             "-": (3, op_minux),
             "==": (2, op_eq),
             "!=": (2, op_neq),
             ">": (2, op_gt),
             "<": (2, op_lt),
             "&": (1, op_and),
             "|": (0, op_or)}

RUS_OPERATORS = {"умножить": (4, op_mul),
             "делить": (4, op_div),
             "модуль": (4, op_mod),
             "плюс": (3, op_plus),
             "минус": (3, op_minux),
             "равно": (1, op_eq),
             "не_равно": (1, op_neq),
             "больше": (1, op_gt),
             "меньше": (1, op_lt),
             "или": (0, op_or)}

def shunting_yard(parsed_formula):
    stack = []
    for token in parsed_formula:
        if token[1] in OPERATORS:
            while stack and stack[-1][1] != "(" and OPERATORS[token[1]][0] <= OPERATORS[stack[-1][1]][0]:
                yield stack.pop()
            stack.append(token)
        elif token[1] == ")":
            while stack:
                x = stack.pop()
                if x[1] == "(":
                    break
                yield x
        elif token[1] == "(":
            stack.append(token)
        else:
            yield token
    while stack:
        yield stack.pop()

def reverse_polish_notation(formula):
    return list(shunting_yard(formula))
