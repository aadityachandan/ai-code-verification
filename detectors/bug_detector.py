import ast


class BugDetector(ast.NodeVisitor):
    def __init__(self):
        self.bugs = []

    def visit_BinOp(self, node):
        # Detect division by zero
        if isinstance(node.op, ast.Div):
            if isinstance(node.right, ast.Constant):
                if node.right.value == 0:
                    self.bugs.append({
                        "type": "DivisionByZero",
                        "line": node.lineno,
                        "message": "Division by zero detected"
                    })

        self.generic_visit(node)

    def visit_For(self, node):
        # Simple index out of bounds check (basic)
        if isinstance(node.iter, ast.Call):
            if hasattr(node.iter.func, 'id') and node.iter.func.id == "range":
                if len(node.iter.args) == 1:
                    # range(len(x)+1) type case
                    if isinstance(node.iter.args[0], ast.BinOp):
                        if isinstance(node.iter.args[0].op, ast.Add):
                            self.bugs.append({
                                "type": "IndexOutOfBounds",
                                "line": node.lineno,
                                "message": "Possible index out-of-bounds"
                            })

        self.generic_visit(node)
    def visit_While(self, node):
        if isinstance(node.test, ast.Constant) and node.test.value is True:

            has_break_or_return = False

            for child in ast.walk(node):
                if isinstance(child, (ast.Break, ast.Return)):
                    has_break_or_return = True
                    break

            if not has_break_or_return:
                self.bugs.append({
                    "type": "InfiniteLoop",
                    "line": node.lineno,
                    "message": "Possible infinite loop (no break/return found)"
                })

        self.generic_visit(node)