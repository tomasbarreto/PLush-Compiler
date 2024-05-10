from plush_ast import *
from emitter import Emitter

def get_expr_type(expr, emitter):
    if expr.type == "int":
        return "i32"
    elif expr.type == "boolean":
        return "i1"
    elif expr.type == "float":
        return "float"
    elif expr.type == "string":
        return "prt"
    elif expr.type == "char":
        return "i8"
    
def str_to_type(type_str):
    if type_str == "int":
        return "i32"
    elif type_str == "boolean":
        return "i1"
    elif type_str == "float":
        return "float"
    elif type_str == "string":
        return "prt"
    elif type_str == "char":
        return "i8"
    elif type_str == "void":
        return "void"
    
def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def are_both_actual_types(left, right):
    if isinstance(left.expr, Int) and isinstance(right.expr, Int) or isinstance(left.expr, Float) and isinstance(right.expr, Float):
        return True
    return False

def hasDefinition(name, instructions):
    for instruction in instructions:
        if isinstance(instruction, FunctionDeclaration):
            if instruction.name == name:
                return True
    return False

def get_function_parameters(parameters, emitter):
    function_parameters = []

    for parameter in parameters:
        expr_type = str_to_type(parameter.type)
        new_pointer = emitter.get_prt_id()
        emitter.context.set_type(parameter.name, new_pointer)
        function_parameters.append(f"{expr_type} %{new_pointer}")

    return ", ".join(function_parameters)

