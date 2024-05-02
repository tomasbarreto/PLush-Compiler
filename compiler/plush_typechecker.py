from context import Context
from plush_ast import *

class TypeError(Exception):
    pass

def verify(node, ctx: Context):
    if isinstance(node, Program):
        verify(node.statements, ctx)
    elif isinstance(node, InstructionList):
        # Verify each instruction in the program
        for instruction in node.instructions:
            verify(instruction, ctx)
    elif isinstance(node, VariableDeclaration):
        # Check if the variable is already declared
        if ctx.has_var_in_current_scope(node.name):
            raise TypeError(f"Variable {node.name} already declared!")
        # Verify the value of the variable
        expr_type = verify(node.value, ctx)

        node_type = node.type

        if isinstance(expr_type, str) and expr_type[0] == '[':
            if expr_type != node.type:
                raise TypeError(f"Incompatible types: {node.type} and {expr_type}")
        elif expr_type != node_type:
            raise TypeError(f"Incompatible types: {node_type} and {expr_type}")
        
        # Save the variable in the context
        ctx.set_type(node.name, node.type)
    elif isinstance(node, VariableAssignment):
        # Check if the variable is not declared
        if not ctx.has_var(node.name):
            raise TypeError(f"Variable {node.name} not declared!")
        # Verify the value of the variable
        expr_type = verify(node.value, ctx)

        var_type = ctx.get_type(node.name)

        if expr_type != var_type:
            raise TypeError(f"Incompatible types: {var_type} and {expr_type}")
    elif isinstance(node, Expression):
        expr_type = verify(node.expr, ctx)
        node.type = expr_type
        
        return expr_type
    elif isinstance(node, (
        Or,
        And
    )):
        # Verify the left and right expressions
        right = verify(node.right, ctx)
        left = verify(node.left, ctx)

        if right != "boolean":
            raise TypeError(f"Incompatible type: {right}")

        if left != "boolean":
            raise TypeError(f"Incompatible type: {left}")

        if right != left:
            raise TypeError(f"Incompatible types: {right} and {left}")
        
        return right
    elif isinstance(node, (
        Equality,
        Compare
    )):
        # Verify the left and right expressions
        right = verify(node.right, ctx)
        left = verify(node.left, ctx)

        if right != left:
            raise TypeError(f"Tipos incompatíveis: {right} e {left}")
        
        return "boolean"
    elif isinstance(node, (
        Add,
        Sub,
        Mult
    )):
        # Verify the left and right expressions
        right = verify(node.right, ctx)
        left = verify(node.left, ctx)

        if right not in ("int", "float", Expression):
            raise TypeError(f"Incompatible type: {right}")
        
        if left not in ("int", "float", Expression):
            raise TypeError(f"Incompatible type: {left}")

        if right != left:
            raise TypeError(f"Incompatible types: {right} and {left}")
        
        return right
    elif isinstance(node, Unary):
        return verify(node.expr, ctx)
    elif isinstance(node, (
        Int,
        Float,
        String,
        Char,
        Boolean
    )):
        return type_to_str(type(node))
    elif isinstance(node, VariableAccess):
        if not ctx.has_var(node.name):
            raise TypeError(f"Variable {node.name} not declared!")
        
        return ctx.get_type(node.name)
    elif isinstance(node, IfStatement):
        expr_type = verify(node.condition, ctx)

        if expr_type != "boolean":
            raise TypeError(f"If conditions must have type booean! Not type {expr_type}!")

        verify(node.then_block, ctx)
        if node.else_block.instructions:
            verify(node.else_block, ctx)
    elif isinstance(node, ThenBlock):
        for instruction in node.instructions:
            verify(instruction, ctx)
    elif isinstance(node, ElseBlock):
        for instruction in node.instructions:
            verify(instruction, ctx)
    elif isinstance(node, WhileStatement):
        expr_type = verify(node.condition, ctx)

        if expr_type != "boolean":
            raise TypeError(f"If conditions must have type booean! Not type {expr_type}!")

        for instruction in node.code_block:
            verify(instruction, ctx)
    elif isinstance(node, FunctionDeclaration):
        if ctx.has_function(node.name):
            raise TypeError(f"Function {node.name} already declared!")
        
        if ctx.has_function_def(node.name):
            nr_args = ctx.get_function_def_nr_args(node.name)
            index_param = 0

            if not node.parameters and nr_args > 0:
                raise TypeError(f"Function {node.name} expects more arguments!")
            
            if len(node.parameters.parameters) > nr_args:
                raise TypeError(f"Function {node.name} expects less arguments!")

            if node.parameters:
                if node.parameters.parameters and nr_args == 0:
                    raise TypeError(f"Function {node.name} does not expect arguments!")

                # Check if the function declaration matches the function definition
                for param in node.parameters.parameters:
                    if ctx.get_type_function_def_param(node.name, index_param) != param.type:
                        raise TypeError(f"Incompatible types in function declaration {node.name}!")
                    index_param += 1
                    nr_args -= 1

            if nr_args != 0:
                raise TypeError(f"Function {node.name} expects more arguments!")
            
        ctx.enter_function_scope()
        ctx.set_type_function(node.name, node.type)  

        if node.parameters:
            for param in node.parameters.parameters:
                ctx.set_type_function(param.name, param.type)

        # typecheck the actual function declaration

        ctx.enter_scope()

        ctx.set_type(node.name, node.type)
        
        if node.parameters:
            for param in node.parameters.parameters:
                ctx.set_type(param.name, param.type)

        for instruction in node.instructions.instructions:
            verify(instruction, ctx)

        ctx.exit_scope()

    elif isinstance(node, FunctionDefinition):
        if ctx.has_function_def(node.name):
            raise TypeError(f"Function {node.name} already defined!")
        
        if ctx.has_function(node.name):
            raise TypeError(f"Cannot define a function that was already declared - function {node.name}")
        
        ctx.enter_function_def_scope()
        ctx.set_type_function_def(node.name, node.type)      
        
        if node.parameters:
            for param in node.parameters.parameters:
                ctx.set_type_function_def(param.name, param.type)
    elif isinstance(node, FunctionCall):
        if not ctx.has_function_def(node.name) and not ctx.has_function(node.name):
            raise TypeError(f"Function {node.name} not defined nor declared!")
        
        if ctx.has_function_def(node.name):
            if ctx.get_type_function_def(node.name) == 'void':
                raise TypeError(f"Function {node.name} returns void!")
            
            nr_args = ctx.get_function_def_nr_args(node.name)
            index_arg = 0

            if node.arguments.arguments and nr_args == 0:
                raise TypeError(f"Function {node.name} does not expect arguments!")

            if len(node.arguments.arguments) > nr_args:
                raise TypeError(f"Function {node.name} expects less arguments!")
            
            for argument in node.arguments.arguments:
                param_type = ctx.get_type_function_def_param(node.name, index_arg)

                if param_type != verify(argument.value.expr, ctx):
                    raise TypeError(f"Incompatible types in function call {node.name}!")
                index_arg += 1
                nr_args -= 1
            
            if nr_args != 0:
                raise TypeError(f"Function {node.name} expects more arguments!")

            function_type = ctx.get_type_function_def(node.name)

        if ctx.has_function(node.name):
            nr_args = ctx.get_function_nr_args(node.name)
            index_arg = 0

            if node.arguments.arguments and nr_args == 0:
                raise TypeError(f"Function {node.name} does not expect arguments!")

            if len(node.arguments.arguments) > nr_args:
                raise TypeError(f"Function {node.name} expects less arguments!")

            for argument in node.arguments.arguments:
                param_type = ctx.get_type_function_param(node.name, index_arg)

                if param_type != verify(argument.value.expr, ctx):
                    raise TypeError(f"Incompatible types in function call {node.name}!")
                index_arg += 1
                nr_args -= 1
            
            if nr_args != 0:
                raise TypeError(f"Function {node.name} expects more arguments!")
        
            function_type = ctx.get_type_function(node.name)

        return function_type
    
    elif isinstance(node, ProcedureCall):
        if not ctx.has_function_def(node.name) and not ctx.has_function(node.name):
            raise TypeError(f"Procedure {node.name} not defined nor declared!")

        if ctx.has_function_def(node.name):

            if ctx.get_type_function_def(node.name) != 'void':
                raise TypeError(f"Procedure {node.name} must be of type void!")

            nr_args = ctx.get_function_def_nr_args(node.name)
            index_param = 0

            if node.arguments.arguments and nr_args == 0:
                raise TypeError(f"Procedure {node.name} does not expect arguments!")
            
            if len(node.arguments.arguments) > nr_args:
                raise TypeError(f"Procedure {node.name} expects less arguments!")
            
            for argument in node.arguments.arguments:
                if ctx.get_type_function_def_param(node.name, index_param) != verify(argument.value.expr, ctx):
                    raise TypeError(f"Incompatible types in procedure call {node.name}!")
                index_param += 1
                nr_args -= 1

            if nr_args != 0:
                raise TypeError(f"Procedure {node.name} expects more arguments!")
        
        if ctx.has_function(node.name):
            nr_args = ctx.get_function_nr_args(node.name)
            index_param = 0

            if node.arguments.arguments and nr_args == 0:
                raise TypeError(f"Function {node.name} does not expect arguments!")
            
            if len(node.arguments.arguments) > nr_args:
                raise TypeError(f"Function {node.name} expects less arguments!")

            for argument in node.arguments.arguments:
                if ctx.get_type_function_param(node.name, index_param) != verify(argument.value.expr, ctx):
                    raise TypeError(f"Incompatible types in function call {node.name}!")
                index_param += 1
                nr_args -= 1
            
            if nr_args != 0:
                raise TypeError(f"Function {node.name} expects more arguments!")
            
    elif isinstance(node, ArrayAccess):
        if isinstance(node.identifier, VariableAccess):
            if not ctx.has_var(node.identifier.name):
                raise TypeError(f"Variable {node.identifier.name} not declared!")
            idenfier_type = ctx.get_type(node.identifier.name)
        elif isinstance(node.identifier, FunctionCall):
            verify(node.identifier, ctx)
            idenfier_type = ctx.get_type_function(node.identifier.name)

        if idenfier_type[0] != '[':
            raise TypeError(f"Variable {node.identifier.name} is not an array!")
        
        rec_l_paren_counter = 0
        index = 0

        while idenfier_type[index] == '[':
            rec_l_paren_counter += 1
            index += 1

        number_input_indexes = len(node.indexes.indexes)

        if number_input_indexes > rec_l_paren_counter:
            raise TypeError(f"Too many indexes in array access {node.identifier.name}!")
        
        for index in node.indexes.indexes:
            if verify(index.value, ctx) != "int":
                raise TypeError(f"Array indexes must be of type int!")
        
        return_type = idenfier_type

        while number_input_indexes > 0:
            return_type = return_type[1:-1]
            number_input_indexes -= 1
        
        return return_type
    elif isinstance(node, ArrayVariableAssigment):
        array_variable_type = verify(node.left, ctx)
        value_type = verify(node.right, ctx)

        if array_variable_type != value_type:
            raise TypeError(f"Incompatible types: {array_variable_type} and {value_type}")
    elif isinstance(node, Array):
        result = list_to_string(covert_types_to_string(getArrayType(node, ctx)))

        processed_result = delete_duplicates(result)

        return processed_result
    
    return node


