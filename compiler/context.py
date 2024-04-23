class Context(object):
    def __init__(self):
        self.stack = [{}]
        self.function_stack = []
        self.function_def_stack = []
    
    def get_type(self, name):
        for scope in self.stack:
            if name in scope:
                return scope[name]
        raise TypeError(f"Variavel {name} nao esta no contexto")
    
    def set_type(self, name, value):
        scope = self.stack[0]
        scope[name] = value

    def has_var(self, name):
        for scope in self.stack:
            if name in scope:
                return True
        return False

    def has_var_in_current_scope(self, name):
        return name in self.stack[0]

    def enter_scope(self):
        self.stack.insert(0, {})

    def exit_scope(self):
        self.stack.pop(0)

    # functions for function stack
    def set_type_function(self, name, value):
        scope = self.function_stack[0]
        scope[name] = value

    def enter_function_scope(self):
        self.function_stack.insert(0, {})

    def has_function(self, function_name):
        for scope in self.function_stack:
            first_key = next(iter(scope))
            if function_name == first_key:
                return True
        return False
    
    def get_type_function_param(self, function_name, param_position):
        for scope in self.function_stack:
            first_key = next(iter(scope))
            if function_name == first_key:
                wanted_scope = scope
        
        return list(wanted_scope.items())[param_position + 1][1]
    
    # functions for function definition stack
    def set_type_function_def(self, name, value):
        scope = self.function_def_stack[0]
        scope[name] = value

    def enter_function_def_scope(self):
        self.function_def_stack.insert(0, {})

    def has_function_def(self, function_name):
        for scope in self.function_def_stack:
            first_key = next(iter(scope))
            if function_name == first_key:
                return True
        return False
    
    def get_type_function_def_param(self, function_name, param_position):
        for scope in self.function_def_stack:
            first_key = next(iter(scope))
            if function_name == first_key:
                wanted_scope = scope
        
        return list(wanted_scope.items())[param_position + 1][1]