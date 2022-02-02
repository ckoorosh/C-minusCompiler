import enum
from anytree import Node, RenderTree
from scanner import TokenType
from code_generator import *
from semantic_analyzer import *


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
        NonTerminals.PROGRAM: ['int', 'void', '$'],
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
        NonTerminals.STATEMENT_LIST: ['ID', ';', 'NUM', '(', '{', 'break', 'if', 'repeat', 'return', ''],
        NonTerminals.STATEMENT: ['ID', ';', 'NUM', '(', '{', 'break', 'if', 'repeat', 'return'],
        NonTerminals.EXPRESSION_STMT: ['ID', ';', 'NUM', '(', 'break'],
        NonTerminals.SELECTION_STMT: ['if'],
        NonTerminals.ELSE_STMT: ['endif', 'else'],
        NonTerminals.ITERATION_STMT: ['repeat'],
        NonTerminals.RETURN_STMT: ['return'],
        NonTerminals.RETURN_STMT_PRIME: ['ID', ';', 'NUM', '('],
        NonTerminals.EXPRESSION: ['ID', 'NUM', '('],
        NonTerminals.B: ['=', '[', '(', '<', '==', '+', '-', '*', ''],
        NonTerminals.H: ['=', '<', '==', '+', '-', '*', ''],
        NonTerminals.SIMPLE_EXPRESSION_ZEGOND: ['NUM', '('],
        NonTerminals.SIMPLE_EXPRESSION_PRIME: ['(', '<', '==', '+', '-', '*', ''],
        NonTerminals.C: ['<', '==', ''],
        NonTerminals.RELOP: ['<', '=='],
        NonTerminals.ADDITIVE_EXPRESSION: ['ID', 'NUM', '('],
        NonTerminals.ADDITIVE_EXPRESSION_PRIME: ['(', '+', '-', '*', ''],
        NonTerminals.ADDITIVE_EXPRESSION_ZEGOND: ['NUM', '('],
        NonTerminals.D: ['+', '-', ''],
        NonTerminals.ADDOP: ['+', '-'],
        NonTerminals.TERM: ['ID', 'NUM', '('],
        NonTerminals.TERM_PRIME: ['(', '*', ''],
        NonTerminals.TERM_ZEGOND: ['NUM', '('],
        NonTerminals.G: ['*', ''],
        NonTerminals.FACTOR: ['ID', 'NUM', '('],
        NonTerminals.VAR_CALL_PRIME: ['[', '(', ''],
        NonTerminals.VAR_PRIME: ['[', ''],
        NonTerminals.FACTOR_PRIME: ['(', ''],
        NonTerminals.FACTOR_ZEGOND: ['NUM', '('],
        NonTerminals.ARGS: ['ID', 'NUM', '(', ''],
        NonTerminals.ARG_LIST: ['ID', 'NUM', '('],
        NonTerminals.ARG_LIST_PRIME: [',', '']
    }

    FOLLOW_SETS = {
        NonTerminals.PROGRAM: [],
        NonTerminals.DECLARATION_LIST: ['$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}'],
        NonTerminals.DECLARATION: ['int', 'void', '$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM',
                                   '}'],
        NonTerminals.DECLARATION_INITIAL: [';', '[', '(', ')', ','],
        NonTerminals.DECLARATION_PRIME: ['int', 'void', '$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(',
                                         'NUM', '}'],
        NonTerminals.VAR_DECLARATION_PRIME: ['int', 'void', '$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(',
                                             'NUM', '}'],
        NonTerminals.FUN_DECLARATION_PRIME: ['int', 'void', '$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(',
                                             'NUM', '}'],
        NonTerminals.TYPE_SPECIFIER: ['ID'],
        NonTerminals.PARAMS: [')'],
        NonTerminals.PARAM_LIST: [')'],
        NonTerminals.PARAM: [')', ','],
        NonTerminals.PARAM_PRIME: [')', ','],
        NonTerminals.COMPOUND_STMT: ['int', 'void', '$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM',
                                     '}', 'endif', 'else', 'until'],
        NonTerminals.STATEMENT_LIST: ['}'],
        NonTerminals.STATEMENT: ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'endif', 'else',
                                 'until'],
        NonTerminals.EXPRESSION_STMT: ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'endif',
                                       'else', 'until'],
        NonTerminals.SELECTION_STMT: ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'endif',
                                      'else', 'until'],
        NonTerminals.ELSE_STMT: ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'endif', 'else',
                                 'until'],
        NonTerminals.ITERATION_STMT: ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'endif',
                                      'else', 'until'],
        NonTerminals.RETURN_STMT: ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'endif', 'else',
                                   'until'],
        NonTerminals.RETURN_STMT_PRIME: ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'endif',
                                         'else', 'until'],
        NonTerminals.EXPRESSION: [';', ']', ')', ','],
        NonTerminals.B: [';', ']', ')', ','],
        NonTerminals.H: [';', ']', ')', ','],
        NonTerminals.SIMPLE_EXPRESSION_ZEGOND: [';', ']', ')', ','],
        NonTerminals.SIMPLE_EXPRESSION_PRIME: [';', ']', ')', ','],
        NonTerminals.C: [';', ']', ')', ','],
        NonTerminals.RELOP: ['ID', 'NUM', '('],
        NonTerminals.ADDITIVE_EXPRESSION: [';', ']', ')', ','],
        NonTerminals.ADDITIVE_EXPRESSION_PRIME: [';', ']', ')', ',', '<', '=='],
        NonTerminals.ADDITIVE_EXPRESSION_ZEGOND: [';', ']', ')', ',', '<', '=='],
        NonTerminals.D: [';', ']', ')', ',', '<', '=='],
        NonTerminals.ADDOP: ['ID', 'NUM', '('],
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
        NonTerminals.ARG_LIST: [')'],
        NonTerminals.ARG_LIST_PRIME: [')']
    }

    TRANSITIONS = {
        0: [{NonTerminals.DECLARATION_LIST: 1, '$': -1}],
        1: [{NonTerminals.DECLARATION: 2, NonTerminals.DECLARATION_LIST: 1},
            {'': -1}],
        2: [{NonTerminals.DECLARATION_INITIAL: 3, NonTerminals.DECLARATION_PRIME: 4}],
        3: [{NonTerminals.TYPE_SPECIFIER: 7, 'ID': -1}],
        4: [{NonTerminals.VAR_DECLARATION_PRIME: 5},
            {NonTerminals.FUN_DECLARATION_PRIME: 6}],
        5: [{';': -1},
            {'[': -1, 'NUM': -1, ']': -1, ';': -1}],
        6: [{'(': -1, '#S_in_scope': -1, NonTerminals.PARAMS: 8, ')': -1, NonTerminals.COMPOUND_STMT: 12,
             '#sf_size': -1, '#return_seq': -1, '#S_out_scope': -1}],
        7: [{'int': -1},
            {'void': -1}],
        8: [{'int': -1, 'ID': -1, NonTerminals.PARAM_PRIME: 11, NonTerminals.PARAM_LIST: 9},
            {'void': -1}],
        9: [{',': -1, NonTerminals.PARAM: 10, NonTerminals.PARAM_LIST: 9},
            {'': -1}],
        10: [{NonTerminals.DECLARATION_INITIAL: 3, NonTerminals.PARAM_PRIME: 11}],
        11: [{'[': -1, ']': -1},
             {'': -1}],
        12: [{'{': -1, NonTerminals.DECLARATION_LIST: 1, NonTerminals.STATEMENT_LIST: 13, '}': -1}],
        13: [{NonTerminals.STATEMENT: 14, NonTerminals.STATEMENT_LIST: 13},
             {'': -1}],
        14: [{NonTerminals.EXPRESSION_STMT: 15},
             {NonTerminals.COMPOUND_STMT: 12},
             {NonTerminals.SELECTION_STMT: 16},
             {NonTerminals.ITERATION_STMT: 18},
             {NonTerminals.RETURN_STMT: 19}],
        15: [{NonTerminals.EXPRESSION: 21, '#close': -1, ';': -1},
             {'#': -1, 'break': -1, ';': -1},
             {';': -1}],
        16: [{'if': -1, '(': -1, NonTerminals.EXPRESSION: 21, ')': -1, '#save': -1, NonTerminals.STATEMENT: 14,
              NonTerminals.ELSE_STMT: 17}],
        17: [{'endif': -1},
             {'else': -1, '#else': -1, NonTerminals.STATEMENT: 14, '#if_else': -1, 'endif': -1}],
        18: [{'repeat': -1, NonTerminals.STATEMENT: 14, '#label': -1, 'until': -1, '(': -1, NonTerminals.EXPRESSION: 21,
              '#until': -1, ')': -1}],
        19: [{'return': -1, NonTerminals.RETURN_STMT_PRIME: 20, '#return_value': -1, '#return_seq': -1}],
        20: [{';': -1},
             {NonTerminals.EXPRESSION: 21, ';': -1}],
        21: [{NonTerminals.SIMPLE_EXPRESSION_ZEGOND: 24},
             {'#push_id': -1, 'ID': -1, NonTerminals.B: 22}],
        22: [{'=': -1, NonTerminals.EXPRESSION: 21, '#assign': -1},
             {'[': -1, NonTerminals.EXPRESSION: 21, ']': -1, NonTerminals.H: 23},
             {NonTerminals.SIMPLE_EXPRESSION_PRIME: 25}],
        23: [{'=': -1, NonTerminals.EXPRESSION: 21, '#assign': -1},
             {NonTerminals.G: 36, NonTerminals.D: 31, NonTerminals.C: 26}],
        24: [{NonTerminals.ADDITIVE_EXPRESSION_ZEGOND: 30, NonTerminals.C: 26}],
        25: [{NonTerminals.ADDITIVE_EXPRESSION_PRIME: 29, NonTerminals.C: 26}],
        26: [{'#save_op': -1, NonTerminals.RELOP: 27, NonTerminals.ADDITIVE_EXPRESSION: 28, '#relop': -1},
             {'': -1}],
        27: [{'<': -1},
             {'==': -1}],
        28: [{NonTerminals.TERM: 33, NonTerminals.D: 31}],
        29: [{NonTerminals.TERM_PRIME: 34, NonTerminals.D: 31}],
        30: [{NonTerminals.TERM_ZEGOND: 35, NonTerminals.D: 31}],
        31: [{'#save_op': -1, NonTerminals.ADDOP: 32, NonTerminals.TERM: 33, '#add_op': -1, NonTerminals.D: 31},
             {'': -1}],
        32: [{'+': -1},
             {'-': -1}],
        33: [{NonTerminals.FACTOR: 37, NonTerminals.G: 36}],
        34: [{NonTerminals.FACTOR_PRIME: 40, NonTerminals.G: 36}],
        35: [{NonTerminals.FACTOR_ZEGOND: 41, NonTerminals.G: 36}],
        36: [{'*': -1, NonTerminals.FACTOR: 37, '#mult': -1, NonTerminals.G: 36},
             {'': -1}],
        37: [{'(': -1, NonTerminals.EXPRESSION: 21, ')': -1},
             {'#push_id': -1, 'ID': -1, NonTerminals.VAR_CALL_PRIME: 38},
             {'#push_const': -1, 'NUM': -1}],
        38: [{'(': -1, NonTerminals.ARGS: 42, ')': -1, '#call_seq': -1},
             {NonTerminals.VAR_PRIME: 39}],
        39: [{'[': -1, NonTerminals.EXPRESSION: 21, ']': -1},
             {'': -1}],
        40: [{'(': -1, NonTerminals.ARGS: 42, ')': -1, '#call_seq': -1},
             {'': -1}],
        41: [{'(': -1, NonTerminals.EXPRESSION: 21, ')': -1},
             {'#push_const': -1, 'NUM': -1}],
        42: [{NonTerminals.ARG_LIST: 43},
             {'': -1}],
        43: [{NonTerminals.EXPRESSION: 21, NonTerminals.ARG_LIST_PRIME: 44}],
        44: [{',': -1, NonTerminals.EXPRESSION: 21, NonTerminals.ARG_LIST_PRIME: 44},
             {'': -1}]
    }


