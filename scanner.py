# Mohammadreza Mofayezi 98106059
# Pouria Momtaz 98106061

# With some help from CS143 stanford course

import enum


class TokenType(enum.Enum):
    EOF = -1
    NUM = 0
    ID = 1
    KEYWORD = 2
    SYMBOL = 3
    COMMENT = 4
    WHITESPACE = 5


class ErrorType(enum.Enum):
    INVALID_INPUT = 'Invalid input'
    UNCLOSED_COMMENT = 'Unclosed comment'
    UNMATCHED_COMMENT = 'Unmatched comment'
    INVALID_NUMBER = 'Invalid number'


class TokenState(enum.Enum):
    INITIAL = 0
    WHITESPACE = 1
    NUM_START = 2
    NUM = 3
    INVALID_NUMBER = 4
    START_ID_OR_KEYWORD = 5
    ID_OR_KEYWORD = 6
    ASTERISK = 7
    UNMATCHED_COMMENT = 8
    START_EQUAL = 9
    EQUAL_EQUAL = 10
    EQUAL = 11
    SYMBOL = 12
    START_SLASH = 13
    START_BLOCK_COMMENT = 14
    BLOCK_COMMENT_ASTERISK = 15
    BLOCK_COMMENT = 16
    START_LINE_COMMENT = 17
    LINE_COMMENT = 18
    NEWLINE = 19
    INVALID_INPUT = 20
    ASTERISK_SYMBOL = 21


