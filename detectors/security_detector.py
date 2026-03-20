import ast


class SecurityDetector(ast.NodeVisitor):
    def __init__(self):
        self.issues = []
        self.tainted_vars = set()
        self.functions = {}  

    def visit_FunctionDef(self, node):
        self.functions[node.name] = node
        
    
    def is_expr_tainted(self, node):

        # Case 1: variable
        if isinstance(node, ast.Name):
            return node.id in self.tainted_vars

        # Case 2: constant → safe
        if isinstance(node, ast.Constant):
            return False

        # Case 3: binary operation (x + "hello")
        if isinstance(node, ast.BinOp):
            return (
                self.is_expr_tainted(node.left) or
                self.is_expr_tainted(node.right)
            )

        # Case 4: function call (optional future)
        if isinstance(node, ast.Call):
            for arg in node.args:
                if self.is_expr_tainted(arg):
                    return True

        # Case 5: f-string
        if isinstance(node, ast.JoinedStr):
            for value in node.values:
                if isinstance(value, ast.FormattedValue):
                    if self.is_expr_tainted(value.value):
                        return True

        return False

    def visit_Call(self, node):
      # -------------------------
        # 🔥 FUNCTION CALL TAINT
        # -------------------------
        if isinstance(node.func, ast.Name):
            func_name = node.func.id

            if func_name in self.functions:
                func_def = self.functions[func_name]

                for i, arg in enumerate(node.args):
                    if i < len(func_def.args.args):

                        param_name = func_def.args.args[i].arg

                        if self.is_expr_tainted(arg):

                            self.tainted_vars.add(param_name)

                            for stmt in func_def.body:
                                self.visit(stmt)

                            self.tainted_vars.remove(param_name)

                return   # 🔥 VERY IMPORTANT

        # -------------------------
        # 🔴 eval() / exec()
        # -------------------------
        if isinstance(node.func, ast.Name):

            if node.func.id == "eval":
                if node.args:
                    arg = node.args[0]

                    # 🔥 NEW LOGIC (VERY IMPORTANT)
                    if self.is_expr_tainted(arg):
                        self.issues.append({
                            "type": "EvalTainted",
                            "line": node.lineno,
                            "message": "Tainted input used in eval()",
                            "severity": "CRITICAL"
                        })
                    else:
                        self.issues.append({
                            "type": "EvalUsage",
                            "line": node.lineno,
                            "message": "Use of eval() is dangerous"
                        })
                    

            if node.func.id == "exec":
                self.issues.append({
                        "type": "ExecUsage",
                        "line": node.lineno,
                        "message": "Use of exec() is dangerous"
                    })

        # -------------------------
        # 🔴 os.system()
        # -------------------------
        if isinstance(node.func, ast.Attribute):
            if node.func.attr == "system":
                if isinstance(node.func.value, ast.Name):
                    if node.func.value.id == "os":
                        self.issues.append({
                            "type": "OSCommand",
                            "line": node.lineno,
                            "message": "Use of os.system() can lead to command injection"
                        })

        # -------------------------
        # 🔴 pickle.loads()
        # -------------------------
        if isinstance(node.func, ast.Attribute):
            if node.func.attr == "loads":
                if isinstance(node.func.value, ast.Name):
                    if node.func.value.id == "pickle":
                        self.issues.append({
                            "type": "UnsafeDeserialization",
                            "line": node.lineno,
                            "message": "Use of pickle.loads() is unsafe"
                        })

        # -------------------------
        # 🔴 open() → Path Traversal
        # -------------------------
        if isinstance(node.func, ast.Name) and node.func.id == "open":

            if node.args:
                arg = node.args[0]

                if isinstance(arg, ast.Name):
                    self.issues.append({
                        "type": "PathTraversal",
                        "line": node.lineno,
                        "message": "File opened using variable input"
                    })

                if isinstance(arg, ast.BinOp):
                    self.issues.append({
                        "type": "PathTraversal",
                        "line": node.lineno,
                        "message": "File path built using concatenation"
                    })

                if isinstance(arg, ast.JoinedStr):
                    self.issues.append({
                        "type": "PathTraversal",
                        "line": node.lineno,
                        "message": "File path built using f-string"
                    })

        self.generic_visit(node)

    def visit_Assign(self, node):
        
        # -------------------------
        # 🔥 TAINT SOURCE: input()
        # -------------------------
        if isinstance(node.value, ast.Call):
            if isinstance(node.value.func, ast.Name):
                if node.value.func.id == "input":
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            self.tainted_vars.add(target.id)

        # -------------------------
        # 🔥 TAINT PROPAGATION
        # -------------------------
        # 🔥 ADVANCED TAINT PROPAGATION
        if self.is_expr_tainted(node.value):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    self.tainted_vars.add(target.id)

        if isinstance(node.value, ast.Constant):
            value = str(node.value.value)

            if "password" in value.lower() or "api_key" in value.lower():
                self.issues.append({
                    "type": "HardcodedSecret",
                    "line": node.lineno,
                    "message": "Possible hardcoded secret detected"
                })

            if "mongodb+srv://" in value:
                self.issues.append({
                    "type": "MongoURI",
                    "line": node.lineno,
                    "message": "Hardcoded MongoDB URI detected"
                })

        self.generic_visit(node)

    # COMMON PATTERNS GENRATED BY AI
    # 1) empty except block->ignores error silently
    def visit_Try(self, node):
        for handler in node.handlers:
            if handler.type is None:
                # bare except
                if len(handler.body) == 1 and isinstance(handler.body[0], ast.Pass):
                    self.issues.append({
                        "type": "EmptyExcept",
                        "line": handler.lineno,
                        "message": "Empty except block detected (AI-generated unsafe pattern)"
                    })

        self.generic_visit(node)
    # 2) Broad exception details ->whatever may be error it will show error detected so thats hides real bugs
    def visit_ExceptHandler(self, node):
        if isinstance(node.type, ast.Name):
            if node.type.id == "Exception":
                self.issues.append({
                    "type": "BroadException",
                    "line": node.lineno,
                    "message": "Catching broad Exception may hide bugs"
                })

        self.generic_visit(node)
    # MORE SECURITY DETECTION
    # 1)SQL INJECTION ->WHEN IF IN STRING CONCATENATION ONE IS VARIABLE THEN HACKER CAN DO AUTHORIZATION BYPASS
    def visit_BinOp(self, node):
       

        # Detect string concatenation in SQL
        if isinstance(node.op, ast.Add):
            if isinstance(node.left, ast.Constant) and isinstance(node.right, ast.Name):

                if isinstance(node.left.value, str):
                    sql_keywords = ["SELECT", "INSERT", "UPDATE", "DELETE"]

                    if any(k in node.left.value.upper() for k in sql_keywords):
                        self.issues.append({
                            "type": "SQLInjection",
                            "line": node.lineno,
                            "message": "Possible SQL injection via string concatenation"
                        })

        self.generic_visit(node)
    # 2)DESERIALIZATION A DATA IS SERIALIZED WHEN SENT/STORED AND THEN DESERIALIZED WHEN USING IT IF ATTACKER CONTROLS WHAT TO BECONTROLLED SO THIS IS DANGEROUS
    
    # 3) PATH TRAVERSAL ->FILE ACCESSING BUT PATH IS CONTROLLED BY A VARIABLE WHAT IF VARIABLE CONTAINS PATH OF SENSITIVE FILES OR OF UNAUTHORIZED FILES OR FILES CONTAINING PASSWORDS
   