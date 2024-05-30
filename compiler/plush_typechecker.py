from z3 import *
from plush_ast import *
from context import Context
from liquid_typechecker import liquid_typecheck, parse

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
        if ctx.has_var_in_current_scope(node.name):
            raise TypeError(f"Variable {node.name} already declared!")
        # Verify the value of the variable
        expr_type = verify(node.value, ctx)

        node_type = node.type

        if not isinstance(node_type, LiquidType):
            if isinstance(expr_type, LiquidType):
                if expr_type.type != node_type:
                    raise TypeError(f"Incompatible types: {node_type} and {expr_type}")
            elif isinstance(expr_type, str) and expr_type[0] == '[':
                if expr_type != node.type:
                    raise TypeError(f"Incompatible types: {node.type} and {expr_type}")
            elif expr_type != node_type:
                raise TypeError(f"Incompatible types: {node_type} and {expr_type}")
            
            if isinstance(node.value.expr, (Int, Float, Boolean, Char, Unary)):
                ctx.set_liquid_type(node.name, Equality('=', VariableAccess(node.name), node.value.expr))

            if isinstance(node.value.expr, VariableAccess):
                ctx.set_liquid_type(node.name, Equality('=', VariableAccess(node.name), node.value.expr))

            if isinstance(node.value.expr, FunctionCall):
                ctx.set_liquid_type(node.name, Equality('=', VariableAccess(node.name), VariableAccess(node.value.expr.name)))

            ctx.set_type(node.name, node.type)
        else:
            if isinstance(node.value.expr, (Int, Float, Boolean, Char, Unary)):
                if node_type.type != expr_type:
                    raise TypeError(f"Incompatible types: {node_type.type} and {expr_type}")

                ctx.set_liquid_type(node.name, node.type.predicate)
                ctx.set_liquid_type(node.name, Equality('=', VariableAccess(node.name), node.value.expr))
                verify_liquid_type(node, ctx)
            elif isinstance(node.value.expr, VariableAccess):  

                if not isinstance(expr_type, LiquidType):
                    if expr_type != node_type.type:
                        raise TypeError(f"Incompatible types: {node_type.type} and {expr_type}")
                else:
                    if node_type.type != expr_type.type:
                        raise TypeError(f"Incompatible types: {node_type.type} and {expr_type.type}")

                if ctx.has_liquid(node.value.expr.name):
                    variable_clauses = ctx.get_liquid_type(node.value.expr.name)

                    for clause in variable_clauses:
                        ctx.set_liquid_type(node.name, clause)

                ctx.set_liquid_type(node.name, node.type.predicate)
                ctx.set_liquid_type(node.name, Equality('=', VariableAccess(node.name), VariableAccess(node.value.expr.name)))

                if isinstance(expr_type, str):
                    if expr_type != node.type.type:
                        raise TypeError(f"Incompatible types: {node_type.type} and {expr_type}")
                elif isinstance(expr_type, LiquidType):
                    if expr_type.type != node_type.type:
                        raise TypeError(f"Incompatible types: {node_type.type} and {expr_type.type}")

                verify_liquid_type(node, ctx)

                value_clauses = ctx.get_liquid_type(node.value.expr.name)

                for clause in value_clauses:
                    ctx.set_liquid_type(node.name, clause)
            elif isinstance(node.value.expr, FunctionCall):
                ctx.set_type(node.name, node.type)

                if not isinstance(expr_type, LiquidType):
                    raise TypeError(f"Function call {node.value.expr.name} does not return a liquid type!")
                else:
                    if node_type.type != expr_type.type:
                        raise TypeError(f"Incompatible types: {node_type.type} and {expr_type.type}")
                    
                ctx.set_liquid_type(node.name, node.type.predicate)
                ctx.set_liquid_type(node.name, Equality('=', VariableAccess(node.name), VariableAccess(node.value.expr.name)))

                verify_liquid_type(node, ctx)
            elif isinstance(node.value.expr, Add):
                ctx.set_type(node.name, node.type)
                left_type = verify(node.value.expr.left, ctx)
                right_type = verify(node.value.expr.right, ctx)

                if isinstance(node.value.expr.left.expr, (Add, Sub, Mult)) or isinstance(node.value.expr.right.expr, (Add, Sub, Mult)):
                    raise TypeError(f"Liquid typechecking only supported for binary sum operations!")

                if isinstance(left_type, LiquidType):
                    if isinstance(right_type, LiquidType):
                        if left_type.type != right_type.type:
                            raise TypeError(f"Incompatible types: {left_type.type} and {right_type.type}")
                    else:
                        if left_type.type != right_type:
                            raise TypeError(f"Incompatible types: {left_type.type} and {right_type}")
                else:
                    if isinstance(right_type, LiquidType):
                        if left_type != right_type.type:
                            raise TypeError(f"Incompatible types: {left_type} and {right_type.type}")
                    else:
                        if left_type != right_type:
                            raise TypeError(f"Incompatible types: {left_type} and {right_type}")
                
                if isinstance(node_type, LiquidType):
                    if isinstance(left_type, LiquidType):
                        if left_type.type != node_type.type:
                            raise TypeError(f"Incompatible types: {left_type.type} and {node_type.type}")
                    else:
                        if left_type != node_type.type:
                            raise TypeError(f"Incompatible types: {left_type} and {node_type.type}")
                else:
                    if isinstance(left_type, LiquidType):
                        if left_type.type != node_type:
                            raise TypeError(f"Incompatible types: {left_type.type} and {node_type}")
                    else:
                        if left_type != node_type:
                            raise TypeError(f"Incompatible types: {left_type} and {node_type}")
                
                solver = Solver()

                if isinstance(node_type, LiquidType):
                    solver = liquid_typecheck(solver, node_type.predicate, ctx)

                if isinstance(node.value.expr.left.expr, VariableAccess):
                    solver = liquid_typecheck(solver, left_type.predicate, ctx)

                    left_clauses = ctx.get_liquid_type(node.value.expr.left.expr.name)

                    for clause in left_clauses:
                        liquid_typecheck(solver, clause, ctx)
                else:
                    if not isinstance(node.value.expr.left.expr, (Int, Float, Unary)):
                        raise TypeError(f"Liquid typechecking not supported for this operation: {node.value.expr.left}")
                
                if isinstance(node.value.expr.right.expr, VariableAccess):
                    solver = liquid_typecheck(solver, right_type.predicate, ctx)

                    right_clauses = ctx.get_liquid_type(node.value.expr.right.expr.name)

                    for clause in right_clauses:
                        liquid_typecheck(solver, clause, ctx)
                else:
                    if not isinstance(node.value.expr.right.expr, (Int, Float, Unary)):
                        raise TypeError(f"Liquid typechecking not supported for this operation: {node.value.expr.right}")

                sum_components = parse(node.value.expr, ctx, solver)

                var_sum = ""

                if isinstance(node_type, LiquidType):
                    if node_type.type == 'int':
                        var_sum = z3.Int(node.name)
                    elif node_type.type == 'float':
                        var_sum = z3.Real(node.name)
                else:
                    if node_type == 'int':
                        var_sum = z3.Int(node.name)
                    elif node_type == 'float':
                        var_sum = z3.Real(node.name)

                solver.add(var_sum == sum_components[0] + sum_components[1])

                if solver.check() == unsat:
                    raise TypeError(f"Variable {node.name} does not satisfy the liquid type!")
                
                ctx.set_liquid_type(node.name, node.type.predicate)
            else:
                raise TypeError(f"Liquid typechecking not supported for this operation: {node.value.expr}")
        
        if node.declaration_type == 'VAL':    
            ctx.set_constant_type(node.name, node.declaration_type)
    elif isinstance(node, VariableAssignment):
        # Check if the variable is not declared
        if not ctx.has_var(node.name):
            raise TypeError(f"Variable {node.name} not declared!")
        
        if ctx.has_const(node.name):
            raise TypeError(f"Cannot assign to a constant variable {node.name}!")
        
        expr_type = verify(node.value, ctx)

        var_type = ctx.get_type(node.name)

        if not isinstance(var_type, LiquidType):
            if isinstance(expr_type, LiquidType):
                raise TypeError(f"Variable {node.name} does not have a liquid type!")
            else:
                if expr_type != var_type:
                    raise TypeError(f"Incompatible types: {var_type} and {expr_type}")
        else:
            if not isinstance(expr_type, LiquidType):
                if expr_type != var_type.type:
                    raise TypeError(f"Incompatible types: {var_type.type} and {expr_type}")
            else:
                if expr_type.type != var_type.type:
                    raise TypeError(f"Incompatible types: {var_type.type} and {expr_type.type}")

            if isinstance(node.value.expr, VariableAccess):
                ctx.reset_liquid_type_clauses(node.name)
                ctx.set_liquid_type(node.name, Equality('=', VariableAccess(node.name), node.value.expr))
                verify_liquid_type(node, ctx)

                value_clauses = ctx.get_liquid_type(node.value.expr.name)

                for clause in value_clauses:
                    ctx.set_liquid_type(node.name, clause)
                    
            elif isinstance(node.value.expr, (Int, Float, Unary)):
                ctx.reset_liquid_type_clauses(node.name)
                ctx.set_liquid_type(node.name, Equality('=', VariableAccess(node.name), node.value.expr))
                verify_liquid_type(node, ctx)
            else:
                raise TypeError(f"Liquid typechecking not supported for this operation: {node.value}")
        
    elif isinstance(node, Expression):
        expr_type = verify(node.expr, ctx)
        node.type = expr_type
        
        return expr_type
    elif isinstance(node, (
        Or,
        And
    )):
        # Verify the left and right expressions
        right = verify(node.right, ctx)
        left = verify(node.left, ctx)

        if right != "boolean":
            raise TypeError(f"Incompatible type: {right}")

        if left != "boolean":
            raise TypeError(f"Incompatible type: {left}")

        if right != left:
            raise TypeError(f"Incompatible types: {right} and {left}")
        
        return right
    elif isinstance(node, (
        Equality,
        Compare
    )):
        # Verify the left and right expressions
        right = verify(node.right, ctx)
        left = verify(node.left, ctx)

        if isinstance(right, LiquidType):
            right = right.type
        
        if isinstance(left, LiquidType):
            left = left.type

        if right != left:
            raise TypeError(f"Tipos incompatíveis: {right} e {left}")
        
        return "boolean"
    elif isinstance(node, (
        Add,
        Sub,
        Mult
    )):
        # Verify the left and right expressions
        right = verify(node.right, ctx)
        left = verify(node.left, ctx)

        if isinstance(right, LiquidType):
            right = right.type
        
        if isinstance(left, LiquidType):
            left = left.type
        
        if isinstance(node, (Add, Sub)) or (isinstance(node, Mult) and node.operator in ['*', '/', '^']):
            if right not in ("int", "float", Expression):
                raise TypeError(f"Incompatible type: {right}")
            
            if left not in ("int", "float", Expression):
                raise TypeError(f"Incompatible type: {left}")
        elif isinstance(node, Mult) and node.operator in ['%']:
            if right not in ("int", Expression):
                raise TypeError(f"Incompatible type: {right}")
            
            if left not in ("int", Expression):
                raise TypeError(f"Incompatible type: {left}")

        if right != left:
            raise TypeError(f"Incompatible types: {right} and {left}")
        
        return right
    elif isinstance(node, Unary):
        return verify(node.expr, ctx)
    elif isinstance(node, (
        Int,
        Float,
        String,
        Char,
        Boolean
    )):
        return type_to_str(type(node))
    elif isinstance(node, VariableAccess):
        if not ctx.has_var(node.name):
            raise TypeError(f"Variable {node.name} not declared!")
        
        return ctx.get_type(node.name)
    elif isinstance(node, IfStatement):
        expr_type = verify(node.condition, ctx)

        if expr_type != "boolean":
            raise TypeError(f"If conditions must have type booean! Not type {expr_type}!")

        ctx.enter_liquid_scope()
        ctx.enter_const_scope()
        ctx.enter_scope()
        verify(node.then_block, ctx)
        ctx.exit_scope()
        ctx.exit_const_scope()
        ctx.exit_liquid_scope()
        if node.else_block.instructions:
            ctx.enter_liquid_scope()
            ctx.enter_const_scope()
            ctx.enter_scope()
            verify(node.else_block, ctx)
            ctx.exit_scope()
            ctx.exit_const_scope()
            ctx.exit_liquid_scope()
    elif isinstance(node, ThenBlock):
        for instruction in node.instructions:
            verify(instruction, ctx)
    elif isinstance(node, ElseBlock):
        for instruction in node.instructions:
            verify(instruction, ctx)
    elif isinstance(node, WhileStatement):
        expr_type = verify(node.condition, ctx)

        if expr_type != "boolean":
            raise TypeError(f"If conditions must have type booean! Not type {expr_type}!")

        ctx.enter_liquid_scope()
        ctx.enter_const_scope()
        ctx.enter_scope()
        for instruction in node.code_block:
            verify(instruction, ctx)
        ctx.exit_scope()
        ctx.exit_const_scope()
        ctx.exit_liquid_scope()
    elif isinstance(node, FunctionDeclaration):
        if ctx.has_function(node.name):
            raise TypeError(f"Function {node.name} already declared!")
        
        if ctx.has_function_def(node.name):
            nr_args = ctx.get_function_def_nr_args(node.name)
            index_param = 0

            if not node.parameters and nr_args > 0:
                raise TypeError(f"Function {node.name} expects more arguments!")
            
            if len(node.parameters.parameters) > nr_args:
                raise TypeError(f"Function {node.name} expects less arguments!")

            if node.parameters:
                if node.parameters.parameters and nr_args == 0:
                    raise TypeError(f"Function {node.name} does not expect arguments!")

                # Check if the function declaration matches the function definition
                for param in node.parameters.parameters:
                    if ctx.get_type_function_def_param(node.name, index_param) != param.type:
                        raise TypeError(f"Incompatible types in function declaration {node.name}!")
                    index_param += 1
                    nr_args -= 1

            if nr_args != 0:
                raise TypeError(f"Function {node.name} expects more arguments!")
            
        ctx.enter_function_scope()
        ctx.enter_const_scope()
        ctx.enter_liquid_scope()
        ctx.set_type_function(node.name, node.type)

        if node.parameters:
            for param in node.parameters.parameters:
                ctx.set_type_function(param.name, param.type)

                if param.declaration_type == 'const':
                    ctx.set_const(param.name)

        # typecheck the actual function declaration

        ctx.enter_scope()

        ctx.set_type(node.name, node.type)

        if isinstance(node.type, LiquidType):
            ctx.set_liquid_type(node.name, node.type.predicate)
        
        if node.parameters:
            for param in node.parameters.parameters:
                ctx.set_type(param.name, param.type)

        for instruction in node.instructions.instructions:
            verify(instruction, ctx)

        ctx.exit_scope()
        ctx.exit_const_scope()
        ctx.exit_liquid_scope()

        if ctx.has_function(node.name) and ctx.has_function_def(node.name):
            if ctx.get_type_function(node.name) != ctx.get_type_function_def(node.name):
                raise TypeError(f"Incompatible types in function declaration {node.name}!")
        
        if isinstance(ctx.get_type_function(node.name), LiquidType):
            ctx.set_liquid_type(node.name, ctx.get_type_function(node.name).predicate)

    elif isinstance(node, FunctionDefinition):
        if ctx.has_function_def(node.name):
            raise TypeError(f"Function {node.name} already defined!")
        
        if ctx.has_function(node.name):
            raise TypeError(f"Cannot define a function that was already declared - function {node.name}")
        
        ctx.enter_function_def_scope()

        if isinstance(node.type, LiquidType):
            if node.type.type == 'void':
                raise TypeError(f"Cannot set a return liquid type for a void function!")
            if node.type.type.startswith('['):
                raise TypeError(f"Liquid typechecking for functions that return an array is not supported!")

        ctx.set_type_function_def(node.name, node.type)      
        
        if node.parameters:
            for param in node.parameters.parameters:
                ctx.set_type_function_def(param.name, param.type)
    elif isinstance(node, FunctionCall):
        if not ctx.has_function_def(node.name) and not ctx.has_function(node.name):
            raise TypeError(f"Function {node.name} not defined nor declared!")
        
        if ctx.has_function_def(node.name):
            if ctx.get_type_function_def(node.name) == 'void':
                raise TypeError(f"Function {node.name} returns void!")
            
            nr_args = ctx.get_function_def_nr_args(node.name)
            index_arg = 0

            if node.arguments.arguments and nr_args == 0:
                raise TypeError(f"Function {node.name} does not expect arguments!")

            if len(node.arguments.arguments) > nr_args:
                raise TypeError(f"Function {node.name} expects less arguments!")
            
            for argument in node.arguments.arguments:
                param_type = ctx.get_type_function_def_param(node.name, index_arg)
                arg_type = verify(argument.value, ctx)
                
                if isinstance(param_type, LiquidType):
                    if isinstance(argument.value.expr, (Int, Float, Unary)):
                        if param_type.type != arg_type:
                            raise TypeError(f"Incompatible types in function call {node.name}!")
                        
                    elif isinstance(argument.value.expr, VariableAccess):
                        if param_type.type != arg_type:
                            raise TypeError(f"Incompatible types in function call {node.name}!")
                        
                    else:
                        raise TypeError(f"Operation not supported for liquid typechecking in function call {node.name}!")
                else:
                    if isinstance(arg_type, LiquidType):
                        if param_type != arg_type.type:
                            raise TypeError(f"Incompatible types in function call {node.name}!")
                    else:
                        if param_type != arg_type:
                            raise TypeError(f"Incompatible types in function call {node.name}!")

                index_arg += 1
                nr_args -= 1
            
            if nr_args != 0:
                raise TypeError(f"Function {node.name} expects more arguments!")

            function_type = ctx.get_type_function_def(node.name)

        if ctx.has_function(node.name):
            nr_args = ctx.get_function_nr_args(node.name)
            index_arg = 0

            if node.arguments.arguments and nr_args == 0:
                raise TypeError(f"Function {node.name} does not expect arguments!")

            if len(node.arguments.arguments) > nr_args:
                raise TypeError(f"Function {node.name} expects less arguments!")

            ctx.enter_liquid_scope()

            for argument in node.arguments.arguments:
                param_type = ctx.get_type_function_param(node.name, index_arg)
                arg_type = verify(argument.value, ctx)
                
                if isinstance(param_type, LiquidType):
                    if isinstance(argument.value.expr, (Int, Float, Unary)):
                        if param_type.type != arg_type:
                            raise TypeError(f"Incompatible types in function call {node.name}!")
                        
                    elif isinstance(argument.value.expr, VariableAccess):
                        if isinstance(arg_type, LiquidType):
                            if isinstance(param_type, LiquidType):
                                if param_type.type != arg_type.type:
                                    raise TypeError(f"Incompatible types in function call {node.name}!")
                            else:
                                if param_type != arg_type.type:
                                    raise TypeError(f"Incompatible types in function call {node.name}!")
                        else:
                            if isinstance(param_type, LiquidType):
                                raise TypeError(f"Arguments in function call {node.name} must be liquid types when the function parameter is a liquid type!")

                            if param_type != arg_type:
                                raise TypeError(f"Incompatible types in function call {node.name}!")

                    else:
                        raise TypeError(f"Operation not supported for liquid typechecking in in the arguments of the function call {node.name}!")
        
                    ctx.set_liquid_type(ctx.get_name_function_param(node.name, index_arg), Equality('=', VariableAccess(ctx.get_name_function_param(node.name, index_arg)), argument.value.expr))
                else:
                    if isinstance(arg_type, LiquidType):
                        if param_type != arg_type.type:
                            raise TypeError(f"Incompatible types in function call {node.name}!")
                    else:
                        if param_type != arg_type:
                            raise TypeError(f"Incompatible types in function call {node.name}!")

                index_arg += 1
                nr_args -= 1
            
            verify_liquid_type(node, ctx)

            ctx.exit_liquid_scope()
            
            if nr_args != 0:
                raise TypeError(f"Function {node.name} expects more arguments!")
        
            function_type = ctx.get_type_function(node.name)

        return function_type
    
    elif isinstance(node, ProcedureCall):
        if not ctx.has_function_def(node.name) and not ctx.has_function(node.name):
            raise TypeError(f"Procedure {node.name} not defined nor declared!")
        
        if isExternalFunction(node.name):
            for argument in node.arguments.arguments:
                verify(argument.value, ctx)

        if ctx.has_function_def(node.name) and not isExternalFunction(node.name):

            if ctx.get_type_function_def(node.name) != 'void':
                raise TypeError(f"Procedure {node.name} must be of type void!")

            nr_args = ctx.get_function_def_nr_args(node.name)
            index_param = 0

            if node.arguments.arguments and nr_args == 0:
                raise TypeError(f"Procedure {node.name} does not expect arguments!")
            
            if len(node.arguments.arguments) > nr_args:
                raise TypeError(f"Procedure {node.name} expects less arguments!")
            
            for argument in node.arguments.arguments:
                param_type = ctx.get_type_function_def_param(node.name, index_param)
                arg_type = verify(argument.value, ctx)
                
                if isinstance(param_type, LiquidType):
                    if isinstance(argument.value.expr, (Int, Float, Unary)):
                        if param_type.type != arg_type:
                            raise TypeError(f"Incompatible types in function call {node.name}!")
                        
                    elif isinstance(argument.value.expr, VariableAccess):
                        if isinstance(arg_type, LiquidType):
                            if param_type.type != arg_type.type:
                                raise TypeError(f"Incompatible types in function call {node.name}!")
                        else:
                            if param_type.type != arg_type:
                                raise TypeError(f"Incompatible types in function call {node.name}!")
                        
                    else:
                        raise TypeError(f"Operation not supported for liquid typechecking in the arguments of the procedure call {node.name}!")
                else:
                    if isinstance(arg_type, LiquidType):
                        if param_type != arg_type.type:
                            raise TypeError(f"Incompatible types in function call {node.name}!")
                    else:
                        if param_type != arg_type:
                            raise TypeError(f"Incompatible types in function call {node.name}!")

                index_param += 1
                nr_args -= 1
            
            if nr_args != 0:
                raise TypeError(f"Procedure {node.name} expects more arguments!")
            
        if ctx.has_function(node.name):
            nr_args = ctx.get_function_nr_args(node.name)
            index_param = 0

            if node.arguments.arguments and nr_args == 0:
                raise TypeError(f"Function {node.name} does not expect arguments!")
            
            if len(node.arguments.arguments) > nr_args:
                raise TypeError(f"Function {node.name} expects less arguments!")

            ctx.enter_liquid_scope()

            for argument in node.arguments.arguments:
                param_type = ctx.get_type_function_param(node.name, index_param)
                arg_type = verify(argument.value, ctx)
                
                if isinstance(param_type, LiquidType):
                    if isinstance(argument.value.expr, (Int, Float, Unary)):
                        if param_type.type != arg_type:
                            raise TypeError(f"Incompatible types in function call {node.name}!")
                        
                    elif isinstance(argument.value.expr, VariableAccess):
                        if isinstance(arg_type, LiquidType):
                            if param_type.type != arg_type.type:
                                raise TypeError(f"Incompatible types in function call {node.name}!")
                        else:
                            if param_type.type != arg_type:
                                raise TypeError(f"Incompatible types in function call {node.name}!")
                        
                    else:
                        raise TypeError(f"Operation not supported for liquid typechecking in function call {node.name}!")
                
                    ctx.set_liquid_type(ctx.get_name_function_param(node.name, index_param), Equality('=', VariableAccess(ctx.get_name_function_param(node.name, index_param)), argument.value.expr))
                else:
                    if isinstance(arg_type, LiquidType):
                        if param_type != arg_type.type:
                            raise TypeError(f"Incompatible types in function call {node.name}!")
                    else:
                        if param_type != arg_type:
                            raise TypeError(f"Incompatible types in function call {node.name}!")

                index_param += 1
                nr_args -= 1
            
            verify_liquid_type(node, ctx)

            ctx.exit_liquid_scope()

            if nr_args != 0:
                raise TypeError(f"Function {node.name} expects more arguments!")
            
    elif isinstance(node, ArrayAccess):
        if isinstance(node.identifier, VariableAccess):
            if not ctx.has_var(node.identifier.name):
                raise TypeError(f"Variable {node.identifier.name} not declared!")
            idenfier_type = ctx.get_type(node.identifier.name)
        elif isinstance(node.identifier, FunctionCall):
            verify(node.identifier, ctx)
            if ctx.has_function(node.identifier.name):
                idenfier_type = ctx.get_type_function(node.identifier.name)
            elif ctx.has_function_def(node.identifier.name):
                idenfier_type = ctx.get_type_function_def(node.identifier.name)

        if idenfier_type[0] != '[':
            raise TypeError(f"Variable {node.identifier.name} is not an array!")
        
        rec_l_paren_counter = 0
        index = 0

        while idenfier_type[index] == '[':
            rec_l_paren_counter += 1
            index += 1

        number_input_indexes = len(node.indexes.indexes)

        if number_input_indexes > rec_l_paren_counter:
            raise TypeError(f"Too many indexes in array access {node.identifier.name}!")
        
        for index in node.indexes.indexes:
            if verify(index.value, ctx) != "int":
                raise TypeError(f"Array indexes must be of type int!")
        
        return_type = idenfier_type

        while number_input_indexes > 0:
            return_type = return_type[1:-1]
            number_input_indexes -= 1
        
        return return_type
    elif isinstance(node, ArrayVariableAssigment):
        array_variable_type = verify(node.left, ctx)
        value_type = verify(node.right, ctx)

        if array_variable_type != value_type:
            raise TypeError(f"Incompatible types: {array_variable_type} and {value_type}")
    elif isinstance(node, Array):
        result = list_to_string(covert_types_to_string(getArrayType(node, ctx)))

        processed_result = delete_duplicates(result)

        return processed_result
    
    return node


