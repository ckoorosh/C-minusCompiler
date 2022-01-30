class CodeGenerator:
    def __init__(self):
        self.semantic_stack = []
        self.program_block = []

    def save_output(self):
        codes = ''
        if self.program_block:
            for line_number, code in self.program_block:
                codes += f'{line_number}\t{code}\n'
        else:
            codes = 'The code has not been generated.'

        with open('output.txt', 'w') as file:
            file.write(codes)
