import re


class LambdaExpression:
    def __init__(self, variable, body):
        self.variable = variable
        self.body = body

    def __str__(self):
        return f"(λ{self.variable}.{self.body})"

class Application:
    def __init__(self, func, arg):
        self.func = func
        self.arg = arg

    def __str__(self):
        return f"({self.func} {self.arg})"

class Variable:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

class TransformationStep:
    def __init__(self, expression: str, transformation: str, previous_step=None):
        self.expression = expression
        self.transformation = transformation
        self.previous_step = previous_step

    def __str__(self):
        return f"Step: {self.transformation}\nExpression: {self.expression}"

    def get_trace(self):
        trace = []
        step = self
        while step:
            trace.append(str(step))
            step = step.previous_step
        return "\n".join(reversed(trace))


def parse_lambda_expression(expression):
    match = re.match(r"λ([a-zA-Z]+)\.(.+)", expression)
    if match:
        vars_part, body = match.groups()

        seen_vars = set()
        unique_vars = []
        for var in vars_part:
            if var not in seen_vars:
                unique_vars.append(var)
                seen_vars.add(var)

        parsed_body = parse_lambda_expression(body)

        for var in reversed(unique_vars):
            parsed_body = LambdaExpression(var, parsed_body)

        return parsed_body

    tokens = expression.split()
    if len(tokens) == 1:
        return Variable(expression)

    return Application(parse_lambda_expression(tokens[0]), parse_lambda_expression(" ".join(tokens[1:])))


def format_lambda_expression(expression):
    expression = expression.strip()
    expression = re.sub(r'\s+', ' ', expression)
    expression = re.sub(r"\. ", ".", expression)
    tokens = expression.split()

    if len(tokens) > 1:
        for i in range(len(tokens)):
            if not tokens[i].startswith("("):
                tokens[i] = f"({tokens[i]})"

    lambda_count = 0
    for i in range(len(tokens)):
        tokens[i], count = re.subn(r"\.λ", ".(λ", tokens[i])

        tokens[i] = f"{tokens[i]}" + (")" * count)

    return "".join(tokens)


def split_lambda_expression(expression):
    expression = expression.strip()

    if expression.startswith("λ"):
        match = re.match(r"(λ[a-zA-Z]+\.)(.+)", expression)
        if match:
            lambda_part, body = match.groups()
            return [lambda_part + body]

    tokens = []
    i = 0
    while i < len(expression):
        if expression[i] == "(":
            start = i
            count = 0
            while i < len(expression):
                if expression[i] == "(":
                    count += 1
                elif expression[i] == ")":
                    count -= 1
                    if count == 0:
                        break
                i += 1
            tokens.append(expression[start+1:i])
            i += 1
        else:
            match = re.match(r"[a-zA-Z0-9]+", expression[i:])
            if match:
                tokens.append(match.group(0))
                i += len(match.group(0))
            else:
                i += 1

    return tokens


def substitute(expression, var, value):
    """Performs substitution of 'var' with 'value' in 'expression'."""
    if isinstance(expression, Variable):
        return value if expression.name == var else expression
    elif isinstance(expression, LambdaExpression):
        if expression.variable == var:
            return expression  # Don't substitute inside bound variables
        return LambdaExpression(expression.variable, substitute(expression.body, var, value))
    elif isinstance(expression, Application):
        return Application(substitute(expression.func, var, value), substitute(expression.arg, var, value))
    return expression


def reduce_lambda_expression(func, arg):
    """Reduces a lambda function application (β-reduction)."""
    if isinstance(func, LambdaExpression):  # If func is λx.body
        return substitute(func.body, func.variable, arg)  # Apply argument
    elif isinstance(func, Application):  # Reduce inside applications
        reduced_func = reduce_lambda_expression(func.func, func.arg)
        return Application(reduced_func, arg)
    return Application(func, arg)


def apply_lambda_reductions(expression: str) -> list:
    lambda_transforms = [expression]

    expression_parts = split_lambda_expression(expression)

    head_expr = expression_parts[0]
    head_expr = parse_lambda_expression(head_expr)

    for i in range(1, len(expression_parts)):
        parsed_expr = parse_lambda_expression(expression_parts[i])
        reduced_expr = reduce_lambda_expression(head_expr, parsed_expr)
        head_expr = parse_lambda_expression(str(reduced_expr))

    lambda_transforms.append(str(head_expr))

    return lambda_transforms


def evaluate(expression_str):
    clean_expression = format_lambda_expression(expression_str)

    if not clean_expression:
        raise ValueError("Error: The input string cannot be empty or None")

    lambda_transforms = apply_lambda_reductions(clean_expression)

    return lambda_transforms
