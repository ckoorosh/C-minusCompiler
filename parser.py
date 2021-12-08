import enum

class NonTerminals(enum.Enum):
    PROGRAM = 0
    DECLARATION_LIST = 1
    DECLARATION = 2
    DECLARATION_INITIAL = 3
    DECLARATION_PRIME = 4
    VAR_DECLARATION_PRIME = 5
    FUN_DECLARATION_PRIME = 6
    TYPE_SPECIFIER = 7
    PARAMS = 8
    PARAM_LIST = 9
    PARAM = 10
    PARAM_PRIME = 11
    COMPOUND_STMT = 12
    STATEMENT_LIST = 13
    STATEMENT = 14
    EXPRESSION_STMT = 15
    SELECTION_STMT = 16
    ELSE_STMT = 17
    ITERATION_STMT = 18
    RETURN_STMT = 19
    RETURN_STMT_PRIME = 20
    EXPRESSION = 21
    B = 22
    H = 23
    SIMPLE_EXPRESSION_ZEGOND = 24
    SIMPLE_EXPRESSION_PRIME = 25
    C = 26
    RELOP = 27
    ADDITIVE_EXPRESSION = 28
    ADDITIVE_EXPRESSION_PRIME = 29
    ADDITIVE_EXPRESSION_ZEGOND = 30
    D = 31
    ADDOP = 32
    TERM = 33
    TERM_PRIME = 34
    TERM_ZEGOND = 35
    G = 36
    FACTOR = 37
    VAR_CALL_PRIME = 38
    VAR_PRIME = 39
    FACTOR_PRIME = 40
    FACTOR_ZEGOND = 41
    ARGS = 42
    ARG_LIST = 43
    ARG_LIST_PRIME = 44

