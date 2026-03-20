import ast

def parse_code(code):
    try:
        return ast.parse(code)
    except SyntaxError as e:
        print(f"Syntax Error: {e}")
        return None