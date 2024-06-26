valid_next_tokens = {"LET":["NAME"],
                     "EQ":["NUMBER", "LPAREN", "NAME", "INPUT_INT"],
                     "ASSIGN":["INPUT_INT", "INPUT_STR", "STRING", "NAME", "NUMBER", "LPAREN"],
                     "NEQ":["NUMBER", "LPAREN", "NAME", "INPUT_INT"],
                     "WHILE":["LPAREN"],
                     "GT":["NUMBER", "LPAREN", "NAME", "INPUT_INT"],
                     "LT":["NUMBER", "LPAREN", "NAME", "INPUT_INT"],
                     "IF":["LPAREN"],
                     "PLUS":["NUMBER", "LPAREN", "NAME", "INPUT_INT"],
                     "MINUS":["NUMBER", "LPAREN", "NAME", "INPUT_INT"],
                     "MUL":["NUMBER", "LPAREN", "NAME", "INPUT_INT"],
                     "DIV":["NUMBER", "LPAREN", "NAME", "INPUT_INT"],
                     "MOD":["NUMBER", "LPAREN", "NAME", "INPUT_INT"],
                     "OR":["NUMBER", "LPAREN", "NAME", "INPUT_INT"],
                     "AND":["NUMBER", "LPAREN", "NAME", "INPUT_INT"],
                     "LPAREN":["NUMBER", "NAME", "LPAREN", "INPUT_INT", "MUL", "DIV", "MOD", "OR", "AND", "GT", "LT", "EQ", "NEQ", "STRING"],
                     "RPAREN":["LBRACE", "RPAREN", "SEMICOLON", "PLUS", "MINUS"],
                     "LBRACE":["LET", "NAME", "WHILE", "IF", "PRINT_INT", "PRINT_STR"],
                     "RBRACE":["LET", "NAME", "WHILE", "IF", "PRINT_INT", "PRINT_STR"],
                     "SEMICOLON":["LET", "NAME", "WHILE", "IF", "PRINT_INT", "PRINT_STR", "RBRACE"],
                     "PRINT_INT":["LPAREN"],
                     "PRINT_STR":["LPAREN"],
                     "INPUT_INT":["NUMBER", "EQ", "NEQ", "GT", "LT", "PLUS", "MINUS", "MUL", "DIV", "MOD", "OR", "AND", "SEMICOLON", "RPAREN"],
                     "INPUT_STR":["SEMICOLON"],
                     "STRING":["SEMICOLON", "RPAREN"],
                     "NAME":["ASSIGN", "NUMBER", "EQ", "NEQ", "GT", "LT", "PLUS", "MINUS", "MUL", "DIV", "MOD", "OR", "AND", "SEMICOLON", "RPAREN"],
                     "NUMBER":["EQ", "NEQ", "GT", "LT", "PLUS", "MINUS", "MUL", "DIV", "MOD", "OR", "AND", "SEMICOLON", "RPAREN"]}

state = {"in_expr": ["NUMBER", "NAME", "INPUT_INT", "EQ", "NEQ", "GT", "LT", "PLUS", "MINUS", "MUL", "DIV", "MOD", "OR", "AND", "RPAREN", "LPAREN","SEMICOLON", "STRING"],
         None: list(valid_next_tokens.keys())}

def AST_syntax_check(tokens):
    cur_state = None
    count_paren = 0
    count_brace = 0
    for i in range(len(tokens)):

        if tokens[i][0] == "LPAREN":
            count_paren += 1
        elif tokens[i][0] == "RPAREN":
            count_paren -= 1
        elif tokens[i][0] == "LBRACE":
            count_brace += 1
        elif tokens[i][0] == "RBRACE":
            count_brace -= 1

        if i + 1 < len(tokens):
            if cur_state is None and tokens[i][0] == "LPAREN":
                cur_state = "in_expr"
            elif cur_state is None and tokens[i][0] == "ASSIGN" and tokens[i-1][0] == "NAME" and not (tokens[i+1][0] == "INPUT_STR" or tokens[i+1][0] == "STRING"):
                cur_state = "in_expr"
            elif cur_state == "in_expr" and (tokens[i][0] == "RPAREN" or tokens[i][0] == "SEMICOLON"):
                cur_state = None
                if count_paren != 0:
                    return False

            if tokens[i+1][0] in valid_next_tokens[tokens[i][0]] and tokens[i + 1][0] in state[cur_state]:
                pass
            else:
                return False
    if count_brace != 0:
        return False
    return True