def compile(node, emitter=Emitter()):
    if isinstance(node, Program):
        compile(node.statements, emitter)
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

        emitter << f"   %{pointer_name} = alloca {expr_type}"
        emitter.push_to_context(node.name, pointer_name)

        if isinstance(expression, int) or is_float(expression):
            emitter << f"   store {expr_type} {expression}, ptr %{pointer_name}"
        else:
            emitter << f"   store {expr_type} %{expression}, ptr %{pointer_name}"

        return

    elif isinstance(node, Expression):
        if isinstance(node.expr, VariableAccess):
            new_pointer = emitter.get_prt_id()
            expression_type = get_expr_type(node, emitter)
            pointer = emitter.get_from_context(node.expr.name)
            emitter << f"   %{new_pointer} = load {expression_type}, ptr %{pointer}"

            return new_pointer
        elif isinstance(node.expr, (Compare, Equality)):
            new_pointer = emitter.get_cmp_id()
            expression_type = get_expr_type(node.expr.left, emitter)
            left = compile(node.expr.left, emitter)
            right = compile(node.expr.right, emitter)

            cmp_type = "i"
            operator_type = ""

            if node.expr.operator != "=" and node.expr.operator != "!=":
                operator_type = "s"

            if expression_type == "float":
                cmp_type = "f"
                operator_type = "o"

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
        # check if the left and right are actual types
        are_actual_types = are_both_actual_types(node.left, node.right)

        if are_actual_types:
            if isinstance(node, Add):
                if isinstance(node.left.expr, Int):
                    return int(node.left.expr.value) + int(node.right.expr.value)
                else:
                    return float(node.left.expr.value) + float(node.right.expr.value)
            else :
                if isinstance(node.left.expr, Int):
                    return int(node.left.expr.value) - int(node.right.expr.value)
                else:
                    return float(node.left.expr.value) - float(node.right.expr.value)
        else:

            left = compile(node.left, emitter)
            right = compile(node.right, emitter)

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
        # check if the left and right are actual types
        are_actual_types = are_both_actual_types(node.left, node.right)

        if are_actual_types:
            if isinstance(node.left.expr, Int):
                return int(node.left.expr.value) * int(node.right.expr.value)
            else:
                return float(node.left.expr.value) * float(node.right.expr.value)
            
        else:

            left = compile(node.left, emitter)
            right = compile(node.right, emitter)

            mult_id = emitter.get_mult_id()
            
            if node.left.type == "int":
                if left.isnumeric() and right.isnumeric():
                    emitter << f"   %{mult_id} = mul nsw i32 {left}, {right}"
                elif left.isnumeric():
                    emitter << f"   %{mult_id} = mul nsw i32 {left}, %{right}"
                elif right.isnumeric():
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

    elif isinstance(node, (
        Int,
        Float,
        Boolean
    )):
        if isinstance(node, Int):
            return int(node.value)
        elif isinstance(node, Float):
            return float(node.value)
        elif isinstance(node, Boolean):
            if node.value == "true":
                return 1
            return 0
    elif isinstance(node, FunctionDefinition):
        emitter.push_to_function_declarations(f"\ndeclare {node.type} @{node.name}(ptr, ...) #{emitter.get_function_id()}\n")
    elif isinstance(node, ProcedureCall):
        argument_list = []

        for argument in node.arguments.arguments:
            expr_type = get_expr_type(argument.value, emitter)
            element = compile(argument, emitter)
            if isinstance(element, int) or is_float(element):
                argument_list.append(f"{expr_type} {element}")
            else:
                argument_list.append(f"{expr_type} %{element}")

        emitter << f"   call void @{node.name}({', '.join(argument_list)})"
    
        return
    elif isinstance(node, Argument):
        return compile(node.value, emitter)
    elif isinstance(node, FunctionDeclaration):
        emitter.context.enter_scope()

        function_parameters = ""
        if node.parameters:
            function_parameters = get_function_parameters(node.parameters.parameters, emitter)

        emitter.push_to_context(node.name, node.name)

        emitter << f"\ndefine dso_local {str_to_type(node.type)} @{node.name}({function_parameters}) {{"
        emitter << f"entry:"

        if node.parameters:
            for parameter in node.parameters.parameters:
                expr_type = str_to_type(parameter.type)
                pointer = emitter.context.get_type(parameter.name)
                emitter << f"   %{pointer}.addr = alloca {expr_type}"
                emitter << f"   store {expr_type} %{pointer}, ptr %{pointer}.addr"

        compile(node.instructions, emitter)

        if node.type == "void":
            emitter << f"   ret void"
        else:
            emitter << f"   ret {str_to_type(node.type)} %{emitter.get_from_context(node.name)}"
        emitter << f"}}"    

        emitter.context.exit_scope()

    elif isinstance(node, IfStatement):
        if_id = emitter.get_if_id()
        condition = compile(node.condition, emitter)

        percentage_symbol = "%"

        if isinstance(condition, int):
            percentage_symbol = ""

        emitter << f"   br i1 {percentage_symbol}{condition}, label %{if_id}.then, label %{if_id}.else"
        emitter << f"{if_id}.then:"
        compile(node.then_block, emitter)
        emitter << f"   br label %{if_id}.end"
        emitter << f"{if_id}.else:"
        compile(node.else_block, emitter)
        emitter << f"   br label %{if_id}.end"
        emitter << f"{if_id}.end:"

        return
    elif isinstance(node, (ThenBlock, ElseBlock)):
        for instruction in node.instructions:
            compile(instruction, emitter)
        
        return
    
    elif isinstance(node, WhileStatement):
        while_id = emitter.get_while_id()
        emitter << f"   br label %{while_id}.cond\n\n"
        emitter << f"{while_id}.cond:"
        cmp_pointer = compile(node.condition, emitter)
        emitter << f"   br i1 %{cmp_pointer}, label %{while_id}.body, label %{while_id}.end\n\n"
        emitter << f"\n\n{while_id}.body:"
        for instruction in node.code_block:
            compile(instruction, emitter)
        emitter << f"   br label %{while_id}.cond\n\n"
        emitter << f"{while_id}.end:"

        return
    elif isinstance(node, VariableAssignment):
        pointer = emitter.get_from_context(node.name)
        expression = compile(node.value, emitter)
        if isinstance(expression, int) or is_float(expression):
            emitter << f"   store {get_expr_type(node.value, emitter)} {expression}, ptr %{pointer}"
        else:
            emitter << f"   store {get_expr_type(node.value, emitter)} %{expression}, ptr %{pointer}"
    elif isinstance(node, And):
        left = compile(node.left, emitter)
        right = compile(node.right, emitter)

        if node.left.expr.value in ['true', 'false']:
            if emitter.add_count != 0:
                new_pointer = emitter.get_add_id()
                emitter << f"{new_pointer}:"
                next_pointer = emitter.get_add_id()
                emitter << f"   br label %{next_pointer}"
            emitter   

    return emitter.lines + emitter.function_declarations