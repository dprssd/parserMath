from pymongoAPI import MongoDB
from parseMath import pyParseMath


# dbase.create_record({'_id': 4, 'name': 'test_formula', 'formula': '2*x^2+3*x - 1', 'values': {'x': 2}})
# dbase.change_record('test_formula', 'out_value', 2)
def dynamic_program_analysis():
    exec(input('exec: '))


class Main:

    def __init__(self):
        self.dbase = MongoDB(host='localhost', port=27017, db_name='test', collection='math')

    def hard_query_find(self):
        query, projection = {}, {}
        keys_q = input('Keys for query: ')
        value_q = input('Value for query: ')
        query[keys_q] = value_q

        for i in range(int(input('How many times do you want to projection? '))):
            keys_p = input('Keys for projection: ')
            if input('Type of projection (int/str): ') == 'int':
                value_p = int(input('Value for projection: '))
            else:
                value_p = input('Value for projection: ')
            projection[keys_p] = value_p
        for i in self.dbase.find(query, projection):
            print(i)

    def create_record(self):
        name = input('Name: ')
        formula = input('Formula: ')
        a = int(input('How many times do you want to create variables? '))
        variables = {}
        for i in range(a):
            print(i+1, '/', a)
            keys = input('Keys: ')
            values = input('Values: ')
            variables[keys] = int(values)
        self.dbase.create_record({'name': name, 'formula': formula, 'variables': variables})

    def calculate_linear_formula(self, name):

        query, projection = {'name': name}, {'_id': 0}

        for i in self.dbase.find(query, projection):
            formula = i['formula']
            variables = i['variables']
            print(f'Formula: {formula}, Values: {variables}')

        my_parse = pyParseMath(formula, variables)

        self.dbase.change_record(name, 'out_value', my_parse.parse_and_evaluate_linear_formula())


main = Main()
choose = input('Input:')
if choose == 'calc':
    main.calculate_linear_formula(name=input('Name: '))
elif choose == 'hard_query':
    main.hard_query_find()
elif choose == 'exec':
    dynamic_program_analysis()
elif choose == 'create_record':
    main.create_record()
