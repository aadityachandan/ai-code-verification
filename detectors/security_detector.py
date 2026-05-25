import ast
from utils.scorer import compute_confidence


class SecurityDetector(ast.NodeVisitor):
    def __init__(self):
        self.issues = []
        self.tainted_vars = set()
        self.functions = {}
        # Track functions that return tainted data
        self.function_returns_tainted = {}
        #WHICH FUNCTIONS ARE RETURNING TRAINT VALUES

        self.safe_functions = {
    "int",
    "float",
    "str",
    "bool",
    "ast.literal_eval",
    "escape",
    "quote"
}

        # Prevent duplicate function analysis
        self.visited_contexts = set()

        # Prevent duplicate issues
        self.seen_issues = set()
    # -------------------------
    # 🔥 CLEAN ISSUE ADDER
    # -------------------------
    def add_issue(self, issue):

        key = (
            issue["type"],
            issue["line"]
        )

        if key not in self.seen_issues:
            self.issues.append(issue)
            self.seen_issues.add(key)
        # -------------------------
        # 🔥 FUNCTION TRACKING
        # -------------------------
    def visit_FunctionDef(self, node):

        # Store function
        self.functions[node.name] = node

        # ---------------------------------
        # STATIC LIGHTWEIGHT ANALYSIS
        # ---------------------------------

        old_taint = self.tainted_vars.copy()

        # Conservatively assume parameters
        # may be tainted
        

        # Analyze function body
        for stmt in node.body:
            self.visit(stmt)

        # ---------------------------------
        # CHECK IF FUNCTION RETURNS TAINTED DATA
        # ---------------------------------

        returns_tainted = False

        for stmt in ast.walk(node):

            if isinstance(stmt, ast.Return):

                if stmt.value and self.is_expr_tainted(stmt.value):
                    returns_tainted = True

        # Store function summary
        self.function_returns_tainted[node.name] = returns_tainted
        # Restore taint state
        self.tainted_vars = old_taint
    # -------------------------
    # 🔥 DEPTH CALCULATION
    # -------------------------
    def get_expr_depth(self, node):
        if isinstance(node, ast.Name):
            return 1

        if isinstance(node, ast.BinOp):
            return 1 + max(
                self.get_expr_depth(node.left),
                self.get_expr_depth(node.right)
            )

        if isinstance(node, ast.Call):
            return 1 + max(
                [self.get_expr_depth(arg) for arg in node.args] or [1]
            )

        return 1

    # -------------------------
    # 🔥 TAINT CHECK
    # -------------------------
    def is_expr_tainted(self, node):
        if isinstance(node, ast.Name):
            return node.id in self.tainted_vars

        if isinstance(node, ast.Constant):
            return False

        if isinstance(node, ast.BinOp):
            return (
                self.is_expr_tainted(node.left) or
                self.is_expr_tainted(node.right)
            )

        if isinstance(node, ast.Call):

            # ---------------------------------
            # input() is direct taint source
            # ---------------------------------

            if isinstance(node.func, ast.Name):
                if node.func.id == "input":
                    return True

            # ---------------------------------
            # Get function name
            # ---------------------------------

            func_name = None

            if isinstance(node.func, ast.Name):
                func_name = node.func.id

            elif isinstance(node.func, ast.Attribute):
                func_name = f"{ast.unparse(node.func.value)}.{node.func.attr}"

            # ---------------------------------
            # Sanitizers
            # ---------------------------------

            if func_name in self.safe_functions:
                return False

            # ---------------------------------
            # ONLY taint if function RETURNS tainted data
            # ---------------------------------

            if func_name in self.function_returns_tainted:
                return self.function_returns_tainted[func_name]

            return False
        if isinstance(node, ast.JoinedStr):
            for value in node.values:
                if isinstance(value, ast.FormattedValue):
                    if self.is_expr_tainted(value.value):
                        return True

        return False

    # -------------------------
    # 🔥 FUNCTION CALL HANDLING
    # -------------------------
    def visit_Call(self, node):


            

        # 🔴 eval()
        if isinstance(node.func, ast.Name) and node.func.id == "eval":
            if node.args:
                arg = node.args[0]

                if self.is_expr_tainted(arg):
                    depth = self.get_expr_depth(arg)
                    confidence = compute_confidence("EvalTainted", depth)

                    self.add_issue({
                        "type": "EvalTainted",
                        "line": node.lineno,
                        "message": "Tainted input used in eval()",
                        "severity": "CRITICAL",
                        "confidence": confidence
                    })
                else:
                    confidence = compute_confidence("EvalUsage")

                    self.add_issue({
                        "type": "EvalUsage",
                        "line": node.lineno,
                        "message": "Use of eval() is dangerous",
                        "severity": "HIGH",
                        "confidence": confidence
                    })
            return

        # 🔴 exec()
        if isinstance(node.func, ast.Name) and node.func.id == "exec":
            if node.args:
                arg = node.args[0]

                if self.is_expr_tainted(arg):
                    depth = self.get_expr_depth(arg)
                    confidence = compute_confidence("ExecTainted", depth)

                    self.add_issue({
                        "type": "ExecTainted",
                        "line": node.lineno,
                        "message": "Tainted input used in exec()",
                        "severity": "CRITICAL",
                        "confidence": confidence
                    })
                else:
                    confidence = compute_confidence("ExecUsage")

                    self.add_issue({
                        "type": "ExecUsage",
                        "line": node.lineno,
                        "message": "Use of exec() is dangerous",
                        "severity": "HIGH",
                        "confidence": confidence
                    })
            return

        # 🔴 os.system()
        if isinstance(node.func, ast.Attribute):
            if node.func.attr == "system":
                if node.args:
                    arg = node.args[0]

                    if self.is_expr_tainted(arg):
                        depth = self.get_expr_depth(arg)
                        confidence = compute_confidence("CommandInjection", depth)

                        self.add_issue({
                            "type": "CommandInjection",
                            "line": node.lineno,
                            "message": "Tainted input in os.system()",
                            "severity": "CRITICAL",
                            "confidence": confidence
                        })
                    else:
                        confidence = compute_confidence("OSCommand")

                        self.add_issue({
                            "type": "OSCommand",
                            "line": node.lineno,
                            "message": "Use of os.system() can be unsafe",
                            "severity": "HIGH",
                            "confidence": confidence
                        })
                return

        # 🔴 open()
        if isinstance(node.func, ast.Name) and node.func.id == "open":
            if node.args:
                arg = node.args[0]

                if self.is_expr_tainted(arg):
                    depth = self.get_expr_depth(arg)
                    confidence = compute_confidence("PathTraversal", depth)

                    self.add_issue({
                        "type": "PathTraversal",
                        "line": node.lineno,
                        "message": "Tainted input used in file path",
                        "severity": "CRITICAL",
                        "confidence": confidence
                    })
                else:
                    confidence = compute_confidence("PathTraversalRisk")

                    self.add_issue({
                        "type": "PathTraversalRisk",
                        "line": node.lineno,
                        "message": "File path may be unsafe",
                        "severity": "HIGH",
                        "confidence": confidence
                    })
            return

        # 🔴 pickle.loads()
        if isinstance(node.func, ast.Attribute):
            if node.func.attr == "loads":
                if isinstance(node.func.value, ast.Name) and node.func.value.id == "pickle":

                    if node.args:
                        arg = node.args[0]

                        if self.is_expr_tainted(arg):
                            depth = self.get_expr_depth(arg)
                            confidence = compute_confidence("UnsafeDeserialization", depth)

                            self.add_issue({
                                "type": "UnsafeDeserialization",
                                "line": node.lineno,
                                "message": "Tainted input used in pickle.loads()",
                                "severity": "CRITICAL",
                                "confidence": confidence
                            })
                        else:
                            confidence = compute_confidence("UnsafeDeserializationRisk")

                            self.add_issue({
                                "type": "UnsafeDeserializationRisk",
                                "line": node.lineno,
                                "message": "pickle.loads() is unsafe",
                                "severity": "HIGH",
                                "confidence": confidence
                            })
                    return

        self.generic_visit(node)

        # 🔥 FUNCTION TAINT PROPAGATION
        # 🔥 FUNCTION PARAMETER TAINT PROPAGATION
        if isinstance(node.func, ast.Name):

            func_name = node.func.id

            if func_name in self.functions:

                func_def = self.functions[func_name]

                # -----------------------------
                # Build analysis context
                # -----------------------------
                context_key = (
                    func_name,
                    tuple(sorted(self.tainted_vars))
                )

                # Prevent duplicate analysis
                if context_key in self.visited_contexts:
                    return

                self.visited_contexts.add(context_key)

                # Save old taint state
                old_taint = self.tainted_vars.copy()

                # Inject tainted parameters
                for i, arg in enumerate(node.args):

                    if i < len(func_def.args.args):

                        param_name = func_def.args.args[i].arg

                        if self.is_expr_tainted(arg):
                            self.tainted_vars.add(param_name)

                # Analyze function body
                for stmt in func_def.body:
                    self.visit(stmt)

                # Restore taint state
                self.tainted_vars = old_taint
    # -------------------------
    # 🔥 TAINT SOURCE + PROPAGATION
    # -------------------------
    def visit_Assign(self, node):
        if isinstance(node.value, ast.Call):
            if isinstance(node.value.func, ast.Name):
                if node.value.func.id == "input":
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            self.tainted_vars.add(target.id)

        if self.is_expr_tainted(node.value):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    self.tainted_vars.add(target.id)

        # ---------------------------------
        # FUNCTION RETURN TAINT PROPAGATION
        # ---------------------------------

        if isinstance(node.value, ast.Call):

            if isinstance(node.value.func, ast.Name):

                func_name = node.value.func.id

                # Function returns tainted data
                if self.function_returns_tainted.get(func_name):

                    for target in node.targets:

                        if isinstance(target, ast.Name):

                            self.tainted_vars.add(target.id)

        # 🔐 Hardcoded secrets
        if isinstance(node.value, ast.Constant):
            value = str(node.value.value)

            if "password" in value.lower() or "api_key" in value.lower():
                self.add_issue({
                    "type": "HardcodedSecret",
                    "line": node.lineno,
                    "message": "Possible hardcoded secret detected",
                    "severity": "HIGH",
                    "confidence": compute_confidence("HardcodedSecret")
                })

            if "mongodb+srv://" in value:
                self.add_issue({
                    "type": "MongoURI",
                    "line": node.lineno,
                    "message": "Hardcoded MongoDB URI detected",
                    "severity": "HIGH",
                    "confidence": compute_confidence("MongoURI")
                })

        self.generic_visit(node)

    # -------------------------
    # 🔥 EXCEPTION HANDLING
    # -------------------------
    def visit_Try(self, node):
        for handler in node.handlers:
            if handler.type is None:
                if len(handler.body) == 1 and isinstance(handler.body[0], ast.Pass):
                    self.add_issue({
                        "type": "EmptyExcept",
                        "line": handler.lineno,
                        "message": "Empty except block detected",
                        "severity": "MEDIUM",
                        "confidence": compute_confidence("EmptyExcept")
                    })

        self.generic_visit(node)

    def visit_ExceptHandler(self, node):
        if isinstance(node.type, ast.Name):
            if node.type.id == "Exception":
                self.add_issue({
                    "type": "BroadException",
                    "line": node.lineno,
                    "message": "Catching broad Exception may hide bugs",
                    "severity": "MEDIUM",
                    "confidence": compute_confidence("BroadException")
                })

        self.generic_visit(node)

    # -------------------------
    # 🔥 SQL Injection
    # -------------------------
    def visit_BinOp(self, node):
        if isinstance(node.op, ast.Add):
            if isinstance(node.left, ast.Constant) and isinstance(node.left.value, str):

                sql_keywords = ["SELECT", "INSERT", "UPDATE", "DELETE"]

                if any(k in node.left.value.upper() for k in sql_keywords):

                    if self.is_expr_tainted(node.right):
                        depth = self.get_expr_depth(node.right)
                        confidence = compute_confidence("SQLInjection", depth)

                        self.add_issue({
                            "type": "SQLInjection",
                            "line": node.lineno,
                            "message": "Tainted input used in SQL query",
                            "severity": "CRITICAL",
                            "confidence": confidence
                        })
                    else:
                        confidence = compute_confidence("SQLInjectionRisk")

                        self.add_issue({
                            "type": "SQLInjectionRisk",
                            "line": node.lineno,
                            "message": "Possible SQL injection",
                            "severity": "HIGH",
                            "confidence": confidence
                        })

        self.generic_visit(node)