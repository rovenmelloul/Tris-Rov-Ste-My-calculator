import re


class CalculatorLogic:
    def __init__(self):
        self.equation = ""
        self.history = []

    # --- RESET ---
    def clear(self):
        self.equation = ""

    # --- AJOUTER UNE VALEUR ---
    def add_value(self, value):
        conversions = {"×": "*", "÷": "/", ",": "."}
        self.equation += conversions.get(value, value)

    # --- CALCULER LE RÉSULTAT ---
    def calculate(self):
        try:
            result = self._evaluate(self.equation)
            result_str = self._format_result(result)
            self.history.insert(0, f"{self.equation} = {result_str}")
            self.equation = str(result)
            return result_str
        except Exception:
            self.equation = ""
            return "Erreur"

    # --- ÉVALUATION PRINCIPALE ---
    def _evaluate(self, expr):
        expr = expr.replace(" ", "")
        tokens = self._tokenize(expr)
        tokens = self._apply_operations(tokens, ["*", "/", "%"])
        tokens = self._apply_operations(tokens, ["+", "-"])
        return tokens[0]

    # --- TOKENISER L'EXPRESSION ---
    def _tokenize(self, expr):
        pattern = r'(\d+\.?\d*|[+\-*/%])'
        elements = re.findall(pattern, expr)

        tokens = []
        for e in elements:
            if re.match(r'\d+\.?\d*', e):
                tokens.append(float(e))
            else:
                tokens.append(e)
        return tokens

    # --- APPLIQUER LES OPÉRATIONS ---
    def _apply_operations(self, tokens, operators):
        i = 0
        while i < len(tokens):
            if tokens[i] in operators:
                left = tokens[i - 1]
                op = tokens[i]
                right = tokens[i + 1]
                result = self._compute(left, op, right)
                tokens[i - 1:i + 2] = [result]
            else:
                i += 1
        return tokens

    # --- CALCUL D'UNE OPÉRATION ---
    def _compute(self, a, op, b):
        operations = {
            "+": lambda x, y: x + y,
            "-": lambda x, y: x - y,
            "*": lambda x, y: x * y,
            "/": lambda x, y: x / y if y != 0 else float('inf'),
            "%": lambda x, y: x % y,
        }
        return operations[op](a, b)

    # --- FORMATER LE RÉSULTAT ---
    def _format_result(self, value):
        return f"{value:g}".replace(".", ",")

    # --- HISTORIQUE FORMATÉ ---
    def get_formatted_history(self):
        formatted = []
        for h in self.history:
            clean = h.replace("*", "×").replace("/", "÷").replace(".", ",")
            formatted.append(clean)
        return "\n\n".join(formatted)