class Sets:
    FIRST_SETS = {
        NonTerminals.PROGRAM: ['int', 'void'],
        NonTerminals.DECLARATION_LIST: ['int', 'void', ''],
        NonTerminals.DECLARATION: ['int', 'void'],
        NonTerminals.DECLARATION_INITIAL: ['int', 'void'],
        NonTerminals.DECLARATION_PRIME: [';', '[', '('],
        NonTerminals.VAR_DECLARATION_PRIME: [';', '['],
        NonTerminals.FUN_DECLARATION_PRIME: ['('],
        NonTerminals.TYPE_SPECIFIER: ['int', 'void'],
        NonTerminals.PARAMS: ['int', 'void'],
        NonTerminals.PARAM_LIST: [',', ''],
        NonTerminals.PARAM: ['int', 'void'],
        NonTerminals.PARAM_PRIME: ['[', ''],
        NonTerminals.COMPOUND_STMT: ['{'],
        NonTerminals.STATEMENT_LIST: ['[A-Za-z][A-Za-z0-9]*', ';', '\d+', '(', '{', 'break', 'if', 'repeat', 'return', ''],
        NonTerminals.STATEMENT: ['[A-Za-z][A-Za-z0-9]*', ';', '\d+', '(', '{', 'break', 'if', 'repeat', 'return'],
        NonTerminals.EXPRESSION_STMT: ['[A-Za-z][A-Za-z0-9]*', ';', '\d+', '(', 'break'],
        NonTerminals.SELECTION_STMT: ['if'],
        NonTerminals.ELSE_STMT: ['endif', 'else'],
        NonTerminals.ITERATION_STMT: ['repeat'],
        NonTerminals.RETURN_STMT: ['return'],
        NonTerminals.RETURN_STMT_PRIME: ['[A-Za-z][A-Za-z0-9]*', ';', '\d+', '('],
        NonTerminals.EXPRESSION: ['[A-Za-z][A-Za-z0-9]*', '\d+', '('],
        NonTerminals.B: ['[A-Za-z][A-Za-z0-9]*', '[', '\d+', '(', '<', '==', '+', '-', '*', ''],
        NonTerminals.H: ['[A-Za-z][A-Za-z0-9]*', '\d+', '(', '<', '==', '+', '-', '*', ''],
        NonTerminals.SIMPLE_EXPRESSION_ZEGOND: ['\d+', '('],
        NonTerminals.SIMPLE_EXPRESSION_PRIME: ['(', '<', '==', '+', '-', '*', ''],
        NonTerminals.C: ['<', '==', ''],
        NonTerminals.RELOP: ['<', '=='],
        NonTerminals.ADDITIVE_EXPRESSION: ['[A-Za-z][A-Za-z0-9]*', '\d+', '('],
        NonTerminals.ADDITIVE_EXPRESSION_PRIME: ['(', '+', '-', '*', ''],
        NonTerminals.ADDITIVE_EXPRESSION_ZEGOND: ['\d+', '('],
        NonTerminals.D: ['+', '-', ''],
        NonTerminals.ADDOP: ['+', '-'],
        NonTerminals.TERM: ['[A-Za-z][A-Za-z0-9]*', '\d+', '('],
        NonTerminals.TERM_PRIME: ['(', '*', ''],
        NonTerminals.TERM_ZEGOND: ['\d+', '('],
        NonTerminals.G: ['*', ''],
        NonTerminals.FACTOR: ['[A-Za-z][A-Za-z0-9]*', '\d+', '('],
        NonTerminals.VAR_CALL_PRIME: ['[', '(', ''],
        NonTerminals.VAR_PRIME: ['[', ''],
        NonTerminals.FACTOR_PRIME: ['(', ''],
        NonTerminals.FACTOR_ZEGOND: ['\d+', '('],
        NonTerminals.ARGS: ['[A-Za-z][A-Za-z0-9]*', '\d+', '(', ''],
        NonTerminals.ARG_LIST: ['[A-Za-z][A-Za-z0-9]*', '\d+', '('],
        NonTerminals.ARG_LIST_PRIME:[',', '']
    }

    FOLLOW_SETS = {
        NonTerminals.PROGRAM: ['$'],
        NonTerminals.DECLARATION_LIST: ['[A-Za-z][A-Za-z0-9]*', ';', '\d+', '(', '{', '}', 'break', 'if', 'repeat', 'return', '$'],
        NonTerminals.DECLARATION: ['[A-Za-z][A-Za-z0-9]*', ';', '\d+', '(', 'int', 'void', '{', '}', 'break', 'if', 'repeat', 'return', '$'],
        NonTerminals.DECLARATION_INITIAL: [';', '[', '(', ')', ','],
        NonTerminals.DECLARATION_PRIME: ['[A-Za-z][A-Za-z0-9]*', ';', '\d+', '(', 'int', 'void', '{', '}', 'break', 'if', 'repeat', 'return', '$'],
        NonTerminals.VAR_DECLARATION_PRIME: ['[A-Za-z][A-Za-z0-9]*', ';', '\d+', '(', 'int', 'void', '{', '}', 'break', 'if', 'repeat', 'return', '$'],
        NonTerminals.FUN_DECLARATION_PRIME: ['[A-Za-z][A-Za-z0-9]*', ';', '\d+', '(', 'int', 'void', '{', '}', 'break', 'if', 'repeat', 'return', '$'],
        NonTerminals.TYPE_SPECIFIER: ['[A-Za-z][A-Za-z0-9]*'],
        NonTerminals.PARAMS: [')'],
        NonTerminals.PARAM_LIST: [')'],
        NonTerminals.PARAM: [')', ','],
        NonTerminals.PARAM_PRIME: [')', ','],
        NonTerminals.COMPOUND_STMT: ['[A-Za-z][A-Za-z0-9]*', ';', '\d+', '(', 'int', 'void', '{', '}', 'break', 'if', 'endif', 'else', 'until', 'repeat', 'return', '$'],
        NonTerminals.STATEMENT_LIST: ['}'],
        NonTerminals.STATEMENT: ['[A-Za-z][A-Za-z0-9]*', ';', '\d+', '(', '{', '}', 'break', 'if', 'endif', 'else', 'until', 'repeat', 'return'],
        NonTerminals.EXPRESSION_STMT: ['[A-Za-z][A-Za-z0-9]*', ';', '\d+', '(', '{', '}', 'break', 'if', 'endif', 'else', 'until', 'repeat', 'return'],
        NonTerminals.SELECTION_STMT: ['[A-Za-z][A-Za-z0-9]*', ';', '\d+', '(', '{', '}', 'break', 'if', 'endif', 'else', 'until', 'repeat', 'return'],
        NonTerminals.ELSE_STMT: ['[A-Za-z][A-Za-z0-9]*', ';', '\d+', '(', '{', '}', 'break', 'if', 'endif', 'else', 'until', 'repeat', 'return'],
        NonTerminals.ITERATION_STMT: ['[A-Za-z][A-Za-z0-9]*', ';', '\d+', '(', '{', '}', 'break', 'if', 'endif', 'else', 'until', 'repeat', 'return'],
        NonTerminals.RETURN_STMT: ['[A-Za-z][A-Za-z0-9]*', ';', '\d+', '(', '{', '}', 'break', 'if', 'endif', 'else', 'until', 'repeat', 'return'],
        NonTerminals.RETURN_STMT_PRIME: ['[A-Za-z][A-Za-z0-9]*', ';', '\d+', '(', '{', '}', 'break', 'if', 'endif', 'else', 'until', 'repeat', 'return'],
        NonTerminals.EXPRESSION: [';', ']', ')', ','],
        NonTerminals.B: [';', ']', ')', ','],
        NonTerminals.H: [';', ']', ')', ','],
        NonTerminals.SIMPLE_EXPRESSION_ZEGOND: [';', ']', ')', ','],
        NonTerminals.SIMPLE_EXPRESSION_PRIME: [';', ']', ')', ','],
        NonTerminals.C: [';', ']', ')', ','],
        NonTerminals.RELOP: ['[A-Za-z][A-Za-z0-9]*', '\d+', '('],
        NonTerminals.ADDITIVE_EXPRESSION: [';', ']', ')', ','],
        NonTerminals.ADDITIVE_EXPRESSION_PRIME: [';', ']', ')', ',', '<', '=='],
        NonTerminals.ADDITIVE_EXPRESSION_ZEGOND: [';', ']', ')', ',', '<', '=='],
        NonTerminals.D: [';', ']', ')', ',', '<', '=='],
        NonTerminals.ADDOP: ['[A-Za-z][A-Za-z0-9]*', '\d+', '('],
        NonTerminals.TERM: [';', ']', ')', ',', '<', '==', '+', '-'],
        NonTerminals.TERM_PRIME: [';', ']', ')', ',', '<', '==', '+', '-'],
        NonTerminals.TERM_ZEGOND: [';', ']', ')', ',', '<', '==', '+', '-'],
        NonTerminals.G: [';', ']', ')', ',', '<', '==', '+', '-'],
        NonTerminals.FACTOR: [';', ']', ')', ',', '<', '==', '+', '-', '*'],
        NonTerminals.VAR_CALL_PRIME: [';', ']', ')', ',', '<', '==', '+', '-', '*'],
        NonTerminals.VAR_PRIME: [';', ']', ')', ',', '<', '==', '+', '-', '*'],
        NonTerminals.FACTOR_PRIME: [';', ']', ')', ',', '<', '==', '+', '-', '*'],
        NonTerminals.FACTOR_ZEGOND: [';', ']', ')', ',', '<', '==', '+', '-', '*'],
        NonTerminals.ARGS: [')'],
        NonTerminals.ARG_LIST:[')'],
        NonTerminals.ARG_LIST_PRIME:[')']
    }