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
            raise TypeError(f"Variable {node.name} already declared!")
        # Set the variable type in the context
        ctx.set_type(node.name, node.type)
        # Verify the value of the variable
        expr_type = verify(node.value, ctx)

        if expr_type != type_map[node.type]:
            raise TypeError(f"Incompatible types: {expr_type} and {type_map[node.type]}")
    elif isinstance(node, VariableAssignment):
        # Check if the variable is not declared
        if not ctx.has_var(node.name):
            raise TypeError(f"Variable {node.name} not declared!")
        # Verify the value of the variable
        expr_type = verify(node.value, ctx)

        if expr_type != type_map[ctx.get_type(node.name)]:
            raise TypeError(f"Incompatible types: {expr_type} and {type_map[ctx.get_type(node.name)]}")
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
            raise TypeError(f"Incompatible type: {right}")

        if left != Boolean:
            raise TypeError(f"Incompatible type: {left}")

        if type(right) != type(left):
            raise TypeError(f"Incompatible types: {type(right)} and {type(left)}")
        
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
        
        return Boolean
    elif isinstance(node, (
        Add,
        Sub,
        Mult
    )):
        # Verify the left and right expressions
        right = verify(node.right, ctx)
        left = verify(node.left, ctx)

        if right not in (Int, Float, Expression):
            raise TypeError(f"Incompatible type: {right}")
        
        if left not in (Int, Float, Expression):
            raise TypeError(f"Incompatible type: {left}")

        if right != left:
            raise TypeError(f"Incompatible types: {right} and {left}")
        
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
            raise TypeError(f"Variable {node.name} not declared!")
        return type_map[ctx.get_type(node.name)]
    elif isinstance(node, IfStatement):
        expr_type = verify(node.condition, ctx)

        if expr_type != Boolean:
            raise TypeError(f"If conditions must have type booean! Not type {expr_type}!")

        verify(node.then_block, ctx)
        if node.else_block.instructions:
            verify(node.else_block, ctx)
    elif isinstance(node, ThenBlock):
        for instruction in node.instructions:
            verify(instruction, ctx)
    elif isinstance(node, ElseBlock):
        for instruction in node.instructions:
            verify(instruction, ctx)
    elif isinstance(node, WhileStatement):
        expr_type = verify(node.condition, ctx)

        if expr_type != Boolean:
            raise TypeError(f"If conditions must have type booean! Not type {expr_type}!")

        for instruction in node.code_block:
            verify(instruction, ctx)
    elif isinstance(node, FunctionDeclaration):
        if ctx.has_function(node.name):
            raise TypeError(f"Function {node.name} already declared!")
        
        if not ctx.has_function_def(node.name):
            # Save the function for function call typecheking
            ctx.enter_function_scope()
            ctx.set_type_function(node.name, node.type)      

            for param in node.parameters.parameters:
                ctx.set_type_function(param.name, param.type)
        else:
            index_param = 0

            # Check if the function declaration matches the function definition
            for param in node.parameters.parameters:
                if ctx.get_type_function_def_param(node.name, index_param) != param.type:
                    raise TypeError(f"Incompatible types in function declaration {node.name}!")
                index_param += 1

        # typecheck the actual function declaration

        ctx.enter_scope()

        ctx.set_type(node.name, node.type)
        
        for param in node.parameters.parameters:
            ctx.set_type(param.name, param.type)

        for instruction in node.instructions.instructions:
            verify(instruction, ctx)

        ctx.exit_scope()

    elif isinstance(node, FunctionDefinition):
        if ctx.has_function_def(node.name):
            raise TypeError(f"Function {node.name} already defined!")
        
        if ctx.has_function(node.name):
            raise TypeError(f"Cannot define a function that was already declared - function {node.name}")
        
        ctx.enter_function_def_scope()
        ctx.set_type_function_def(node.name, node.type)      

        for param in node.parameters.parameters:
            ctx.set_type_function_def(param.name, param.type)