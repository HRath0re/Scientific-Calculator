import tkinter as tk
import math

class SciCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Scientific Calculator")
        self.geometry("420x620")
        self.resizable(False, False)
        self.configure(bg="#1E1E1E")

        self.equation = ""
        self.result_var = tk.StringVar()

        self.create_widgets()
        self.bind_keys()

    def create_widgets(self):
        # Display
        entry = tk.Entry(
            self, textvariable=self.result_var, font=("Consolas", 28),
            bg="#1E1E1E", fg="white", bd=0, relief="flat",
            justify="right", insertbackground="white"
        )
        entry.grid(row=0, column=0, columnspan=5, padx=15, pady=20, sticky="nsew")

        # Button Layout
        btn_texts = [
            ['C', 'DEL', '(', ')', '/'],
            ['7', '8', '9', '*', 'sqrt'],
            ['4', '5', '6', '-', '^'],
            ['1', '2', '3', '+', 'log'],
            ['0', '.', 'pi', 'e', '='],
            ['sin', 'cos', 'tan', 'ln', 'exp']
        ]

        for i, row in enumerate(btn_texts):
            for j, text in enumerate(row):
                btn = tk.Button(
                    self, text=text, font=("Segoe UI", 16, "bold"),
                    bd=0, fg="white",
                    bg="#2D2D30" if text not in {"=", "C"} 
                    else "#007ACC" if text == "=" else "#D9534F",
                    activebackground="#3E3E40",
                    activeforeground="white",
                    command=lambda val=text: self.on_click(val)
                )
                btn.grid(row=i+1, column=j, padx=4, pady=4, sticky="nsew")
                btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#444"))
                btn.bind("<Leave>", lambda e, b=btn, t=text: b.config(
                    bg="#2D2D30" if t not in {"=", "C"} 
                    else "#007ACC" if t == "=" else "#D9534F"))

        # Make grid responsive
        for i in range(7):
            self.rowconfigure(i, weight=1)
        for j in range(5):
            self.columnconfigure(j, weight=1)

    def bind_keys(self):
        """Allow keyboard input."""
        self.bind("<Return>", lambda e: self.on_click("="))
        self.bind("<BackSpace>", lambda e: self.on_click("DEL"))
        self.bind("<Escape>", lambda e: self.on_click("C"))
        for char in "0123456789+-*/().":
            self.bind(char, lambda e, c=char: self.on_click(c))

    def on_click(self, key):
        if key == "=":
            try:
                expr = self.equation.replace("^", "**")
                expr = expr.replace('pi', str(math.pi)).replace('e', str(math.e))
                allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
                result = eval(expr, {"__builtins__": None}, allowed_names)
                self.result_var.set(str(result))
                self.equation = str(result)
            except Exception:
                self.result_var.set("Error")
                self.equation = ""
        elif key == "C":
            self.equation = ""
            self.result_var.set("")
        elif key == "DEL":
            self.equation = self.equation[:-1]
            self.result_var.set(self.equation)
        elif key == "sqrt":
            self.equation += "sqrt("
            self.result_var.set(self.equation)
        elif key in {"sin", "cos", "tan", "log", "ln", "exp"}:
            if key == "log": self.equation += "log10("
            elif key == "ln": self.equation += "log("
            else: self.equation += f"{key}("
            self.result_var.set(self.equation)
        else:
            self.equation += key
            self.result_var.set(self.equation)

if __name__ == "__main__":
    app = SciCalculator()
    app.mainloop()
