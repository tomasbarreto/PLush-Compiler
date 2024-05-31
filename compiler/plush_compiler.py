from plush_ast import *
from emitter import Emitter
import struct

def get_expr_type(expr, emitter):
    if isinstance(expr.type, str):
        if expr.type == "int":
            return "i32"
        elif expr.type == "boolean":
            return "i1"
        elif expr.type == "float":
            return "float"
        elif expr.type == "string":
            return "ptr"
        elif expr.type == "char":
            return "i8"
        elif expr.type.startswith('['):
            return "ptr"
    elif isinstance(expr.type, LiquidType):
        return get_expr_type(expr.type, emitter)
    
    return expr.type
    
def str_to_type(type_str):
    if isinstance(type_str, str):
        if type_str == "int":
            return "i32"
        elif type_str == "boolean":
            return "i1"
        elif type_str == "float":
            return "float"
        elif type_str == "string":
            return "ptr"
        elif type_str == "char":
            return "i8"
        elif type_str == "void":
            return "void"
        elif type_str.startswith('['):
            return "ptr"
    elif isinstance(type_str, LiquidType):
        return str_to_type(type_str.type)

    return type_str
    
def float_to_hex(f):
    hex_representation = hex(struct.unpack('<Q', struct.pack('<d', f))[0])

    hex_value = int(hex_representation, 16)

    # & 64bits
    hex_value = hex_value & 0xFFFFFFFF00000000

    result = hex(hex_value)

    result = result.upper()
    lst = list(result)
    lst[1] = 'x'

    return "".join(lst)

def convert_to_next_hex(hex):
    if hex == '0':
        return '1'
    elif hex == '1':
        return '2'
    elif hex == '2':
        return '3'
    elif hex == '3':
        return '4'
    elif hex == '4':
        return '5'
    elif hex == '5':
        return '6'
    elif hex == '6':
        return '7'
    elif hex == '7':
        return '8'
    elif hex == '8':
        return '9'
    elif hex == '9':
        return 'A'
    elif hex == 'A':
        return 'B'
    elif hex == 'B':
        return 'C'
    elif hex == 'C':
        return 'D'
    elif hex == 'D':
        return 'E'
    elif hex == 'E':
        return 'F'

def pad_with_zeros(str, desired_length):
    zeros_needed = max(0, desired_length - len(str))
    padded_str = str + '0' * zeros_needed
    return padded_str
    
def is_float(string):
    try:
        if isinstance(string, int):
            return False
        float(string)
        return True
    except ValueError:
        return False

def are_both_actual_types(left, right):
    if isinstance(left, int) and isinstance(right, int) or isinstance(left, float) and isinstance(right, float):
        return True
    return False

def hasDefinition(name, instructions):
    for instruction in instructions:
        if isinstance(instruction, FunctionDeclaration):
            if instruction.name == name:
                return True
    return False

def process_function_parameters(parameters, emitter):
    function_parameters = []

    for parameter in parameters:
        expr_type = str_to_type(parameter.type)
        new_pointer = emitter.get_prt_id()
        emitter.context.set_type(parameter.name, new_pointer)
        function_parameters.append(f"{expr_type} %{new_pointer}")

    return ", ".join(function_parameters)

def create_return_var(name, type, emitter):
    if isinstance(type, str):
        if type != "void":
            new_pointer = name
            emitter.context.set_type(name, new_pointer)

            if type == "int":
                emitter << f"   %{new_pointer} = alloca i32"
                emitter << f"   store i32 0, ptr %{new_pointer}"
            elif type == "float":
                emitter << f"   %{new_pointer} = alloca float"
                emitter << f"   store float {float_to_hex(0.0)}, ptr %{new_pointer}"
            elif type == "boolean":
                emitter << f"   %{new_pointer} = alloca i1"
                emitter << f"   store i1 0, ptr %{new_pointer}"
            elif type == "string":
                emitter << f"   %{new_pointer} = alloca ptr"
                emitter << f"   store ptr null, ptr %{new_pointer}"
            elif type == "char":
                emitter << f"   %{new_pointer} = alloca i8"
                emitter << f"   store i8 0, ptr %{new_pointer}"
            elif type.startswith('['):
                emitter << f"   %{new_pointer} = alloca ptr"
                emitter << f"   store ptr null, ptr %{new_pointer}"
            
            return new_pointer
    elif isinstance(type, LiquidType):
        create_return_var(name, type.type, emitter)

