import numpy as np
import pytest
from ..evaluator import eval_node

# ----------------------------------------------------------------------
# Contexto base
# ----------------------------------------------------------------------

CTX = {
    "values": {
        "cert_1": 72.0,
        "ctrl_1": 55.0,
        "ctrl_2": 60.0,
        "ctrl_3": 48.0
    },
    "templates": {
        "certamen": ["cert_1"],
        "control": ["ctrl_1", "ctrl_2", "ctrl_3"]
    }
}

# ----------------------------------------------------------------------
# Tests de operadores primitivos
# ----------------------------------------------------------------------

def test_const():
    node = {"op": "const", "value": 3.5}
    assert eval_node(node, CTX) == 3.5

def test_ref():
    node = {"op": "ref", "id": "cert_1"}
    assert eval_node(node, CTX) == 72.0

def test_refs_by_template():
    node = {"op": "refs_by_template", "template": "control"}
    out = eval_node(node, CTX)
    assert isinstance(out, np.ndarray)
    assert np.allclose(out, [55.0, 60.0, 48.0])

def test_add_mul_chain():
    ast = {
        "op": "add",
        "args": [
            {"op": "mul", "args": [
                {"op":"const","value":2},
                {"op":"const","value":3}
            ]},
            {"op": "const", "value": 4}
        ]
    }
    assert eval_node(ast, CTX) == 10

# ----------------------------------------------------------------------
# Tests vectoriales
# ----------------------------------------------------------------------

def test_mean_controls():
    ast = {"op":"mean", "args":[
        {"op":"refs_by_template", "template":"control"}
    ]}
    assert np.isclose(eval_node(ast, CTX), (55+60+48)/3)

def test_sort_slice_best2():
    ast = {
        "op":"slice",
        "args":[
            {"op":"sort","args":[
                {"op":"refs_by_template","template":"control"}
            ]},
            {"op":"const","value":-2}
        ]
    }
    out = eval_node(ast, CTX)
    # controles: [55,60,48] -> sort asc: [48,55,60] -> últimos 2: [55,60]
    assert np.allclose(out, [55, 60])

# ----------------------------------------------------------------------
# Test de fórmula compuesta real
# 0.6 * certamen + 0.4 * mean(controles)
# ----------------------------------------------------------------------

def test_full_formula():
    ast = {
        "op":"add",
        "args":[
            {
                "op":"mul",
                "args":[
                    {"op":"const","value":0.6},
                    {"op":"ref","id":"cert_1"}
                ]
            },
            {
                "op":"mul",
                "args":[
                    {"op":"const","value":0.4},
                    {
                        "op":"mean",
                        "args":[
                            {"op":"refs_by_template","template":"control"}
                        ]
                    }
                ]
            }
        ]
    }
    expected = 0.6*72 + 0.4*((55+60+48)/3)
    assert np.isclose(eval_node(ast, CTX), expected)

# ----------------------------------------------------------------------
# Tests de comparaciones y condicional
# ----------------------------------------------------------------------

def test_conditional_then():
    ast = {
        "op":"if",
        "cond":{
            "op":"lt",
            "args":[
                {"op":"ref","id":"cert_1"},
                {"op":"const","value":100}
            ]
        },
        "then":{"op":"const","value":1},
        "else":{"op":"const","value":0}
    }
    assert eval_node(ast, CTX) == 1

def test_conditional_else():
    ast = {
        "op":"if",
        "cond":{
            "op":"lt",
            "args":[
                {"op":"ref","id":"cert_1"},
                {"op":"const","value":10}
            ]
        },
        "then":{"op":"const","value":1},
        "else":{"op":"const","value":0}
    }
    assert eval_node(ast, CTX) == 0

def test_slice_out_of_bounds():
    ast = {
        "op":"slice",
        "args":[
            {"op":"array","value":np.array([1,2,3])},
            {"op":"const","value":10}
        ]
    }
    out = eval_node(ast, CTX)
    assert len(out) == 0
