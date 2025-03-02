import tkinter as tk
from interpreter import evaluate

class LambdaCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Lambda Calculator")
        self.geometry("400x250")

        self.expression_entry = tk.Entry(self, width=50)
        self.expression_entry.pack(pady=20)

        eval_button = tk.Button(self, text="Evaluate", command=self.evaluate_expression)
        eval_button.pack()

        self.result_label = tk.Label(self, text="Result: Waiting for input...")
        self.result_label.pack(pady=20)

    def evaluate_expression(self):
        expression = self.expression_entry.get()
        print(f"Expression entered: {expression}")
        trace = evaluate(expression)
        result = trace[-1]
        print(f"Result calculated: {result}")
        self.result_label.config(text=f"Result: {result}")
