import ast
from scipy.integrate import quad

class pyParseMath(object):

    def __init__(self):
        pass

    def evaluate_formula(self, formula, values):
        return eval(formula, values)

    def parse_and_evaluate_linear_formula(input_formula, input_values):
        try:
            parsed_formula = ast.parse(input_formula, mode='eval')

            if isinstance(parsed_formula, ast.Expression):

                compiled_formula = compile(parsed_formula, filename='<ast>', mode='eval')
                result = eval(compiled_formula, input_values)

                return result
            else:
                return "Формула не является корректным выражением"
        except SyntaxError:
            return "Ошибка в синтаксисе формулы"
        except NameError as e:
            return f"Ошибка: {e}"
