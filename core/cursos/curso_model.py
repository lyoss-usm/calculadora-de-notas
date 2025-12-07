import numpy as np
from core.utils import read_json, write_json


class Curso:
    """
    Modelo que representa un curso con sus evaluaciones y notas.
    """
    
    def __init__(self, sigla, func):
        self.sigla = sigla
        data_curso = read_json('core/data/data_cursos.json')[sigla]

        self.nombre = data_curso['nombre']
        self.objetivo = data_curso['objetivo']

        evals = data_curso['evaluaciones']
        self.__evaluaciones, self.__notas, self.__bools, self.__indep = self._get_evals_arrays(evals)

        self.func = func

    def __str__(self):
        title = f"[{self.sigla}] {self.nombre}"
        return f"{title}"

    def __eq__(self, other):
        if isinstance(other, Curso):
            return (self.nombre == other.nombre and
                    self.codigo == other.codigo)
        return False

    @staticmethod
    def _get_evals_arrays(evals):
        """
        Extrae los arrays de nombres, notas, bools e indep de las evaluaciones.
        """
        names = np.array([eval[0] for eval in evals], dtype=str)
        notas = np.array([eval[1] for eval in evals], dtype=float)
        bools = np.array([eval[2] for eval in evals], dtype=bool)
        indep = np.array([eval[3] for eval in evals], dtype=bool)
        return names, notas, bools, indep

    def update(self):
        """Actualiza los datos del curso desde el archivo JSON."""
        data_curso = read_json('core/data/data_cursos.json')[self.sigla]
        self.nombre = data_curso['nombre']
        self.objetivo = data_curso['objetivo']
        evals = data_curso['evaluaciones']
        self.__evaluaciones, self.__notas, self.__bools, self.__indep = self._get_evals_arrays(evals)

    def get_notas_info(self):
        """
        Retorna un diccionario con la información de las notas del curso.
        Útil para renderizar en templates.
        """
        notas_rendidas = []
        notas_pendientes = []
        
        for eval_name, nota, rendida in zip(self.__evaluaciones, self.__notas, self.__bools):
            if rendida:
                notas_rendidas.append({
                    'nombre': eval_name,
                    'nota': nota
                })
            else:
                notas_pendientes.append({
                    'nombre': eval_name
                })
        
        resultado = {
            'curso': self.nombre,
            'sigla': self.sigla,
            'objetivo': self.objetivo,
            'notas_rendidas': notas_rendidas,
            'notas_pendientes': notas_pendientes,
            'todas_rendidas': len(notas_pendientes) == 0
        }
        
        # Si todas las evaluaciones están rendidas, calcular nota final
        if resultado['todas_rendidas']:
            from core.utils import AppConfig
            cfg = AppConfig()
            NP = self.func(self.__notas)
            resultado['nota_final'] = NP
            resultado['aprobado'] = NP >= cfg.get("nota_aprobar", 55)
            resultado['objetivo_alcanzado'] = NP >= self.objetivo
        
        return resultado

    def save(self):
        """Guarda el curso en el archivo JSON."""
        evals_data = []
        for eval_name, nota, rendida, is_indep in zip(self.__evaluaciones, self.__notas, self.__bools, self.__indep):
            evals_data.append([eval_name, nota, rendida, is_indep])

        curso_dict = {
            "nombre": self.nombre,
            "objetivo": self.objetivo,
            "evaluaciones": evals_data
        }

        current_data = read_json('core/data/data_cursos.json')
        current_data[self.sigla] = curso_dict
        write_json('core/data/data_cursos.json', current_data)

    # Getters
    def get_notas(self):
        return self.__notas.copy()

    def get_evaluaciones(self):
        return self.__evaluaciones.copy()

    def get_bools(self):
        return self.__bools.copy()

    def get_indep(self):
        return self.__indep.copy()

    def set_indep(self, indep_indices):
        """
        Establece las evaluaciones independientes.
        
        Args:
            indep_indices: Lista de índices de evaluaciones independientes
        
        Returns:
            tuple: (mask_indep, mask_dep) máscaras booleanas
        """
        false_indices = np.where(~self.__bools)[0]
        selected_indices = false_indices[indep_indices]
        new_indep = np.zeros_like(self.__indep)
        new_indep[selected_indices] = True

        self.__indep = new_indep.copy()

        mask_indep = self.__bools & self.__indep
        mask_dep = self.__bools & ~self.__indep

        self.save()

        return mask_indep, mask_dep

    def to_dict(self):
        """Convierte el curso a un diccionario para serialización JSON."""
        return {
            'sigla': self.sigla,
            'nombre': self.nombre,
            'objetivo': self.objetivo,
            'evaluaciones': self.__evaluaciones.tolist(),
            'notas': self.__notas.tolist(),
            'rendidas': self.__bools.tolist(),
            'independientes': self.__indep.tolist()
        }
