import math
import pytest
from flask import Flask

import app.routes as routes


@pytest.fixture()
def client():
    app = Flask(__name__)
    app.register_blueprint(routes.bp)
    app.testing = True
    with app.test_client() as c:
        yield c


def fake_course_model_line():
    # nota_final = mean(ref0, ref1, ref2)
    # Si ref2=80 fijo y target=60:
    # (x + y + 80)/3 = 60  =>  y = 100 - x
    return {
        "meta": {"code": "TST100", "name": "Test Line"},
        "AST": {
            "op": "mean",
            "args": [
                {"op": "ref", "id": 0},
                {"op": "ref", "id": 1},
                {"op": "ref", "id": 2},
            ],
        },
        "context": {"values": [0.0, 0.0, 80.0], "templates": {}},
    }


def fake_course_model_multi_x():
    # nota_final = mean(ref0, ref1, ref2, ref3)
    # ref3=80 fijo, X en ref0 y ref1, Y en ref2:
    # (x + x + y + 80)/4 = target  =>  y = 4*target - 80 - 2x
    return {
        "meta": {"code": "TST200", "name": "Test Multi X"},
        "AST": {
            "op": "mean",
            "args": [
                {"op": "ref", "id": 0},
                {"op": "ref", "id": 1},
                {"op": "ref", "id": 2},
                {"op": "ref", "id": 3},
            ],
        },
        "context": {"values": [0.0, 0.0, 0.0, 80.0], "templates": {}},
    }


def test_contour_ok_simple_line(client, monkeypatch):
    monkeypatch.setattr(routes, "load_course", lambda _code: fake_course_model_line())

    payload = {
        "grades": [None, None, 80.0],
        "x_indices": [0],
        "y_indices": [1],
        "target_grade": 60.0,
    }

    resp = client.post("/api/grades/TST100/contour", json=payload)
    assert resp.status_code == 200

    data = resp.get_json()
    assert "x" in data and "y" in data
    assert len(data["x"]) == len(data["y"])
    assert len(data["x"]) > 0

    # y ≈ 100 - x
    for x, y in list(zip(data["x"], data["y"]))[::10]:
        assert 0.0 <= x <= 100.0
        assert 0.0 <= y <= 100.0
        assert abs((100.0 - x) - y) < 1e-2


def test_contour_deterministic(client, monkeypatch):
    monkeypatch.setattr(routes, "load_course", lambda _code: fake_course_model_line())

    payload = {
        "grades": [None, None, 80.0],
        "x_indices": [0],
        "y_indices": [1],
        "target_grade": 60.0,
    }

    r1 = client.post("/api/grades/TST100/contour", json=payload).get_json()
    r2 = client.post("/api/grades/TST100/contour", json=payload).get_json()

    # mismo input => resultados iguales (tolerancia numérica pequeña)
    assert r1["x"] == pytest.approx(r2["x"], abs=1e-9)
    assert r1["y"] == pytest.approx(r2["y"], abs=1e-6)


def test_contour_multiple_x_indices(client, monkeypatch):
    monkeypatch.setattr(routes, "load_course", lambda _code: fake_course_model_multi_x())

    payload = {
        "grades": [None, None, None, 80.0],
        "x_indices": [0, 1],
        "y_indices": [2],
        "target_grade": 60.0,
    }

    resp = client.post("/api/grades/TST200/contour", json=payload)
    assert resp.status_code == 200
    data = resp.get_json()

    # y = 160 - 2x (y se filtra a [0,100])
    for x, y in list(zip(data["x"], data["y"]))[::10]:
        assert abs((160.0 - 2.0 * x) - y) < 1e-2
        assert 0.0 <= x <= 100.0
        assert 0.0 <= y <= 100.0


def test_contour_404_course_not_found(client, monkeypatch):
    def _missing(_code):
        raise KeyError("no existe")
    monkeypatch.setattr(routes, "load_course", _missing)

    payload = {
        "grades": [None, None, 80.0],
        "x_indices": [0],
        "y_indices": [1],
        "target_grade": 60.0,
    }

    resp = client.post("/api/grades/NOPE/contour", json=payload)
    assert resp.status_code == 404


def test_contour_400_overlap_indices(client, monkeypatch):
    monkeypatch.setattr(routes, "load_course", lambda _code: fake_course_model_line())

    payload = {
        "grades": [None, None, 80.0],
        "x_indices": [0],
        "y_indices": [0],  # solape
        "target_grade": 60.0,
    }

    resp = client.post("/api/grades/TST100/contour", json=payload)
    assert resp.status_code == 400


def test_contour_400_null_outside_axes(client, monkeypatch):
    monkeypatch.setattr(routes, "load_course", lambda _code: fake_course_model_line())

    payload = {
        "grades": [None, None, None],  # idx2 null pero NO está en X/Y
        "x_indices": [0],
        "y_indices": [1],
        "target_grade": 60.0,
    }

    resp = client.post("/api/grades/TST100/contour", json=payload)
    assert resp.status_code == 400


def test_contour_400_inconsistent_length(client, monkeypatch):
    monkeypatch.setattr(routes, "load_course", lambda _code: fake_course_model_line())

    payload = {
        "grades": [None, None],  # debería ser len=3
        "x_indices": [0],
        "y_indices": [1],
        "target_grade": 60.0,
    }

    resp = client.post("/api/grades/TST100/contour", json=payload)
    assert resp.status_code == 400
