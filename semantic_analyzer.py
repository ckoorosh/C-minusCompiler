import os

script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class SemanticAnalyzer:

    def __init__(self, code_generator, scanner):
        self.code_generator = code_generator
        self.scanner = scanner
        self.semantic_stacks = {
            "main_check": [],
            "type_assign": [],
            "type_check": [],
            "fun_check": [],
        }

        # flags
        self.main_found = False
        self.main_not_last = False

        # counters
        self.arity_counter = 0
        self.while_counter = 0
        self.switch_counter = 0

        # lists
        self.fun_param_list = []
        self.fun_arg_list = []
        self._semantic_errors = []

        self.semantic_error_file = os.path.join(script_dir, "errors", "semantic_errors.txt")

    def in_scope(self):
        self.scanner.scope_stack.append(len(self.scanner.symbol_table))

    def out_scope(self):
        scope_start = self.scanner.scope_stack.pop()
        self.scanner.symbol_table = self.scanner.symbol_table[:scope_start]

    @property
    def scope(self):
        return len(self.scanner.scope_stack) - 1

    @property
    def semantic_errors(self):
        semantic_errors = []
        if self._semantic_errors:
            for lineno, error in self._semantic_errors:
                semantic_errors.append(f"#{lineno} : Semantic Error! {error}\n")
        else:
            semantic_errors.append("The input program is semantically correct.\n")
        return "".join(semantic_errors)

    def _get_lexim(self, token):
        if token[0] == "ID":
            return self.scanner.symbol_table[token[1]]['lexeme']
        else:
            return token[1]

    def save_semantic_errors(self):
        with open(self.semantic_error_file, "w") as f:
            f.write(self.semantic_errors)

    ''' semantic routines start here '''

    def save_main(self, input_token):
        self.semantic_stacks["main_check"].append(self._get_lexim(input_token))

    def pop_main(self):
        self.semantic_stacks["main_check"] = self.semantic_stacks["main_check"][:-2]

    def save_type(self, input_token):
        self.scanner.declaration_flag = True
        self.semantic_stacks["type_assign"].append(input_token[1])

    def assign_type(self, input_token):
        if input_token[0].name == "ID" and self.semantic_stacks["type_assign"]:
            symbol_idx = input_token[1]
            self.scanner.symbol_table[symbol_idx]["type"] = self.semantic_stacks["type_assign"].pop()
            self.semantic_stacks["type_assign"].append(symbol_idx)
            self.scanner.declaration_flag = False

    def assign_fun_role(self):
        print(self.semantic_stacks["type_assign"])
        if self.semantic_stacks["type_assign"]:
            symbol_idx = self.semantic_stacks["type_assign"][-1]
            self.scanner.symbol_table[symbol_idx]["fnuc/var"] = "function"
            self.scanner.symbol_table[symbol_idx]["address"] = self.code_generator.program_block_index

    def assign_param_role(self, input_token, line_number):
        self.assign_var_role(input_token, line_number, "param")

    def assign_var_role(self, input_token, line_number, role="local_var"):
        if self.semantic_stacks["type_assign"]:
            symbol_idx = self.semantic_stacks["type_assign"][-1]
            symbol_row = self.scanner.symbol_table[symbol_idx]
            symbol_row["fnuc/var"] = role
            if self.scope == 0:
                symbol_row["fnuc/var"] = "global_var"
            if symbol_row["type"] == "void":
                self.scanner.error_flag = True
                self._semantic_errors.append(
                    (line_number, "Illegal type of void for '{}'.".format(symbol_row["lexim"])))
                symbol_row.pop("type")  # void types are not considered to be defined
            if input_token[1] == "[":
                symbol_row["type"] = "array"

    def assign_length(self, input_token):
        if self.semantic_stacks["type_assign"]:
            symbol_idx = self.semantic_stacks["type_assign"].pop()
            symbol_row = self.scanner.symbol_table[symbol_idx]
            if input_token[0].name == "NUM":
                symbol_row["no.Args"] = int(input_token[1])
                if symbol_row["fnuc/var"] == "param":
                    symbol_row["offset"] = self.code_generator.get_param_offset()
                else:
                    symbol_row["address"] = self.code_generator.get_static(int(input_token[1]))
            else:
                self.scanner.symbol_table[symbol_idx]["no.Args"] = 1
                if symbol_row["fnuc/var"] == "param":
                    symbol_row["offset"] = self.code_generator.get_param_offset()
                else:
                    symbol_row["address"] = self.code_generator.get_static()

            if input_token[1] == "[" and self.fun_param_list:
                self.fun_param_list[-1] = "array"

    def save_param(self, input_token):
        self.fun_param_list.append(input_token[1])

    def push_arg_stack(self):
        self.scanner.arg_list_stack.append([])

    def pop_arg_stack(self):
        if len(self.scanner.arg_list_stack) > 1:
            self.scanner.arg_list_stack.pop()

    def save_arg(self, input_token):
        if input_token[0].name == "ID":
            self.scanner.arg_list_stack[-1].append(self.scanner.symbol_table[input_token[1]].get("type"))
        else:
            self.scanner.arg_list_stack[-1].append("int")

    def assign_fun_attrs(self):
        if self.semantic_stacks["type_assign"]:
            symbol_idx = self.semantic_stacks["type_assign"].pop()
            params = self.fun_param_list
            self.scanner.symbol_table[symbol_idx]["no.Args"] = len(params)
            # self.scanner.symbol_table[symbol_idx]["params"] = params
            self.fun_param_list = []
            self.scanner.temp_stack.append(0)  # init temp counter for this function

    def check_main(self):
        main_signature = ("void", "main", "void")
        try:
            top_three = tuple(self.semantic_stacks["main_check"][-3:])
            self.semantic_stacks["main_check"] = self.semantic_stacks["main_check"][:-3]

            if not self.main_found:
                self.main_found = (top_three == main_signature and self.scope == 1)
            # check whether main is the last global function definition 
            elif not self.main_not_last and self.main_found and self.scope == 1:
                self.main_not_last = True

        except IndexError:
            pass

    def check_declaration(self, input_token, line_number):
        if "type" not in self.scanner.symbol_table[input_token[1]]:
            lexim = self._get_lexim(input_token)
            self.scanner.error_flag = True
            self._semantic_errors.append((line_number, f"'{lexim}' is not defined."))

    def save_fun(self, input_token):
        if self.scanner.symbol_table[input_token[1]].get("fnuc/var") == "function":
            self.semantic_stacks["fun_check"].append(input_token[1])

    def check_args(self, line_number):
        if self.semantic_stacks["fun_check"]:
            fun_id = self.semantic_stacks["fun_check"].pop()
            lexim = self.scanner.symbol_table[fun_id]["lexeme"]
            args = self.scanner.arg_list_stack[-1]
            if args is not None:
                self.semantic_stacks["type_check"] = self.semantic_stacks["type_check"][:len(args)]
                if self.scanner.symbol_table[fun_id]["no.Args"] != len(args):
                    self.scanner.error_flag = True
                    self._semantic_errors.append((line_number, f"Mismatch in numbers of arguments of '{lexim}'."))
                else:
                    params = self.scanner.symbol_table[fun_id]["params"]
                    i = 1
                    for param, arg in zip(params, args):
                        if param != arg and arg is not None:
                            self.scanner.error_flag = True
                            self._semantic_errors.append((line_number,
                                                          f"Mismatch in type of argument {i} of '{lexim}'. Expected '{param}' but got '{arg}' instead."))
                        i += 1

    def check_break(self, line_number):
        if self.while_counter <= 0 and self.switch_counter <= 0:
            self.scanner.error_flag = True
            self._semantic_errors.append((line_number, "No 'while' or 'switch' found for 'break'."))

    def pop_switch(self):
        self.switch_counter -= 1

    def save_type_check(self, input_token):
        if input_token[0].name == "ID":
            operand_type = self.scanner.symbol_table[input_token[1]].get("type")
        else:
            operand_type = "int"
        self.semantic_stacks["type_check"].append(operand_type)

    def index_array(self):
        if self.semantic_stacks["type_check"]:
            self.semantic_stacks["type_check"][-1] = "int"

    def index_array_pop(self):
        if self.semantic_stacks["type_check"]:
            self.semantic_stacks["type_check"].pop()

    def type_check(self, line_number):
        try:
            operand_b_type = self.semantic_stacks["type_check"].pop()
            operand_a_type = self.semantic_stacks["type_check"].pop()
            if operand_b_type is not None and operand_a_type is not None:
                if operand_a_type == "array":
                    self.scanner.error_flag = True
                    self._semantic_errors.append((line_number,
                                                  f"Type mismatch in operands, Got '{operand_a_type}' instead of 'int'."))
                elif operand_a_type != operand_b_type:
                    self.scanner.error_flag = True
                    self._semantic_errors.append((line_number,
                                                  f"Type mismatch in operands, Got '{operand_b_type}' instead of '{operand_a_type}'."))
                else:
                    self.semantic_stacks["type_check"].append(operand_a_type)
        except IndexError:
            pass

    ''' semantic routines end here '''

    def semantic_check(self, action_symbol, input_token, line_number):
        try:
            self.semantic_checks[action_symbol](input_token, line_number)
        except Exception as e:
            print(f"{line_number} : Error in semantic routine {action_symbol}:", str(e))

    def eof_check(self, line_number):
        if not self.main_found or self.main_not_last:
            self.scanner.error_flag = True
            self._semantic_errors.append((line_number, "main function not found!"))
