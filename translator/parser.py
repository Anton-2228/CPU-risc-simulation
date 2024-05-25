import re
from enum import Enum

class Token(Enum):
    LET = r"let"
    EQ = r"=="
    ASSIGN = r"="
    NEQ = r"!="
    WHILE = r"while"
    GT = r">"
    LT = r"<"
    IF = r"if"
    PLUS = r"\+"
    MINUS = r"-"
    MUL = r"\*"
    DIV = r"/"
    MOD = r"%"
    OR = r"\|"
    AND = r"&"
    LPAREN = r"\("
    RPAREN = r"\)"
    LBRACE = r"{"
    RBRACE = r"}"
    SEMICOLON = r";"
    PRINT_INT = r"print_int"
    PRINT_STR = r"print_str"
    INPUT_INT = r"input_int"
    INPUT_STR = r"input_str"
    STRING = r"'[\w\s,.:;!?()\\-]+'"
    NAME = r"[a-zA-Z][a-zA-Z0-9]*"
    NUMBER = r"-?[0-9]+"

class RuToken(Enum):
    LET = r"объявить"
    NEQ = r"не_равно"
    EQ = r"равно"
    ASSIGN = r"приравнять"
    WHILE = r"пока"
    GT = r"больше"
    LT = r"меньше"
    IF = r"если"
    PLUS = r"плюс"
    MINUS = r"меньше"
    MUL = r"умножить"
    DIV = r"делить"
    MOD = r"модуль"
    OR = r"или"
    AND = r"и"
    LPAREN = r"\("
    RPAREN = r"\)"
    LBRACE = r"{"
    RBRACE = r"}"
    SEMICOLON = r";"
    PRINT_INT = r"вывести_число"
    PRINT_STR = r"вывести_строку"
    INPUT_INT = r"ввести_число"
    INPUT_STR = r"ввести_строку"
    STRING = r"'[\w\s,.:;!?()\\-]+'"
    NAME = r"[a-zA-Zа-яА-Я][a-zA-Zа-яА-Я0-9]*"
    NUMBER = r"-?[0-9]+"

def parser(program):
    # regex = "|".join(f"(?P<{t.name}>{t.value})" for t in RuToken)
    regex = "|".join(f"(?P<{t.name}>{t.value})" for t in Token)
    found_tokens = re.finditer(regex, program)
    tokens = []
    for token in found_tokens:
        t_type = token.lastgroup
        t_value = token.group(t_type)
        tokens.append((t_type, t_value))
    return tokens