import unittest
from interpreter import split_lambda_expression  # Import your function


class TestSplitLambdaExpression(unittest.TestCase):

    def test_single_lambda(self):
        self.assertEqual(split_lambda_expression("λx.x"), ["λx.x"])

    def test_simple_application(self):
        self.assertEqual(split_lambda_expression("(λx.x) 5"), ["λx.x", "5"])

    def test_multiple_applications(self):
        self.assertEqual(split_lambda_expression("(λx.x) (5) (10)"), ["λx.x", "5", "10"])

    def test_nested_lambda(self):
        self.assertEqual(split_lambda_expression("λx.(λy.xy)"), ["λx.(λy.xy)"])

    def test_complex_lambda(self):
        self.assertEqual(split_lambda_expression("λx.(λy.(λz.xyz))"), ["λx.(λy.(λz.xyz))"])

    def test_lambda_with_application(self):
        self.assertEqual(split_lambda_expression("(λx.(λy.xy)) 5 10"), ["λx.(λy.xy)", "5", "10"])

    def test_lambda_with_parentheses(self):
        self.assertEqual(split_lambda_expression("λx.(λy.xy)"), ["λx.(λy.xy)"])

    def test_lambda_with_inner_application(self):
        """Test lambda expression where an inner function is applied"""
        self.assertEqual(split_lambda_expression("(λx.(λy.(λz.xyz))) (3)"), ["λx.(λy.(λz.xyz))", "3"])


if __name__ == "__main__":
    unittest.main()
