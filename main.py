from pymongoAPI import MongoDB
from parseMath import pyParseMath

dbase = MongoDB(host='localhost', port=27017, db_name='test', collection='math')

dbase.create_record({'_id': 3, '_name': 'fake_formula', 'formula': '2*x^2 + 3*x - 1 ='})

result = dbase.get_all_users()
for i in result:
    print(i)



formula = 'Ta + (Ia / (k0 + k1 * Vw))'
values = {"Ta": 10, "Ia": 10, "k0": "30.02", "k1": 6.28, "Vw": 10}
print(pyParseMath.parse_and_evaluate_linear_formula(formula, values))