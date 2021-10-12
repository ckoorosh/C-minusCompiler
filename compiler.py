class Scanner:
    def __init__(self):
        self.tokens = dict()
        self.errors = dict()
        self.symbol_table = []

    def scan(self):
        while True:
            pass
        pass

    def get_next_token(self):
        pass


scanner = Scanner()
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
    symbol_table += str(line_number) + '.' + '	' + symbol + '\n'
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
