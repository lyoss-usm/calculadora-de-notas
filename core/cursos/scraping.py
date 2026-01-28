from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional, Tuple

import json
import requests
from bs4 import BeautifulSoup

try:
  from core.cursos.search import normalize
except:
  from search import normalize



BASE_URL = "https://siga.usm.cl/prog_oai/"
ACADEMIA_PATH = "oai_academia.jsp"
HEADERS = {
  "User-Agent": (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
  )
}
TARGET_TABLE_INDICES = [3, 5, 7, 9]
OUTPUT_DIR = Path("core/cursos/models")


def get_html(
  url: str,
  *,
  session: Optional[requests.Session] = None,
  data: Optional[Dict[str, str]] = None,
  timeout: int = 10,
) -> Optional[str]:
  """Obtiene el HTML de una URL.

  Si se proporciona `data`, realiza una petición POST; de lo contrario, GET.

  Args:
    url: URL destino.
    session: Sesión de requests reutilizable.
    data: Datos para una petición POST.
    timeout: Tiempo máximo de espera en segundos.

  Returns:
    El HTML como texto si la petición fue exitosa; de lo contrario, None.
  """
  try:
    s = session or requests.Session()
    if data is None:
      resp = s.get(url, headers=HEADERS, timeout=timeout)
    else:
      resp = s.post(url, headers=HEADERS, data=data, timeout=timeout)
    resp.raise_for_status()
    return resp.text
  except requests.RequestException as exc:
    print(f"Error al solicitar {url}: {exc}")
    return None


def get_soup(
  url: str,
  *,
  session: Optional[requests.Session] = None,
  data: Optional[Dict[str, str]] = None,
) -> Optional[BeautifulSoup]:
  """Devuelve un BeautifulSoup a partir de una URL."""
  html = get_html(url, session=session, data=data)
  return BeautifulSoup(html, "html.parser") if html else None


def obtener_opciones_sede(soup: BeautifulSoup) -> List[Tuple[str, str]]:
  """Obtiene las opciones de sede como pares (valor, texto)."""
  select = soup.find("select", {"id": "sede"})
  if not select:
    return []
  options = select.find_all("option")
  return [(opt.get("value", ""), opt.text.strip()) for opt in options if opt.get("value")]


def obtener_departamentos(session: requests.Session, payload_sede: Dict[str, str]) -> Dict[str, str]:
  """Obtiene el diccionario de departamentos código -> nombre para una sede."""
  soup = get_soup(BASE_URL + ACADEMIA_PATH, session=session, data=payload_sede)
  if not soup:
    return {}
  select_deptos = soup.find("select", {"name": "cod_departamento"})
  if not select_deptos:
    return {}
  opciones = select_deptos.find_all("option")
  return {opt["value"]: opt.text.strip() for opt in opciones if opt.get("value") and opt["value"] != "0"}


def obtener_cursos(session: requests.Session, payload_depto: Dict[str, str]) -> List[Tuple[str, str]]:
  """Obtiene la lista de cursos como pares (código, nombre) para un departamento."""
  soup = get_soup(BASE_URL + ACADEMIA_PATH, session=session, data=payload_depto)
  if not soup:
    return []

  cursos: List[Tuple[str, str]] = []
  tablas = soup.find_all("table")
  for idx in TARGET_TABLE_INDICES:
    if idx >= len(tablas):
      continue
    filas = tablas[idx].find_all("tr")[1:]
    for fila in filas:
      cols = [td.text.strip() for td in fila.find_all("td")]
      if len(cols) >= 2:
        cursos.append((cols[0], cols[1]))
  return sorted(cursos, key=lambda x: x[0])


def plantilla_modelo_curso(
  codigo: str,
  nombre: str,
  sede_nombre: str,
  depto_nombre: str,
) -> Dict:
  """Construye la plantilla JSON del modelo de curso."""
  return {
    "meta": {
      "code": codigo,
      "norm_code": normalize(codigo),
      "name": nombre,
      "norm_name": normalize(nombre),
      "campus": sede_nombre,
      "depto": depto_nombre,
      "icon": {
        "gradient": "linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)",
        "svg": "codigo",
      },
    },
    "evaluations": [
      "Certamen 1",
      "Certamen 2",
      "Certamen 3",
      "Control 1",
      "Control 2",
      "Control 3",
      "Control 4",
      "Control 5",
      "Control 6",
    ],
    "context": {
      "values": [None, None, None, None, None, None, None, None, None],
      "templates": {"certamen": [0, 1, 2], "control": [3, 4, 5, 6, 7, 8]},
    },
    "AST": {
      "op": "linear_comb",
      "weights": [0.2, 0.25, 0.3, 0.25],
      "args": [
        {"op": "ref", "id": 0},
        {"op": "ref", "id": 1},
        {"op": "ref", "id": 2},
        {
          "op": "mean",
          "args": [{"op": "ref_template", "template": "control"}],
        },
      ],
    },
  }


def guardar_modelo(modelo: Dict, collection):
  """Guarda el modelo JSON dentro de la base de datos mongodb"""
  collection.insert_one(modelo)


def elegir_opcion(codigo_a_nombre: Dict[str, str], prompt: str) -> Tuple[str, str]:
  """Muestra opciones y solicita un código válido, devolviendo (código, nombre)."""
  for code, name in codigo_a_nombre.items():
    print(f"{code}: {name}")
  while True:
    codigo = input(prompt).strip()
    nombre = codigo_a_nombre.get(codigo)
    if nombre:
      return codigo, nombre.title()
    print("Código inválido, intente nuevamente.")


def main(collection) -> None:
  """Script interactivo para descargar cursos y generar modelos JSON."""
  soup_inicio = get_soup(BASE_URL + ACADEMIA_PATH)
  if not soup_inicio:
    print("No se pudo obtener la página inicial.")
    return

  sedes = obtener_opciones_sede(soup_inicio)
  if not sedes:
    print("No se encontraron sedes.")
    return

  print("Sedes disponibles:")
  sedes_dict = {code: name for code, name in sedes}
  sede_code, sede_nombre = elegir_opcion(sedes_dict, "Ingrese el código de la sede: ")
  print(f"Sede seleccionada: {sede_nombre}")

  session = requests.Session()
  payload_sede = {"sede": sede_code, "idioma": "0", "año": "0", "semestre": "0"}

  print("Departamentos encontrados:")
  departamentos = obtener_departamentos(session, payload_sede)
  if not departamentos:
    print("No se encontraron departamentos para la sede seleccionada.")
    return
  depto_code, depto_nombre = elegir_opcion(departamentos, "Ingrese el código del departamento: ")
  print(f"Departamento seleccionado: {depto_nombre}")

  payload_depto = {**payload_sede, "cod_departamento": depto_code}
  cursos = obtener_cursos(session, payload_depto)
  if not cursos:
    print("No se encontraron cursos para el departamento seleccionado.")
    return

  print("Cursos encontrados:")
  for codigo, nombre in cursos:
    print(f"{codigo:<10} - {nombre}")
    modelo = plantilla_modelo_curso(codigo, nombre, sede_nombre, depto_nombre)
    guardar_modelo(modelo, collection)

  print(f"Total de cursos: {len(cursos)}")


if __name__ == "__main__":
  main()
