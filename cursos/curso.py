from PIL.Image import preinit

import utils as ut
import numpy as np
from config import Config

class Curso:
    def __init__(self, sigla, func):
        self.sigla = sigla

        data_curso = ut.read_json('data/data_cursos.json')[sigla]

        self.nombre = data_curso['nombre']
        self.objetivo = data_curso['objetivo']

        evals = data_curso['evaluaciones']
        self.__evaluaciones, self.__notas, self.__bools, self.__indep = ut.get_evals_arrays(evals)

        self.func = func

    def __str__(self):
        title = f"[{self.sigla}] {self.nombre}"

        return f"{title}"

    def __eq__(self, other):
        if isinstance(other, Curso):
            return (self.nombre == other.nombre and
                    self.codigo == other.codigo)
        return False

    def update(self):
        data_curso = ut.read_json('data/data_cursos.json')[self.sigla]

        self.nombre = data_curso['nombre']
        self.objetivo = data_curso['objetivo']

        evals = data_curso['evaluaciones']
        self.__evaluaciones, self.__notas, self.__bools, self.__indep = ut.get_evals_arrays(evals)


    def print_notas(self):
        """
        Print the evaluations and their corresponding notes.
        """
        print(f"Notas del curso {self.nombre}:")
        print("-"*(24+3))
        for eval_name, nota, rendida in zip(self.__evaluaciones, self.__notas, self.__bools):
            if not rendida:
                continue

            print(f"{eval_name:>12} : {f'{nota:.2f}':<12}")
        print("-"*(24+3))

        if np.sum(~self.__bools) > 0:
            print("Evaluaciones no rendidas:")
            print("-" * (24 + 3))
            for eval_name in self.__evaluaciones[~self.__bools]:
                print(f"{eval_name:>12} : {'-':<12}")
            print("-" * (24 + 3))
        else:
            print("Todas las evaluaciones han sido rendidas.")
            NP = self.func(self.__notas)
            print(f"Nota obtenida: {NP:.2f}")
            cfg = Config()
            if NP < cfg.get("nota_aprobar", 55):
                print("No aprobaste el curso.")
            elif NP < self.objetivo:
                print("Aprobaste el curso, pero no alcanzaste el objetivo.")
            else:
                print("Aprobaste el curso y alcanzaste el objetivo! Felicidades!")

    def save(self):
        evals_data = []

        for eval_name, nota, rendida, is_indep in zip(self.__evaluaciones, self.__notas, self.__bools, self.__indep):
            evals_data.append([
                eval_name,
                nota,
                rendida,
                is_indep
            ])

        curso_dict = {
            "nombre": self.nombre,
            "objetivo": self.objetivo,
            "evaluaciones": evals_data
        }

        current_data = ut.read_json('data/data_cursos.json')
        current_data[self.sigla] = curso_dict

        ut.write_json('data/data_cursos.json', current_data)

    def get_notas(self):
        return self.__notas.copy()

    def get_evaluaciones(self):
        return self.__evaluaciones.copy()

    def get_bools(self):
        return self.__bools.copy()

    def get_indep(self):
        return self.__indep.copy()

    def set_indep(self):
        """
        Set the independent evaluations based on the current state of the course.
        Returns:
            mask_indep: Boolean mask for independent evaluations.
            mask_dep: Boolean mask for dependent evaluations.
        """
        print("Indique las evaluaciones independientes (separadas por comas):")
        for i, evaluacion in enumerate(self.__evaluaciones[~self.__bools]):
            print(f"{i+1}. {evaluacion}")

        indep_indices = input("Ingrese los números de las evaluaciones independientes: ")
        indep_indices = [int(i.strip()) - 1 for i in indep_indices.split(",")]

        false_indices = np.where(~self.__bools)[0]
        selected_indices = false_indices[indep_indices]
        new_indep = np.zeros_like(self.__indep)
        new_indep[selected_indices] = True

        self.__indep = new_indep.copy()

        mask_indep = self.__bools & self.__indep
        mask_dep = self.__bools & ~self.__indep

        self.save()

        return mask_indep, mask_dep

