from cursos.curso import Curso
import menu

from cursos.funciones import CC, DIU, GEOMETRIA_COMPUTACIONAL, IA, DS, DISTRIBUIDOS, DL, SIGES

cursos = [
    Curso("DISTRIBUIDOS", DISTRIBUIDOS.NP),
    Curso("GEOMETRY COMP", GEOMETRIA_COMPUTACIONAL.NP),
    Curso("IA", IA.NP),
    Curso("SIGES", SIGES.NP),
    Curso("DIU", DIU.NP),
    #Curso("DS", DS.NP),
    #Curso("DL", DL.NP),
    Curso("CC", CC.NP)
]

current_curso: Curso = None

def main():
    global current_curso
    while True:
        if current_curso is None:
            current_curso = menu.seleccion_curso(cursos)
            current_curso.update()
        else:
            current_curso = menu.menu_curso(current_curso)


if __name__ == "__main__":
    main()

