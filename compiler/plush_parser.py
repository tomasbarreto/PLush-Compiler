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

        if lookahead() in ['VAR', 'VAL', 'IF', 'WHILE', 'IDENTIFIER']:
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
        if lookahead() in ['VAR', 'VAL', 'IF', 'WHILE', 'RETURN', 'IDENTIFIER']:
            FUNCTION_STATEMENT()
            FUNCTION_STATEMENT_LIST()
        else:
            pass
    
    def FUNCTION_STATEMENT():
        if lookahead() in ['VAR', 'VAL']:
            VARIABLE_DECLARATION()
        elif lookahead() == 'IDENTIFIER':
            IDENTIFIER_ACCESS()
        elif lookahead() == 'IF':
            IF_STATEMENT()
        elif lookahead() == 'WHILE':
            WHILE()
        elif lookahead() == 'RETURN':
            RETURN()
        else:
            raise ParsingException()
    
    def RETURN():
        if lookahead() == 'RETURN':
            eat('RETURN')
            VALUE()
            eat('SEMICOLON')
        else:
            raise ParsingException()

    def STATEMENT():
        if lookahead() in ['VAR', 'VAL']:
            return VARIABLE_DECLARATION()
        elif lookahead() == 'IDENTIFIER':
            return IDENTIFIER_ACCESS()
        elif lookahead() == 'IF':
            return IF_STATEMENT()
        elif lookahead() == 'WHILE':
            return WHILE()
        else:
            raise ParsingException()
        
    def IDENTIFIER_ACCESS():
        if lookahead() == 'IDENTIFIER':
            name = eat('IDENTIFIER')
            return IDENTIFIER_ACCESSp(name)
        else:
            raise ParsingException()
        
    def IDENTIFIER_ACCESSp(name):
        if lookahead() == 'ASSIGNMENT':
            eat('ASSIGNMENT')
            value = VALUE()
            eat('SEMICOLON')

            return VariableAssignment(
                name = name[1],
                value = value
            )
        elif lookahead() == 'LPAREN':
            return PROCEDURE_CALL(name)
        elif lookahead() == 'LRECPAREN':
            indexes = ARRAY_ACCESS()
            eat('ASSIGNMENT')
            value = VALUE()
            eat('SEMICOLON')

            return ArrayVariableAssigment(
                name = name[1],
                indexes = indexes,
                value = value
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
            value = VALUE()
            eat('SEMICOLON')

            return VariableDeclaration(
                declaration_type = declaration_type,
                name = name[1],
                type = type,
                value = value
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
        elif lookahead() == 'NUMBER':
            eat('NUMBER')
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
            value = VALUE()
            indexes.append(Index(value))
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

        if lookahead() in ['STRING', 'NUMBER', 'BOOLEAN', 'LRECPAREN', 'IDENTIFIER']:
            arguments.append(Argument(VALUE()))
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
        if lookahead() in ['STRING', 'NUMBER', 'BOOLEAN']:
            VALUE()
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
            CONDITION()
            eat('LCURLYPAREN')
            STATEMENT_LIST()
            eat('RCURLYPAREN')
            IF_STATEMENTp()
        else:
            raise ParsingException()
        
    def IF_STATEMENTp():
        if lookahead() == 'ELSE':
            eat('ELSE')
            eat('LCURLYPAREN')
            STATEMENT_LIST()
            eat('RCURLYPAREN')
        else:
            pass

    def WHILE():
        if lookahead() == 'WHILE':
            eat('WHILE')
            CONDITION()
            eat('LCURLYPAREN')
            STATEMENT_LIST()
            eat('RCURLYPAREN')
        else:
            raise ParsingException()

    def STATEMENT_LIST():
        if lookahead() in ['VAR', 'VAL', 'IF', 'WHILE', 'IDENTIFIER']:
            STATEMENT()
            STATEMENT_LIST()
        else:
            pass

    def CONDITION():
        MULTIPLICATIVE()
    
    def MULTIPLICATIVE():
        ADDITIVE()
        if lookahead() == 'MULTIPLICATIONOPERATOR':
            eat('MULTIPLICATIONOPERATOR')
            ADDITIVE()
        else:
            pass

    def ADDITIVE():
        RELATIONAL()
        if lookahead() == 'ADDICTIONOPERATOR':
            eat('ADDICTIONOPERATOR')
            RELATIONAL()
        elif lookahead() == 'SUBTRACTIONOPERATOR':
            eat('SUBTRACTIONOPERATOR')
            RELATIONAL()
        else:
            pass
    
    def RELATIONAL():
        EQUALITY()
        if lookahead() == 'COMPAREOPERATOR':
            eat('COMPAREOPERATOR')
            EQUALITY()
        else:
            pass

    def EQUALITY():
        NEG()
        if lookahead() == 'EQUALITYOPERATOR':
            eat('EQUALITYOPERATOR')
            NEG()
        else:
            pass

    def NEG():
        if lookahead() == 'NEG':
            eat('NEG')
            AND()
        else:
            AND()

    def AND():
        OR()
        if lookahead() == 'LOGICOPERATOR':
            eat('LOGICOPERATOR')
            OR()
        else:
            pass

    def OR():
        TERMINAL()
        if lookahead() == 'LOGICOPERATOR':
            eat('LOGICOPERATOR')
            TERMINAL()
        else:
            pass
    
        
    def TERMINAL():
        if lookahead() == 'LPAREN':
            eat('LPAREN')
            VALUE()
            eat('RPAREN')
        else:
            VALUE()

    def CONDITIONp():
        if lookahead() == 'LOGICOPERATOR':
            eat('LOGICOPERATOR')
            CONDITION()
        elif lookahead() == 'COMPAREOPERATOR':
            eat('COMPAREOPERATOR')
            CONDITION()
        elif lookahead() == 'EQUALITYOPERATOR':
            eat('EQUALITYOPERATOR')
            CONDITION()
        elif lookahead() == 'ADDICTIONOPERATOR':
            eat('ADDICTIONOPERATOR')
            CONDITION()
        elif lookahead() == 'SUBTRACTIONOPERATOR':
            eat('SUBTRACTIONOPERATOR')
            CONDITION()
        elif lookahead() == 'MULTIPLICATIONOPERATOR':
            eat('MULTIPLICATIONOPERATOR')
            CONDITION()
        else:
            pass

    ast = S()

    print("\nPARSING SUCCESSFUL!")

    print(ast)
