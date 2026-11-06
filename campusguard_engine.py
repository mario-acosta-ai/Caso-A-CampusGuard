"""
Módulo: campusguard_engine.py
Proyecto Integrador: Modelado formal y arquitectónico del Agente Racional CampusGuard
Asignatura: Inteligencia Artificial I - Grupo D
Universidad Militar Nueva Granada (FAEDIS)

Este módulo implementa el núcleo formal del agente racional de búsqueda basada en objetivos
y utilidad para la plataforma CampusGuard. Modela el espacio de estados determinista y discreto
del estudiante en riesgo de deserción y proporciona las implementaciones canónicas de:
  1. Búsqueda en Anchura (BFS - Breadth-First Search)
  2. Búsqueda en Profundidad (DFS - Depth-First Search)
  3. Búsqueda Informada A* (A-Star Search con Heurística Admisible)

Arquitectura basada en el libro 'Artificial Intelligence: A Modern Approach' (Russell & Norvig, 2020)
y el repositorio oficial de referencia 'aima-python/search.py'.
"""

# =============================================================================
# IMPORTACIÓN DE MÓDULOS DEL SISTEMA
# =============================================================================
import time                 # Provee funciones para medir el tiempo de ejecución de CPU de alta precisión (perf_counter)
import heapq                # Implementación de cola de prioridad binaria (Binary Heap) requerida para A*
from collections import deque  # Estructura de cola de doble extremo (Double-Ended Queue) optimizada O(1) para la frontera FIFO de BFS


# =============================================================================
# ESTRUCTURA DE DATOS: NODO DE BÚSQUEDA (Russell & Norvig, Cap. 3)
# =============================================================================
class Node:
    """
    Representa un nodo en el árbol/grafo de búsqueda.
    Difiere de un 'estado' en que el estado representa una configuración del entorno físico,
    mientras que el nodo es una estructura contable que incluye punteros genealógicos (parent),
    la acción que lo generó (action), la profundidad (depth) y los costos acumulados.
    """
    def __init__(self, state, parent=None, action=None, path_cost=0, f_score=0):
        """
        Constructor del nodo de búsqueda.
        :param state: Tupla con la configuración del espacio de estados en este punto.
        :param parent: Puntero de referencia al nodo padre que generó este nodo (permite reconstruir la ruta).
        :param action: Acción legal ejecutada sobre el padre para transicionar a este estado.
        :param path_cost: Costo real acumulado g(n) en horas desde la raíz s0 hasta este nodo.
        :param f_score: Función de evaluación f(n) = g(n) + h(n) utilizada por algoritmos como A*.
        """
        self.state = state          # Asigna la tupla que representa el estado del estudiante
        self.parent = parent        # Almacena la referencia en memoria al nodo predecesor
        self.action = action        # Almacena el nombre de la acción que condujo a este estado
        self.path_cost = path_cost  # g(n): Horas operacionales acumuladas de acompañamiento
        self.f_score = f_score      # f(n): Prioridad estimada de costo total hasta la meta
        # Si no tiene padre es el nodo raíz (profundidad 0); de lo contrario incrementa en 1 la del padre
        self.depth = 0 if parent is None else parent.depth + 1

    def solution(self):
        """
        Reconstruye de forma retrospectiva la secuencia ordenada de acciones ejecutadas.
        Parte desde el nodo actual (nodo meta) hacia atrás siguiendo los punteros parent,
        y luego invierte la lista para entregar la secuencia cronológica [a1, a2, ..., ak].
        """
        node, path_back = self, []  # Inicializa el puntero de rastreo en el nodo actual y una lista vacía
        while node.parent:          # Mientras exista un nodo padre (es decir, no hayamos llegado a la raíz s0)
            path_back.append(node.action)  # Agrega la acción aplicada al recorrido inverso
            node = node.parent             # Salta al nodo padre
        return list(reversed(path_back))   # Invierte la lista para retornar el orden temporal correcto

    def __lt__(self, other):
        """
        Sobrecarga del operador relacional menor que ('<').
        Permite que el módulo heapq compare dos nodos dentro de la cola de prioridad de A*
        atendiendo al valor de evaluación f_score (f(n) = g(n) + h(n)).
        """
        return self.f_score < other.f_score


