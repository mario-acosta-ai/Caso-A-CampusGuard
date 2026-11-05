# src/problem_model.py
from typing import Tuple, List, Optional

State = Tuple[str, int, str]

class CampusGuardProblem:
    """
    Modelado formal del problema de búsqueda para CampusGuard.
    Define el espacio de estados, acciones, transiciones, meta y costos.
    """
    def __init__(self, initial: State, goal: Optional[State] = None) -> None:
        self.initial = initial
        self.goal = goal
        # Costos en horas según el documento Actividad 1 Proyecto Integrador Modelado formal y arquitectónico de un Agente Racional
        self.action_costs = {
            'Asignar_Tutoria': 12,
            'Notificar_Bienestar': 24,
            'Ajustar_Carga': 6,
            'Evaluar_Progreso': 4
        }

    def actions(self, state: State) -> List[str]:
        """Retorna las acciones válidas para un estado dado."""
        riesgo, inasistencia, estado_int = state
        accs = []
        if estado_int == 'Sin_Accion':
            accs.extend(['Asignar_Tutoria', 'Notificar_Bienestar'])
        elif estado_int == 'Tutoria_Asignada':
            accs.extend(['Ajustar_Carga', 'Evaluar_Progreso'])
        elif estado_int == 'Bienestar_Notificado':
            accs.extend(['Ajustar_Carga', 'Asignar_Tutoria'])
        elif estado_int == 'Carga_Reducida':
            accs.append('Evaluar_Progreso')
        return accs

    def result(self, state: State, action: str) -> State:
        """Modelo de transición: Retorna el nuevo estado tras aplicar la acción."""
        riesgo, inasistencia, estado_int = state
        if action == 'Asignar_Tutoria':
            return ('Medio', max(0, inasistencia - 10), 'Tutoria_Asignada')
        elif action == 'Notificar_Bienestar':
            return ('Medio', inasistencia, 'Bienestar_Notificado')
        elif action == 'Ajustar_Carga':
            return ('Bajo', max(0, inasistencia - 15), 'Carga_Reducida')
        elif action == 'Evaluar_Progreso':
            nuevo_riesgo = 'Bajo' if inasistencia < 20 else 'Medio'
            return (nuevo_riesgo, inasistencia, 'Recuperado')
        return state

    def goal_test(self, state: State) -> bool:
        """Prueba de meta: Verifica si el estudiante está recuperado."""
        riesgo, inasistencia, estado_int = state
        return riesgo == "Bajo" and (estado_int == "Recuperado" or estado_int == "Carga_Reducida")

    def path_cost(self, c: int, state1: State, action: str, state2: State) -> int:
        """Función de costo: Suma el costo de la acción al costo acumulado."""
        return c + self.action_costs.get(action, 1)

    def h(self, node) -> int:
        """
        Heurística admisible h(n): Estima el costo mínimo restante sin sobreestimarlo.
        Se basa en las horas mínimas requeridas para reducir el riesgo.
        """
        state = node.state if hasattr(node, 'state') else node
        riesgo, inasistencia, estado_int = state
        
        if self.goal_test(state):
            return 0
            
        costo_estimado = 0
        if riesgo == 'Alto':
            costo_estimado += 12 # Mínimo para bajar el riesgo
        if estado_int != 'Carga_Reducida':
            costo_estimado += 6  # Mínimo para ajustar carga
        return costo_estimado
