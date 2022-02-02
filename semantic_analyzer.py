class SemanticAnalyzer:
    def __init__(self, code_generator):
        self.code_generator = code_generator

    def in_scope(self):
        self.code_generator.scope_stack.append(len(self.code_generator.symbol_table))

    def out_scope(self):
        scope_start = self.code_generator.scope_stack.pop()
        self.code_generator.symbol_table = self.code_generator.symbol_table[:scope_start]
