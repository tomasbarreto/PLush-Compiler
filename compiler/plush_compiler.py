from plush_ast import *
from emitter import Emitter

def get_expr_type(expr, emitter):
    if expr.type == "int":
        return "i32"
    elif expr.type == "bool":
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
    elif type_str == "bool":
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

def get_function_parameters(parameters):
    function_parameters = []

    for parameter in parameters:
        expr_type = str_to_type(parameter.type)
        function_parameters.append(f"{expr_type} %{parameter.name}")

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

        if node.value.type == "int" or node.value.type == "float":
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

        return compile(node.expr, emitter)
    elif isinstance(node, (
        Add
    )):
        # check if the left and right are actual types
        are_actual_types = are_both_actual_types(node.left, node.right)

        if are_actual_types:
            if isinstance(node.left.expr, Int):
                return int(node.left.expr.value) + int(node.right.expr.value)
            else:
                return float(node.left.expr.value) + float(node.right.expr.value)
            
        else:

            left = compile(node.left, emitter)
            right = compile(node.right, emitter)

            add_id = emitter.get_add_id()
            
            if node.left.type == "int":
                if left.isnumeric() and right.isnumeric():
                    emitter << f"   %{add_id} = add nsw i32 {left}, {right}"
                elif left.isnumeric():
                    emitter << f"   %{add_id} = add nsw i32 {left}, %{right}"
                elif right.isnumeric():
                    emitter << f"   %{add_id} = add nsw i32 %{left}, {right}"
                else:
                    emitter << f"   %{add_id} = add nsw i32 %{left}, %{right}"
            elif node.left.type == "float":
                if left.isnumeric() and right.isnumeric():
                    emitter << f"   %{add_id} = fadd float {left}, {right}"
                elif left.isnumeric():
                    emitter << f"   %{add_id} = fadd float {left}, %{right}"
                elif right.isnumeric():
                    emitter << f"   %{add_id} = fadd float %{left}, {right}"
                else:
                    emitter << f"   %{add_id} = fadd float %{left}, %{right}"

        return add_id
    
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
        function_parameters = ""
        if node.parameters:
            function_parameters = get_function_parameters(node.parameters.parameters)

        emitter << f"\ndefine dso_local {node.type} @{node.name}({function_parameters}) {{"
        emitter << f"   entry:"

        compile(node.instructions, emitter)

        if node.type == "void":
            emitter << f"   ret void"
        else:
            emitter << f"   ret {node.type}"
        emitter << f"}}"    

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

    return emitter.lines