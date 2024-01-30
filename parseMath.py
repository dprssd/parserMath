import ast
from scipy.integrate import quad


class pyParseMath:

    def __init__(self, formula, values):
        self.formula = formula
        self.values = values

    def evaluate_formula(self):
        return eval(self.formula, self.values)

    def parse_and_evaluate_linear_formula(self):
        try:
            parsed_formula = ast.parse(self.formula, mode='eval')

            if isinstance(parsed_formula, ast.Expression):
                compiled_formula = compile(parsed_formula, filename='<ast>', mode='eval')
                result = eval(compiled_formula, self.values)
                print(result)
                return result
            else:
                return "Формула не является корректным выражением"
        except SyntaxError:
            return "Ошибка в синтаксисе формулы"
        except NameError as e:
            return f"Ошибка: {e}"
