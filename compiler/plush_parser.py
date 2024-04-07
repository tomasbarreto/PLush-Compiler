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
        elif lookahead() == 'NUMBER':
            eat('NUMBER')
        elif lookahead() == 'BOOLEAN':
            eat('BOOLEAN')
        elif lookahead() == 'LPAREN':
            ARRAY()
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

    S()
