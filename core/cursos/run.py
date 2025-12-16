from evaluator import eval_node
import numpy as np
import json

# Read models/MAT021.json and run the evaluation
with open("core/cursos/models/MAT021.json", "r") as f:
    course_model = json.load(f)

CTX = course_model['context']

CTX['values'] = {
    "cert_1": 72.0,
    "cert_2": 32.0,
    "cert_3": 57.0,
    "ctrl_1": 55.0,
    "ctrl_2": 60.0,
    "ctrl_3": 48.0,
    "ctrl_4": 88.0,
    "ctrl_5": 98.0,
    "ctrl_6": 78.0,
}

node = course_model['AST']
print("Evaluating course model...")

final_grade = eval_node(node, CTX)
print(f"Final grade: {final_grade} (node_eval)")

PC = np.mean(np.array([CTX['values'][f'ctrl_{i}'] for i in range(1,7)]))
final_grade = 0.25*PC + 0.2*CTX['values']['cert_1'] + 0.25*CTX['values']['cert_2'] + 0.3*CTX['values']['cert_3']
print(f"Final grade: {final_grade} (manual calc)")