def getArrayType(array, ctx):
    seen_elements = set()

    def deleteRepeatedTypes(array):
        if isinstance(array, Array):
            seen_elements.clear()
            for i in range(len(array.content)):
                array.content[i] = deleteRepeatedTypes(array.content[i])
        else:
            type = verify(array, ctx)
            if type in seen_elements:
                return None
            seen_elements.add(type)
            return type

        return remove_duplicates(remove_nones(array.content))
    
    return deleteRepeatedTypes(array)

def remove_nones(lst):
    if isinstance(lst, list):
        return [remove_nones(item) for item in lst if item is not None]
    else:
        return lst
    
def remove_duplicates(lst):
    seen = set()
    result = []

    for item in lst:
        if isinstance(item, list):
            items = remove_duplicates(item)
            items = tuple(items)
        else:
            items = item

        if items not in seen:
            result.append(item)
            seen.add(items)

    return result

def type_to_str(node):
    if node == Int:
        return 'int'
    elif node == Float:
        return 'float'
    elif node == String:
        return 'string'
    elif node == Char:
        return 'char'
    elif node == Boolean:
        return 'boolean'
    return node

def list_to_string(lst):
    def convert_to_string(item):
        if isinstance(item, list):
            inner_strings = [convert_to_string(sub_item) for sub_item in item]
            return '[' + ','.join(inner_strings) + ']'
        else:
            return str(item)

    return convert_to_string(lst)
    
