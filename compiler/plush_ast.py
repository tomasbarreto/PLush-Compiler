from dataclasses import dataclass

@dataclass
class Program:
    def __init__ (self, statements):
        self.statements = statements

    def __repr__(self) -> str:
        if self.statements is None:
            return "Program()"
        
        return f"Program({', '.join([str(statement) for statement in self.statements])})"

@dataclass
class IfStatement:
    def __init__ (self, condition, then_code, else_code):
        self.condition = condition
        self.then_code = then_code
        self.else_code = else_code

    def __repr__(self) -> str:
        return f"IfStatement({self.condition}, {self.then_code}, {self.else_code})"

@dataclass
class WhileStatement:
    def __init__ (self, condition, code):
        self.condition = condition
        self.code = code

    def __repr__(self) -> str:
        return f"WhileStatement({self.condition}, {self.code})"

@dataclass
class VariableDeclaration:
    def __init__ (self, declaration_type, name, type, value):
        self.declaration_type = declaration_type
        self.name = name
        self.type = type
        self.value = value

    def __repr__(self) -> str:
        return f"VariableDeclaration({self.declaration_type}, {self.name}, {self.type}, {self.value})"
    
@dataclass
class FunctionDeclaration:
    def __init__ (self, name, parameters, type, body):
        self.name = name
        self.parameters = parameters
        self.type = type
        self.body = body

    def __repr__(self) -> str:
        return f"FunctionDeclaration({self.name}, {self.parameters}, {self.type}, {self.body})"
    
@dataclass
class FunctionCall:
    def __init__ (self, name, arguments):
        self.name = name
        self.arguments = arguments

    def __repr__(self) -> str:
        return f"FunctionCall({self.name}, {self.arguments})"

@dataclass
class Assignment:
    def __init__ (self, name, value):
        self.name = name
        self.value = value

    def __repr__(self) -> str:
        return f"Assignment({self.name}, {self.value})"

@dataclass
class Mult:
    def __init__ (self, left, right):
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"Mult({self.left}, {self.right})"

@dataclass
class Div:
    def __init__ (self, left, right):
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"Div({self.left}, {self.right})"
    
@dataclass
class Add:
    def __init__ (self, left, right):
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"Add({self.left}, {self.right})"

@dataclass
class Sub:
    def __init__ (self, left, right):
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"Sub({self.left}, {self.right})"

@dataclass
class Number:
    def __init__ (self, value):
        self.value = value

    def __repr__(self) -> str:
        return f"Number({self.value})"
    
@dataclass
class ArrayType:
    def __init__ (self, type):
        self.type = type

    def __repr__(self) -> str:
        return f"ArrayType({self.type})"
    
@dataclass
class ProcedureCall:
    def __init__ (self, name, arguments):
        self.name = name
        self.arguments = arguments

    def __repr__(self) -> str:
        return f"ProcedureCall({self.name}, {self.arguments})"
    
@dataclass
class Argument:
    def __init__ (self, value):
        self.value = value

    def __repr__(self) -> str:
        return f"Argument({self.value})"
    
@dataclass
class ArgumentList:
    def __init__ (self, arguments):
        self.arguments = arguments

    def __repr__(self) -> str:
        return f"ArgumentList({self.arguments})"