from context import Context
from plush_ast import *

def plush_interpretor(node, ctx: Context):
    if isinstance(node, Program):
        plush_interpretor(node.statements, ctx)
    elif isinstance(node, InstructionList):
        for instruction in node.instructions:
            plush_interpretor(instruction, ctx)
    elif isinstance(node, FunctionDeclaration):
        plush_interpretor(node.instructions, ctx)
    elif isinstance(node, VariableDeclaration):
        if ctx.has_var_in_current_scope(node.name):
            raise TypeError(f"Variable {node.name} already declared!")
        
        ctx.set_type(node.name, plush_interpretor(node.value, ctx))
    elif isinstance(node, Expression):
        return plush_interpretor(node.expr, ctx)
    elif isinstance(node, Add):
        return plush_interpretor(node.left, ctx) + plush_interpretor(node.right, ctx)
    elif isinstance(node, Sub):
        return plush_interpretor(node.left, ctx) - plush_interpretor(node.right, ctx)
    elif isinstance(node, Mult):
        if node.operator == "*":
            return plush_interpretor(node.left, ctx) * plush_interpretor(node.right, ctx)
        elif node.operator == "/":
            return plush_interpretor(node.left, ctx) / plush_interpretor(node.right, ctx)
        else:
            return plush_interpretor(node.left, ctx) ** plush_interpretor(node.right, ctx)
    elif isinstance(node, Unary):
        if node.operator == "+":
            return plush_interpretor(node.expr, ctx)
        elif node.operator == "-":
            return -plush_interpretor(node.expr, ctx)
        else:
            return not plush_interpretor(node.expr, ctx)
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