class Scanner:
    SYMBOLS = [';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-', '<']
    KEYWORDS = ['if', 'else', 'void', 'int', 'repeat', 'break', 'until', 'return', 'endif']
    WHITESPACES = [' ', '\r', '\t', '\v', '\f']

    def __init__(self, input_file, chunk_size=8192):
        self.tokens = dict()
        self.errors = dict()
        self.symbol_table = []
        self.input_file = input_file
        self.text = ''
        self.file_pointer = 0
        self.current_line = 1
        self.unclosed_comment_size = 7
        self.chunk_size = chunk_size
        self.read_text()
        self.init_symbol_table()

    def read_text(self):
        with open(self.input_file, "rb") as f:
            f.seek(self.file_pointer)
            chunk = f.read(self.chunk_size)
        if not chunk:
            raise EOFError
        self.text += chunk.decode()
        self.file_pointer += self.chunk_size

    def init_symbol_table(self):
        for keyword in self.KEYWORDS:
            self.symbol_table.append(keyword)

    def scan(self):
        token = self.get_next_token()
        if token is not None:
            (token_type, lexeme) = token
            while token_type != TokenType.EOF:
                if token is not None:
                    if token_type == TokenType.KEYWORD or token_type == TokenType.ID:
                        if lexeme not in self.symbol_table:
                            self.symbol_table.append(lexeme)
                    self.add_token(token_type, lexeme)

                    token = self.get_next_token()
                    (token_type, lexeme) = token
        self.save_tokens()
        self.save_symbol_table()
        self.save_errors()

    def save_tokens(self):
        tokens = ''
        for line_number, line_tokens in self.tokens.items():
            tokens += str(line_number) + '.' + '\t'
            for token in line_tokens:
                (token_type, lexeme) = token
                tokens += '(' + str(token_type) + ', ' + lexeme + ') '
            tokens += '\n'
        with open('tokens.txt', 'w') as file:
            file.write(tokens)

    def save_symbol_table(self):
        symbol_table = ''
        for line_number, symbol in enumerate(self.symbol_table):
            symbol_table += str(line_number + 1) + '.' + '	' + symbol + '\n'
        with open('symbol_table.txt', 'w') as file:
            file.write(symbol_table)

    def save_errors(self):
        errors = ''
        if self.errors:
            for line_number, line_errors in self.errors.items():
                errors += str(line_number) + '.' + '\t'
                for error in line_errors:
                    (lexeme, error_type) = error
                    errors += '(' + lexeme + ', ' + str(error_type) + ') '
                errors += '\n'
        else:
            errors = 'There is no lexical error.'
        with open('lexical_errors.txt', 'w') as file:
            file.write(errors)

    def add_error(self, error):
        (error_type, lexeme) = error
        if self.current_line not in self.errors:
            self.errors[self.current_line] = []
        self.errors[self.current_line].append((lexeme, error_type.value))

    def add_token(self, token_type, lexeme):
        if self.current_line not in self.tokens:
            self.tokens[self.current_line] = []
        self.tokens[self.current_line].append((token_type.name, lexeme))

    def get_next_token(self):
        input_ended = False
        state = TokenState.INITIAL

        while True:
            if not self.text or input_ended:
                try:
                    self.read_text()
                except EOFError:
                    if state == TokenState.START_BLOCK_COMMENT or state == TokenState.BLOCK_COMMENT_ASTERISK or \
                            state == TokenState.START_LINE_COMMENT:
                        comment_size = self.unclosed_comment_size
                        lexeme = self.text[:comment_size]
                        if len(self.text) > len(lexeme):
                            lexeme = lexeme + '...'
                        self.add_error((ErrorType.UNCLOSED_COMMENT, lexeme))
                    elif state == TokenState.NUM_START:
                        token = (TokenType.NUM, self.text)
                        self.text = ''
                        return token
                    elif state == TokenState.START_ID_OR_KEYWORD:
                        token_type = TokenType.KEYWORD if self.text in self.KEYWORDS else TokenType.ID
                        token = (token_type, self.text)
                        self.text = ''
                        return token
                    self.current_line += self.text.count("\n")
                    self.text = ''
                    return TokenType.EOF, '$'

            tokens = []
            error_occurred = False
            input_ended = False

            state = TokenState.INITIAL

            for i in range(len(self.text) + 1):
                try:
                    next_character = self.text[i]
                except IndexError:
                    next_character = self.text[-1]

                if state == TokenState.INITIAL:  # 0
                    if next_character in self.WHITESPACES:
                        state = TokenState.WHITESPACE
                    elif next_character.isdigit():
                        state = TokenState.NUM_START
                    elif next_character.isalpha():
                        state = TokenState.START_ID_OR_KEYWORD
                    elif next_character == '*':
                        state = TokenState.ASTERISK
                    elif next_character == '=':
                        state = TokenState.START_EQUAL
                    elif next_character in self.SYMBOLS:
                        state = TokenState.SYMBOL
                    elif next_character == '/':
                        state = TokenState.START_SLASH
                    elif next_character == '\n':
                        state = TokenState.NEWLINE
                    else:
                        state = TokenState.INVALID_INPUT
                elif state == TokenState.WHITESPACE:  # 1
                    if next_character in self.WHITESPACES or next_character == '\n':
                        state = TokenState.WHITESPACE
                    else:
                        break
                elif state == TokenState.NUM_START:  # 2
                    if next_character in self.WHITESPACES:
                        state = TokenState.NUM
                    elif next_character.isdigit():
                        state = TokenState.NUM_START
                    elif next_character.isalpha():
                        state = TokenState.INVALID_NUMBER
                    elif next_character == '*' or next_character == '=' or next_character in self.SYMBOLS or \
                            next_character == '/' or next_character == '\n':
                        state = TokenState.NUM
                    else:
                        state = TokenState.INVALID_NUMBER
                elif state == TokenState.NUM:  # 3
                    tokens.append((TokenType.NUM, self.text[:i - 1]))
                    state = None
                elif state == TokenState.INVALID_NUMBER:  # 4
                    error = (ErrorType.INVALID_NUMBER, self.text[:i])
                    self.add_error(error)
                    self.text = self.text[i:]
                    error_occurred = True
                    break
                elif state == TokenState.START_ID_OR_KEYWORD:  # 5
                    if next_character in self.WHITESPACES:
                        state = TokenState.ID_OR_KEYWORD
                    elif next_character.isdigit() or next_character.isalpha():
                        state = TokenState.START_ID_OR_KEYWORD
                    elif next_character == '*' or next_character == '=' or next_character in self.SYMBOLS or \
                            next_character == '/' or next_character == '\n':
                        state = TokenState.ID_OR_KEYWORD
                    else:
                        state = TokenState.INVALID_INPUT
                elif state == TokenState.ID_OR_KEYWORD:  # 6
                    tokens.append((TokenType.ID, self.text[:i - 1]))
                    state = None
                elif state == TokenState.ASTERISK:  # 7
                    if next_character in self.WHITESPACES or next_character.isdigit() or next_character.isalpha() or \
                            next_character == '*' or next_character == '=' or \
                            next_character == '\n' or next_character in self.SYMBOLS:
                        state = TokenState.ASTERISK_SYMBOL
                    elif next_character == '/':
                        state = TokenState.UNMATCHED_COMMENT
                    else:
                        state = TokenState.INVALID_INPUT
                elif state == TokenState.UNMATCHED_COMMENT:  # 8
                    error = (ErrorType.UNMATCHED_COMMENT, self.text[:i])
                    self.add_error(error)
                    self.text = self.text[i:]
                    error_occurred = True
                    break
                elif state == TokenState.START_EQUAL:  # 9
                    if next_character in self.WHITESPACES or next_character.isdigit() or next_character.isalpha() or \
                            next_character == '*' or next_character == '/' or next_character == '\n' \
                            or next_character in self.SYMBOLS:
                        state = TokenState.EQUAL
                    elif next_character == '=':
                        state = TokenState.EQUAL_EQUAL
                    else:
                        state = TokenState.INVALID_INPUT
                elif state == TokenState.EQUAL_EQUAL:  # 10
                    tokens.append((TokenType.SYMBOL, self.text[:i]))
                    state = None
                elif state == TokenState.EQUAL:  # 11
                    tokens.append((TokenType.SYMBOL, self.text[:i - 1]))
                    state = None
                elif state == TokenState.SYMBOL:  # 12
                    tokens.append((TokenType.SYMBOL, self.text[:i]))
                    state = None
                elif state == TokenState.START_SLASH:  # 13
                    if next_character == '*':
                        state = TokenState.START_BLOCK_COMMENT
                    elif next_character == '/':
                        state = TokenState.START_LINE_COMMENT
                    else:
                        error = (ErrorType.INVALID_INPUT, self.text[:i])
                        self.add_error(error)
                        self.text = self.text[i:]
                        error_occurred = True
                        break
                elif state == TokenState.START_BLOCK_COMMENT:  # 14
                    if next_character == '*':
                        state = TokenState.BLOCK_COMMENT_ASTERISK
                    else:
                        state = TokenState.START_BLOCK_COMMENT
                elif state == TokenState.BLOCK_COMMENT_ASTERISK:  # 15
                    if next_character == '*':
                        state = TokenState.BLOCK_COMMENT_ASTERISK
                    elif next_character == '/':
                        state = TokenState.BLOCK_COMMENT
                    else:
                        state = TokenState.START_BLOCK_COMMENT
                elif state == TokenState.BLOCK_COMMENT:  # 16
                    tokens.append((TokenType.COMMENT, self.text[:i]))
                    state = None
                elif state == TokenState.START_LINE_COMMENT:  # 17
                    if next_character == '\n':
                        state = TokenState.LINE_COMMENT
                    else:
                        state = TokenState.START_LINE_COMMENT
                elif state == TokenState.LINE_COMMENT:  # 18
                    tokens.append((TokenType.COMMENT, self.text[:i]))
                    state = None
                elif state == TokenState.NEWLINE:  # 19
                    if next_character in self.WHITESPACES or next_character == '\n':
                        state = TokenState.NEWLINE
                    else:
                        tokens.append((TokenType.WHITESPACE, self.text[:i]))
                        state = None
                elif state == TokenState.INVALID_INPUT:  # 20
                    error = (ErrorType.INVALID_INPUT, self.text[:i])
                    self.add_error(error)
                    self.text = self.text[i:]
                    error_occurred = True
                    break
                elif state == TokenState.ASTERISK_SYMBOL:  # 21
                    tokens.append((TokenType.SYMBOL, self.text[:i - 1]))
                    state = None

                if state is None:
                    break
                elif i >= len(self.text):
                    input_ended = True
                    break

            if error_occurred or input_ended:
                continue

            if tokens:
                max_token = tokens[-1]
                (token, lexeme) = max_token
                self.text = self.text[len(lexeme):]

                if token == TokenType.WHITESPACE or token == TokenType.COMMENT:
                    self.current_line += lexeme.count('\n')
                    continue

                if token == TokenType.ID:
                    token = TokenType.KEYWORD if lexeme in self.KEYWORDS else TokenType.ID

                return token, lexeme
            else:
                self.text = self.text[1:]
