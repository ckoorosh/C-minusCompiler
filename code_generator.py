class CodeGenerator:
    def __init__(self, scanner):
        self.scanner = scanner
        self.semantic_stack = []
        self.break_stack = []
        self.program_block = []
        self.stack = [0]
        self.program_block_index = 0
        self.static_base_pointer = 100
        self.base_pointer = 500
        self.stack_base_pointer = 1000
        self.static_offset = 0
        self.offset = 0

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

    def add_placeholder(self):
        self.add_code('Placeholder')

    def init_program(self):
        code = self.get_code("assign", f'#{self.stack_base_pointer}', self.static_base_pointer)
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

    def get_operand(self, operand):
        if isinstance(operand, int):
            address = operand
        elif "address" in operand:
            address = operand["address"]
        else:
            temp = self.get_temp()
            self.add_code(self.get_code(self.stack_base_pointer, f"#{operand['offset']}", temp))
            address = f"@{temp}"
        return address

    def add_op(self):
        try:
            result = self.get_temp()
            operand1 = self.get_operand(self.semantic_stack.pop())
            op = self.semantic_stack.pop()
            operand2 = self.get_operand(self.semantic_stack.pop())
            self.add_code((op, operand1, operand2, result))
            self.semantic_stack.append(result)
        except IndexError:
            pass

    def mult(self):
        try:
            result = self.get_temp()
            operand1 = self.get_operand(self.semantic_stack.pop())
            operand2 = self.get_operand(self.semantic_stack.pop())
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
            self.add_code(("ASSIGN", operand, result,))
        except IndexError:
            pass

    def find_addr(self, lexeme):
        for i in range(len(self.scanner.symbol_table)):
            # print(self.scanner.symbol_table[i], "baghali")
            if self.scanner.symbol_table[i]["lexeme"] == lexeme:
                return i

        # TODO error
        print("Errrrrrrrrrrrrrrror")

    def push_id(self, input_token):
        try:
            # print(self.scanner.symbol_table, "chaghaliiiii")
            id_address = self.find_addr(input_token)  # TODO: find address of input using symbol table
            self.semantic_stack.append(id_address)
        except IndexError:
            pass

    def push_const(self, input_token):
        try:
            constant_value = "#" + input_token
            address = self.get_static()
            self.add_code(self.get_code("ASSIGN", constant_value, address))
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
            # print(self.semantic_stack)
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

    def return_seq(self):
        return_address = self.get_temp()
        self.add_code(self.get_code("SUB", self.static_base_pointer, "#4", return_address))
        temp = self.get_temp()
        self.add_code(self.get_code("assign", f"@{return_address}", temp))
        self.add_code(self.get_code("jp", f"@{temp}"))

    def call_seq(self, backpatch=False):
        pass

    #     ''' expects semantic stack to contain:
    #         ----------------------------------
    #         ss(top)         = arg_n addr
    #         ...
    #         ss(top - n + 2) = arg_2 addr
    #         ss(top - n + 1) = arg_1 addr
    #         ss(top - n)     = fun   addr
    #     '''
    #     stack = self.semantic_stack if not backpatch else self.call_seq_stack
    #
    #     if backpatch:
    #         callee = stack.pop()
    #         store_idx = MemoryManager.pb_index
    #         t_ret_val = stack.pop()
    #         self.arg_counter[-1] = stack.pop()
    #         self.program_block_index = stack.pop()
    #     else:
    #         callee = stack[-(self.arg_counter[-1] + 1)]
    #
    #     caller = SymbolTableManager.get_enclosing_fun()
    #
    #     if callee["lexim"] == "output":
    #         arg = stack.pop()
    #         stack.pop()  # pop output row off the stack
    #         arg_addr = self._resolve_addr(arg)
    #         self._add_three_addr_code(self._get_three_addr_code("assign", arg_addr, self.print_addr))
    #         self._add_three_addr_code(self._get_three_addr_code("PRINT", self.print_addr))
    #         self.arg_counter[-1] = 0
    #         self.semantic_stack.append("void")
    #         return
    #
    #     if not backpatch:
    #         t_ret_val = self.get_temp()
    #
    #     if "frame_size" in caller:
    #         # current top_sp and access link pointer
    #         top_sp = self.stack_frame_ptr_addr
    #         frame_size = caller["frame_size"]
    #         t_new_top_sp = MemoryManager.get_temp()
    #         self._add_three_addr_code(self._get_add_code(top_sp, f"#{frame_size}", t_new_top_sp), insert=backpatch)
    #         # assign access link address to new stack frame
    #         self._add_three_addr_code(self._get_three_addr_code("assign", top_sp, f"@{t_new_top_sp}"), insert=backpatch)
    #         t_args = MemoryManager.get_temp()
    #         self._add_three_addr_code(self._get_add_code(t_new_top_sp, "#4", t_args), insert=backpatch)
    #         n_args = callee["arity"]
    #         args = stack[-n_args:]
    #         for i in range(n_args):
    #             stack.pop()
    #             arg = args[i]
    #             if isinstance(arg, int):
    #                 arg_addr = arg
    #             elif "address" in arg:
    #                 arg_addr = arg["address"]  # static address
    #             else:
    #                 # need to calculate dynamic address
    #                 t_arg_addr = MemoryManager.get_temp()
    #                 self._add_three_addr_code(
    #                     self._get_add_code(self.stack_frame_ptr_addr, f"#{arg['offset']}", t_arg_addr),
    #                     insert=backpatch)
    #                 arg_addr = f"@{t_arg_addr}"
    #             if callee["params"][-i - 1] == "array":
    #                 arg_addr = f"#{arg}"  # pass by reference
    #             self._add_three_addr_code(self._get_three_addr_code("assign", arg_addr, f"@{t_args}"), insert=backpatch)
    #             self._add_three_addr_code(self._get_add_code(t_args, "#4", t_args), insert=backpatch)
    #         fun_addr = stack.pop()["address"]
    #         # put pointers for return address and return value in temp variables
    #         t_ret_addr = MemoryManager.get_temp()
    #         t_ret_val_callee = MemoryManager.get_temp()
    #         self._add_three_addr_code(self._get_sub_code(t_new_top_sp, "#4", t_ret_addr), insert=backpatch)
    #         self._add_three_addr_code(self._get_sub_code(t_new_top_sp, "#8", t_ret_val_callee), insert=backpatch)
    #         # increment stack frame pointer by frame size TODO: update stack pointer via access link and static offset
    #         # self._add_three_addr_code(self._get_add_code(top_sp, f"#{frame_size}", top_sp), insert=backpatch)
    #         self._add_three_addr_code(self._get_three_addr_code("assign", t_new_top_sp, top_sp), insert=backpatch)
    #         # self._add_three_addr_code(self._get_three_addr_code("print", top_sp), insert=backpatch)
    #         # assign value for return address in callee stack frame
    #         self._add_three_addr_code(
    #             self._get_three_addr_code("assign", f"#{MemoryManager.pb_index + 2}", f"@{t_ret_addr}"),
    #             insert=backpatch)
    #         # jump to function address
    #         self._add_three_addr_code(self._get_three_addr_code("jp", fun_addr), insert=backpatch)
    #         # fetch the return value to a temporary and push it to the stack
    #         self._add_three_addr_code(self._get_three_addr_code("assign", f"@{t_ret_val_callee}", t_ret_val),
    #                                   insert=backpatch)
    #         # decrement stack frame pointer by frame size
    #         self._add_three_addr_code(self._get_sub_code(top_sp, f"#{frame_size}", top_sp), insert=backpatch)
    #         # self._add_three_addr_code(self._get_three_addr_code("print", top_sp), insert=backpatch)
    #     else:  # in recursive calls we need to backpatch
    #         callee = stack[-(self.arg_counter[-1] + 1)]
    #         self.call_seq_stack += self.semantic_stack[-(self.arg_counter[-1] + 1):]
    #         num_offset_vars = 0
    #         for i in range(1, callee["arity"] + 1):
    #             arg = self.semantic_stack[-i]
    #             if not isinstance(arg, int) and "offset" in arg:
    #                 num_offset_vars += 1
    #         self.semantic_stack = self.semantic_stack[:-(self.arg_counter[-1] + 1)]
    #         self.call_seq_stack.append(MemoryManager.pb_index)
    #         self.call_seq_stack.append(self.arg_counter[-1])
    #         self.call_seq_stack.append(t_ret_val)
    #         self.call_seq_stack.append(callee)
    #
    #         for _ in range(10 + callee["arity"] * 2 + num_offset_vars):  # reserve space for call seq
    #             self._add_placeholder()
    #
    #     if backpatch:
    #         self.program_block_index = store_idx
    #     else:
    #         if callee["type"] == "void":
    #             self.semantic_stack.append("void")
    #         else:
    #             self.semantic_stack.append(t_ret_val)

    def sf_size(self):
        # TODO: need some info
        pass
        # scope_stack, symbol_table = self._get_context_info()
        # fun_row = SymbolTableManager.get_enclosing_fun()
        # fun_row["args_size"] = 0
        # fun_row["locals_size"] = 0
        # fun_row["arrays_size"] = 0
        # fun_row["temps_size"] = SymbolTableManager.temp_stack.pop()
        # if not SymbolTableManager.temp_stack:
        #     SymbolTableManager.temp_stack = [0]
        # for i in range(scope_stack[-1], len(symbol_table)):
        #     if symbol_table[i]["role"] == "local_var":
        #         if symbol_table[i]["type"] == "array":
        #             fun_row["arrays_size"] += 4 * symbol_table[i]["arity"]
        #         fun_row["locals_size"] += 4
        #     else:
        #         fun_row["args_size"] += 4
        # fun_row["frame_size"] = fun_row["args_size"] + 12
        # # If arrays are to be implemented use this
        # # fun_row["frame_size"] = fun_row["args_size"] + fun_row["locals_size"] \
        # #                       + fun_row["arrays_size"] + fun_row["temps_size"] + 12
        # fun_row["args_offset"] = 4
        # fun_row["locals_offset"] = fun_row["args_offset"] + fun_row["args_size"]
        # fun_row["arrays_offset"] = fun_row["locals_offset"] + fun_row["locals_size"]
        # fun_row["temps_offset"] = fun_row["arrays_offset"] + fun_row["arrays_size"]
        #
        # while self.call_seq_stack:
        #     self.call_seq_caller_routine(input_token, backpatch=True)
        #
        # MemoryManager.reset()

    def until(self):
        condition = self.semantic_stack.pop()
        jp_address = self.semantic_stack.pop()
        self.add_placeholder()
        self.add_code(("jpf", condition, self.program_block_index), jp_address, True, False)
        self.semantic_stack.append(self.program_block_index)
        pass
