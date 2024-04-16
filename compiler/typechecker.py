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
        if ctx.has_var(node.name):
            raise TypeError(f"Variavel {node.name} ja foi declarada")
        # Set the variable type in the context
        ctx.set_type(node.name, node.type)
        # Verify the value of the variable
        verify(node.value, ctx)
    elif isinstance(node, VariableAssignment):
        # Verify the value of the variable
        verify(node.value, ctx)
    elif isinstance(node, (
        Or or
        And or
        Equality or
        Compare or
        Add or
        Sub or
        Mult
    )):
        # Verify the left and right expressions
        verify(node.left, ctx)
        verify(node.right, ctx)
    elif isinstance(node, Unary):
        verify(node.expr, ctx)
