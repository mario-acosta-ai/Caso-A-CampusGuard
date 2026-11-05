# src/problem_model.py

class CampusGuardProblem:
    def __init__(self, initial, goal=None):
        self.initial = initial
        self.goal = goal
        self.action_costs = {
            'Asignar_Tutoria': 12,
            'Notificar_Bienestar': 24,
            'Ajustar_Carga': 6,
            'Evaluar_Progreso': 4
        }

    def actions(self, state):
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

    def result(self, state, action):
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

    def goal_test(self, state):
        riesgo, inasistencia, estado_int = state
        return riesgo == "Bajo" and (estado_int == "Recuperado" or estado_int == "Carga_Reducida")

    def path_cost(self, c, state1, action, state2):
        return c + self.action_costs.get(action, 1)

    def h(self, node):
        # Heurística admisible definida en el documento
        riesgo, inasistencia, estado_int = node.state if hasattr(node, 'state') else node
        if self.goal_test(riesgo, inasistencia, estado_int) if isinstance(riesgo, tuple) else self.goal_test((riesgo, inasistencia, estado_int)):
            return 0
        
        costo_estimado = 0
        if riesgo == 'Alto':
            costo_estimado += 12
        if estado_int != 'Carga_Reducida':
            costo_estimado += 6
        return costo_estimado
