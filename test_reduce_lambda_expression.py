import unittest
from interpreter import reduce_lambda_expression, parse_lambda_expression, LambdaExpression, Variable, Application


class TestReduceLambdaExpression(unittest.TestCase):
    def test_identity_function(self):
        expr = reduce_lambda_expression(parse_lambda_expression("λx.x"), parse_lambda_expression("a"))
        self.assertEqual(str(expr), "a")

    def test_constant_function(self):
        expr = reduce_lambda_expression(parse_lambda_expression("λx.y"), parse_lambda_expression("z"))
        self.assertEqual(str(expr), "y")

    def test_simple_application(self):
        expr = reduce_lambda_expression(parse_lambda_expression("λx.x"), parse_lambda_expression("5"))
        self.assertEqual(str(expr), "5")

    def test_lambda_application(self):  # fix
        expr = reduce_lambda_expression(parse_lambda_expression("λx.λy.xy"), parse_lambda_expression("a"))
        self.assertEqual(str(expr), "λy.ay")

    def test_lambda_application_second(self):
        expr = reduce_lambda_expression(parse_lambda_expression("λx.yx"), parse_lambda_expression("a"))
        self.assertEqual(str(expr), "ya")

    def test_application_with_lambda_body(self):
        expr = reduce_lambda_expression(parse_lambda_expression("λx.(λy.xy)"), parse_lambda_expression("a"))
        self.assertEqual(str(expr), "λy.ay")

    def test_double_application(self):
        expr = reduce_lambda_expression(parse_lambda_expression("λx.x"), parse_lambda_expression("λy.y"))
        self.assertEqual(str(expr), "λy.y")


if __name__ == "__main__":
    unittest.main()
