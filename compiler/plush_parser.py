from plush_ast import *

class ParsingException(Exception):
    pass

def parse(tokens):
    stream = tokens

    def lookahead():
        if stream:
            return stream[0][0]
        else:
            return None
    
    def eat(token_type):
        if lookahead() == token_type:
            h = stream[0]
            stream.pop(0)
            return h
        else:
            raise ParsingException()
        
    def S():
        return Program(STATEMENT_FUNCTION_LIST())

    def STATEMENT_FUNCTION_LIST(result = list()):

        if lookahead() in ['VAR', 'VAL', 'IDENTIFIER']:
            result.append(STATEMENT())
            STATEMENT_FUNCTION_LISTp(result)
        elif lookahead() == 'FUNCTION':
            result.append(FUNCTION())
            STATEMENT_FUNCTION_LISTp(result)
        else:
            raise ParsingException()
        
        return InstructionList(result)
        
    def FUNCTION():
        if lookahead() == 'FUNCTION':
            eat('FUNCTION')
            name = eat('IDENTIFIER')
            eat('LPAREN')
            parameters = FUNCTION_DECLARATION_PARAMETERS()
            eat('RPAREN')
            eat('COLON')
            type = TYPE()
            instructions = FUNCTIONp()

            if not instructions:
                return FunctionDefinition(
                    name = name[1],
                    parameters = parameters,
                    type = type
                )

            return FunctionDeclaration(
                name = name[1],
                parameters = parameters,
                type = type,
                instructions = instructions
            )
        else:
            raise ParsingException()
        
    def FUNCTIONp():
        if lookahead() == 'LCURLYPAREN':
            eat('LCURLYPAREN')
            instructions = FUNCTION_STATEMENT_LIST(list())
            eat('RCURLYPAREN')
            return InstructionList(instructions)
        elif lookahead() == 'SEMICOLON':
            eat('SEMICOLON')
            return list()
        else:
            raise ParsingException()
        
    def FUNCTION_DECLARATION_PARAMETERS():
        if lookahead() in ['VAL', 'VAR']:
            return FUNCTION_DECLARATION_PARAMETER_LIST(list())
        else:
            pass
    
    def FUNCTION_DECLARATION_PARAMETER_LIST(parameters=list()):
        if lookahead() in ['VAL', 'VAR']:
            parameters.append(FUNCTION_PARAMETER())
            FUNCTION_DECLARATION_PARAMETER_LISTp(parameters)

            return ParameterList(parameters)
        else:
            raise ParsingException()
        
    def FUNCTION_PARAMETER():
        if lookahead() in ['VAL', 'VAR']:
            declaration_type = lookahead()
            VDECLARATION()
            name = eat('IDENTIFIER')
            eat('COLON')
            type = TYPE()

            return Parameter(
                declaration_type = declaration_type,
                name = name[1],
                type = type
            )
        else:
            raise ParsingException()
        
    def FUNCTION_DECLARATION_PARAMETER_LISTp(parameters):
        if lookahead() == 'COMMA':
            eat('COMMA')
            FUNCTION_DECLARATION_PARAMETER_LIST(parameters)
        else:
            pass

    def FUNCTION_STATEMENT_LIST(instructions=list()):
        if lookahead() in ['VAR', 'VAL', 'IF', 'WHILE', 'IDENTIFIER']:
            instructions.append(FUNCTION_STATEMENT())
            FUNCTION_STATEMENT_LIST(instructions)
        else:
            pass
        
        return instructions
    
    def FUNCTION_STATEMENT():
        if lookahead() in ['VAR', 'VAL']:
            return VARIABLE_DECLARATION()
        elif lookahead() == 'IDENTIFIER':
            return IDENTIFIER_ACCESS()
        elif lookahead() == 'IF':
            return IF_STATEMENT()
        elif lookahead() == 'WHILE':
            return WHILE()
        #elif lookahead() == 'RETURN':
        #    RETURN()
        else:
            raise ParsingException()
    
    #def RETURN():
    #    if lookahead() == 'RETURN':
    #        eat('RETURN')
    #        OPERATION()
    #        eat('SEMICOLON')
    #    else:
    #        raise ParsingException()

    def STATEMENT():
        if lookahead() in ['VAR', 'VAL']:
            return VARIABLE_DECLARATION()
        elif lookahead() == 'IDENTIFIER':
            return IDENTIFIER_ACCESS(False)
        else:
            raise ParsingException()
        
    def IDENTIFIER_ACCESS(isFunction = True):
        if lookahead() == 'IDENTIFIER':
            name = eat('IDENTIFIER')
            return IDENTIFIER_ACCESSp(name, isFunction)
        else:
            raise ParsingException()
        
    def IDENTIFIER_ACCESSp(name, isFunction=True):
        if lookahead() == 'ASSIGNMENT':
            eat('ASSIGNMENT')
            expr = OPERATION()
            eat('SEMICOLON')

            return VariableAssignment(
                name = name[1],
                value = expr
            )
        elif isFunction and lookahead() == 'LPAREN':
            return PROCEDURE_CALL(name)
        elif not isFunction and lookahead() == 'LPAREN':
            raise ParsingException()
        elif lookahead() == 'LRECPAREN':
            indexes = ARRAY_ACCESS(list())
            eat('ASSIGNMENT')
            expr = OPERATION()
            eat('SEMICOLON')

            return ArrayVariableAssigment(
                left = ArrayAccess(
                    name = name[1],
                    indexes = indexes
                ),
                right = expr
            )
        else:
            raise ParsingException()

    def PROCEDURE_CALL(name):
        if lookahead() == 'LPAREN':
            eat('LPAREN')
            arguments = FUNCTION_PARAMETER_LIST(list())
            eat('RPAREN')
            eat('SEMICOLON')

            return ProcedureCall(
                name = name[1],
                arguments = arguments
            )
        else:
            raise ParsingException()

    def STATEMENT_FUNCTION_LISTp(result):
        if lookahead() in ['VAR', 'VAL', 'IF', 'WHILE', 'FUNCTION', 'IDENTIFIER']:
            STATEMENT_FUNCTION_LIST(result)
        else:
            pass

    def VARIABLE_DECLARATION():
        if lookahead() in ['VAR', 'VAL']:
            declaration_type = lookahead()
            VDECLARATION()
            name = eat('IDENTIFIER')
            eat('COLON')
            type = TYPE()
            eat('ASSIGNMENT')
            expr = OPERATION()
            eat('SEMICOLON')

            return VariableDeclaration(
                declaration_type = declaration_type,
                name = name[1],
                type = type,
                value = expr
            )
        else:
            raise ParsingException()

    def VDECLARATION():
        if lookahead() == 'VAR':
            eat('VAR')
        elif lookahead() == 'VAL':
            eat('VAL')
        else:
            raise ParsingException()

    def TYPE():
        if lookahead() == 'TYPE':
            return eat('TYPE')[1]
        elif lookahead() == 'LRECPAREN':
            eat('LRECPAREN')
            type = TYPE()
            eat('RRECPAREN')

            return ArrayType(
                type = type
            )
        else:
            raise ParsingException()
        
    def VALUE():
        if lookahead() == 'STRING':
            return String(eat('STRING')[1])
        elif lookahead() == 'CHAR':
            return Char(eat('CHAR')[1])
        elif lookahead() == 'INT':
            return Int(eat('INT')[1])
        elif lookahead() == 'FLOAT':
            return Float(eat('FLOAT')[1])
        elif lookahead() == 'BOOLEAN':
            return Boolean(eat('BOOLEAN')[1])
        elif lookahead() == 'LRECPAREN':
            return ARRAY()
        elif lookahead() == 'IDENTIFIER':
            name = eat('IDENTIFIER')
            function = FUNCTION_CALL()
            indexes = VALUEp()

            if function and indexes:
                return ArrayAccess(
                    name = FunctionCall(name[1], function),
                    indexes = indexes
                )
            elif function and not indexes:
                return FunctionCall(
                    name = name[1],
                    arguments = function
                )
            elif indexes:
                return ArrayAccess(
                    name = name[1],
                    indexes = indexes
                )
            else:
                return VariableAccess(
                    name = name[1]
                )
        else:
            raise ParsingException()
        
    def VALUEp():
        if lookahead() == 'LRECPAREN':
            return ARRAY_ACCESS(list())
        else:
            pass
    
    def ARRAY_ACCESS(indexes=list()):
        if lookahead() == 'LRECPAREN':
            eat('LRECPAREN')
            expr = OPERATION()
            indexes.append(Index(expr))
            eat('RRECPAREN')
            ARRAY_ACCESSp(indexes)
        else:
            raise ParsingException()
        
        return IndexList(indexes)
        
    def ARRAY_ACCESSp(indexes):
        if lookahead() == 'LRECPAREN':
            ARRAY_ACCESS(indexes)
        else:
            pass

    def FUNCTION_CALL():
        if lookahead() == 'LPAREN':
            eat('LPAREN')
            parameters = FUNCTION_PARAMETER_LIST(list())
            eat('RPAREN')

            return parameters
        else:
            pass

    def FUNCTION_PARAMETER_LIST(arguments=list()):

        if lookahead() in ['STRING', 'INT', 'FLOAT', 'BOOLEAN', 'LRECPAREN', 'IDENTIFIER']:
            arguments.append(Argument(OPERATION()))
            FUNCTION_PARAMETER_LISTp(arguments)
        else:
            pass

        return ArgumentList(arguments)
    
    def FUNCTION_PARAMETER_LISTp(arguments):
        if lookahead() == 'COMMA':
            eat('COMMA')
            FUNCTION_PARAMETER_LIST(arguments)
        else:
            pass
        
    def ARRAY():
        if lookahead() == 'LRECPAREN':
            eat('LRECPAREN')
            array_content = ARRAY_CONTENT()
            eat('RRECPAREN')

            return array_content
        else:
            raise ParsingException()
        
    def ARRAY_CONTENT():
        if lookahead() == 'RRECPAREN':
            pass
        else:
            return VALUE_LIST(list())

    def VALUE_LIST(content=list()):
        if lookahead() in ['STRING', 'INT', 'FLOAT', 'BOOLEAN', 'IDENTIFIER']:
            content.append(OPERATION())
            VALUE_LISTp(content)

            return Array(content)
        elif lookahead() == 'LRECPAREN':
            content.append(ARRAY())
            VALUE_LISTp2(content)

            return Array(content)
        else:
            raise ParsingException()
        
    def VALUE_LISTp(content):
        if lookahead() == 'COMMA':
            eat('COMMA')
            VALUE_LIST(content)
        else:
            pass
    
    def VALUE_LISTp2():
        if lookahead() == 'COMMA':
            eat('COMMA')
            ARRAY_CONTENT()
        else:
            pass

    def IF_STATEMENT():
        if lookahead() == 'IF':
            eat('IF')
            condition = OPERATION()
            eat('LCURLYPAREN')
            then_block = FUNCTION_STATEMENT_LIST(list())
            eat('RCURLYPAREN')
            else_block = IF_STATEMENTp()

            return IfStatement(
                condition = condition,
                then_block = ThenBlock(then_block),
                else_block = ElseBlock(else_block)
            )
        else:
            raise ParsingException()
        
    def IF_STATEMENTp():
        if lookahead() == 'ELSE':
            eat('ELSE')
            eat('LCURLYPAREN')
            instructions = FUNCTION_STATEMENT_LIST(list())
            eat('RCURLYPAREN')

            return instructions
        else:
            pass

    def WHILE():
        if lookahead() == 'WHILE':
            eat('WHILE')
            condition = OPERATION()
            eat('LCURLYPAREN')
            instructions = FUNCTION_STATEMENT_LIST(list())
            eat('RCURLYPAREN')
        
            return WhileStatement(
                condition = condition,
                code_block = instructions
            )
        else:
            raise ParsingException()

    def STATEMENT_LIST(instructions = list()):
        if lookahead() in ['VAR', 'VAL', 'IF', 'WHILE', 'IDENTIFIER']:
            instructions.append(STATEMENT())
            STATEMENT_LIST(instructions)
        else:
            pass
        
        return InstructionList(instructions)
    
    def REMOVE_PAREN():
        if lookahead() == 'LPAREN':
            eat('LPAREN')
        elif lookahead() == 'RPAREN':
            eat('RPAREN')
        else:
            pass

    def OPERATION():
        return Expression(OR())

    def OR():
        left = AND()
        if lookahead() == 'OROPERATOR':
            operator = eat('OROPERATOR')[1]
            right = OPERATION()

            return Or(
                operator = operator,
                left = left,
                right = right
            )
        else:
            pass

        return left
    
    def AND():
        left = NEG()
        if lookahead() == 'ANDOPERATOR':
            operator = eat('ANDOPERATOR')[1]
            right = OPERATION()

            return And(
                operator = operator,
                left = left,
                right = right
            )
        else:
            pass

        return left
    
    def NEG():
        if lookahead() == 'NEG':
            operator = eat('NEG')[1]
            expr = OPERATION()

            return Unary(
                operator = operator,
                expr = expr
            )
        elif lookahead() == 'SUBTRACTIONOPERATOR':
            operator = eat('SUBTRACTIONOPERATOR')[1]
            expr = OPERATION()

            return Unary(
                operator = operator,
                expr = expr
            )
        elif lookahead() == 'ADDICTIONOPERATOR':
            operator = eat('ADDICTIONOPERATOR')[1]
            expr = OPERATION()

            return Unary(
                operator = operator,
                expr = expr
            )
        else:
            return EQUALITY()
        
    def EQUALITY():
        left = RELATIONAL()
        if lookahead() == 'EQUALITYOPERATOR':
            operator = eat('EQUALITYOPERATOR')[1]
            right = OPERATION()

            return Equality(
                operator = operator,
                left = left,
                right = right
            )
        else:
            pass

        return left
    
    def RELATIONAL():
        left = ADDITIVE()
        if lookahead() == 'COMPAREOPERATOR':
            operator = eat('COMPAREOPERATOR')[1]
            right = OPERATION()

            return Compare(
                operator = operator,
                left = left,
                right = right
            )
        else:
            pass

        return left
    
    def ADDITIVE():
        left = MULTIPLICATIVE()
        if lookahead() == 'ADDICTIONOPERATOR':
            operator = eat('ADDICTIONOPERATOR')[1]
            right = OPERATION()

            return Add(
                operator = operator,
                left = left,
                right = right
            )
        elif lookahead() == 'SUBTRACTIONOPERATOR':
            operator = eat('SUBTRACTIONOPERATOR')[1]
            right = OPERATION()

            return Sub(
                operator = operator,
                left = left,
                right = right
            )
        else:
            pass

        return left

    def MULTIPLICATIVE():
        left = TERMINAL()
        if lookahead() == 'MULTIPLICATIONOPERATOR':
            operator = eat('MULTIPLICATIONOPERATOR')[1]
            right = OPERATION()

            return Mult(
                operator = operator,
                left = left,
                right = right
            )
        else:
            pass

        return left
    
    def TERMINAL():
        if lookahead() == 'LPAREN':
            REMOVE_PAREN()
            expr = OPERATION()
            REMOVE_PAREN()

            return Expression(expr)
        else:
            result = VALUE()
            return result

    ast = S()

    print("\nPARSING SUCCESSFUL!")

    print(ast)

    return ast
