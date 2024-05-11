from context import Context

class Emitter(object):
    def __init__(self):
        self.count = 0
        self.prt_count = 0
        self.if_count = 0
        self.if_end_count = 0
        self.while_count = 0
        self.while_end_count = 0
        self.add_count = 0
        self.sub_count = 0
        self.mult_count = 0
        self.function_count = 0
        self.call_count = 0
        self.cmp_count = 0
        self.add_count = 0
        self.condition_count = 0
        self.lines = []
        self.function_declarations = []
        self.context = Context()
        self.condition_context = Context()
        self.current_and_end = ""
        self.current_while_body = ""
        self.current_while_end = ""
        self.condition_context = []

    def get_count(self):
        self.count += 1
        return self.count
    
    def get_prt_count(self):
        self.prt_count += 1
        return self.prt_count
    
    def get_if_count(self):
        self.if_count += 1
        return self.if_count
    
    def get_if_end_count(self):
        self.if_end_count += 1
        return self.if_end_count
    
    def get_while_count(self):
        self.while_count += 1
        return self.while_count
    
    def get_while_end_count(self):
        self.while_end_count += 1
        return self.while_end_count
    
    def get_add_count(self):
        self.add_count += 1
        return self.add_count
    
    def get_sub_count(self):
        self.sub_count += 1
        return self.sub_count
    
    def get_mult_count(self):
        self.mult_count += 1
        return self.mult_count
    
    def get_function_count(self):
        self.function_count += 1
        return self.function_count
    
    def get_call_count(self):
        self.call_count += 1
        return self.call_count
    
    def get_cmp_count(self):
        self.cmp_count += 1
        return self.cmp_count
    
    def get_add_count(self):
        self.add_count += 1
        return self.add_count
    
    def get_condition_count(self):
        self.condition_count += 1
        return self.condition_count

    def get_id(self):
        id = self.get_count()
        return f"cas_{id}"
    
    def get_prt_id(self):
        id = self.get_prt_count()
        return f"prt_{id}"
    
    def get_if_id(self):
        id = self.get_if_count()
        return f"if_{id}"
    
    def get_if_end_id(self):
        id = self.get_if_end_count()
        return f"if_end_{id}"
    
    def get_while_id(self):
        id = self.get_while_count()
        return f"while_{id}"
    
    def get_while_end_id(self):
        id = self.get_while_end_count()
        return f"while_end_{id}"
    
    def get_add_id(self):
        id = self.get_add_count()
        return f"add_{id}"
    
    def get_sub_id(self):
        id = self.get_sub_count()
        return f"sub_{id}"
    
    def get_mult_id(self):
        id = self.get_mult_count()
        return f"mult_{id}"

    def get_function_id(self):
        id = self.get_function_count()
        return id
    
    def get_call_id(self):
        id = self.get_call_count()
        return f"call_{id}"
    
    def get_cmp_id(self):
        id = self.get_cmp_count()
        return f"cmp_{id}"
    
    def get_add_id(self):
        id = self.get_add_count()
        return f"add_{id}"
    
    def get_condition_id(self):
        id = self.get_condition_count()
        return f"cond_{id}"

    def __lshift__(self, v):
        self.lines.append(v)

    def get_code(self):
        return "\n".join(self.lines)
    
    def push_to_context(self, name, llvm_name):
        self.context.set_type(name, llvm_name)
    
    def get_from_context(self, name):
        return self.context.get_type(name)
    
    def push_to_function_declarations(self, declaration):
        self.function_declarations.append(declaration)

    def push_to_condition_context(self, name, llvm_name):
        self.condition_context.set_type(name, llvm_name)
    
    def get_from_condition_context(self, name):
        return self.condition_context.get_type(name)
    
    def enter_condition_scope(self):
        self.condition_context.enter_scope()
    
    def exit_condition_scope(self):
        self.condition_context.exit_scope()
