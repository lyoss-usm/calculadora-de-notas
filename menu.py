from cursos.curso import Curso
from analisis import roots
from analisis import simulation as sim

def seleccion_curso(cursos) -> Curso:
    print("Seleccione un curso:")
    for i, curso in enumerate(cursos):
        print(f"{i + 1}. {curso}")
    try:
        seleccion = int(input("Ingrese el número del curso: ")) - 1
    except ValueError:
        print("Entrada no válida. Por favor, ingrese un número.")
        return None
    return cursos[seleccion]

def menu_curso(curso):
    print("\n" * 50)
    print(f"Menú del curso: {curso.nombre}")
    print("1. Ver notas")
    print("2. Gráfico de notas")
    print("3. Simulación de notas")
    print("4. Salir")

    try:
        opcion = int(input("Seleccione una opción: "))
    except:
        print("Entrada no válida. Por favor, ingrese un número.")
        return curso

    print("\n" * 50)

    if opcion == 1:
        print("=" * 50)
        curso.print_notas()
        print("=" * 50)
        input("Presione Enter para continuar...")
    elif opcion == 2:
        print("=" * 50)
        roots.plot_notas(curso)
        print("=" * 50)
        input("Presione Enter para continuar...")
    elif opcion == 3:
        notas, mask_obj, mask_aprobado = sim.montecarlo(curso)
        print("="*50)
        sim.plot_histogram(notas, mask_obj, mask_aprobado, curso)
        print("="*50)
        input("Presione Enter para continuar...")
    elif opcion == 4:
        return None
    else:
        print("Opción no válida.")

    return curso
