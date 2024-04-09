from dataclasses import dataclass

@dataclass
class Program:
    statements: list

    def __ini__ (self, statements):
        self.statements = statements

    def __str__(self):
        return f"Program({', '.join([str(statement) for statement in self.statements])})"
    