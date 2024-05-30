class Context(object):
    def __init__(self):
        self.stack = [{}]
        self.function_stack = []
        self.function_def_stack = []
        self.constant_stack = [{}]
        self.liquid_stack = [{}]
        self.function_sign_stack = [{}]
    
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
    
    def get_name_function_param(self, function_name, param_position):
        for scope in self.function_stack:
            first_key = next(iter(scope))
            if function_name == first_key:
                wanted_scope = scope
                return list(wanted_scope.items())[param_position + 1][0]
        
    def get_type_function(self, function_name):
        for scope in self.function_stack:
            first_key = next(iter(scope))
            if function_name == first_key:
                wanted_scope = scope
                return wanted_scope[function_name]
        
    def get_function_nr_args(self, function_name):
        for scope in self.function_stack:
            first_key = next(iter(scope))
            if function_name == first_key:
                wanted_scope = scope
                return len(wanted_scope) - 1
        
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
    
    def get_type_function_def(self, function_name):
        for scope in self.function_def_stack:
            first_key = next(iter(scope))
            if function_name == first_key:
                wanted_scope = scope
                return wanted_scope[function_name]
        
    def get_type_function_def_param(self, function_name, param_position):
        for scope in self.function_def_stack:
            first_key = next(iter(scope))
            if function_name == first_key:
                wanted_scope = scope
                return list(wanted_scope.items())[param_position + 1][1]
        
    def get_function_def_nr_args(self, function_name):
        for scope in self.function_def_stack:
            first_key = next(iter(scope))
            if function_name == first_key:
                wanted_scope = scope
                return len(wanted_scope) - 1
            
    # constant stack
    def get_constant_type(self, name):
        for scope in self.constant_stack:
            if name in scope:
                return scope[name]
        raise TypeError(f"Variavel {name} nao esta no contexto")
    
    def set_constant_type(self, name, value):
        scope = self.constant_stack[0]
        scope[name] = value

    def has_const(self, name):
        for scope in self.constant_stack:
            if name in scope:
                return True
        return False

    def has_const_in_current_scope(self, name):
        return name in self.constant_stack[0]

    def enter_const_scope(self):
        self.constant_stack.insert(0, {})

    def exit_const_scope(self):
        self.constant_stack.pop(0)

    # liquid stack
    def get_liquid_type(self, name):
        for scope in self.liquid_stack:
            if name in scope:
                return scope[name]
        raise TypeError(f"Variavel {name} nao esta no contexto")

    def set_liquid_type(self, name, value):
        if name in self.liquid_stack[0]:
            target_scope = self.liquid_stack[0][name]
            target_scope.append(value)
        else:
            scope = self.liquid_stack[0]
            scope[name] = [value]

    def has_liquid(self, name):
        for scope in self.liquid_stack:
            if name in scope:
                return True
        return False
    
    def has_liquid_in_current_scope(self, name):
        return name in self.liquid_stack[0]
    
    def enter_liquid_scope(self):
        self.liquid_stack.insert(0, {})

    def exit_liquid_scope(self):
        self.liquid_stack.pop(0)

    def reset_liquid_type_clauses(self, name):
        for scope in self.liquid_stack:
            if name in scope:
                scope[name] = [scope[name][0]]

    # function sign stack
    def set_function_sign(self, name, value):
        scope = self.function_sign_stack[0]
        scope[name] = value
    
    def get_function_sign(self, name):
        for scope in self.function_sign_stack:
            if name in scope:
                return scope[name]
        raise TypeError(f"Variavel {name} nao esta no contexto")
    
    def has_function_sign(self, name):
        for scope in self.function_sign_stack:
            if name in scope:
                return True
        return False
    
    def enter_function_sign_scope(self):
        self.function_sign_stack.insert(0, {})

    def exit_function_sign_scope(self):
        self.function_sign_stack.pop(0)

    def get_type_function_sign_param(self, function_name, param_position):
        for scope in self.function_sign_stack:
            first_key = next(iter(scope))
            if function_name == first_key:
                wanted_scope = scope
                return list(wanted_scope.items())[param_position + 1][1]
            
    def get_name_function_sign_param(self, function_name, param_position):
        for scope in self.function_stack:
            first_key = next(iter(scope))
            if function_name == first_key:
                wanted_scope = scope
                return list(wanted_scope.items())[param_position + 1][0]