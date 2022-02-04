class CodeGenerator:
    def __init__(self, scanner):
        self.scanner = scanner
        self.semantic_stack = []
        self.break_stack = []
        self.program_block = []
        self.call_seq_stack = []
        self.stack = [0]
        self.program_block_index = 0
        self.static_base_pointer = 100
        self.base_pointer = 500
        self.stack_base_pointer = 1000
        self.static_offset = 0
        self.offset = 0
        self.args_field_offset = 4
        self.locals_field_offset = 0
        self.array_field_offset = 0
        self.temp_field_offset = 0

    @property
    def arg_counter(self):
        return [len(l) for l in self.scanner.arg_list_stack]

    def reset(self):
        self.args_field_offset = 4
        self.locals_field_offset = 0
        self.array_field_offset = 0
        self.temp_field_offset = 0

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
        code = "(" + str(opcode).upper()
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

    def add_reserved(self):
        self.add_code('Reserved')

    def init_program(self):
        code = self.get_code("assign", f'#{self.stack_base_pointer}', self.static_base_pointer)
        self.add_code(code)
        self.static_offset += 8
        for _ in range(3):
            self.add_reserved()

    def finish_program(self):
        return_address = self.get_temp()
        self.program_block[1] = (1, self.get_code("SUB", self.static_base_pointer, "#4", return_address))
        self.program_block[2] = (2, self.get_code("assign", f"#{self.program_block_index}", f"@{return_address}"))
        self.program_block[3] = (
            3, self.get_code("jp", self.scanner.symbol_table[self.scanner.find_address("main", 0)]["address"]))

    def save_output(self):
        codes = ''
        if self.program_block:
            for line_number, code in self.program_block:
                codes += f'{line_number}\t{code}\n'
        else:
            codes = 'The code has not been generated.'

        with open('output.txt', 'w') as file:
            file.write(codes)

    def get_operand(self, operand):
        if isinstance(operand, int):
            address = operand
        elif "address" in operand:
            address = operand["address"]
        else:
            temp = self.get_temp()
            self.add_code(self.get_code("ADD", self.static_base_pointer, f"#{operand['offset']}", temp))
            address = f"@{temp}"
        return address

    def get_param_offset(self):
        offset = self.args_field_offset
        self.args_field_offset += 4
        return offset

    def add_op(self):
        try:
            op = self.semantic_stack.pop(-2)
            result = self.get_temp()
            operand2 = self.get_operand(self.semantic_stack.pop())
            operand1 = self.get_operand(self.semantic_stack.pop())
            self.add_code((op, operand1, operand2, result))
            self.semantic_stack.append(result)
        except IndexError:
            pass

    def mult(self):
        try:
            result = self.get_temp()
            operand2 = self.get_operand(self.semantic_stack.pop())
            operand1 = self.get_operand(self.semantic_stack.pop())
            self.add_code(("MULT", operand1, operand2, result))
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
            self.add_reserved()
        except IndexError:
            pass

    def break_save(self):
        self.break_stack[-1].append(self.program_block_index)
        self.add_reserved()

    def label(self):
        try:
            save_address = self.program_block_index
            self.semantic_stack.append(save_address)
        except IndexError:
            pass

    def relop(self):
        try:
            op = self.semantic_stack.pop(-2)
            result = self.get_temp()
            operand2 = self.get_operand(self.semantic_stack.pop())
            operand1 = self.get_operand(self.semantic_stack.pop())
            self.add_code((op, operand1, operand2, result))
            self.semantic_stack.append(result)
        except IndexError:
            pass

    def assign(self):
        try:
            operand = self.get_operand(self.semantic_stack.pop())
            result = self.get_operand(self.semantic_stack[-1])
            self.add_code(("ASSIGN", operand, result))
        except IndexError:
            pass

    def push_id(self, input_token):
        scope = self.scanner.scope_stack[-1]
        id_address = self.scanner.find_address(input_token, scope)
        self.semantic_stack.append(self.scanner.symbol_table[id_address])

    def push_const(self, input_token):
        try:
            constant_value = "#" + input_token
            address = self.get_static()
            self.add_code(self.get_code("ASSIGN", constant_value, address))
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
            condition = self.get_operand(self.semantic_stack.pop())
            self.semantic_stack.append(self.program_block_index)
            self.add_reserved()
            self.add_code(("jpf", condition, self.program_block_index), jump_address, True, False)
        except IndexError:
            pass

    def close(self):
        if self.semantic_stack:
            self.semantic_stack.pop()

    def return_value(self):
        result = self.get_temp()
        self.add_code(self.get_code("SUB", self.static_base_pointer, "#8", result))
        try:
            ret_val_address = self.get_operand(self.semantic_stack.pop())
        except IndexError:
            code = self.get_code("assign", "#0", f"@{result}")
            self.add_code(code)
        else:
            code = self.get_code("assign", ret_val_address, f"@{result}")
            self.add_code(code)

    def return_seq(self):
        return_address = self.get_temp()
        self.add_code(self.get_code("SUB", self.static_base_pointer, "#4", return_address))
        temp = self.get_temp()
        self.add_code(self.get_code("assign", f"@{return_address}", temp))
        self.add_code(self.get_code("jp", f"@{temp}"))

    def call_seq(self, backpatch=False):
        
        stack = self.semantic_stack if not backpatch else self.call_seq_stack

        if backpatch:
            callee = stack.pop()
            store_idx = self.program_block_index
            return_value = stack.pop()
            self.arg_counter[-1] = stack.pop()
            self.program_block_index = stack.pop()
        else:
            callee = stack[-(self.arg_counter[-1] + 1)]

        caller = self.scanner.symbol_table[self.scanner.scope_stack[-1] - 1]

        if callee["lexeme"] == "output":
            arg = stack.pop()
            stack.pop()
            arg_address = self.get_operand(arg)
            self.add_code(self.get_code("assign", arg_address, self.static_base_pointer + 4))
            self.add_code(self.get_code("PRINT", self.static_base_pointer + 4))
            self.arg_counter[-1] = 0
            self.semantic_stack.append("void")
            return

        if not backpatch:
            return_value = self.get_temp()

        if "frame_size" in caller:
            top_sp = self.static_base_pointer
            frame_size = caller["frame_size"]
            t_new_top_sp = self.get_temp()
            self.add_code(self.get_code("ADD", top_sp, f"#{frame_size}", t_new_top_sp), insert=backpatch)
            self.add_code(self.get_code("assign", top_sp, f"@{t_new_top_sp}"), insert=backpatch)
            t_args = self.get_temp()
            self.add_code(self.get_code("ADD", t_new_top_sp, "#4", t_args), insert=backpatch)
            n_args = callee["no.Args"]
            args = stack[-n_args:]
            for i in range(n_args):
                stack.pop()
                arg = args[i]
                if isinstance(arg, int):
                    arg_address = arg
                elif "address" in arg:
                    arg_address = arg["address"]
                else:
                    temp = self.get_temp()
                    self.add_code(
                        self.get_code("ADD", self.static_base_pointer, f"#{arg['offset']}", temp),
                        insert=backpatch)
                    arg_address = f"@{temp}"
                # if callee["params"][-i - 1] == "array":
                #     arg_address = f"#{arg}"  # pass by reference
                self.add_code(self.get_code("assign", arg_address, f"@{t_args}"), insert=backpatch)
                self.add_code(self.get_code("ADD", t_args, "#4", t_args), insert=backpatch)
            fun_addr = stack.pop()["address"]
            t_ret_addr = self.get_temp()
            t_ret_val_callee = self.get_temp()
            self.add_code(self.get_code("SUB", t_new_top_sp, "#4", t_ret_addr), insert=backpatch)
            self.add_code(self.get_code("SUB", t_new_top_sp, "#8", t_ret_val_callee), insert=backpatch)
            # increment stack frame pointer by frame size TODO: update stack pointer via access link and static offset
            # self._add_three_addr_code(self._get_add_code(top_sp, f"#{frame_size}", top_sp), insert=backpatch)
            self.add_code(self.get_code("assign", t_new_top_sp, top_sp), insert=backpatch)
            # self._add_three_addr_code(self._get_three_addr_code("print", top_sp), insert=backpatch)

            self.add_code(
                self.get_code("assign", f"#{self.program_block_index + 2}", f"@{t_ret_addr}"),
                insert=backpatch)
            self.add_code(self.get_code("jp", fun_addr), insert=backpatch)
            self.add_code(self.get_code("assign", f"@{t_ret_val_callee}", return_value),
                          insert=backpatch)
            self.add_code(self.get_code("SUB", top_sp, f"#{frame_size}", top_sp), insert=backpatch)
            # self._add_three_addr_code(self._get_three_addr_code("print", top_sp), insert=backpatch)
        else:
            print(stack)
            callee = stack[-(self.arg_counter[-1] + 1)]
            self.call_seq_stack += self.semantic_stack[-(self.arg_counter[-1] + 1):]
            num_offset_vars = 0
            for i in range(1, callee["no.Args"] + 1):
                arg = self.semantic_stack[-i]
                if not isinstance(arg, int) and "offset" in arg:
                    num_offset_vars += 1
            self.semantic_stack = self.semantic_stack[:-(self.arg_counter[-1] + 1)]
            self.call_seq_stack.append(self.program_block_index)
            self.call_seq_stack.append(self.arg_counter[-1])
            self.call_seq_stack.append(return_value)
            self.call_seq_stack.append(callee)

            for _ in range(10 + callee["no.Args"] * 2 + num_offset_vars):
                self.add_reserved()

        if backpatch:
            self.program_block_index = store_idx
        else:
            if callee["type"] == "void":
                self.semantic_stack.append("void")
            else:
                self.semantic_stack.append(return_value)

    def sf_size(self):
        scope_stack, symbol_table = self.scanner.scope_stack, self.scanner.symbol_table
        fun_row = symbol_table[scope_stack[-1] - 1]

        fun_row["args_size"] = 0
        fun_row["locals_size"] = 0
        fun_row["arrays_size"] = 0
        fun_row["temps_size"] = self.stack.pop()
        if not self.stack:
            self.stack = [0]
        for i in range(scope_stack[-1], len(symbol_table)):
            if symbol_table[i]["fnuc/var"] == "local_var":
                if "type" in symbol_table[i].keys() and symbol_table[i]["type"] == "array":
                    fun_row["arrays_size"] += 4 * symbol_table[i]["no.Args"]
                fun_row["locals_size"] += 4
            else:
                fun_row["args_size"] += 4
        fun_row["frame_size"] = fun_row["args_size"] + 12
        # If arrays are to be implemented use this
        # fun_row["frame_size"] = fun_row["args_size"] + fun_row["locals_size"] \
        #                       + fun_row["arrays_size"] + fun_row["temps_size"] + 12
        fun_row["args_offset"] = 4
        fun_row["locals_offset"] = fun_row["args_offset"] + fun_row["args_size"]
        fun_row["arrays_offset"] = fun_row["locals_offset"] + fun_row["locals_size"]
        fun_row["temps_offset"] = fun_row["arrays_offset"] + fun_row["arrays_size"]

        while self.call_seq_stack:
            self.call_seq(backpatch=True)

        self.reset()

    def call_call(self):
        arg = self.semantic_stack[-2]
        for i in range(arg['no.Args'] + 1):
            self.semantic_stack.append(arg['address'] + i * 4)
        print(self.semantic_stack)

    def until(self):
        condition = self.semantic_stack.pop()
        jp_address = self.semantic_stack.pop()
        self.add_reserved()
        self.add_code(("jpf", condition, self.program_block_index), jp_address, True, False)
        self.semantic_stack.append(self.program_block_index)
        pass
