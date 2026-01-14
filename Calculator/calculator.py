class Calculator:

    PI = 3.14159265358979
    E = 2.71828182845904

    def __init__(self):
        self.equation = ""
        self.display_eq = ""
        self.history = []

    def clear(self):
        self.equation = ""
        self.display_eq = ""

    # --- FONCTIONS MATH ---

    def racine(self, n):
        if n < 0:
            return None
        x = n
        for _ in range(20):
            x = (x + n / x) / 2
        return x

    def fact(self, n):
        r = 1
        for i in range(2, int(n) + 1):
            r *= i
        return r

    def pow(self, b, e):
        if e == 0:
            return 1
        if e < 0:
            return 1 / self.pow(b, -e)
        if e == int(e):
            r = 1
            for _ in range(int(e)):
                r *= b
            return r
        return b ** e  # fallback Python pour décimaux

    def sin(self, deg):
        x = deg * self.PI / 180
        while x > self.PI: x -= 2 * self.PI
        while x < -self.PI: x += 2 * self.PI
        r, s = 0, 1
        for i in range(15):
            r += s * (x ** (2*i+1)) / self.fact(2*i+1)
            s *= -1
        return r

    def cos(self, deg):
        x = deg * self.PI / 180
        while x > self.PI: x -= 2 * self.PI
        while x < -self.PI: x += 2 * self.PI
        r, s = 0, 1
        for i in range(15):
            r += s * (x ** (2*i)) / self.fact(2*i)
            s *= -1
        return r

    def tan(self, deg):
        c = self.cos(deg)
        return None if c == 0 else self.sin(deg) / c

    # --- EVALUATION ---

    def add_value(self, val):
        conv = {"×": "*", "÷": "/", ",": ".", "%": "/100"}
        disp = {"×": "×", "÷": "÷", ",": ",", "%": "%"}

        funcs = {
            "sin": ("SIN(", "sin("), "cos": ("COS(", "cos("),
            "tan": ("TAN(", "tan("), "√": ("SQRT(", "√("),
            "π": (str(self.PI), "π"), "e": (str(self.E), "e"),
            "xʸ": ("**", "^"), "x²": ("**2", "²")
        }

        if val in conv:
            self.equation += conv[val]
            self.display_eq += disp[val]
        elif val in funcs:
            self.equation += funcs[val][0]
            self.display_eq += funcs[val][1]
        else:
            self.equation += val
            self.display_eq += val

    def get_display(self):
        return self.display_eq

    def find_closing(self, expr, start):
        level = 0
        for i in range(start, len(expr)):
            if expr[i] == "(": level += 1
            elif expr[i] == ")":
                if level == 0: return i
                level -= 1
        return len(expr)

    def eval_expr(self, expr):
        # Traiter fonctions
        for name, func in [("SIN", self.sin), ("COS", self.cos), ("TAN", self.tan), ("SQRT", self.racine)]:
            while name + "(" in expr:
                i = expr.find(name + "(")
                j = self.find_closing(expr, i + len(name) + 1)
                inner = self.eval_expr(expr[i + len(name) + 1:j])
                expr = expr[:i] + str(func(inner)) + expr[j + 1:]

        # Traiter parenthèses
        while "(" in expr:
            i = expr.rfind("(")
            j = expr.find(")", i)
            expr = expr[:i] + str(self.eval_simple(expr[i + 1:j])) + expr[j + 1:]

        return self.eval_simple(expr)

    def eval_simple(self, expr):
        # Tokenizer
        tokens, num = [], ""
        for i, c in enumerate(expr):
            if c in "0123456789.":
                num += c
            elif c == "-" and (i == 0 or expr[i-1] in "+-*/("):
                num += c
            elif c == "*" and i + 1 < len(expr) and expr[i + 1] == "*":
                if num: tokens.append(float(num)); num = ""
                tokens.append("**")
            elif c in "+-*/" and not (c == "*" and i > 0 and expr[i-1] == "*"):
                if num: tokens.append(float(num)); num = ""
                tokens.append(c)
        if num: tokens.append(float(num))

        # Priorité: ** puis */ puis +-
        for ops in [["**"], ["*", "/"], ["+", "-"]]:
            i = 0
            while i < len(tokens):
                if tokens[i] in ops:
                    a, op, b = tokens[i-1], tokens[i], tokens[i+1]
                    if op == "**": r = self.pow(a, b)
                    elif op == "*": r = a * b
                    elif op == "/": r = a / b if b != 0 else float('inf')
                    elif op == "+": r = a + b
                    else: r = a - b
                    tokens[i-1:i+2] = [r]
                else:
                    i += 1
        return tokens[0] if tokens else 0

    def calculate(self):
        try:
            # Fermer parenthèses
            n = self.equation.count("(") - self.equation.count(")")
            self.equation += ")" * n
            self.display_eq += ")" * n

            result = self.eval_expr(self.equation)

            if isinstance(result, float) and result == int(result):
                result = int(result)
            elif isinstance(result, float):
                result = round(result, 8)

            result_str = str(result).replace(".", ",")
            self.history.append(f"{self.display_eq} = {result_str}")
            self.equation = str(result)
            self.display_eq = result_str
            return result_str
        except:
            self.equation = ""
            self.display_eq = ""
            return "Erreur"

    def get_formatted_history(self):
        return "\n".join(reversed(self.history[-20:]))
