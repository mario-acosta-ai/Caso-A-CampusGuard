# src/problem.py
from typing import Tuple, List

State = Tuple[str, int, str]

class CampusGuardProblem:
    """Modelado formal del problema de búsqueda para CampusGuard."""
    def __init__(self, initial: State) -> None:
        self.initial = initial
        self.action_costs = {
            'Asignar_Tutoria': 12, 'Notificar_Bienestar': 24,
            'Ajustar_Carga': 6, 'Evaluar_Progreso': 4
        }

    def actions(self, state: State) -> List[str]:
        _, _, estado_int = state
        if estado_int == 'Sin_Accion': return ['Asignar_Tutoria', 'Notificar_Bienestar']
        if estado_int == 'Tutoria_Asignada': return ['Ajustar_Carga', 'Evaluar_Progreso']
        if estado_int == 'Bienestar_Notificado': return ['Ajustar_Carga', 'Asignar_Tutoria']
        if estado_int == 'Carga_Reducida': return ['Evaluar_Progreso']
        return []

    def result(self, state: State, action: str) -> State:
        _, inasistencia, _ = state
        if action == 'Asignar_Tutoria': return ('Medio', max(0, inasistencia - 10), 'Tutoria_Asignada')
        if action == 'Notificar_Bienestar': return ('Medio', inasistencia, 'Bienestar_Notificado')
        if action == 'Ajustar_Carga': return ('Bajo', max(0, inasistencia - 15), 'Carga_Reducida')
        if action == 'Evaluar_Progreso': return ('Bajo' if inasistencia < 20 else 'Medio', inasistencia, 'Recuperado')
        return state

    def goal_test(self, state: State) -> bool:
        riesgo, _, estado_int = state
        return riesgo == "Bajo" and estado_int in ["Recuperado", "Carga_Reducida"]

    # CORRECCIÓN AQUÍ: Se añaden state1 y state2 a la firma para cumplir con AIMA
    def path_cost(self, c: int, state1: State, action: str, state2: State) -> int:
        return c + self.action_costs.get(action, 1)

    def h(self, state: State) -> int:
        riesgo, _, estado_int = state
        if self.goal_test(state): return 0
        return (12 if riesgo == 'Alto' else 0) + (6 if estado_int != 'Carga_Reducida' else 0)
