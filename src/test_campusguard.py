"""
Módulo: tests/test_campusguard.py
Pruebas unitarias automatizadas para validar el comportamiento del motor de búsqueda.
Evalúa la lógica del dominio, la admisibilidad de la heurística, la consistencia
monótona y la optimalidad de los algoritmos frente al problema CampusGuard (Grupo D).
"""

# Importación de librerías estándar de Python
import os          # Permite interactuar con el sistema operativo (rutas de archivos)
import sys         # Provee acceso a variables y funciones que interactúan con el intérprete
import unittest    # Framework integrado en Python para crear y ejecutar pruebas unitarias (tests)

# Se agrega la ruta del directorio padre (la carpeta raíz del proyecto) al sistema (sys.path).
# Esto es obligatorio porque este archivo está dentro de la subcarpeta 'tests/', y necesitamos
# que Python encuentre e importe el archivo 'campusguard_engine.py' que está un nivel arriba.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importación de la clase del problema y los algoritmos desde el motor principal del proyecto
from campusguard_engine import (
    CampusGuardProblem,     # Clase que define el entorno, estados, acciones y costos
    breadth_first_search,   # Algoritmo de Búsqueda en Anchura (BFS)
    depth_first_search,     # Algoritmo de Búsqueda en Profundidad (DFS)
    astar_search            # Algoritmo de Búsqueda Informada (A*)
)

class TestCampusGuardEngine(unittest.TestCase):
    """
    Clase de pruebas (Test Suite) que hereda de unittest.TestCase.
    Contiene todos los métodos de prueba para el Agente Racional.
    """

    def setUp(self):
        """
        Método de preparación (Setup). Se ejecuta automáticamente ANTES de CADA prueba individual.
        Aquí inicializamos una instancia fresca del problema para que los tests no interfieran entre sí.
        """
        # Instanciamos el problema usando el estado crítico definido en el Corte 1:
        # Riesgo Alto, 35% de inasistencia, 2 materias críticas, sin ninguna intervención aún.
        self.problem = CampusGuardProblem(initial=('Alto', 35, 2, 'Sin_Intervencion'))

    def test_estado_inicial_y_acciones_disponibles(self):
        """
        Prueba Unitaria 1: Verifica que desde el estado crítico inicial el agente
        detecte correctamente cuáles son las acciones legales permitidas.
        """
        # Se solicitan las acciones legales aplicables al estado inicial (s0)
        accs = self.problem.actions(self.problem.initial)
        
        # Validamos que las 3 acciones críticas de la fase 'Sin_Intervencion' estén disponibles en la lista 'accs'
        self.assertIn('Notificar_Bienestar', accs)   # Requerida porque inasistencia (35) >= 20
        self.assertIn('Reestructurar_Carga', accs)   # Requerida porque materias críticas (2) >= 2
        self.assertIn('Agendar_Tutoria_LMS', accs)   # Requerida porque el riesgo es 'Alto'

    def test_modelo_transicion_determinista(self):
        """
        Prueba Unitaria 2: Verifica que la función de transición (RESULT) calcule de
        forma determinista y exacta el estado siguiente tras aplicar una acción.
        """
        # Simulamos aplicar la acción 'Reestructurar_Carga' sobre el estado inicial
        s_siguiente = self.problem.result(self.problem.initial, 'Reestructurar_Carga')
        
        # Comprobamos que el nuevo estado sea el esperado según las reglas del dominio:
        # El riesgo baja de 'Alto' a 'Medio', las materias críticas bajan de 2 a 1,
        # la inasistencia se mantiene en 35, y la fase cambia a 'Carga_Reestructurada'.
        self.assertEqual(s_siguiente, ('Medio', 35, 1, 'Carga_Reestructurada'))

    def test_admisibilidad_heuristica(self):
        """
        Prueba Unitaria 3: Valida la propiedad matemática de Admisibilidad en A*.
        Una heurística es admisible si NUNCA sobreestima el costo real: h(n) <= h*(n).
        """
        # Calculamos el valor de la heurística estimada h(n) para el estado inicial
        h_s0 = self.problem.heuristic(self.problem.initial)
        
        # Verificamos que el cálculo teórico retorne 24 horas (16h de Bienestar + 8h de Carga)
        self.assertEqual(h_s0, 24)
        
        # Sabiendo por el benchmark que el costo óptimo real (h*) de la ruta completa es 28 horas,
        # verificamos rigurosamente que 24 <= 28, demostrando que no sobreestima el costo.
        self.assertLessEqual(h_s0, 28)

    def test_consistencia_monotona(self):
        """
        Prueba Unitaria 4: Valida la propiedad de Consistencia (Desigualdad Triangular).
        Verifica que h(s) <= c(s, a, s') + h(s') para cada acción 'a' y estado resultante 's_prima'.
        Si una heurística es consistente, el primer camino que encuentra A* hacia un nodo es el óptimo.
        """
        s = self.problem.initial  # Tomamos el estado inicial como pivote
        
        # Iteramos sobre todas las acciones legales desde el estado inicial
        for a in self.problem.actions(s):
            # Calculamos el estado resultante tras aplicar la acción 'a'
            s_prima = self.problem.result(s, a)
            # Obtenemos el costo real en horas de ejecutar la acción 'a'
            costo = self.problem.action_cost(a)
            
            # Verificamos la desigualdad: h(nodo_actual) <= costo_accion + h(nodo_siguiente)
            self.assertLessEqual(self.problem.heuristic(s), costo + self.problem.heuristic(s_prima))

    def test_optimalidad_astar(self):
        """
        Prueba Unitaria 5: Verifica empíricamente que A* es óptimo y encuentra un camino
        mejor o igual que la búsqueda ciega BFS (que sufre con costos no unitarios).
        """
        # Ejecutamos Búsqueda en Anchura (BFS) y guardamos el nodo final
        nodo_bfs, _, _ = breadth_first_search(self.problem)
        
        # Ejecutamos Búsqueda Informada (A*) y guardamos el nodo final
        nodo_astar, _, _ = astar_search(self.problem)
        
        # Verificamos que A* efectivamente haya encontrado una solución (no sea un valor nulo)
        self.assertIsNotNone(nodo_astar)
        
        # Comparamos costos acumulados g(n): El costo de A* debe ser menor o igual al de BFS.
        # BFS encuentra la ruta en menos pasos pero suma 34 horas; A* garantiza la de 28 horas.
        self.assertLessEqual(nodo_astar.path_cost, nodo_bfs.path_cost)
        
        # Verificamos que el costo exacto retornado por A* sea la ruta óptima demostrada de 28 horas
        self.assertEqual(nodo_astar.path_cost, 28)

# Bloque de ejecución principal del script
if __name__ == '__main__':
    # Esta línea indica que si el archivo se ejecuta directamente desde la terminal
    # (python test_campusguard.py), se correrán todas las pruebas definidas en la clase.
    unittest.main()
