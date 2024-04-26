from dataclasses import dataclass

@dataclass
class Program:
    def __init__ (self, statements):
        self.statements = statements

    def __repr__(self) -> str:
        if self.statements is None:
            return "Program()"
        
        return f"Program({self.statements})"
    
@dataclass
class InstructionList:
    def __init__ (self, instructions):
        self.instructions = instructions

    def __repr__(self) -> str:
        if self.instructions is None:
            return "InstructionList()"
        return f"InstructionList({', '.join([str(instruction) for instruction in self.instructions])})"


@dataclass
class IfStatement:
    def __init__ (self, condition, then_block, else_block):
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block

    def __repr__(self) -> str:
        if str(self.else_block) == "ElseBlock()":
            return f"IfStatement({self.condition}, {self.then_block})"
        return f"IfStatement({self.condition}, {self.then_block}, {self.else_block})"

@dataclass
class ThenBlock:
    def __init__ (self, instructions):
        self.instructions = instructions

    def __repr__(self) -> str:
        if self.instructions is None:
            return "ThenBlock()"
        return f"ThenBlock({', '.join([str(instruction) for instruction in self.instructions])})"



@dataclass
class ElseBlock:
    def __init__ (self, instructions):
        self.instructions = instructions

    def __repr__(self) -> str:
        if self.instructions is None:
            return "ElseBlock()"
        return f"ElseBlock({self.instructions})"

@dataclass
class WhileStatement:
    def __init__ (self, condition, code_block):
        self.condition = condition
        self.code_block = code_block

    def __repr__(self) -> str:
        return f"WhileStatement({self.condition}, {self.code_block})"

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
    def __init__ (self, name, type, parameters=None, instructions=None):
        self.name = name
        self.parameters = parameters
        self.type = type
        self.instructions = instructions

    def __repr__(self) -> str:
        if self.parameters is None and self.instructions is None:
            return f"FunctionDeclaration({self.name}, {self.type})"
        elif self.parameters is None:
            return f"FunctionDeclaration({self.name}, {self.type}, {self.instructions})"
        elif self.instructions is None:
            return f"FunctionDeclaration({self.name}, {self.parameters}, {self.type})"
        
        return f"FunctionDeclaration({self.name}, {self.parameters}, {self.type}, {self.instructions})"
    
@dataclass
class FunctionDefinition:
    def __init__ (self, name, type, parameters=None):
        self.name = name
        self.parameters = parameters
        self.type = type

    def __repr__(self) -> str:
        if self.parameters is None:
            return f"FunctionDefinition({self.name}, {self.type})"
        
        return f"FunctionDefinition({self.name}, {self.parameters}, {self.type})"
    
@dataclass
class FunctionCall:
    def __init__ (self, name, arguments):
        self.name = name
        self.arguments = arguments

    def __repr__(self) -> str:
        return f"FunctionCall({self.name}, {self.arguments})"

@dataclass
class VariableAssignment:
    def __init__ (self, name, value):
        self.name = name
        self.value = value

    def __repr__(self) -> str:
        return f"VariableAssignment({self.name}, {self.value})"

@dataclass
class ArrayVariableAssigment:
    def __init__ (self, left, right):
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"ArrayAssigment({self.left}, {self.right})"
    
@dataclass
class IndexList:
    def __init__ (self, indexes):
        self.indexes = indexes

    def __repr__(self) -> str:
        if self.indexes is None:
            return "IndexList()"
        return f"IndexList({', '.join([str(index) for index in self.indexes])})"
    
@dataclass
class Index:
    def __init__ (self, value):
        self.value = value

    def __repr__(self) -> str:
        return f"Index({self.value})"
    
@dataclass
class Expression:
    def __init__ (self, expr):
        self.expr = expr

    def __repr__(self) -> str:
        return f"{self.expr}"

@dataclass
class Mult:
    def __init__ (self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"Mult({self.operator}, {self.left}, {self.right})"

@dataclass
class Div:
    def __init__ (self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"Div({self.operator}, {self.left}, {self.right})"
    
@dataclass
class Add:
    def __init__ (self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"Add({self.operator}, {self.left}, {self.right})"

@dataclass
class Sub:
    def __init__ (self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"Sub({self.operator}, {self.left}, {self.right})"

@dataclass
class Compare:
    def __init__ (self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"Compare({self.operator}, {self.left}, {self.right})"

@dataclass
class Equality:
    def __init__ (self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"Equality({self.operator}, {self.left}, {self.right})"

@dataclass
class Unary:
    def __init__ (self, operator, expr):
        self.operator = operator
        self.expr = expr

    def __repr__(self) -> str:
        return f"Unary({self.operator}, {self.expr})"
    
@dataclass
class And:
    def __init__ (self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"And({self.operator}, {self.left}, {self.right})"

@dataclass
class Or:
    def __init__ (self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"Or({self.operator}, {self.left}, {self.right})"

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
        return f"ArgumentList({', '.join([str(argument) for argument in self.arguments])})"
    
@dataclass
class Int:
    def __init__ (self, value):
        self.value = value

    def __repr__(self) -> str:
        return f"Int({self.value})"
    
@dataclass
class String:
    def __init__ (self, value):
        self.value = value

    def __repr__(self) -> str:
        return f"String({self.value})"
    
@dataclass
class Float:
    def __init__ (self, value):
        self.value = value

    def __repr__(self) -> str:
        return f"Float({self.value})"
    
@dataclass
class Char:
    def __init__ (self, value):
        self.value = value

    def __repr__(self) -> str:
        return f"Char({self.value})"

@dataclass
class Boolean:
    def __init__ (self, value):
        self.value = value

    def __repr__(self) -> str:
        return f"Boolean({self.value})"

@dataclass
class Array:
    def __init__ (self, content):
        self.content = content

    def __repr__(self) -> str:
        return f"Array({', '.join([str(content) for content in self.content])})"
@dataclass
class VariableAccess:
    def __init__ (self, name):
        self.name = name

    def __repr__(self) -> str:
        return f"VariableAccess({self.name})"

@dataclass
class FunctionCall:
    def __init__ (self, name, arguments=None):
        self.name = name
        self.arguments = arguments

    def __repr__(self) -> str:
        if self.arguments is None:
            return f"FunctionCall({self.name})"
        return f"FunctionCall({self.name}, {self.arguments})"
    
@dataclass
class ArrayAccess:
    def __init__ (self, identifier, indexes=None):
        self.identifier = identifier
        self.indexes = indexes

    def __repr__(self) -> str:
        return f"ArrayAccess({self.identifier}, {self.indexes})"    

@dataclass
class ParameterList:
    def __init__ (self, parameters=None):
        self.parameters = parameters

    def __repr__(self) -> str:
        if self.parameters is None:
            return "ParameterList()"
        return f"ParameterList({', '.join([str(parameter) for parameter in self.parameters])})"

@dataclass
class Parameter:
    def __init__ (self, declaration_type, name, type):
        self.declaration_type = declaration_type
        self.name = name
        self.type = type

    def __repr__(self) -> str:
        return f"Parameter({self.declaration_type}, {self.name}, {self.type})"