def covert_types_to_string(lst):
    def convert_to_type_string(item):
        if isinstance(item, list):
            inner_types = [convert_to_type_string(sub_item) for sub_item in item]
            return inner_types
        else:
            return type_to_str(item)

    return convert_to_type_string(lst)

def delete_duplicates(lst):
    content = lst[1:-1].split(',')

    seen = set()
    result = []

    for item in content:
        if item not in seen:
            result.append(item)
            seen.add(item)
    
    return '[' + ', '.join(result) + ']'

def isExternalFunction(name):
    return name in ['printf']

def verify_liquid_type(node, ctx: Context):
    if isinstance(node, VariableDeclaration):
        ctx.set_type(node.name, node.type)
        
    if isinstance(node, (ProcedureCall, FunctionCall)):
        for param_index in range(len(node.arguments.arguments)):
            if ctx.has_function(node.name):
                solver = Solver()
                
                predicate_param = ctx.get_type_function_param(node.name, param_index)

                if not isinstance(predicate_param, LiquidType):
                    continue

                predicate_arg = ctx.get_liquid_type(ctx.get_name_function_param(node.name, param_index))

                if isinstance(node.arguments.arguments[param_index].value.expr, VariableAccess):
                    previous_arg_clauses = ctx.get_liquid_type(node.arguments.arguments[param_index].value.expr.name)

                    for clause in previous_arg_clauses:
                        solver = liquid_typecheck(solver, clause, ctx)

                ctx.enter_scope()
                ctx.set_type(ctx.get_name_function_param(node.name, param_index), predicate_param.type)

                for clause in predicate_arg:
                    solver = liquid_typecheck(solver, clause, ctx)  

                solver = liquid_typecheck(solver, predicate_param.predicate, ctx)

                ctx.exit_scope()

                if solver.check() == unsat:
                    raise TypeError(f"Something went wrong with the liquid typechecking of the function/procedure call {node.name}!")
            
            param_index += 1
    elif isinstance(node.value.expr, FunctionCall):
        function_predicate = ctx.get_liquid_type(node.value.expr.name)
        variable_predicate = ctx.get_liquid_type(node.name)

        solver = Solver()

        function_return_type = ctx.get_type_function(node.value.expr.name)
        variable_type = ctx.get_type(node.name)

        liquid_typecheck(solver, function_return_type.predicate, ctx)
        liquid_typecheck(solver, variable_type.predicate, ctx)
        liquid_typecheck(solver, Equality('=', VariableAccess(node.name), VariableAccess(node.value.expr.name)), ctx)

        if solver.check() == unsat:
            raise TypeError(f"Variable {node.name} does not satisfy the liquid type!")

        solver = Solver()

        for clause in variable_predicate:
            solver = liquid_typecheck(solver, clause, ctx)

        for clause in function_predicate:
            solver = liquid_typecheck(solver, clause, ctx)

        if solver.check() == unsat:
            raise TypeError(f"Variable {node.name} does not satisfy the liquid type!")
        
    elif isinstance(node.value.expr, VariableAccess):
        if not ctx.has_liquid(node.value.expr.name):
            raise TypeError(f"Variable {node.value.expr.name} does not have a liquid type!")
        
        value_predicate = ctx.get_liquid_type(node.value.expr.name)

        solver = Solver()

        variable_predicate = ctx.get_liquid_type(node.name)

        for clause in variable_predicate:
            solver = liquid_typecheck(solver, clause, ctx)

        for clause in value_predicate:
            solver = liquid_typecheck(solver, clause, ctx)

        if solver.check() == unsat:
            raise TypeError(f"Variable {node.name} does not satisfy the liquid type!")
    elif isinstance(node.value.expr, (Int, Float, Boolean, Char, Unary)):
        solver = Solver()

        variable_predicate = ctx.get_liquid_type(node.name)

        for clause in variable_predicate:
            solver = liquid_typecheck(solver, clause, ctx)

        if solver.check() == unsat:
            raise TypeError(f"Variable {node.name} does not satisfy the liquid type!")
    
def uniformize_variables_predicate_param(predicate, variable_name_to_replace):
    if isinstance(predicate, (Equality, Compare, And, Or)):
        result_left = uniformize_variables_predicate_param(predicate.left, variable_name_to_replace)
        result_right = uniformize_variables_predicate_param(predicate.right, variable_name_to_replace)

        if isinstance(predicate, Equality):
            return Equality(predicate.operator, result_left, result_right)
        elif isinstance(predicate, Compare):
            return Compare(predicate.operator, result_left, result_right)
        elif isinstance(predicate, And):
            return And(result_left, result_right)
        elif isinstance(predicate, Or):
            return Or(result_left, result_right)
    elif isinstance(predicate, VariableAccess):
        return VariableAccess(variable_name_to_replace)
    elif isinstance(predicate, Expression):
        return uniformize_variables_predicate_param(predicate.expr, variable_name_to_replace)

    return predicate