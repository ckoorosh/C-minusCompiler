class SemanticAnalyzer:
    def __init__(self, code_generator, scanner):
        self.code_generator = code_generator
        self.scanner = scanner

    def in_scope(self):
        self.scanner.scope_stack.append(len(self.scanner.symbol_table))

    def out_scope(self):
        scope_start = self.scanner.scope_stack.pop()
        self.scanner.symbol_table = self.scanner.symbol_table[:scope_start]
