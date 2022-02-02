class CodeGenerator:
    def __init__(self):
        self.semantic_stack = []
        self.break_stack = []
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

    def finish_program(self):
        return_address = self.get_temp()
        self.program_block[1] = (1, self.get_code("SUB", self.static_base_pointer, "#4", return_address))
        self.program_block[2] = (2, self.get_code("assign", f"#{self.program_block_index}", f"@{return_address}"))
        # self.program_block[3] = (3, self.get_code("jp", SymbolTableManager.findrow("main")["address"]))

    def save_output(self):
        codes = ''
        if self.program_block:
            for line_number, code in self.program_block:
                codes += f'{line_number}\t{code}\n'
        else:
            codes = 'The code has not been generated.'

        with open('output.txt', 'w') as file:
            file.write(codes)

    # routines

    def add_op(self):
        try:
            result = self.get_temp()
            operand1 = self.semantic_stack.pop()
            operand2 = self.semantic_stack.pop()
            op = self.semantic_stack.pop()
            self.add_code((op, operand1, operand2, result))
            self.semantic_stack.append(result)
        except IndexError:
            pass

    def mult(self):
        try:
            result = self.get_temp()
            operand1 = self.semantic_stack.pop()
            operand2 = self.semantic_stack.pop()
            self.add_code(("*", operand1, operand2, result))
            self.semantic_stack.append(result)
        except IndexError:
            pass

    def save_op(self, input_token):
        operand = ''
        if input_token == '+':
            operand = 'ADD'
        elif input_token == '-':
            operand = 'SUB'
        elif input_token == '==':
            operand = 'EQ'
        elif input_token == '<':
            operand = 'LT'
        self.semantic_stack.append(operand)

    def save(self):
        try:
            save_address = self.program_block_index
            self.semantic_stack.append(save_address)
            self.add_placeholder()
        except IndexError:
            pass

    def break_save(self):
        self.break_stack[-1].append(self.program_block_index)
        self.add_placeholder()

    def label(self):
        try:
            save_address = self.program_block_index
            self.semantic_stack.append(save_address)
        except IndexError:
            pass

    def relop(self):
        try:
            result = self.get_temp()
            operand1 = self.semantic_stack.pop()
            operand2 = self.semantic_stack.pop()
            op = self.semantic_stack.pop()
            self.add_code((op, operand1, operand2, result))
            self.semantic_stack.append(result)
        except IndexError:
            pass

    def assign(self):
        try:
            operand = self.semantic_stack.pop()
            result = self.semantic_stack.pop()
            self.add_code(("=", operand, result,))
        except IndexError:
            pass

    def push_id(self):
        try:
            id_address = ""  # TODO: find address of input using symbol table
            self.semantic_stack.append(id_address)
        except IndexError:
            pass

    def push_const(self, input_token):
        try:
            constant_value = "#" + input_token
            address = self.get_static()
            self.add_code(self.get_code("assign", constant_value, address))
            # TODO: find address of input using symbol table
            self.semantic_stack.append(address)
        except IndexError:
            pass

    def if_else(self):
        try:
            jump_address = self.semantic_stack.pop()
            self.add_code(("jp", self.program_block_index), jump_address, True, False)
        except IndexError:
            pass

    def else_(self):
        try:
            jump_address = self.semantic_stack.pop()
            condition = self.semantic_stack.pop()
            self.add_placeholder()
            self.add_code(("jpf", condition, self.program_block_index), jump_address, True, False)
            self.semantic_stack.append(self.program_block_index)
        except IndexError:
            pass

    def close(self):
        if self.semantic_stack:
            self.semantic_stack.pop()

    def return_value(self):
        result = self.get_temp()
        self.add_code(self.get_code("SUB", self.static_base_pointer, "#8", result))
        try:
            ret_val_address = self.semantic_stack.pop()
        except IndexError:
            code = self.get_code("assign", "#0", f"@{result}")
            self.add_code(code)
        else:
            code = self.get_code("assign", ret_val_address, f"@{result}")
            self.add_code(code)

    def sf_size(self):
        # TODO: need some info
        pass

    def until(self):
        condition = self.semantic_stack.pop()
        jp_address = self.semantic_stack.pop()
        self.add_placeholder()
        self.add_code(("jpf", condition, self.program_block_index), jp_address, True, False)
        self.semantic_stack.append(self.program_block_index)
        pass
