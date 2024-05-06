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

        if expression.isnumeric() or is_float(expression):
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
        elif isinstance(node.expr, Compare):
            new_pointer = emitter.get_cmp_id()
            expression_type = get_expr_type(node, emitter)
            left = compile(node.expr.left, emitter)
            right = compile(node.expr.right, emitter)

            cmp_type = "i"
            operator_type = ""

            if node.expr.operator != "eq" or node.expr.operator != "ne":
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
                if left.isnumeric() and right.isnumeric():
                    emitter << f"   %{id} = {operation} nsw i32 {left}, {right}"
                elif left.isnumeric():
                    emitter << f"   %{id} = {operation} nsw i32 {left}, %{right}"
                elif right.isnumeric():
                    emitter << f"   %{id} = {operation} nsw i32 %{left}, {right}"
                else:
                    emitter << f"   %{id} = {operation} nsw i32 %{left}, %{right}"
            elif node.left.type == "float":
                if left.isnumeric() and right.isnumeric():
                    emitter << f"   %{id} = {operation} float {left}, {right}"
                elif left.isnumeric():
                    emitter << f"   %{id} = {operation} float {left}, %{right}"
                elif right.isnumeric():
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
        Float
    )):
        return node.value
    elif isinstance(node, FunctionDefinition):
        emitter << f"\ndeclare {node.type} @{node.name}(ptr, ...) #{emitter.get_function_id()}"
    elif isinstance(node, ProcedureCall):
        argument_list = []
        call_name = emitter.get_call_id()

        for argument in node.arguments.arguments:
            expr_type = get_expr_type(argument.value, emitter)
            argument_list.append(f"{expr_type} %{compile(argument, emitter)}")

        emitter << f"   %{call_name} = call void @{node.name}({', '.join(argument_list)})"
    
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

        emitter << f"   br i1 %{condition}, label %if.then{if_id}, label %if.else{if_id}"
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
        compile(node.condition, emitter)
        emitter << f"\n\n{while_id}.body:"
        compile(node.code_block, emitter)
        emitter << f"br label %{while_id}.cond\n\n"
        emitter << f"{while_id}.end:"

        return
    elif isinstance(node, VariableAssignment):
        pointer = emitter.get_from_context(node.name)
        expression = compile(node.value, emitter)
        emitter << f"   store {get_expr_type(node.value, emitter)} {expression}, ptr %{pointer}"

    return emitter.lines