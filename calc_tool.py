from langchain.tools import tool

@tool
def calculator(expression: str):
    """
    Evaluate a mathematical expression.
    """
    return str(eval(expression))