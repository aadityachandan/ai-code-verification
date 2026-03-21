import ast
def add_subprocess_import(tree):
    for node in tree.body:
        if isinstance(node, ast.Import):
            for name in node.names:
                if name.name == "subprocess":
                    return tree  # already imported

    # add import at top
    import_node = ast.Import(names=[ast.alias(name="subprocess", asname=None)])
    tree.body.insert(0, import_node)

    return tree
import ast

def add_ast_import(tree):
    # Check if 'ast' is already imported
    for node in tree.body:
        if isinstance(node, ast.Import):
            for name in node.names:
                if name.name == "ast":
                    return tree  # already present

        # also handle: from ast import ...
        if isinstance(node, ast.ImportFrom):
            if node.module == "ast":
                return tree  # already present

    # If not found → add import at top
    import_node = ast.Import(
        names=[ast.alias(name="ast", asname=None)]
    )

    tree.body.insert(0, import_node)

    return tree


class ASTFixer(ast.NodeTransformer):

    def visit_Call(self, node):
        # Fix eval() → ast.literal_eval()
        if isinstance(node.func, ast.Name) and node.func.id == "eval":
            node.func = ast.Attribute(
                value=ast.Name(id="ast", ctx=ast.Load()),
                attr="literal_eval",
                ctx=ast.Load()
            )
        #fix os.system()
        if isinstance(node.func, ast.Attribute):
            if node.func.attr == "system":
                if isinstance(node.func.value, ast.Name):
                    if node.func.value.id == "os":

                        # Replace with subprocess.run(...)
                        node.func = ast.Attribute(
                            value=ast.Name(id="subprocess", ctx=ast.Load()),
                            attr="run",
                            ctx=ast.Load()
                        )

        return self.generic_visit(node)
    def visit_BinOp(self, node):
        # 🔴 Detect division
        if isinstance(node.op, ast.Div):

            # 🔴 Check if right side is 0
            if isinstance(node.right, ast.Constant) and node.right.value == 0:

                # Replace 0 → 1
                node.right = ast.Constant(value=1)

        return self.generic_visit(node)
class RepairGenerator:
    def __init__(self):
        pass
    def apply_fix(self, code, issue):
        issue_type = issue["type"]

        if issue_type == "EvalUsage" or issue_type == "EvalUserInput" or issue_type=="EvalTainted":
            try:
                tree = ast.parse(code)
                fixer = ASTFixer()
                new_tree = fixer.visit(tree)
                new_tree = add_ast_import(new_tree)
                

                return ast.unparse(new_tree)  # convert AST → code

            except:
                return code

        # fallback for others (still string-based for now)
        elif issue_type == "OSCommand":
            try:
                tree = ast.parse(code)
                fixer = ASTFixer()
                new_tree = fixer.visit(tree)
                new_tree = add_subprocess_import(new_tree)

                return ast.unparse(new_tree)  # convert AST → code

            except:
                return code
        elif issue_type== "DivisionByZero":
            try:
                tree = ast.parse(code)
                fixer = ASTFixer()
                new_tree = fixer.visit(tree)
                return ast.unparse(new_tree)  # convert AST → code

            except:
                return code


        return code

    def generate_fix(self, issue):
        issue_type = issue["type"]

        severity_map = {
    # 🔴 CRITICAL / HIGH SECURITY (tainted)
    "EvalTainted": "CRITICAL",
    "ExecTainted": "CRITICAL",
    "CommandInjection": "CRITICAL",
    "UnsafeDeserialization": "CRITICAL",
    "SQLInjection": "CRITICAL",
    "PathTraversal": "CRITICAL",

    # ⚠️ HIGH RISK (non-tainted but dangerous)
    "EvalUsage": "HIGH",
    "ExecUsage": "HIGH",
    "OSCommand": "HIGH",
    "SQLInjectionRisk": "HIGH",
    "PathTraversalRisk": "HIGH",
    "UnsafeDeserializationRisk": "HIGH",

    # 🔐 Secrets
    "HardcodedSecret": "HIGH",
    "MongoURI": "HIGH",

    # 🐞 Bugs
    "DivisionByZero": "MEDIUM",
    "IndexOutOfBounds": "MEDIUM",
    "InfiniteLoop": "MEDIUM",
    "EmptyExcept": "MEDIUM",
    "BroadException": "MEDIUM",

    "NoneComparison": "LOW"
}
            # 🔥 NEW: Confidence calculation (simple logic)
        confidence_map = {
        "EvalUsage": 95,
        "EvalUserInput": 98,
        "ExecUsage": 95,
        "OSCommand": 90,

        "DivisionByZero": 85,
        "IndexOutOfBounds": 75,
        "InfiniteLoop": 70,

        "NoneComparison": 60
    }

        severity = severity_map.get(issue_type, "LOW")
        confidence = confidence_map.get(issue_type, 50)

        if issue_type == "EvalUsage":
            fix = "Replace eval() with ast.literal_eval()"
        elif issue_type == "ExecUsage":
            fix = "Avoid exec(), refactor code"
        elif issue_type == "OSCommand":
            fix = "Use subprocess module safely"
        elif issue_type == "HardcodedSecret":
            fix = "Move secrets to environment variables"
        elif issue_type == "MongoURI":
            fix = "Store Mongo URI in .env file"
        elif issue_type == "DivisionByZero":
            fix = "Check denominator before division"
        elif issue_type == "NoneComparison":
            fix = "Use 'is None' instead of '== None'"
        elif issue_type == "InfiniteLoop":
            fix = "Ensure loop has break/return condition"
        elif issue_type == "IndexOutOfBounds":
            fix = "Check index limits properly"
        elif issue_type == "EmptyExcept":
            fix = "Handle exception properly or log the error"

        elif issue_type == "BroadException":
            fix = "Catch specific exceptions instead of general Exception"

        elif issue_type == "EvalUserInput":
            fix = "Avoid eval() on user input, use safer parsing methods"
        elif issue_type == "EvalTainted":
            fix = "Replaced eval() with ast.literal_eval() using AST transformation"
        else:
            fix = "No fix available"
        

        return {
            "fix": fix,
            "severity": severity,
            "confidence": confidence
        }