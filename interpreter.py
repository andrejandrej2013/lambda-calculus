import re
import string


class LambdaExpression:
    def __init__(self, variable, body):
        self.variable = variable
        self.body = body

    def __str__(self):
        return f"λ{self.variable}.{self.body}"


class Application:
    def __init__(self, func, arg):
        self.func = func
        self.arg = arg

    def __str__(self):
        return f"{self.func} {self.arg}"


class Variable:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class TransformationStep:
    def __init__(self, expression: str, transformation_name: str):
        self.expression = expression
        self.transformation_name = transformation_name

    def __str__(self):
        return f"Step: {self.transformation_name}\nExpression: {self.expression}"


def parse_lambda_expression(expression):
    match = re.match(r"λ([a-zA-Z]+)\.(.+)", expression)
    if match:
        vars_part, body = match.groups()

        body = remove_outer_parentheses(body)

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


def format_lambda_expression(expression) -> str:
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
            tokens.append(expression[start + 1:i])
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
    if isinstance(expression, Variable):
        return value if expression.name == var else expression
    elif isinstance(expression, LambdaExpression):
        if expression.variable == var:
            return expression
        return LambdaExpression(expression.variable, substitute(expression.body, var, value))
    elif isinstance(expression, Application):
        return Application(substitute(expression.func, var, value), substitute(expression.arg, var, value))
    return expression


def reduce_lambda_expression(func, arg):
    if isinstance(func, LambdaExpression):
        return substitute(func.body, func.variable, arg)
    elif isinstance(func, Application):
        reduced_func = reduce_lambda_expression(func.func, func.arg)
        return Application(reduced_func, arg)
    return Application(func, arg)


def apply_lambda_reductions(expression: str) -> list:
    lambda_transforms = add_trace([], expression, 'Start')

    expression_parts = split_lambda_expression(expression)

    head_expr = expression_parts[0]
    head_expr = parse_lambda_expression(head_expr)
    lambda_transforms = add_trace(lambda_transforms, head_expr, 'α conversion of first part')

    for i in range(1, len(expression_parts)):
        lambda_transforms = add_trace(lambda_transforms, expression_parts[i], 'Take next part')

        parsed_expr = parse_lambda_expression(expression_parts[i])
        lambda_transforms = add_trace(lambda_transforms, parsed_expr, 'α conversion', expression_parts[i])

        resolved_head_expr = resolve_variable_conflicts(head_expr, parsed_expr)
        if str(resolved_head_expr) != str(head_expr):
            lambda_transforms = add_trace(lambda_transforms, f"{resolved_head_expr} -> {head_expr}", 'resolve variable conflicts')
            head_expr = resolved_head_expr

        reduced_expr = reduce_lambda_expression(head_expr, parsed_expr)
        lambda_transforms = add_trace(lambda_transforms, reduced_expr, 'β reduction', parsed_expr)

        head_expr = parse_lambda_expression(str(reduced_expr))
        lambda_transforms = add_trace(lambda_transforms, head_expr, 'α conversion', str(reduced_expr))

    head_expr_str = format_lambda_expression(str(head_expr))

    lambda_transforms = add_trace(lambda_transforms, head_expr_str, 'End')

    church_result = detect_church_encoding(head_expr)
    if church_result:
        lambda_transforms = add_trace(lambda_transforms, church_result, "Church Encoding Recognition")

    return lambda_transforms


def resolve_variable_conflicts(lambda_expr, arg_expr):
    if not isinstance(lambda_expr, LambdaExpression):
        return lambda_expr

    bound = get_bound(arg_expr)
    existing_var = get_bound(lambda_expr)
    existing_var.update(bound)

    return replace_variable_conflicts(lambda_expr, bound, existing_var)


def replace_variable_conflicts(lambda_expr, bound, existing_var):
    if len(bound) == 0:
        return lambda_expr

    replacement_variable = generate_unique_variable(existing_var)

    lambda_expr = str(lambda_expr)

    for var in bound:
        lambda_expr, count = re.subn(var, replacement_variable, lambda_expr)

        if count > 0:
            existing_var.add(replacement_variable)
            replacement_variable = generate_unique_variable(existing_var)

    return parse_lambda_expression(lambda_expr)


def generate_unique_variable(existing_vars):
    for char in string.ascii_lowercase:  # Uses 'a' to 'z'
        if char not in existing_vars:
            return char

    counter = 1
    while True:
        candidate = f"x{counter}"
        if candidate not in existing_vars:
            return candidate
        counter += 1


def get_bound(expression, bound=None):
    if bound is None:
        bound = set()
    if isinstance(expression, Variable):
        for var in expression.name:
            bound.add(var)
        return bound
    if isinstance(expression, LambdaExpression):
        bound = get_bound(expression.variable, bound)
        bound = get_bound(expression.body, bound)
    return bound



def detect_church_encoding(expression):
    str_expr = str(expression)

    match = re.match(r"λ([a-zA-Z]+)\.λ([a-zA-Z]+)\.\1$", str_expr)
    if match:
        return "True"

    match = re.match(r"λ([a-zA-Z]+)\.λ([a-zA-Z]+)\.\2$", str_expr)
    if match:
        return "False"

    return None


def remove_outer_parentheses(expression):
    while expression.startswith("(") and expression.endswith(")"):
        balance = 0
        for i, char in enumerate(expression):
            if char == "(":
                balance += 1
            elif char == ")":
                balance -= 1
            if balance == 0 and i != len(expression) - 1:
                return expression
        expression = expression[1:-1]
    return expression


def add_trace(
        lambda_transforms: list,
        current_transformation,
        transformation_name,
        previous_transformation=None,
) -> list:
    if str(previous_transformation) != str(current_transformation):
        lambda_transforms.append(TransformationStep(current_transformation, transformation_name))

    return lambda_transforms


def evaluate(expression_str):
    clean_expression = format_lambda_expression(expression_str)

    if not clean_expression:
        raise ValueError("Error: The input string cannot be empty or None")

    lambda_transforms = apply_lambda_reductions(clean_expression)

    return lambda_transforms
