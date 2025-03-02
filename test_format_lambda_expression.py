import unittest
from interpreter import format_lambda_expression


class TestFormatLambdaExpression(unittest.TestCase):

    def test_single_lambda(self):
        self.assertEqual(format_lambda_expression("λx.x"), "λx.x")

    def test_simple_application(self):
        self.assertEqual(format_lambda_expression("λx.x 5"), "(λx.x)(5)")

    def test_nested_lambda(self):
        self.assertEqual(format_lambda_expression("λx.λy.xy"), "λx.(λy.xy)")

    def test_multiple_applications(self):
        self.assertEqual(format_lambda_expression("λx.λy.xy z w"), "(λx.(λy.xy))(z)(w)")

    def test_nested_application(self):
        self.assertEqual(format_lambda_expression("λa.λb.ab c d e"), "(λa.(λb.ab))(c)(d)(e)")

    def test_lambda_with_complex_body(self):
        self.assertEqual(format_lambda_expression("λx. (λy. xy) 5"), "(λx.(λy.xy))(5)")

    def test_lambda_with_nested_structure(self):
        self.assertEqual(format_lambda_expression("λysy.(λl.(λz.xyz)) 4 5"), "(λysy.(λl.(λz.xyz)))(4)(5)")

    def test_application_with_parentheses(self):
        self.assertEqual(format_lambda_expression("(λx. x) (λy. y)"), "(λx.x)(λy.y)")

    def test_single_variable(self):
        self.assertEqual(format_lambda_expression("x"), "x")


if __name__ == '__main__':
    unittest.main()
