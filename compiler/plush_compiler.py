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

def are_both_actual_types(left, right):
    if isinstance(left.expr, Int) and isinstance(right.expr, Int) or isinstance(left.expr, Float) and isinstance(right.expr, Float):
        return True
    return False

def compile(node, emitter=Emitter()):
    if isinstance(node, Program):
        compile(node.statements, emitter)
    elif isinstance(node, InstructionList):
        for instruction in node.instructions:
            compile(instruction, emitter)
    elif isinstance(node, VariableDeclaration):
        # get a pointer name
        pointer_name = emitter.get_pointer_name()
        # compile the expression
        expression = compile(node.value, emitter)

        # check the type of the expression
        expr_type = get_expr_type(expression, emitter)

        emitter << f"   %{pointer_name} = alloca {expr_type}"
        emitter.push_to_context(node.name, pointer_name)
        emitter << f"   store {expr_type} {expression}, i32* %{pointer_name}"

    elif isinstance(node, Expression):
        return compile(node.expr, emitter)
    elif isinstance(node, (
        Or,
        And
    )):
        left = compile(node.left, emitter)
        right = compile(node.right, emitter)

        # check if the left and right are actual types
        are_actual_types = are_both_actual_types(node.left, node.right)

        if are_actual_types:
            value = node.left.expr.value + node.right.expr.value
            
            if isinstance(node.left.expr, (Int, Float)):
                return value
            
        else:

            if isinstance(node.left.expr, Int):
                emitter << f"   {emitter.get_add_id()} = add nsw i32 {node.left.expr.value}, {right}"
            elif isinstance(node.right.expr, Int):
                emitter << f"   {emitter.get_add_id()} = add nsw i32 {left}, {node.right.expr.value}"
            elif isinstance(node.left.expr, Float):
                emitter << f"   {emitter.get_add_id()} = fadd float {node.left.expr.value}, {right}"
            elif isinstance(node.right.expr, Float):
                emitter << f"   {emitter.get_add_id()} = fadd float {left}, {node.right.expr.value}"