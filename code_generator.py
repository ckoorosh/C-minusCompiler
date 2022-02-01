class CodeGenerator:
    def __init__(self):
        self.semantic_stack = []
        self.program_block = []
        self.program_block_index = 0
        self.static_base_pointer = 100
        self.base_pointer = 500
        self.stack_base_pointer = 1000
        self.static_offset = 0
        self.offset = 0
        self.stack = [0]

    def get_temp(self):
        temp = self.base_pointer + self.offset
        self.offset += 4
        self.stack[-1] += 4
        return temp

    def get_static(self, arity=1):
        temp = self.static_base_pointer + self.static_offset
        self.static_offset += 4 * arity
        return temp

    def get_code(self, opcode, *args):
        code = "(" + opcode.upper()
        for i in range(3):
            try:
                arg = args[i]
                code = code + ", " + str(arg)
            except IndexError:
                code = code + ", "
        return code + ")"

    def add_code(self, code, idx=None, insert=False, increment=True):
        if idx is None:
            idx = self.program_block_index
        if isinstance(code, tuple):
            code = self.get_code(code[0], *code[1:])
        if insert:
            self.program_block[idx] = (idx, code)
        else:
            self.program_block.append((idx, code))
        if increment:
            self.program_block_index += 1

    def add_placeholder(self):
        self.add_code('Placeholder')

    def init_program(self):
        code = self.get_code("assign", f'#{self.static_base_pointer}', self.static_base_pointer)
        self.add_code(code)
        self.static_offset += 8
        for _ in range(3):
            self.add_placeholder()

    def save_output(self):
        codes = ''
        if self.program_block:
            for line_number, code in self.program_block:
                codes += f'{line_number}\t{code}\n'
        else:
            codes = 'The code has not been generated.'

        with open('output.txt', 'w') as file:
            file.write(codes)




#routines

    def add_op_routine(self, input_token):
        try:
            result = self.get_temp()
            operand1 = self.semantic_stack.pop()
            operand2 = self.semantic_stack.pop()
            op = self.semantic_stack.pop()
            self.add_code((op, operand1, operand2, result))
            self.semantic_stack.append(result)
        except IndexError:
            pass

    
    def save_op_routine(self, input_token):
        try:
            self.semantic_stack.append(input_token)
        except IndexError:
            pass


    def relop_routine(self, input_token):
        try:
            result = self.get_temp()
            operand1 = self.semantic_stack.pop()
            operand2 = self.semantic_stack.pop()
            op = self.semantic_stack.pop()
            self.add_code((op, operand1, operand2, result))
            self.semantic_stack.append(result)
        except IndexError:
            pass


    def assign_routine(self, input_token):
        try:
            operand = self.semantic_stack.pop()
            result = self.semantic_stack.pop()
            self.add_code(("=", operand, result, ))
        except IndexError:
            pass
    

    def push_id_routine(self, input_token):
        try:
            id_address = "" #TODO: find address of input using symbol table
            self.semantic_stack.append(id_address)
        except IndexError:
            pass

    
    def push_const_routine(self, input_token):
        try:
            constant_value = "#" + input_token
            address = self.get_static()
            self.add_code(self.get_code("assign", constant_value, address))
            #TODO: find address of input using symbol table
            self.semantic_stack.append(address)
        except IndexError:
            pass