# =============================================================================
# FORMALIZACIÓN MATEMÁTICA DEL PROBLEMA: P = {S, s0, ACTIONS, RESULT, GOAL, c}
# =============================================================================
class CampusGuardProblem:
    """
    Especificación formal del problema de decisión y planificación para CampusGuard (Grupo D).
    Modela el universo de intervenciones tempranas para retención estudiantil.
    """
    def __init__(self, initial=('Alto', 35, 2, 'Sin_Intervencion')):
        """
        Constructor que define las propiedades iniciales del problema.
        :param initial: Estado inicial s0 formulado en el Corte 1:
                        - Riesgo: 'Alto' (alertas académicas tempranas)
                        - Inasistencia: 35% (deserción potencial)
                        - Materias Críticas: 2 (asignaturas en pérdida inminente)
                        - Fase: 'Sin_Intervencion' (caso recién clasificado en el LMS)
        """
        self.initial = initial  # Guarda el estado inicial del estudiante

        # Función de costo de acción c(s, a, s'): Representa las horas operativas indispensables
        # para que el personal ejecute la intervención. Todos los valores están estrictamente
        # acotados para garantizar una respuesta institucional integral en menos de 48 horas.
        self.action_costs = {
            'Notificar_Bienestar': 16,  # 16 horas: Detección, validación psicosocial y contacto al estudiante
            'Agendar_Tutoria_LMS': 10,  # 10 horas: Cruce de disponibilidad docente y asignación de refuerzo
            'Reestructurar_Carga': 8,   # 8 horas: Solicitud a dirección de programa y ajuste de créditos
            'Cierre_Seguimiento': 4     # 4 horas: Verificación final en consejería y auditoría de retención
        }

    def actions(self, state):
        """
        Función de acciones válidas ACTIONS(s).
        Retorna las intervenciones institucionales permitidas aplicando las reglas
        de negocio y permanencia estudiantil definidas en el diseño del Corte 1.
        """
        riesgo, inasist, mat_crit, fase = state  # Desempaqueta las 4 variables de estado
        accs = []                                # Lista para recolectar las acciones legales

        # ---------------------------------------------------------------------
        # REGLAS PARA LA FASE 1: Sin_Intervencion (Caso inicial detectado)
        # ---------------------------------------------------------------------
        if fase == 'Sin_Intervencion':
            if inasist >= 20:
                accs.append('Notificar_Bienestar')  # Regla 1: Inasistencia >= 20% exige remisión a Bienestar
            if riesgo in ('Alto', 'Medio'):
                accs.append('Agendar_Tutoria_LMS')  # Regla 2: Riesgo alto o medio requiere refuerzo académico
            if mat_crit >= 2:
                accs.append('Reestructurar_Carga')  # Regla 3: Dos o más materias críticas exigen revisión de carga

        # ---------------------------------------------------------------------
        # REGLAS PARA LA FASE 2: Bienestar_Notificado (Se atendió la parte emocional)
        # ---------------------------------------------------------------------
        elif fase == 'Bienestar_Notificado':
            if mat_crit >= 2:
                accs.append('Reestructurar_Carga')  # Permite complementar con alivio curricular si hay sobrecarga
            if riesgo in ('Alto', 'Medio'):
                accs.append('Agendar_Tutoria_LMS')  # Permite sumar apoyo pedagógico si persisten notas bajas
            if inasist <= 20 and riesgo == 'Bajo':
                accs.append('Cierre_Seguimiento')   # Si ya se normalizó, permite cerrar y auditar el caso

        # ---------------------------------------------------------------------
        # REGLAS PARA LA FASE 3: Tutoria_Programada (Se activó el refuerzo en LMS)
        # ---------------------------------------------------------------------
        elif fase == 'Tutoria_Programada':
            if mat_crit >= 2:
                accs.append('Reestructurar_Carga')  # Si persisten muchas materias perdidas, se ajusta la carga
            if inasist >= 20:
                accs.append('Notificar_Bienestar')  # Si faltas continúan altas, se involucra a Bienestar
            if riesgo == 'Bajo':
                accs.append('Cierre_Seguimiento')   # Si el riesgo cayó a bajo, se habilita el cierre

        # ---------------------------------------------------------------------
        # REGLAS PARA LA FASE 4: Carga_Reestructurada (Se redujo el volumen curricular)
        # ---------------------------------------------------------------------
        elif fase == 'Carga_Reestructurada':
            if riesgo in ('Alto', 'Medio'):
                accs.append('Agendar_Tutoria_LMS')  # Refuerzo en las materias remanentes
            if inasist >= 20:
                accs.append('Notificar_Bienestar')  # Soporte de bienestar si el ausentismo no cedió
            accs.append('Cierre_Seguimiento')       # Permite validar estabilización

        # ---------------------------------------------------------------------
        # REGLAS PARA LA FASE 5: Intervencion_Integral (Protocolos combinados en marcha)
        # ---------------------------------------------------------------------
        elif fase == 'Intervencion_Integral':
            accs.append('Cierre_Seguimiento')  # Tras intervención integral, el agente procede al seguimiento final

        return accs  # Retorna el conjunto de acciones legales aplicables al estado actual

    def result(self, state, action):
        """
        Modelo de Transición determinista RESULT(s, a) -> s'.
        Calcula el estado exacto resultante de aplicar una acción legal sobre un estado dado.
        """
        riesgo, inasist, mat_crit, fase = state  # Desempaquetado del estado previo

        # Caso A: Se notifica a Bienestar Universitario
        if action == 'Notificar_Bienestar':
            nueva_inasist = max(0, inasist - 15)  # El acompañamiento psicosocial reduce el ausentismo en un 15%
            # Si ya se tenía tutoría o ajuste curricular, escala a Intervención Integral; de lo contrario Bienestar Notificado
            nueva_fase = 'Intervencion_Integral' if fase in ('Tutoria_Programada', 'Carga_Reestructurada') else 'Bienestar_Notificado'
            return (riesgo, nueva_inasist, mat_crit, nueva_fase)

        # Caso B: Se agenda tutoría académica en el LMS
        elif action == 'Agendar_Tutoria_LMS':
            nuevo_riesgo = 'Medio' if riesgo == 'Alto' else 'Bajo'  # Mitiga la debilidad conceptual reduciendo el nivel de riesgo
            # Si venía de otra área de apoyo, se consolida como integral; de lo contrario queda en tutoría activa
            nueva_fase = 'Intervencion_Integral' if fase in ('Bienestar_Notificado', 'Carga_Reestructurada') else 'Tutoria_Programada'
            return (nuevo_riesgo, inasist, mat_crit, nueva_fase)

        # Caso C: Se reestructura la carga académica (cancelación preventiva autorizada)
        elif action == 'Reestructurar_Carga':
            nuevas_mat = max(0, mat_crit - 1)                      # Disminuye 1 materia crítica de la carga del alumno
            nuevo_riesgo = 'Medio' if riesgo == 'Alto' else 'Bajo'  # Alivia el estrés cognitivo reduciendo el nivel de riesgo
            return (nuevo_riesgo, inasist, nuevas_mat, 'Carga_Reestructurada')

        # Caso D: Cierre y auditoría por consejería institucional
        elif action == 'Cierre_Seguimiento':
            # Valida formalmente si los indicadores de riesgo han sido normalizados a límites seguros
            nuevo_riesgo = 'Bajo' if (inasist <= 20 and mat_crit <= 1) else riesgo
            return (nuevo_riesgo, inasist, mat_crit, 'Caso_Estabilizado')

        return state  # En caso de acción desconocida, mantiene el estado intacto por seguridad

    def is_goal(self, state):
        """
        Prueba de Meta IS-GOAL(s).
        Evalúa si el estudiante ha alcanzado condiciones cuantitativas y cualitativas de permanencia:
          - Riesgo Académico == 'Bajo'
          - Porcentaje de Inasistencias <= 20%
          - Materias Críticas en riesgo <= 1
          - Fase de acompañamiento estabilizada o integralmente resuelta.
        """
        riesgo, inasist, mat_crit, fase = state
        return (riesgo == 'Bajo' and 
                inasist <= 20 and 
                mat_crit <= 1 and 
                fase in ('Caso_Estabilizado', 'Carga_Reestructurada', 'Intervencion_Integral'))

    def goal_test(self, state):
        """Método de alias estándar compatible con la nomenclatura del repositorio AIMA."""
        return self.is_goal(state)

    def action_cost(self, action):
        """Retorna el costo en horas operativas asociado a una acción particular."""
        return self.action_costs.get(action, 1)

    def path_cost(self, c, state1, action, state2):
        """
        Función acumuladora de costo de trayectoria g(n):
        Suma el costo g acumulado previo más el peso de la nueva arista ejecutada.
        """
        return c + self.action_cost(action)

    def heuristic(self, state):
        """
        Función Heurística Admisible h(n).
        Calcula una cota inferior relajada del número mínimo de horas necesarias para alcanzar la meta.
        Demostración de admisibilidad (h(n) <= h*(n)):
          1. Si inasist > 20%, obligatoriamente se debe llamar a Bienestar (cota indivisible = 16h).
          2. Si mat_crit >= 2, obligatoriamente se debe reestructurar carga (cota indivisible = 8h).
          3. Si riesgo es Alto y no hay materias críticas acumuladas, se requiere al menos tutoría (8h).
        Dado que asume costos mínimos optimistas ignorando transiciones intermedias, jamás sobreestima h*.
        """
        riesgo, inasist, mat_crit, _ = state  # Extrae las variables del estado recibido

        if self.is_goal(state):  # Si el nodo ya es un estado meta, el costo restante es cero
            return 0

        h_val = 0  # Inicializa el acumulador heurístico en horas

        # Requisito obligatorio por inasistencia excesiva
        if inasist > 20:
            h_val += 16  # Suma el costo de 'Notificar_Bienestar'

        # Requisito obligatorio por sobrecarga de materias
        if mat_crit >= 2:
            h_val += 8   # Suma el costo de 'Reestructurar_Carga'
        elif riesgo == 'Alto':
            h_val += 8   # Cota inferior para reducir el riesgo alto a aceptable

        return h_val  # Retorna el valor h(n) en horas

    def h(self, node):
        """Método envoltorio compatible con funciones de búsqueda basadas en AIMA."""
        state = node.state if hasattr(node, 'state') else node
        return self.heuristic(state)


