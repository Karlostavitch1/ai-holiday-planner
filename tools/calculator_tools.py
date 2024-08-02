from langchain.tools import tool
import ast

class CalculatorTools:

    @tool("Make a calculation")
    def calculate(operation):
        """Useful to perform any mathematical calculations, 
        like sum, minus, multiplication, division, etc.
        The input to this tool should be a mathematical 
        expression, a couple examples are `200*7` or `5000/2*10`
        """
        try:
            # Safely evaluate the expression
            return eval(compile(ast.parse(operation, mode='eval'), '', 'eval'))
        except (SyntaxError, ValueError, TypeError) as e:
            return f"Error: Invalid syntax in mathematical expression ({e})"
