import tkinter as tk
from interpreter import evaluate, TransformationStep


class LambdaCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Lambda Calculator")
        self.geometry("500x400")

        self.expression_entry = tk.Entry(self, width=50, font=("Arial", 14))
        self.expression_entry.pack(pady=10)

        lambda_button = tk.Button(self, text="Insert λ", command=self.insert_lambda, font=("Arial", 12))
        lambda_button.pack(pady=5)

        eval_button = tk.Button(self, text="Evaluate", command=self.evaluate_expression, font=("Arial", 12))
        eval_button.pack(pady=5)

        text_frame = tk.Frame(self)
        text_frame.pack(pady=10, fill="both", expand=True)

        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side="right", fill="y")

        self.result_text = tk.Text(text_frame, height=10, width=60, font=("Arial", 12), state="disabled",
                                   yscrollcommand=scrollbar.set)
        self.result_text.pack(side="left", fill="both", expand=True)

        scrollbar.config(command=self.result_text.yview)

    def insert_lambda(self):
        self.expression_entry.insert(tk.INSERT, "λ")

    def evaluate_expression(self):
        expression = self.expression_entry.get()
        print(f"Expression entered: {expression}")

        trace_steps = evaluate(expression)

        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)

        i = 1
        for step in trace_steps:
            if isinstance(step, TransformationStep):
                step_text = f"Step: {step.transformation_name}\nExpression: {step.expression}\n\n"
            else:
                step_text = str(step) + "\n\n"

            step_text = f"{i}. {step_text}"
            self.result_text.insert(tk.END, step_text)
            i += 1

        self.result_text.config(state="disabled")
