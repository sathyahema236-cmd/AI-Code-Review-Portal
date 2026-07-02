from utils.gemini_ai import review_code

code = """
a = 10
b = 20
print(a+b)
"""

result = review_code(code)

print(result)