import ast


class PatchVerifier:
    def verify_syntax(self, code):
        try:
            ast.parse(code)
            return True, "Syntax is valid"
        except SyntaxError as e:
            return False, f"Syntax Error: {e}"

    

    def basic_validation(self, code):
        try:
            tree = ast.parse(code)
        except:
            return False, "Invalid syntax"

        for node in ast.walk(tree):
            if isinstance(node, ast.Call):

                # Detect eval()
                if isinstance(node.func, ast.Name) and node.func.id == "eval":
                    return False, "Unsafe eval still present"

                # Detect os.system()
                if isinstance(node.func, ast.Attribute):
                    if node.func.attr == "system":
                        if isinstance(node.func.value, ast.Name):
                            if node.func.value.id == "os":
                                return False, "Unsafe os.system still present"

        return True, "Basic validation passed"

 