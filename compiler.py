import enum
import sys


class TokenType(enum.Enum):
    EOF = -1
    NUM = 0
    ID = 1
    KEYWORD = 2
    SYMBOL = 3
    COMMENT = 4
    WHITESPACE = 5


class Scanner:
    SYMBOLS = [';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-', '*', '=', '<', '==']
    KEYWORDS = ['if', 'else', 'void', 'int', 'repeat', 'break', 'until', 'return']
    WHITESPACES = [' ', '\n', '\r', '\t', '\v', '\f']

    def __init__(self, text):
        self.tokens = dict()
        self.errors = dict()
        self.symbol_table = []
        self.text = text
        self.current_char = ''
        self.current_position = -1
        self.next_char()

    def next_char(self):
        self.current_position += 1
        if self.current_position >= len(self.text):
            self.current_char = '\0'  # EOF
        else:
            self.current_char = self.text[self.current_position]

    def look_ahead(self):
        if self.current_position + 1 >= len(self.text):
            return '\0'
        return self.text[self.current_position + 1]

    def scan(self):
        token = self.get_next_token()
        (token_type, lexeme) = token
        while token_type != TokenType.EOF:
            print(token)
            token = self.get_next_token()

    def get_next_token(self):
        token = None

        while self.current_char in self.WHITESPACES:
            self.next_char()
        self.skip_comment()

        if self.current_char in self.SYMBOLS:
            if self.current_char == '=':
                if self.look_ahead() == '=':
                    last_char = self.current_char
                    self.next_char()
                    token = (last_char + self.current_char, TokenType.SYMBOL)
                else:
                    token = (self.current_char, TokenType.SYMBOL)
            else:
                token = (self.current_char, TokenType.SYMBOL)
        elif self.current_char == '\0':
            token = ('', TokenType.EOF)
        else:
            # Unknown token!
            sys.exit("Lexing error. " + 'Unknown token')
            pass

        self.next_char()
        return token

    def skip_comment(self):
        # TODO
        pass


def main():
    with open('input.txt', 'r') as file:
        # text = file.read()
        text = '+- */'
        scanner = Scanner(text)
        scanner.scan()

    tokens = ''
    for line_number, line_tokens in scanner.tokens.items():
        tokens += str(line_number) + '.' + '	'
        for token in line_tokens:
            (token_type, lexeme) = token
            tokens += '(' + str(token_type) + ', ' + lexeme + ') '
        tokens += '\n'
    with open('tokens.txt', 'w') as file:
        file.write(tokens)

    symbol_table = ''
    for line_number, symbol in enumerate(scanner.symbol_table):
        symbol_table += str(line_number + 1) + '.' + '	' + symbol + '\n'
    with open('symbol_table.txt', 'w') as file:
        file.write(symbol_table)

    errors = ''
    if scanner.errors:
        for line_number, line_errors in scanner.tokens.items():
            for error in line_errors:
                (lexeme, error_type) = error
                errors += str(line_number) + '.' + '	' + '(' + lexeme + ', ' + str(error_type) + ')' + '\n'
    else:
        errors = 'There is no lexical error.'
    with open('lexical_errors.txt', 'w') as file:
        file.write(errors)


if __name__ == '__main__':
    main()
