from context import Context
from plush_ast import *

type_map = {
    'int': Int,
    'float': Float,
    'string': String,
    'char': Char,
    'boolean': Boolean,
    'array': Array,
}

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
        expr_type = verify(node.value, ctx)

        if expr_type != type_map[node.type]:
            raise TypeError(f"Tipos incompatíveis: {expr_type} e {type_map[node.type]}")
    elif isinstance(node, VariableAssignment):
        # Check if the variable is not declared
        if not ctx.has_var(node.name):
            raise TypeError(f"Variavel {node.name} nao foi declarada")
        # Verify the value of the variable
        expr_type = verify(node.value, ctx)

        if expr_type != type_map[ctx.get_type(node.name)]:
            raise TypeError(f"Tipos incompatíveis: {expr_type} e {type_map[ctx.get_type(node.name)]}")
    elif isinstance(node, Expression):
        return verify(node.expr, ctx)
    elif isinstance(node, (
        Or,
        And
    )):
        # Verify the left and right expressions
        right = verify(node.right, ctx)
        left = verify(node.left, ctx)

        if right != Boolean:
            raise TypeError(f"Tipo incompatível: {right}")

        if left != Boolean:
            raise TypeError(f"Tipo incompatível: {left}")

        if type(right) != type(left):
            raise TypeError(f"Tipos incompatíveis: {type(right)} e {type(left)}")
        
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
        
        return right
    elif isinstance(node, (
        Add,
        Sub,
        Mult
    )):
        # Verify the left and right expressions
        right = verify(node.right, ctx)
        left = verify(node.left, ctx)

        if right not in (Int, Float, Expression):
            raise TypeError(f"Tipo incompatível: {right}")
        
        if left not in (Int, Float, Expression):
            raise TypeError(f"Tipo incompatível: {left}")

        if right != left:
            raise TypeError(f"Tipos incompatíveis: {right} e {left}")
        
        return right
    elif isinstance(node, Unary):
        verify(node.expr, ctx)
    elif isinstance(node, (
        Int,
        Float,
        String,
        Char,
        Boolean
    )):
        return type(node)
    elif isinstance(node, VariableAccess):
        if not ctx.has_var(node.name):
            raise TypeError(f"Variavel {node.name} nao foi declarada")
        return type_map[ctx.get_type(node.name)]
    elif isinstance(node, FunctionDeclaration):
        # Check if the function is already declared
        if ctx.has_var(node.name):
            raise TypeError(f"Funcao {node.name} ja foi declarada")
        # Set the function type in the context
        ctx.set_type(node.name, node.type)
        # Enter a new scope
        ctx.enter_scope()
        for param in node.parameters.parameters:
            ctx.set_type(param.name, param.type)
        # Verify the function body
        verify(node.instructions, ctx)
        # Exit the scope
        ctx.exit_scope()