# =============================================================================
# ALGORITMO 1: BÚSQUEDA EN ANCHURA (BFS - BREADTH-FIRST SEARCH)
# =============================================================================
def breadth_first_search(problem):
    """
    Búsqueda en Anchura en Grafo (Graph-Search FIFO).
    Explora sistemáticamente el espacio nivel por nivel.
    Garantiza el menor número de aristas (pasos), pero NO la solución óptima en costos acumulados
    cuando las acciones poseen pesos diferenciados no unitarios (16h, 10h, 8h, 4h).
    """
    start_time = time.perf_counter()     # Inicia el cronómetro de alta resolución
    node = Node(problem.initial)         # Instancia el nodo raíz con el estado inicial s0
    
    # Verificación temprana de meta sobre el nodo inicial (Russell & Norvig, 3ra ed.)
    if problem.is_goal(node.state):
        return node, 1, (time.perf_counter() - start_time) * 1000

    frontier = deque([node])  # Estructura de datos FIFO (First-In, First-Out) para la frontera
    explored = set()          # Conjunto hash (O(1)) para evitar ciclos y repetición de estados
    nodes_expanded = 0        # Contador de nodos extraídos y procesados de la frontera

    while frontier:  # Mientras queden nodos por explorar en la frontera
        node = frontier.popleft()  # Extrae el nodo más superficial del nivel actual (FIFO)
        nodes_expanded += 1        # Incrementa el conteo de expansión
        explored.add(node.state)   # Marca el estado del nodo como explorado

        # Genera los hijos expandiendo cada acción legal aplicable
        for action in problem.actions(node.state):
            child_state = problem.result(node.state, action)                     # Genera el estado sucesor determinista
            child_cost = node.path_cost + problem.action_cost(action)            # Suma el costo real acumulado g(n)
            child_node = Node(child_state, parent=node, action=action, path_cost=child_cost)  # Construye el nodo sucesor

            # Condición de grafo: solo agrega si no ha sido explorado y no está duplicado en la frontera
            if child_state not in explored and all(n.state != child_state for n in frontier):
                if problem.is_goal(child_state):  # Prueba de meta temprana al generar el nodo hijo
                    exec_time = (time.perf_counter() - start_time) * 1000  # Tiempo transcurrido en ms
                    return child_node, nodes_expanded, exec_time           # Retorna solución, nodos y tiempo
                frontier.append(child_node)  # Encola el nodo al final de la frontera

    # Si se agota la frontera sin hallar la meta, retorna fracaso
    return None, nodes_expanded, (time.perf_counter() - start_time) * 1000


