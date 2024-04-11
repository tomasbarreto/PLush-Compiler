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
            eat('IDENTIFIER')
            eat('LPAREN')
            FUNCTION_DECLARATION_PARAMETERS()
            eat('RPAREN')
            eat('COLON')
            TYPE()
            FUNCTIONp()
        else:
            raise ParsingException()
        
    def FUNCTIONp():
        if lookahead() == 'LCURLYPAREN':
            eat('LCURLYPAREN')
            FUNCTION_STATEMENT_LIST()
            eat('RCURLYPAREN')
        elif lookahead() == 'COMMA':
            eat('COMMA')
        else:
            raise ParsingException()
        
    def FUNCTION_DECLARATION_PARAMETERS():
        if lookahead() in ['VAL', 'VAR']:
            FUNCTION_DECLARATION_PARAMETER_LIST()
        else:
            pass
    
    def FUNCTION_DECLARATION_PARAMETER_LIST():
        if lookahead() in ['VAL', 'VAR']:
            FUNCTION_PARAMETER()
            FUNCTION_DECLARATION_PARAMETER_LISTp()
        else:
            raise ParsingException()
        
    def FUNCTION_PARAMETER():
        if lookahead() in ['VAL', 'VAR']:
            VDECLARATION()
            eat('IDENTIFIER')
            eat('COLON')
            TYPE()
        else:
            raise ParsingException()
        
    def FUNCTION_DECLARATION_PARAMETER_LISTp():
        if lookahead() == 'COMMA':
            eat('COMMA')
            FUNCTION_DECLARATION_PARAMETER_LIST()
        else:
            pass

    def FUNCTION_STATEMENT_LIST():
        if lookahead() in ['VAR', 'VAL', 'IF', 'WHILE', 'IDENTIFIER']:
            FUNCTION_STATEMENT(True)
            FUNCTION_STATEMENT_LIST()
        else:
            pass
    
    def FUNCTION_STATEMENT(isFunction = False):
        if lookahead() in ['VAR', 'VAL']:
            VARIABLE_DECLARATION()
        elif lookahead() == 'IDENTIFIER':
            IDENTIFIER_ACCESS(isFunction)
        elif lookahead() == 'IF':
            IF_STATEMENT()
        elif lookahead() == 'WHILE':
            WHILE()
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
        elif lookahead() == 'IF':
            return IF_STATEMENT()
        elif lookahead() == 'WHILE':
            return WHILE()
        else:
            raise ParsingException()
        
    def IDENTIFIER_ACCESS(isFunction = False):
        if lookahead() == 'IDENTIFIER':
            name = eat('IDENTIFIER')
            return IDENTIFIER_ACCESSp(name, isFunction)
        else:
            raise ParsingException()
        
    def IDENTIFIER_ACCESSp(name, isFunction=False):
        if lookahead() == 'ASSIGNMENT':
            eat('ASSIGNMENT')
            expr = OPERATION()
            eat('SEMICOLON')

            return VariableAssignment(
                name = name[1],
                value = expr
            )
        elif isFunction:
            if lookahead() == 'LPAREN':
                return PROCEDURE_CALL(name)
        elif lookahead() == 'LRECPAREN':
            indexes = ARRAY_ACCESS()
            eat('ASSIGNMENT')
            expr = OPERATION()
            eat('SEMICOLON')

            return ArrayVariableAssigment(
                name = name[1],
                indexes = indexes,
                value = expr
            )
        else:
            raise ParsingException()

    def PROCEDURE_CALL(name):
        if lookahead() == 'LPAREN':
            eat('LPAREN')
            arguments = FUNCTION_PARAMETER_LIST()
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
        if lookahead() == 'RETURN':
            raise
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
        if lookahead() == 'SUBTRACTIONOPERATOR':
            eat('SUBTRACTIONOPERATOR')
            VALUEp()
        else:
            VALUEp()

    def VALUEp():
        if lookahead() == 'STRING':
            eat('STRING')
            CONDITIONp()
        elif lookahead() == 'INT':
            eat('INT')
            CONDITIONp()
        elif lookahead() == 'FLOAT':
            eat('FLOAT')
            CONDITIONp()
        elif lookahead() == 'BOOLEAN':
            eat('BOOLEAN')
            CONDITIONp()
        elif lookahead() == 'LRECPAREN':
            ARRAY()
            CONDITIONp()
        elif lookahead() == 'IDENTIFIER':
            eat('IDENTIFIER')
            FUNCTION_CALL()
            VALUEpp()
            CONDITIONp()
        else:
            raise ParsingException()
        
    def VALUEpp():
        if lookahead() == 'LRECPAREN':
            ARRAY_ACCESS()
            CONDITIONp()
        else:
            pass
    
    def ARRAY_ACCESS(indexes = list()):
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
            FUNCTION_PARAMETER_LIST()
            eat('RPAREN')
        else:
            pass

    def FUNCTION_PARAMETER_LIST():
        arguments = list()

        if lookahead() in ['STRING', 'INT', 'FLOAT', 'BOOLEAN', 'LRECPAREN', 'IDENTIFIER']:
            arguments.append(Argument(OPERATION()))
            FUNCTION_PARAMETER_LISTp()
        else:
            pass

        return ArgumentList(arguments)
    
    def FUNCTION_PARAMETER_LISTp():
        if lookahead() == 'COMMA':
            eat('COMMA')
            FUNCTION_PARAMETER_LIST()
        else:
            pass
        
    def ARRAY():
        if lookahead() == 'LRECPAREN':
            eat('LRECPAREN')
            ARRAY_CONTENT()
            eat('RRECPAREN')
        else:
            raise ParsingException()
        
    def ARRAY_CONTENT():
        if lookahead() == 'RRECPAREN':
            pass
        else:
            VALUE_LIST()

    def VALUE_LIST():
        if lookahead() in ['STRING', 'INT', 'FLOAT', 'BOOLEAN']:
            OPERATION()
            VALUE_LISTp()
        elif lookahead() == 'LRECPAREN':
            ARRAY()
            VALUE_LISTp2()
        else:
            raise ParsingException()
        
    def VALUE_LISTp():
        if lookahead() == 'COMMA':
            eat('COMMA')
            VALUE_LIST()
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
            then_block = STATEMENT_LIST(list())
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
            instructions = STATEMENT_LIST(list())
            eat('RCURLYPAREN')

            return instructions
        else:
            pass

    def WHILE():
        if lookahead() == 'WHILE':
            eat('WHILE')
            condition = OPERATION()
            eat('LCURLYPAREN')
            instructions = STATEMENT_LIST()
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

    '''
    def OPERATION():
        return Expression(MULTIPLICATIVE())
    
    def MULTIPLICATIVE():
        expr1 = ADDITIVE()
        if lookahead() == 'MULTIPLICATIONOPERATOR':
            operator = eat('MULTIPLICATIONOPERATOR')[1]
            expr2 = OPERATION()

            return Mult(
                operator = operator,
                left = expr1,
                right = expr2
            )
        else:
            pass

        return expr1

    def ADDITIVE():
        expr1 = RELATIONAL()
        if lookahead() == 'ADDICTIONOPERATOR':
            eat('ADDICTIONOPERATOR')
            expr2 = OPERATION()

            return Add(
                left = expr1,
                right = expr2
            )
        elif lookahead() == 'SUBTRACTIONOPERATOR':
            operator = eat('SUBTRACTIONOPERATOR')[1]
            expr2 = OPERATION()

            return Sub(
                operator = operator,
                left = expr1,
                right = expr2
            )
        else:
            pass

        return expr1
    
    def RELATIONAL():
        expr1 = EQUALITY()
        if lookahead() == 'COMPAREOPERATOR':
            operator = eat('COMPAREOPERATOR')[1]
            expr2 = OPERATION()

            return Compare(
                operator = operator,
                left = expr1,
                right = expr2
            )
        else:
            pass

        return expr1

    def EQUALITY():
        expr1 = NEG()
        if lookahead() == 'EQUALITYOPERATOR':
            operator = eat('EQUALITYOPERATOR')[1]
            expr2 = OPERATION()

            return Equality(
                operator = operator,
                left = expr1,
                right = expr2
            )
        else:
            pass

        return expr1

    def NEG():
        if lookahead() == 'NEG':
            operator = eat('NEG')[1]
            expr1 = OPERATION()

            return Neg(
                operator = operator,
                expr = expr1
            )
        else:
            return AND()

    def AND():
        expr1 = OR()
        if lookahead() == 'ANDOPERATOR':
            operator = eat('ANDOPERATOR')[1]
            expr2 = OPERATION()

            return And(
                operator = operator,
                left = expr1,
                right = expr2
            )
        else:
            pass

        return expr1

    def OR():
        expr1 = TERMINAL()
        if lookahead() == 'OROPERATOR':
            operator = eat('OROPERATOR')[1]
            expr2 = OPERATION()

            return Or(
                operator = operator,
                left = expr1,
                right = expr2
            )
        else:
            pass
        
        return expr1
        
    def TERMINAL():
        REMOVE_PAREN()
        terminal = VALUE()
        REMOVE_PAREN()

        return Terminal(terminal)
    '''

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
            return Terminal(VALUE())

    '''
    def TERMINAL():
        if lookahead() == 'LPAREN': 
            eat('LPAREN')  
            expr = OPERATION() 
            eat('RPAREN')  
            return Expression(expr)
        else:
            return Terminal(VALUE())
    '''

    def CONDITIONp():
        if lookahead() in ['ANDOPERATOR', 'OROPERATOR', 'COMPAREOPERATOR', 'EQUALITYOPERATOR', 'ADDICTIONOPERATOR', 'SUBTRACTIONOPERATOR', 'MULTIPLICATIONOPERATOR']:
            return
        else:
            pass

    ast = S()

    print("\nPARSING SUCCESSFUL!")

    print(ast)
