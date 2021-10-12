class Analyzer:
    def __init__(self):
        self.tokens = dict()
        self.errors = dict()
        self.symbol_table = []

    def analyze(self):
        pass

    def get_next_token(self):
        pass


analyzer = Analyzer()
analyzer.analyze()

tokens = ''
for line_number, line_tokens in analyzer.tokens.items():
    tokens += str(line_number) + '.' + '	'
    for token in line_tokens:
        (token_type, lexeme) = token
        tokens += '(' + str(token_type) + ', ' + lexeme + ') '
    tokens += '\n'
with open('tokens.txt', 'w') as file:
    file.write(tokens)

symbol_table = ''
for line_number, symbol in enumerate(analyzer.symbol_table):
    symbol_table += str(line_number) + '.' + '	' + symbol + '\n'
with open('symbol_table.txt', 'w') as file:
    file.write(symbol_table)

errors = ''
if analyzer.errors:
    for line_number, line_errors in analyzer.tokens.items():
        for error in line_errors:
            (lexeme, error_type) = error
            errors += str(line_number) + '.' + '	' + '(' + lexeme + ', ' + str(error_type) + ')' + '\n'
else:
    errors = 'There is no lexical error.'
with open('lexical_errors.txt', 'w') as file:
    file.write(errors)
