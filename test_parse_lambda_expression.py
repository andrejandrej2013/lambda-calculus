import unittest
from interpreter import parse_lambda_expression, LambdaExpression, Application, Variable


class TestParseLambdaExpression(unittest.TestCase):
    def test_single_variable(self):
        expr = parse_lambda_expression("x")
        self.assertIsInstance(expr, Variable)
        self.assertEqual(str(expr), "x")

    def test_simple_lambda_expression(self):
        expr = parse_lambda_expression("λx.x")
        self.assertIsInstance(expr, LambdaExpression)
        self.assertEqual(str(expr), "λx.x")

    def test_lambda_with_multiple_variables(self):
        expr = parse_lambda_expression("λxy.xy")
        self.assertIsInstance(expr, LambdaExpression)
        self.assertEqual(str(expr), "λx.λy.xy")

    def test_lambda_application(self):
        expr = parse_lambda_expression("(λx.x) (y)")
        self.assertIsInstance(expr, Application)
        self.assertEqual(str(expr), "(λx.x) (y)")

    def test_complex_application(self):
        expr = parse_lambda_expression("(λx.x) (λy.y)")
        self.assertIsInstance(expr, Application)
        self.assertEqual(str(expr), "(λx.x) (λy.y)")

    def test_application_with_multiple_arguments(self):
        expr = parse_lambda_expression("(λx.x) (y) (z)")
        self.assertIsInstance(expr, Application)
        self.assertEqual(str(expr), "(λx.x) (y) (z)")

    def test_lambda_with_the_same_variables(self):
        expr = parse_lambda_expression("λxyx.xy")
        self.assertIsInstance(expr, LambdaExpression)
        self.assertEqual(str(expr), "λx.λy.xy")


if __name__ == "__main__":
    unittest.main()
