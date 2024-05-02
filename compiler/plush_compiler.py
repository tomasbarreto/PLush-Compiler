from plush_ast import *
from emitter import Emitter

def compile(node, emitter=Emitter()):
    if isinstance(node, Program):
        compile(node.statements, emitter)
    elif isinstance(node, InstructionList):
        for instruction in node.instructions:
            compile(instruction, emitter)
    elif isinstance(node, VariableDeclaration):
        pointer = emitter.get_pointer_name()
        emitter << f"   %{pointer} = alloca i32"
        emitter.push_to_context(node.name, pointer)
        value = compile(node.value, emitter)
        emitter << f"   store i32 {value}, i32* %{pointer}"