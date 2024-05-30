from z3 import *
from context import Context
from plush_ast import *

def liquid_typecheck(solver: Solver, predicate, ctx: Context):
    parse_expr_to_z3(predicate, ctx, solver)
    return solver


def parse_expr_to_z3(node, ctx: Context, solver: Solver):
    if isinstance(node, (
        Add,
        Sub,
        Mult
    )):
        raise TypeError("Predicates cannot be used in arithmetic expressions")
    else:
        parse(node, ctx, solver)

def parse(node, ctx: Context, solver: Solver):
    if isinstance(node, And):
        left = parse(node.left, ctx, solver)
        right = parse(node.right, ctx, solver)
        solver.add(z3.And(left, right))
        return
    elif isinstance(node, Or):
        left = parse(node.left, ctx, solver)
        right = parse(node.right, ctx, solver)

        solver.add(z3.Or(left, right))
        return
    elif isinstance(node, Unary):
        if node.operator == '!':
            return z3.Not(parse(node.expr, ctx, solver))
        elif node.operator == '-':
            return -parse(node.expr, ctx, solver)
        elif node.operator == '+':
            return parse(node.expr, ctx, solver)
    elif isinstance(node, Equality):
        left = parse(node.left, ctx, solver)
        right = parse(node.right, ctx, solver)

        if node.operator == '=':
            solver.add(left == right)
            return z3.Not(z3.Not(left == right))
        elif node.operator == '!=':
            solver.add(left != right)
            return z3.Not(z3.Not(left != right))
        
    elif isinstance(node, Compare):
        left = parse(node.left, ctx, solver)
        right = parse(node.right, ctx, solver)

        if node.operator == '<':
            solver.add(left < right)
            return z3.Not(z3.Not(left < right))
        elif node.operator == '<=':
            solver.add(left <= right)
            return z3.Not(z3.Not(left <= right))
        elif node.operator == '>':
            solver.add(left > right)
            return z3.Not(z3.Not(left > right))
        elif node.operator == '>=':
            solver.add(left >= right)
            return z3.Not(z3.Not(left >= right))

    elif isinstance(node, (
        Int,
        Float,
        Boolean,
        Char
    )):
        if isinstance(node, Int):
            return int(node.value)
        elif isinstance(node, Float):
            return float(node.value)
        elif isinstance(node, Boolean):
            if node.value == 'true':
                return True
            return False
        elif isinstance(node, Char):
            return node.value
    elif isinstance(node, VariableAccess):
        node_type = ""
        if ctx.has_var(node.name):
            node_type = ctx.get_type(node.name)
        elif ctx.has_function(node.name):
            node_type = ctx.get_type_function(node.name)

        if isinstance(node_type, LiquidType):
            node_type = node_type.type

        if node_type == 'int':
            return z3.Int(node.name)
        elif node_type == 'float':
            return z3.Real(node.name)
        elif node_type == 'boolean':
            return z3.Bool(node.name)
    elif isinstance(node, Expression):
        return parse(node.expr, ctx, solver)
    elif isinstance(node, Add):
        left = parse(node.left, ctx, solver)
        right = parse(node.right, ctx, solver)

        return (left, right)