# =============================================================================
# ALGORITMO 2: BÚSQUEDA EN PROFUNDIDAD (DFS - DEPTH-FIRST SEARCH)
# =============================================================================
def depth_first_search(problem):
    """
    Búsqueda en Profundidad en Grafo (Graph-Search LIFO).
    Explora la rama más profunda antes de retroceder (backtracking).
    Posee bajo consumo espacial O(b * m), pero no garantiza optimalidad.
    """
    start_time = time.perf_counter()  # Inicia medición de tiempo de ejecución
    start_node = Node(problem.initial)  # Construye el nodo raíz inicial
    frontier = [start_node]             # Estructura de pila LIFO (Last-In, First-Out) usando lista estándar de Python
    explored = set()                    # Lista cerrada de estados explorados para evitar ciclos infinitos
    nodes_expanded = 0                 # Contador de nodos expandidos

    while frontier:  # Mientras existan nodos apilados en la frontera
        node = frontier.pop()  # Desapila el nodo más reciente/profundo (LIFO)
        nodes_expanded += 1    # Registra la expansión del nodo

        # En DFS en grafo, la prueba de meta se realiza formalmente al extraer el nodo
        if problem.is_goal(node.state):
            exec_time = (time.perf_counter() - start_time) * 1000
            return node, nodes_expanded, exec_time

        explored.add(node.state)  # Registra el estado actual en la lista cerrada

        # Explora los sucesores del nodo
        for action in problem.actions(node.state):
            child_state = problem.result(node.state, action)                     # Transición determinista
            child_cost = node.path_cost + problem.action_cost(action)            # Acumula costo g(n)
            child_node = Node(child_state, parent=node, action=action, path_cost=child_cost)

            # Condición de inserción para evitar ciclos y repetición en frontera LIFO
            if child_state not in explored and all(n.state != child_state for n in frontier):
                frontier.append(child_node)  # Empuja el nuevo nodo en la cima de la pila

    return None, nodes_expanded, (time.perf_counter() - start_time) * 1000


