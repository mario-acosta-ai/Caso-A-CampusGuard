# src/problem.py

class CampusGuardProblem:
    def __init__(self, initial_state):
        self.initial_state = initial_state
        self.goal_risk = "Bajo"

    def actions(self, state):
        _, causa, _ = state
        acciones = []
        if causa == "Academico":
            acciones.append("Agendar_Tutoria")
        elif causa == "Socioemocional":
            acciones.append("Notificar_Bienestar")
        elif causa == "Carga":
            acciones.append("Ajustar_Materias")
            acciones.append("Agendar_Tutoria")
        
        # Acción universal de contingencia
        if "Notificar_Bienestar" not in acciones:
            acciones.append("Notificar_Bienestar")
        return acciones

    def result(self, state, action):
        nivel, causa, _ = state
        if action == "Agendar_Tutoria":
            return ("Bajo", "Academico", "Tutoria")
        elif action == "Notificar_Bienestar":
            return ("Medio", "Socioemocional", "Bienestar")
        elif action == "Ajustar_Materias":
            return ("Bajo", "Carga", "Ajuste")
        return state

    def goal_test(self, state):
        return state[0] == self.goal_risk

    def step_cost(self, state, action):
        if action == "Agendar_Tutoria": return 1
        if action == "Notificar_Bienestar": return 3
        if action == "Ajustar_Materias": return 4
        return 0