def declare_global_variables(statements, emitter):
    result = []
    for statement in statements.instructions:
        if isinstance(statement, VariableDeclaration):
            new_pointer = emitter.get_prt_id()
            expr_type = get_expr_type(statement.value, emitter)

            if isinstance(statement.value.expr, FunctionCall):
                raise Exception("Global variables cannot be initialized with function calls")
            elif isinstance(statement.value.expr, VariableAccess):
                raise Exception("Global variables cannot be initialized with variable accesses")
            
            if expr_type == "ptr":
                print(statement.value.expr.value)
                print(len(statement.value.expr.value))
                string_len = len(statement.value.expr.value) - 4 + 1
                string_len -= 2 * statement.value.expr.value.count("\\n")
                element = statement.value.expr.value.replace('\\n', r'0A')
                emitter.global_variables.append(f'@{new_pointer} = private unnamed_addr constant [{string_len} x i8] c"{element[1:-1][1:-1]}\\00"')
                emitter.global_variables_context.set_type(statement.name, new_pointer)
            elif expr_type == "i32":
                if isinstance(statement.value.expr, Unary):
                    if statement.value.expr.operator == "-":
                        emitter.global_variables.append(f'@{new_pointer} = dso_local global i32 {-int(statement.value.expr.expr.expr.value)}')
                    elif statement.value.expr.operator == "+":
                        emitter.global_variables.append(f'@{new_pointer} = dso_local global i32 {statement.value.expr.expr.expr.value}')

                    emitter.global_variables_context.set_type(statement.name, new_pointer)
                else:
                    emitter.global_variables.append(f'@{new_pointer} = dso_local global i32 {statement.value.expr.value}')
                    emitter.global_variables_context.set_type(statement.name, new_pointer)
            elif expr_type == "i1":
                emitter.global_variables.append(f'@{new_pointer} = dso_local global i1 {statement.value.expr.value}')
                emitter.global_variables_context.set_type(statement.name, new_pointer)
            elif expr_type == "float":
                if isinstance(statement.value.expr, Unary):
                    if statement.value.expr.operator == "-":
                            emitter.global_variables.append(f'@{new_pointer} = dso_local global float {float_to_hex(-float(statement.value.expr.expr.expr.value))}')
                    elif statement.value.expr.operator == "+":
                        emitter.global_variables.append(f'@{new_pointer} = dso_local global float {float_to_hex(float(statement.value.expr.expr.expr.value))}')

                    emitter.global_variables_context.set_type(statement.name, new_pointer)
                else:    
                    emitter.global_variables.append(f'@{new_pointer} = dso_local global float {float_to_hex(float(statement.value.expr.value))}')
                    emitter.global_variables_context.set_type(statement.name, new_pointer)
        else:
            result.append(statement)
    
    return InstructionList(result)

def process_string(string):
    string_len = len(string) - 4 + 1
    string_len -= 2 * string.count("\\n")
    str = string.replace('\\n', r'0A')

    return (str[1:-1][1:-1], string_len)

def get_expr_symbol(expr):
    symbol = "%"

    if isinstance(expr, int):
        symbol = ""
    
    return symbol

def get_operator_type(operator, expression_type):
    operator_type = ""

    if operator != "=" and operator != "!=":
        operator_type = "s"

    if expression_type == "float":
        operator_type = "o"

    return operator_type

def get_operation_type(expression_type):
    operation_type = "i"

    if expression_type == "float":
        operation_type = "f"

    return operation_type

def save_array_dimensions(get_array_function, emitter):
    indexes = []
    for argument in get_array_function.arguments.arguments:
        indexes.append(compile(argument.value))

    emitter.array_dimensions_context.set_type(get_array_function.name, indexes)