# =============================================================================
# ALGORITMO 3: BÚSQUEDA INFORMADA A* (A-STAR GRAPH SEARCH)
# =============================================================================
def astar_search(problem):
    """
    Búsqueda Heurística Informada A* en Grafo.
    Ordena la frontera por la función f(n) = g(n) + h(n).
    Garantiza encontrar la solución con el menor costo global acumulado g(n)
    debido a que h(n) es una heurística admisible y monótonamente consistente.
    """
    start_time = time.perf_counter()                # Inicia medición precisa de tiempo
    start_h = problem.heuristic(problem.initial)    # Calcula la cota heurística h(s0)
    # El nodo inicial tiene g=0 y f = 0 + h(s0)
    start_node = Node(problem.initial, path_cost=0, f_score=start_h)

    counter = 0      # Desempate único para evitar colisiones en heapq cuando dos nodos tienen igual f_score
    frontier = []    # Cola de prioridad (Priority Queue) basada en min-heap binario
    # Se introduce la tupla ordenada: (f_score, counter, nodo)
    heapq.heappush(frontier, (start_node.f_score, counter, start_node))
    
    # Diccionario 'reached': Guarda el menor costo g(n) conocido para llegar a cada estado.
    # Permite podar o actualizar nodos si se descubre una ruta con menor tiempo operacional acumulado.
    reached = {problem.initial: 0}
    nodes_expanded = 0

    while frontier:  # Mientras existan nodos en la cola de prioridad
        # Extrae de la frontera el nodo con el menor valor de f(n) disponible
        _, _, node = heapq.heappop(frontier)
        nodes_expanded += 1

        # En A*, la prueba de meta DEBE realizarse estrictamente al extraer el nodo de la frontera,
        # para preservar la garantía matemática de optimalidad en grafos
        if problem.is_goal(node.state):
            exec_time = (time.perf_counter() - start_time) * 1000
            return node, nodes_expanded, exec_time

        # Genera y evalúa los sucesores
        for action in problem.actions(node.state):
            child_state = problem.result(node.state, action)          # Estado resultante
            g_cost = node.path_cost + problem.action_cost(action)     # Costo acumulado real: g(hijo)
            h_cost = problem.heuristic(child_state)                   # Cota heurística optimista: h(hijo)
            f_cost = g_cost + h_cost                                  # Función de evaluación: f(hijo) = g + h

            # Criterio de aceptación A*: se expande si el estado nunca se ha alcanzado
            # o si la nueva ruta ofrece un costo acumulado g_cost estrictamente menor
            if child_state not in reached or g_cost < reached[child_state]:
                reached[child_state] = g_cost                         # Actualiza la ruta más económica hacia este estado
                child_node = Node(child_state, parent=node, action=action, path_cost=g_cost, f_score=f_cost)
                counter += 1
                heapq.heappush(frontier, (f_cost, counter, child_node))  # Encola en orden de f(n)

    return None, nodes_expanded, (time.perf_counter() - start_time) * 1000
