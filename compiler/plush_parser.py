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
        if lookahead() in ['VAR', 'VAL', 'IF', 'WHILE']:
            STATEMENT()
            STATEMENT_FUNCTION_LISTp()
        else:
            raise ParsingException()

    def STATEMENT():
        if lookahead() in ['VAR', 'VAL']:
            VARIABLE_DECLARATION()
        elif lookahead() == 'VNAME':
            VARIABLE_ASSIGNMENT()
        elif lookahead() == 'IF':
            IF_STATEMENT()
        elif lookahead() == 'WHILE':
            WHILE()
        else:
            raise ParsingException()

    def STATEMENT_FUNCTION_LISTp():
        if lookahead() in ['VAR', 'VAL', 'IF', 'WHILE']:
            STATEMENT_FUNCTION_LIST()
        else:
            pass

    def VARIABLE_DECLARATION():
        if lookahead() in ['VAR', 'VAL']:
            VDECLARATION()
            eat('VNAME')
            eat('COLON')
            TYPE()
            eat('ASSIGNMENT')
            VALUE()
            eat('SEMICOLON')
        else:
            raise ParsingException()

    def VARIABLE_ASSIGNMENT():
        if lookahead() == 'VNAME':
            eat('VNAME')
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
        elif lookahead() == 'LPAREN':
            i = 0
            while lookahead() == 'LPAREN':
                eat('LPAREN')
                i += 1
            TYPE()
            while i > 0:
                eat('RPAREN')
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
        elif lookahead() == 'LPAREN':
            ARRAY()
            CONDITIONp()
            MATH_CALC()
        else:
            raise ParsingException()

        
    def ARRAY():
        if lookahead() == 'LPAREN':
            eat('LPAREN')
            ARRAY_CONTENT()
            eat('RPAREN')
        else:
            raise ParsingException()
        
    def ARRAY_CONTENT():
        if lookahead() == 'RPAREN':
            pass
        else:
            VALUE_LIST()

    def VALUE_LIST():
        if lookahead() in ['STRING', 'NUMBER', 'BOOLEAN']:
            VALUE()
            VALUE_LISTp()
        elif lookahead() == 'LPAREN':
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
        if lookahead() in ['VAR', 'VAL', 'IF', 'WHILE']:
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
