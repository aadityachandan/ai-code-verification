# examples/test_ai.py

user_input = input()

eval(user_input)

try:
    x = 10 / 0
except:
    pass

try:
    y = int("abc")
except Exception:
    print("error")