def send_string_to_global_variables(string, emitter):
    new_pointer = emitter.get_prt_id()
    processed_str = process_string(string)
    emitter.global_variables.append(f'@{new_pointer} = private unnamed_addr constant [{processed_str[1]} x i8] c"{processed_str[0]}\\00"')

    #save it to global variables context
    emitter.global_variables_context.set_type(new_pointer, new_pointer)

    return new_pointer

def get_array_base_type(identifier, emitter):
    if isinstance(identifier, VariableAccess):
        return str_to_type(emitter.variable_type_context.get_type(identifier.name).replace("[", "").replace("]", ""))
    elif isinstance(identifier, FunctionCall):
        return str_to_type(emitter.function_declarations_context.get_type(identifier.name).replace("[", "").replace("]", ""))

def compile(node, emitter=Emitter()):
    if isinstance(node, Program):
        instructions = declare_global_variables(node.statements, emitter)
        compile(instructions, emitter)
    elif isinstance(node, InstructionList):
        for instruction in node.instructions:
            if isinstance(instruction, FunctionDefinition):
                # check if the function has a declaration because if it does, we don't want to define it, we just want to declare it
                if not hasDefinition(instruction.name, node.instructions):
                    compile(instruction, emitter)
                continue
            compile(instruction, emitter)
    elif isinstance(node, VariableDeclaration):
        # get a pointer name
        pointer_name = emitter.get_prt_id()
        # compile the expression
        expression = compile(node.value, emitter)

        # check the type of the expression
        expr_type = get_expr_type(node.value, emitter)
        emitter.variable_type_context.set_type(node.name, node.value.type)

        if emitter.global_variables_context.has_var(expression):
            emitter << f"   %{pointer_name} = alloca {expr_type}"
            emitter.push_to_context(node.name, pointer_name)
            emitter << f"   store {expr_type} @{expression}, ptr %{pointer_name}"
            return

        emitter << f"   %{pointer_name} = alloca {expr_type}"
        emitter.push_to_context(node.name, pointer_name)

        if isinstance(expression, int):
            emitter << f"   store {expr_type} {expression}, ptr %{pointer_name}"
        elif is_float(expression):
            expression = float_to_hex(expression)
            emitter << f"   store {expr_type} {expression}, ptr %{pointer_name}"
        elif emitter.global_variables_context.has_var(expression):
            emitter << f"   store {get_expr_type(node.value, emitter)} @{expression}, ptr %{pointer}"
        else:
            emitter << f"   store {expr_type} %{expression}, ptr %{pointer_name}"

        return

    elif isinstance(node, Expression):
        if isinstance(node.expr, VariableAccess):
            new_pointer = emitter.get_prt_id()
            expression_type = get_expr_type(node, emitter)

            if emitter.global_variables_context.has_var(node.expr.name) and not emitter.context.has_var(node.expr.name):
                pointer = emitter.global_variables_context.get_type(node.expr.name)
                symbol = "@"
            elif emitter.global_variables_context.has_var(node.expr.name) and emitter.context.has_var(node.expr.name):
                pointer = emitter.get_from_context(node.expr.name)
                symbol = "%"
            else:
                pointer = emitter.get_from_context(node.expr.name)
                symbol = "%"

            emitter << f"   %{new_pointer} = load {expression_type}, ptr {symbol}{pointer}"

            return new_pointer
        elif isinstance(node.expr, (Compare, Equality)):
            new_pointer = emitter.get_cmp_id()
            expression_type = get_expr_type(node.expr.left, emitter)
            left = compile(node.expr.left, emitter)
            right = compile(node.expr.right, emitter)

            cmp_type = get_operation_type(expression_type)
            operator_type = get_operator_type(node.expr.operator, expression_type)

            percentage_symbol_right = "%"

            if isinstance(right, int) or is_float(right):
                percentage_symbol_right = ""

            percentage_symbol_left = "%"

            if isinstance(left, int) or is_float(left):
                percentage_symbol_left = ""

            if node.expr.operator == "<":
                emitter << f"   %{new_pointer} = {cmp_type}cmp {operator_type}lt {expression_type} {percentage_symbol_left}{left}, {percentage_symbol_right}{right}"
            elif node.expr.operator == ">":
                emitter << f"   %{new_pointer} = {cmp_type}cmp {operator_type}gt {expression_type} {percentage_symbol_left}{left}, {percentage_symbol_right}{right}"
            elif node.expr.operator == "<=":
                emitter << f"   %{new_pointer} = {cmp_type}cmp {operator_type}le {expression_type} {percentage_symbol_left}{left}, {percentage_symbol_right}{right}"
            elif node.expr.operator == ">=":
                emitter << f"   %{new_pointer} = {cmp_type}cmp {operator_type}ge {expression_type} {percentage_symbol_left}{left}, {percentage_symbol_right}{right}"
            elif node.expr.operator == "=":
                emitter << f"   %{new_pointer} = {cmp_type}cmp {operator_type}eq {expression_type} {percentage_symbol_left}{left}, {percentage_symbol_right}{right}"
            elif node.expr.operator == "!=":
                emitter << f"   %{new_pointer} = {cmp_type}cmp {operator_type}ne {expression_type} {percentage_symbol_left}{left}, {percentage_symbol_right}{right}"

            return new_pointer

        return compile(node.expr, emitter)
    elif isinstance(node, (
        Add,
        Sub
    )):
        left = compile(node.left, emitter)
        right = compile(node.right, emitter)
        # check if the left and right are actual types
        are_actual_types = are_both_actual_types(left, right)

        left_type = node.left.type
        right_type = node.right.type

        if isinstance(left_type, LiquidType):
            node.left.type = left_type.type

        if isinstance(right_type, LiquidType):
            node.right.type = right_type.type

        if are_actual_types:
            if isinstance(node, Add):
                if isinstance(node.left.expr, Int):
                    return left + right
                else:
                    return float_to_hex(left + right)
            else :
                if isinstance(node.left.expr, Int):
                    return left - right
                else:
                    return float_to_hex(left - right)
        else:

            if node.left.type == "int":
                id = emitter.get_add_id()
            else:
                id = emitter.get_sub_id()

            if isinstance(node, Add):
                if node.left.type == "int":
                    operation = "add"
                else:
                    operation = "fadd"
            else:
                if node.left.type == "int":
                    operation = "sub"
                else:
                    operation = "fsub"
            
            if node.left.type == "int":
                if isinstance(left, int):
                    emitter << f"   %{id} = {operation} nsw i32 {left}, %{right}"
                elif isinstance(right, int):
                    emitter << f"   %{id} = {operation} nsw i32 %{left}, {right}"
                else:
                    emitter << f"   %{id} = {operation} nsw i32 %{left}, %{right}"
            elif node.left.type == "float":
                if isinstance(left, float):
                    emitter << f"   %{id} = {operation} float {left}, %{right}"
                elif isinstance(right, float):
                    emitter << f"   %{id} = {operation} float %{left}, {right}"
                else:
                    emitter << f"   %{id} = {operation} float %{left}, %{right}"

        return id
    
    elif isinstance(node, (
        Mult
    )):
        left = compile(node.left, emitter)
        right = compile(node.right, emitter)

        left_type = node.left.type
        right_type = node.right.type

        if isinstance(left_type, LiquidType):
            node.left.type = left_type.type

        if isinstance(right_type, LiquidType):
            node.right.type = right_type.type

        # check if the left and right are actual types
        are_actual_types = are_both_actual_types(left, right)

        if are_actual_types:
            if node.operator == "*":
                if isinstance(node.left.expr, Int):
                    return left * right
                else:
                    return float_to_hex(left * right)
            elif node.operator == "/":
                if isinstance(node.left.expr, Int):
                    return left / right
                else:
                    return float_to_hex(left / right)
            elif node.operator == "%":
                if isinstance(node.left.expr, Int):
                    return left % right
                else:
                    return float_to_hex(left % right)
            elif node.operator == "^":
                if isinstance(node.left.expr, Int):
                    return left ** right
                else:
                    return float_to_hex(left ** right)
            
        else:

            if node.operator == "*":
                mult_id = emitter.get_mult_id()
                
                if node.left.type == "int":
                    if isinstance(left, int) and isinstance(right, int):
                        emitter << f"   %{mult_id} = mul nsw i32 {left}, {right}"
                    elif isinstance(left, int):
                        emitter << f"   %{mult_id} = mul nsw i32 {left}, %{right}"
                    elif isinstance(right, int):
                        emitter << f"   %{mult_id} = mul nsw i32 %{left}, {right}"
                    else:
                        emitter << f"   %{mult_id} = mul nsw i32 %{left}, %{right}"
                elif node.left.type == "float":
                    if is_float(left) and is_float(right):
                        emitter << f"   %{mult_id} = fmul float {left}, {right}"
                    elif is_float(left):
                        emitter << f"   %{mult_id} = fmul float {left}, %{right}"
                    elif is_float(right):
                        emitter << f"   %{mult_id} = fmul float %{left}, {right}"
                    else:
                        emitter << f"   %{mult_id} = fmul float %{left}, %{right}"

                return mult_id
            elif node.operator == "/":
                div_id = emitter.get_div_id()
                
                if node.left.type == "int":
                    if isinstance(left, int) and isinstance(right, int):
                        emitter << f"   %{div_id} = sdiv i32 {left}, {right}"
                    elif isinstance(left, int):
                        emitter << f"   %{div_id} = sdiv i32 {left}, %{right}"
                    elif isinstance(right, int):
                        emitter << f"   %{div_id} = sdiv i32 %{left}, {right}"
                    else:
                        emitter << f"   %{div_id} = sdiv i32 %{left}, %{right}"
                elif node.left.type == "float":
                    if is_float(left) and is_float(right):
                        emitter << f"   %{div_id} = fdiv float {left}, {right}"
                    elif is_float(left):
                        emitter << f"   %{div_id} = fdiv float {left}, %{right}"
                    elif is_float(right):
                        emitter << f"   %{div_id} = fdiv float %{left}, {right}"
                    else:
                        emitter << f"   %{div_id} = fdiv float %{left}, %{right}"

                return div_id
            
            elif node.operator == "%":
                mod_id = emitter.get_div_id()
                
                if node.left.type == "int":
                    if isinstance(left, int) and isinstance(right, int):
                        emitter << f"   %{mod_id} = srem i32 {left}, {right}"
                    elif isinstance(left, int):
                        emitter << f"   %{mod_id} = srem i32 {left}, %{right}"
                    elif isinstance(right, int):
                        emitter << f"   %{mod_id} = srem i32 %{left}, {right}"
                    else:
                        emitter << f"   %{mod_id} = srem i32 %{left}, %{right}"
                elif node.left.type == "float":
                    if is_float(left) and is_float(right):
                        emitter << f"   %{mod_id} = frem float {left}, {right}"
                    elif is_float(left):
                        emitter << f"   %{mod_id} = frem float {left}, %{right}"
                    elif is_float(right):
                        emitter << f"   %{mod_id} = frem float %{left}, {right}"
                    else:
                        emitter << f"   %{mod_id} = frem float %{left}, %{right}"

                return mod_id
            elif node.operator == "^":
                pow_id = emitter.get_mult_id()

                newleft = left
                newright = right
                
                if node.left.type == "float":
                    if isinstance(left, float) and isinstance(right, float):
                        newleft = emitter.get_prt_id()
                        newright = emitter.get_prt_id()
                        emitter << f"   %{newleft} = fpext float {left} to double"
                        emitter << f"   %{newright} = fpext float {right} to double"
                    elif isinstance(left, float):
                        newleft = emitter.get_prt_id()
                        newright = emitter.get_prt_id()
                        emitter << f"   %{newleft} = fpext float {left} to double"
                        emitter << f"   %{newright} = fpext float %{right} to double"
                    elif isinstance(right, float):
                        newleft = emitter.get_prt_id()
                        newright = emitter.get_prt_id()
                        emitter << f"   %{newleft} = fpext float %{left} to double"
                        emitter << f"   %{newright} = fpext float {right} to double"
                    else:
                        newleft = emitter.get_prt_id()
                        newright = emitter.get_prt_id()
                        emitter << f"   %{newleft} = fpext float %{left} to double"
                        emitter << f"   %{newright} = fpext float %{right} to double"
                elif node.left.type == "float":
                    if is_float(left) and is_float(right):
                        newleft = emitter.get_prt_id()
                        newright = emitter.get_prt_id()
                        emitter << f"   %{newleft} = fpext float {left} to double"
                        emitter << f"   %{newright} = fpext float {right} to double"
                    elif is_float(left):
                        newleft = emitter.get_prt_id()
                        newright = emitter.get_prt_id()
                        emitter << f"   %{newleft} = fpext float {left} to double"
                        emitter << f"   %{newright} = fpext float %{right} to double"
                    elif is_float(right):
                        newleft = emitter.get_prt_id()
                        newright = emitter.get_prt_id()
                        emitter << f"   %{newleft} = fpext float %{left} to double"
                        emitter << f"   %{newright} = fpext float {right} to double"
                    else:
                        newleft = emitter.get_prt_id()
                        newright = emitter.get_prt_id()
                        emitter << f"   %{newleft} = fpext float %{left} to double"
                        emitter << f"   %{newright} = fpext float %{right} to double"

                emitter << f"   %{pow_id} = call double @pow(double %{newleft}, double %{newright})"

                pow_id2 = emitter.get_mult_id()

                emitter << f"   %{pow_id2} = fptrunc double %{pow_id} to float"

                return pow_id2

            
            

    elif isinstance(node, (
        Int,
        Float,
        Boolean,
        String,
        Char
    )):
        if isinstance(node, Int):
            return int(node.value)
        elif isinstance(node, Float):
            return float(node.value)
        elif isinstance(node, Boolean):
            if node.value == "true":
                return 1
            return 0
        elif isinstance(node, String):
            return send_string_to_global_variables(node.value, emitter)
        elif isinstance(node, Char):
            return ord(node.value.replace("'", ""))

    elif isinstance(node, FunctionDefinition):
        emitter.push_to_function_declarations(f"\ndeclare {get_expr_type(node, emitter)} @{node.name}(ptr, ...) #{emitter.get_function_id()}\n")
        emitter.function_declarations_context.set_type(node.name, node.type)
    elif isinstance(node, (ProcedureCall, FunctionCall)):
        argument_list = []

        # process the arguments
        for argument in node.arguments.arguments:
            expr_type = get_expr_type(argument.value, emitter)
            content = compile(argument, emitter)
            if isinstance(argument.value.expr, Int) or is_float(content):
                argument_list.append(f"{expr_type} {argument.value.expr.value}")
            elif isinstance(content, int):
                argument_list.append(f"{expr_type} {content}")
            elif content.startswith("0x"):
                argument_list.append(f"{expr_type} {content}")
            elif isinstance(argument.value.expr, String):
                argument_list.append(f"{expr_type} @{content}")
            elif isinstance(argument.value.expr, VariableAccess):
                if emitter.global_variables_context.has_var(argument.value.expr.name):
                    print(emitter.global_variables_context.get_type(argument.value.expr.name))
                    argument_list.append(f"{expr_type} @{emitter.global_variables_context.get_type(argument.value.expr.name)}")
                else:
                    argument_list.append(f"{expr_type} %{content}")
            else:
                    argument_list.append(f"{expr_type} %{content}")


        if isinstance(node, ProcedureCall):
            emitter << f"   call void @{node.name}({', '.join(argument_list)})"
        elif isinstance(node, FunctionCall):
            new_pointer = emitter.get_prt_id()
            function_type = emitter.function_declarations_context.get_type(node.name)
            emitter << f"   %{new_pointer} = call {str_to_type(function_type)} @{node.name}({', '.join(argument_list)})"

            return new_pointer
        
        return
    elif isinstance(node, Argument):
        return compile(node.value, emitter)
    elif isinstance(node, FunctionDeclaration):
        emitter.context.enter_scope()
        emitter.variable_type_context.enter_scope()

        function_parameters = ""
        if node.parameters:
            function_parameters = process_function_parameters(node.parameters.parameters, emitter)

        emitter.push_to_context(node.name, node.name)
        emitter.function_declarations_context.set_type(node.name, node.type)

        # create the function
        emitter << f"\ndefine dso_local {str_to_type(node.type)} @{node.name}({function_parameters}) {{"

        create_return_var(node.name, node.type, emitter)
            
        # process the parameters
        if node.parameters:
            for parameter in node.parameters.parameters:
                expr_type = str_to_type(parameter.type)
                pointer = emitter.context.get_type(parameter.name)
                emitter << f"   %{pointer}.addr = alloca {expr_type}"
                emitter << f"   store {expr_type} %{pointer}, ptr %{pointer}.addr"
                emitter.push_to_context(parameter.name, f"{pointer}.addr")
                emitter.variable_type_context.set_type(parameter.name, parameter.type)

        compile(node.instructions, emitter)

        if node.type == "void":
            emitter << f"   ret void"
        else:
            new_pointer = emitter.get_prt_id()
            emitter << f"   %{new_pointer} = load {str_to_type(node.type)}, ptr %{emitter.get_from_context(node.name)}"
            emitter << f"   ret {str_to_type(node.type)} %{new_pointer}"
        emitter << f"}}"    

        emitter.context.exit_scope()
        emitter.variable_type_context.exit_scope()

    elif isinstance(node, IfStatement):
        if_id = emitter.get_if_id()

        condition_result_pointer = compile(node.condition, emitter)
        emitter << f"   br i1 %{condition_result_pointer}, label %{if_id}.then, label %{if_id}.else"

        emitter << f"{if_id}.then:"
        compile(node.then_block, emitter)
        emitter << f"   br label %{if_id}.end"
        emitter << f"{if_id}.else:"
        compile(node.else_block, emitter)
        emitter << f"   br label %{if_id}.end"
        emitter << f"{if_id}.end:"

        return
    elif isinstance(node, (ThenBlock, ElseBlock)):
        emitter.context.enter_scope()
        emitter.variable_type_context.enter_scope()

        if node.instructions:
            for instruction in node.instructions:
                compile(instruction, emitter)

        emitter.context.exit_scope()
        emitter.variable_type_context.exit_scope()

        return
    
    elif isinstance(node, WhileStatement):
        while_id = emitter.get_while_id()
        condition_pointer = emitter.get_condition_id()
        
        emitter << f"   br label %{condition_pointer}\n"

        emitter << f"\n{condition_pointer}:"
        # Compile the condition
        pointer = compile(node.condition, emitter)

        # Condition
        emitter << f"   br i1 %{pointer}, label %{while_id}.body, label %{while_id}.end\n"
        
        emitter.context.enter_scope()
        emitter.variable_type_context.enter_scope()
        
        # Body
        emitter << f"\n\n{while_id}.body:"
        for instruction in node.code_block:
            compile(instruction, emitter)
        emitter << f"   br label %{condition_pointer}\n"

        emitter.context.exit_scope()
        emitter.variable_type_context.exit_scope()

        # End
        emitter << f"{while_id}.end:"

        return
    elif isinstance(node, VariableAssignment):
        pointer = emitter.get_from_context(node.name)
        expression = compile(node.value, emitter)
        if isinstance(expression, int):
            emitter << f"   store {get_expr_type(node.value, emitter)} {expression}, ptr %{pointer}"
        elif is_float(expression):
            emitter << f"   store {get_expr_type(node.value, emitter)} {float_to_hex(expression)}, ptr %{pointer}"
        elif emitter.global_variables_context.has_var(expression):
            emitter << f"   store {get_expr_type(node.value, emitter)} @{expression}, ptr %{pointer}"
        else:
            emitter << f"   store {get_expr_type(node.value, emitter)} %{expression}, ptr %{pointer}"
    elif isinstance(node, And):
        left = compile(node.left, emitter)
        right = compile(node.right, emitter)

        new_pointer = emitter.get_condition_id()
        emitter << f"   %{new_pointer} = and i1 %{left}, %{right}"
        
        return new_pointer
    elif isinstance(node, Or):
        left = compile(node.left, emitter)
        right = compile(node.right, emitter)

        new_pointer = emitter.get_condition_id()
        emitter << f"   %{new_pointer} = or i1 %{left}, %{right}"
        
        return new_pointer
    elif isinstance(node, Unary):
        value = compile(node.expr, emitter)
        
        if isinstance(value, int) or is_float(value):
            if node.operator == "-":
                return -value
            elif node.operator == "+":
                return value
        elif isinstance(node.expr.expr, VariableAccess):
            ptr_type = str_to_type(node.expr.type)
            zero = 0
            operation = ""

            new_pointer = emitter.get_prt_id()

            if ptr_type == "float":
                operation = "f"
                zero = float_to_hex(0.0)
            
            emitter << f"   %{new_pointer} = alloca {ptr_type}"

            if node.operator == "-":
                sub_pointer = emitter.get_sub_id()
                emitter << f"   %{sub_pointer} = {operation}sub {ptr_type} {zero}, %{value}"

                return sub_pointer
            elif node.operator == "+":
                add_pointer = emitter.get_add_id()
                emitter << f"   %{add_pointer} = {operation}add {ptr_type} {zero}, %{value}"

                return add_pointer
            elif node.operator == "!":
                not_pointer = emitter.get_condition_id()
                emitter << f"   %{not_pointer} = xor i1 1, %{value}"

                return not_pointer
            
            return 
        elif isinstance(node.expr, Unary):
            return compile(node.expr, emitter)
    elif isinstance(node, ArrayAccess):
        new_pointer = ""
        node_type = ""
        if isinstance(node.identifier, VariableAccess):
            node_type = emitter.variable_type_context.get_type(node.identifier.name)
        elif isinstance(node.identifier, FunctionCall):
            node_type = emitter.function_declarations_context.get_type(node.identifier.name)

        counter = node_type.count("[")

        if isinstance(node.identifier, VariableAccess):
            index_pointer = emitter.get_from_context(node.identifier.name)
        elif isinstance(node.identifier, FunctionCall):
            index_pointer = compile(node.identifier, emitter)
            new_pointer = emitter.get_prt_id()
            emitter << f"   %{new_pointer} = alloca ptr"
            emitter << f"   store ptr %{index_pointer}, ptr %{new_pointer}"
            index_pointer = new_pointer

        array_pointer = emitter.get_prt_id()
        new_pointer = array_pointer

        emitter << f"   %{array_pointer} = load ptr, ptr %{index_pointer}"

        for index in node.indexes.indexes:
            index_value = compile(index.value, emitter)
            index_value2 = ""
            
            if not isinstance(index_value, int):
                index_value = f"%{index_value}"
            index_value2 = emitter.get_prt_id()
            emitter << f"   %{index_value2} = sext i32 {index_value} to i64"
            index_value2 = f"%{index_value2}"
            
            type1 = "ptr"
            type2 = "ptr"

            if counter == 1:
                type1 = get_array_base_type(node.identifier, emitter)

            index_pointer = emitter.get_index_id()

            emitter << f"   %{index_pointer} = getelementptr inbounds {type1}, {type2} %{new_pointer}, i64 {index_value2}"

            new_pointer = emitter.get_prt_id()

            emitter << f"   %{new_pointer} = load {type1}, {type2} %{index_pointer}"

            counter -= 1

        if isinstance(node.identifier, FunctionCall) and counter == 0:
            old_pointer = new_pointer
            new_pointer = emitter.get_prt_id()
            emitter << f"   %{new_pointer} = alloca {type1}"
            emitter << f"   store {type1} %{old_pointer}, ptr %{new_pointer}"
            old_pointer = new_pointer
            new_pointer = emitter.get_prt_id()
            emitter << f"   %{new_pointer} = load {type1}, ptr %{old_pointer}"

        if emitter.is_array_assignment:
            return index_pointer
        
        return new_pointer
    elif isinstance(node, ArrayVariableAssigment):
        emitter.is_array_assignment = True
        array_position_pointer = compile(node.left, emitter)
        emitter.is_array_assignment = False

        expression = compile(node.right, emitter)

        symbol = ""

        if isinstance(node.right.expr, (
            VariableAccess,
            FunctionCall,
            Add,
            Sub,
            Mult,
            ArrayAccess
        )):
            symbol = "%"
        

        emitter << f"   store {get_expr_type(node.right, emitter)} {symbol}{expression}, ptr %{array_position_pointer}"

    return emitter.global_variables + emitter.lines + emitter.function_declarations