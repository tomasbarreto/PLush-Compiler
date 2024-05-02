from context import Context
from plush_ast import *

def interpretor(node, ctx: Context):
    if isinstance(node, Program):
        interpretor(node.statements, ctx)
    elif isinstance(node, InstructionList):
        for instruction in node.instructions:
            interpretor(instruction, ctx)
    elif isinstance(node, FunctionDeclaration):
        interpretor(node.instructions, ctx)
    elif isinstance(node, VariableDeclaration):
        if ctx.has_var_in_current_scope(node.name):
            raise TypeError(f"Variable {node.name} already declared!")
        
        ctx.set_type(node.name, interpretor(node.value, ctx))
    elif isinstance(node, Expression):
        return interpretor(node.expr, ctx)
    elif isinstance(node, Add):
        return interpretor(node.left, ctx) + interpretor(node.right, ctx)
    elif isinstance(node, Sub):
        return interpretor(node.left, ctx) - interpretor(node.right, ctx)
    elif isinstance(node, Mult):
        if node.operator == "*":
            return interpretor(node.left, ctx) * interpretor(node.right, ctx)
        elif node.operator == "/":
            return interpretor(node.left, ctx) / interpretor(node.right, ctx)
        else:
            return interpretor(node.left, ctx) ** interpretor(node.right, ctx)
    elif isinstance(node, Unary):
        if node.operator == "+":
            return interpretor(node.expr, ctx)
        elif node.operator == "-":
            return -interpretor(node.expr, ctx)
        else:
            return not interpretor(node.expr, ctx)
    elif isinstance(node, Int):
        return int(node.value)
    elif isinstance(node, Float):
        return float(node.value)
    elif isinstance(node, String):
        return str(node.value)
    elif isinstance(node, Char):
        return chr(node.value)
    elif isinstance(node, Boolean):
        return bool(node.value)
    elif isinstance(node, ProcedureCall):
        if node.name == "print":
            print(ctx.get_type(node.arguments.arguments[0].value.expr.name), ctx)
    else:
        pass
