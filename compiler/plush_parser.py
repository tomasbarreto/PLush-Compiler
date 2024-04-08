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
        STATEMENT_FUNCTION_LIST()

    def STATEMENT_FUNCTION_LIST():
        if lookahead() in ['VAR', 'VAL', 'IF', 'WHILE', 'IDENTIFIER']:
            STATEMENT()
            STATEMENT_FUNCTION_LISTp()
        elif lookahead() == 'FUNCTION':
            FUNCTION()
            STATEMENT_FUNCTION_LISTp()
        else:
            raise ParsingException()
        
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
        if lookahead() in ['VAR', 'VAL', 'IF', 'WHILE', 'RETURN']:
            FUNCTION_STATEMENT()
            FUNCTION_STATEMENT_LIST()
        else:
            pass
    
    def FUNCTION_STATEMENT():
        if lookahead() in ['VAR', 'VAL']:
            VARIABLE_DECLARATION()
        elif lookahead() == 'IDENTIFIER':
            VARIABLE_ASSIGNMENT()
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
            VARIABLE_DECLARATION()
        elif lookahead() == 'IDENTIFIER':
            IDENTIFIER_ACCESS()
        elif lookahead() == 'IF':
            IF_STATEMENT()
        elif lookahead() == 'WHILE':
            WHILE()
        else:
            raise ParsingException()
        
    def IDENTIFIER_ACCESS():
        if lookahead() == 'IDENTIFIER':
            eat('IDENTIFIER')
            IDENTIFIER_ACCESSp()
        else:
            raise ParsingException()
        
    def IDENTIFIER_ACCESSp():
        if lookahead() == 'ASSIGNMENT':
            eat('ASSIGNMENT')
            VALUE()
            eat('SEMICOLON')
        elif lookahead() == 'LPAREN':
            PROCEDURE_CALL()
        else:
            raise ParsingException()

    def PROCEDURE_CALL():
        if lookahead() == 'LPAREN':
            eat('LPAREN')
            FUNCTION_PARAMETER_LIST()
            eat('RPAREN')
            eat('SEMICOLON')
        else:
            raise ParsingException()

    def STATEMENT_FUNCTION_LISTp():
        if lookahead() in ['VAR', 'VAL', 'IF', 'WHILE', 'FUNCTION', 'IDENTIFIER']:
            STATEMENT_FUNCTION_LIST()
        if lookahead() == 'RETURN':
            raise
        else:
            pass

    def VARIABLE_DECLARATION():
        if lookahead() in ['VAR', 'VAL']:
            VDECLARATION()
            eat('IDENTIFIER')
            eat('COLON')
            TYPE()
            eat('ASSIGNMENT')
            VALUE()
            eat('SEMICOLON')
        else:
            raise ParsingException()

    def VARIABLE_ASSIGNMENT():
        if lookahead() == 'IDENTIFIER':
            eat('IDENTIFIER')
            eat('ASSIGNMENT')
            VALUE()
            eat('SEMICOLON')
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
            eat('TYPE')
        elif lookahead() == 'LRECPAREN':
            i = 0
            while lookahead() == 'LRECPAREN':
                eat('LRECPAREN')
                i += 1
            TYPE()
            while i > 0:
                eat('RRECPAREN')
                i -= 1
        else:
            raise ParsingException()

    def VALUE():
        if lookahead() == 'STRING':
            eat('STRING')
            CONDITIONp()
            MATH_CALC()
        elif lookahead() == 'NUMBER':
            eat('NUMBER')
            CONDITIONp()
            MATH_CALC()
        elif lookahead() == 'BOOLEAN':
            eat('BOOLEAN')
            CONDITIONp()
            MATH_CALC()
        elif lookahead() == 'LRECPAREN':
            ARRAY()
            CONDITIONp()
            MATH_CALC()
        elif lookahead() == 'IDENTIFIER':
            eat('IDENTIFIER')
            FUNCTION_CALL()
            VALUEp()
        else:
            raise ParsingException()
        
    def VALUEp():
        if lookahead() == 'LRECPAREN':
            ARRAY_ACCESS()
            CONDITIONp()
            MATH_CALC()
        else:
            pass
    
    def ARRAY_ACCESS():
        if lookahead() == 'LRECPAREN':
            eat('LRECPAREN')
            VALUE()
            eat('RRECPAREN')
            ARRAY_ACCESSp()
        else:
            raise ParsingException()
        
    def ARRAY_ACCESSp():
        if lookahead() == 'LRECPAREN':
            ARRAY_ACCESS()
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
        if lookahead() in ['STRING', 'NUMBER', 'BOOLEAN', 'LRECPAREN', 'IDENTIFIER']:
            VALUE()
            FUNCTION_PARAMETER_LISTp()
        else:
            pass
    
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
        OR()
    
    def OR():
        AND()
        if lookahead() == 'OR':
            eat('OR')
            AND()
        else:
            pass

    def AND():
        NEG()
        if lookahead() == 'AND':
            eat('AND')
            NEG()
        else:
            pass
    
    def NEG():
        if lookahead() == 'NEG':
            eat('NEG')
            EQUALITY()
        else:
            EQUALITY()

    def EQUALITY():
        RELATIONAL()
        if lookahead() == 'EQUALS':
            eat('EQUALS')
            RELATIONAL()
        elif lookahead() == 'NOTEQUALS':
            eat('NOTEQUALS')
            RELATIONAL()
        else:
            pass
    
    def RELATIONAL():
        ADDITIVE()
        if lookahead() == 'LOGICOPERATOR':
            eat('LOGICOPERATOR')
            ADDITIVE()
        else:
            pass
    
    def ADDITIVE():
        MULTIPLICATIVE()
        if lookahead() == 'ADDICTIONOPERATOR':
            eat('ADDICTIONOPERATOR')
            MULTIPLICATIVE()
        else:
            pass
    
    def MULTIPLICATIVE():
        TERMINAL()
        if lookahead() == 'MULTIPLICATIONOPERATOR':
            eat('MULTIPLICATIONOPERATOR')
            TERMINAL()
        else:
            pass
        
    def TERMINAL():
        VALUE()

    def CONDITIONp():
        if lookahead() == 'LOGICOPERATOR':
            eat('LOGICOPERATOR')
            CONDITION()
        else:
            pass

    def MATH_CALC():
        if lookahead() == 'ADDICTIONOPERATOR':
            eat('ADDICTIONOPERATOR')
            ADDITIVE()
        elif lookahead() == 'MULTIPLICATIONOPERATOR':
            eat('MULTIPLICATIONOPERATOR')
            MULTIPLICATIVE()
        else:
            pass

    S()

    print("\nPARSING SUCCESSFUL!")