class Parser:
    def __init__(self, scanner):
        self.scanner = scanner
        self.code_generator = CodeGenerator(scanner)
        self.semantic_analyzer = SemanticAnalyzer(self.code_generator)
        self.errors = []
        self.parse_tree = Node('Program')
        self.state = 0
        self.current_token = None
        self.get_next_token()
        self.eof_error = False

    def get_next_token(self):
        self.current_token = self.scanner.get_next_token()
        self.scanner.add_to_symbol_table(self.current_token)

    def get_current_lexeme(self):
        token, lexeme = self.current_token
        parse_lexeme = lexeme
        if token == TokenType.NUM or token == TokenType.ID:
            lexeme = token.name
        return lexeme, parse_lexeme

    def get_next_lexeme(self):
        self.get_next_token()
        return self.get_current_lexeme()

    def get_path(self, state):
        for path in Sets.TRANSITIONS[state]:
            edge = list(path.keys())[0]
            for e in path.keys():
                if (path[e] == -1 and not e.startswith('#')) or path[e] != -1:
                    edge = e
                    break
            next_state = path[edge]
            lexeme, _ = self.get_current_lexeme()
            if next_state != -1:
                if lexeme in Sets.FIRST_SETS[edge]:
                    return path
            else:
                if lexeme == edge:
                    return path
        return self.get_epsilon(state)

    def get_epsilon(self, state):
        for path in Sets.TRANSITIONS[state]:
            edge = list(path.keys())[0]
            next_state = path[edge]
            if next_state == -1:
                if edge == '':
                    return path
            else:
                if '' in Sets.FIRST_SETS[edge]:
                    return path
        return None

    def get_non_terminal_name(self, non_terminal):
        return str.capitalize(str.lower(non_terminal)).replace('_', '-')

    def parse(self):
        # self.code_gen('init', None)
        self._parse(0)
        self.code_generator.save_output()
        # self.code_gen('finish', None)

    def _parse(self, state, parent=None):
        if NonTerminals(state).name != "PROGRAM":
            node = Node(self.get_non_terminal_name(NonTerminals(state).name), parent=parent)
        else:
            node = Node(self.get_non_terminal_name(NonTerminals(state).name))
            self.parse_tree = node
        path = self.get_path(state)

        for edge in path:
            next_state = path[edge]
            while True:
                lexeme, parse_lexeme = self.get_current_lexeme()
                if next_state != -1:  # non-terminal
                    if lexeme in Sets.FIRST_SETS[edge]:
                        self._parse(next_state, node)
                        if self.eof_error:
                            return
                        break
                    elif lexeme in Sets.FOLLOW_SETS[edge]:
                        if '' in Sets.FIRST_SETS[edge]:
                            self._parse(next_state, node)
                            break
                        else:
                            self.add_error(f'missing {self.get_non_terminal_name(edge.name)}')
                            break
                    else:
                        if lexeme == '$':
                            self.add_error('Unexpected EOF')
                            self.eof_error = True
                            return
                        else:
                            self.add_error(f'illegal {lexeme}')
                            self.get_next_token()
                elif edge.startswith('#S_'):  # Semantic Analyzer
                    pass
                elif edge.startswith('#'):  # Intermediate Code Generator
                    self.code_gen(edge, self.get_current_lexeme()[1])
                    break
                else:  # terminal
                    if edge == '':
                        terminal_node = Node('epsilon', parent=node)
                        break
                    if lexeme == edge:
                        if edge == '$':
                            terminal_node = Node('$', parent=node)
                            return
                        else:
                            terminal_node = Node(f'({self.current_token[0].name}, {parse_lexeme})', parent=node)
                            self.get_next_token()
                            break
                    else:
                        self.add_error(f'missing {edge}')
                        break

    def code_gen(self, symbol, token):
        # TODO: Call semantic action routines
        print(symbol)
        if symbol == 'init':
            self.code_generator.init_program()
        elif symbol == 'finish':
            self.code_generator.finish_program()
        elif symbol == '#add_op':
            self.code_generator.add_op()
        elif symbol == '#mult':
            self.code_generator.mult()
        elif symbol == '#save_op':
            self.code_generator.save_op(token)
        elif symbol == '#save':
            self.code_generator.save()
        elif symbol == '#break_save':
            self.code_generator.break_save()
        elif symbol == '#label':
            self.code_generator.label()
        elif symbol == '#relop':
            self.code_generator.relop()
        elif symbol == '#assign':
            self.code_generator.assign()
        elif symbol == '#push_id':
            self.code_generator.push_id(token)
        elif symbol == '#push_const':
            self.code_generator.push_const(token)
        elif symbol == '#if_else':
            self.code_generator.if_else()
        elif symbol == '#else':
            self.code_generator.else_()
        elif symbol == '#close':
            self.code_generator.close()
        elif symbol == '#return_value':
            self.code_generator.return_value()
        elif symbol == '#return_seq':
            self.code_generator.return_seq()
        elif symbol == '#call_seq':
            self.code_generator.call_seq()
        elif symbol == '#sf_size':
            self.code_generator.sf_size()

    def semantic(self, action):
        if action == '#S_in_scope':
            self.semantic_analyzer.in_scope()
        elif action == '#S_out_scope':
            self.semantic_analyzer.out_scope()

    def add_error(self, error):
        self.errors.append((self.scanner.current_line, error))

    def save_parse_tree(self):
        line = 0
        for _, _, _ in RenderTree(self.parse_tree):
            line += 1
        with open('parse_tree.txt', 'w', encoding="utf-8") as file:
            for pre, _, node in RenderTree(self.parse_tree):
                if line == 1:
                    file.write(f'{pre}{node.name}')
                else:
                    file.write(f'{pre}{node.name}\n')
                line -= 1

    def save_errors(self):
        errors = ''
        if self.errors:
            for line_number, error in self.errors:
                errors += f'#{line_number} : syntax error, {error}\n'
        else:
            errors = 'There is no syntax error.'
        with open('syntax_errors.txt', 'w') as file:
            file.write(errors)