def getArrayType(array, ctx):
    seen_elements = set()

    def deleteRepeatedTypes(array):
        if isinstance(array, Array):
            seen_elements.clear()
            for i in range(len(array.content)):
                array.content[i] = deleteRepeatedTypes(array.content[i])
        else:
            type = verify(array, ctx)
            if type in seen_elements:
                return None
            seen_elements.add(type)
            return type

        return remove_duplicates(remove_nones(array.content))
    
    return deleteRepeatedTypes(array)

def remove_nones(lst):
    if isinstance(lst, list):
        return [remove_nones(item) for item in lst if item is not None]
    else:
        return lst
    
def remove_duplicates(lst):
    seen = set()
    result = []

    for item in lst:
        if isinstance(item, list):
            items = remove_duplicates(item)
            items = tuple(items)
        else:
            items = item

        if items not in seen:
            result.append(item)
            seen.add(items)

    return result

def type_to_str(node):
    if node == Int:
        return 'int'
    elif node == Float:
        return 'float'
    elif node == String:
        return 'string'
    elif node == Char:
        return 'char'
    elif node == Boolean:
        return 'boolean'
    return node

def list_to_string(lst):
    def convert_to_string(item):
        if isinstance(item, list):
            inner_strings = [convert_to_string(sub_item) for sub_item in item]
            return '[' + ','.join(inner_strings) + ']'
        else:
            return str(item)

    return convert_to_string(lst)
    
def covert_types_to_string(lst):
    def convert_to_type_string(item):
        if isinstance(item, list):
            inner_types = [convert_to_type_string(sub_item) for sub_item in item]
            return inner_types
        else:
            return type_to_str(item)

    return convert_to_type_string(lst)

def delete_duplicates(lst):
    content = lst[1:-1].split(',')

    seen = set()
    result = []

    for item in content:
        if item not in seen:
            result.append(item)
            seen.add(item)
    
    return '[' + ', '.join(result) + ']'