import ast
import re
from scipy.integrate import quad


class pyParseMath:

    def __init__(self):
        pass
    #     self.formula = formula
    #     self.values = values
    #

    def evaluate_formula(self):
        return eval(formula, svalues)

    def parse_and_evaluate_linear_formula(self, formula, values):
        try:
            parsed_formula = ast.parse(formula, mode='eval')

            if isinstance(parsed_formula, ast.Expression):
                compiled_formula = compile(parsed_formula, filename='<ast>', mode='eval')
                print(values)
                print(formula)
                result = eval(compiled_formula, values)
                print(result)
                return result
            else:
                return "Формула не является корректным выражением"
        except SyntaxError:
            return "Ошибка в синтаксисе формулы"
        except NameError as e:
            return f"Ошибка: {e}"

    def search_variables(self, formula):

        sample = r"[a-zA-Z_][a-zA-Z0-9_]*"
        variables = re.findall(sample, formula)
        unique_variables = list(set(variables))

        return unique_variables
