import re

class Calculator:
    def __init__(self):
        self.operators = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
        }
        # Precedence for operators. Higher number means higher precedence.
        # Parentheses are handled separately in the evaluation logic.
        self.precedence = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
        }

    def _tokenize(self, expression):
        # This regex will match:
        # - Numbers (integers or floats): r'\d+\.?\d*'
        # - Operators: r'[+\-*/]'
        # - Parentheses: r'[()]'
        # It will also handle any other non-whitespace character as a separate token r'\S'
        # The order matters: more specific patterns first.
        token_pattern = re.compile(r'\d+\.?\d*|[+\-*/()]|\S')
        tokens = token_pattern.findall(expression)
        return tokens

    def evaluate(self, expression):
        if not expression or expression.isspace():
            return None
        tokens = self._tokenize(expression)
        return self._evaluate_infix(tokens)

    def _evaluate_infix(self, tokens):
        values = []
        operators = []

        for token in tokens:
            if token == '(':
                operators.append(token)
            elif token == ')':
                # Pop and apply operators until an opening parenthesis is found
                while operators and operators[-1] != '(':
                    self._apply_operator(operators, values)
                if not operators or operators[-1] != '(':
                    raise ValueError("Mismatched parentheses")
                operators.pop()  # Pop the '('
            elif token in self.operators:
                # Apply operators from the stack with higher or equal precedence
                # Stop if an opening parenthesis is encountered, as it defines a new scope
                while (
                    operators
                    and operators[-1] != '('
                    and self.precedence.get(operators[-1], 0) >= self.precedence.get(token, 0)
                ):
                    self._apply_operator(operators, values)
                operators.append(token)
            else:
                try:
                    values.append(float(token))
                except ValueError:
                    raise ValueError(f"Invalid token: {token}")

        # After processing all tokens, apply any remaining operators
        while operators:
            if operators[-1] == '(':
                raise ValueError("Mismatched parentheses") # Unmatched opening parenthesis
            self._apply_operator(operators, values)

        if len(values) != 1:
            raise ValueError("Invalid expression")

        return values[0]

    def _apply_operator(self, operators, values):
        if not operators:
            return

        operator = operators.pop()
        if len(values) < 2:
            raise ValueError(f"Not enough operands for operator {operator}")

        b = values.pop()
        a = values.pop()
        values.append(self.operators[operator](a, b))
