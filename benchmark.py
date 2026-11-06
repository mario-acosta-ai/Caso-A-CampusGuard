"""
Módulo: benchmark.py
Script de evaluación experimental y benchmarking comparativo de algoritmos de búsqueda.
Compara empíricamente el rendimiento de Búsqueda en Anchura (BFS), Búsqueda en Profundidad (DFS)
y Búsqueda Informada (A*) frente al problema de intervención estudiantil CampusGuard (Grupo D).

Métricas evaluadas:
  - Nodos Expandidos (consumo de memoria y esfuerzo computacional)
  - Tiempo de ejecución de CPU en milisegundos (eficiencia temporal)
  - Costo acumulado del camino g(n) en horas operativas
  - Garantía matemática de optimalidad en entornos con costos no unitarios
"""

# Importación de librerías externas y módulos del sistema
import pandas as pd  # Librería para manipulación y visualización tabular estructurada de datos

# Importación de la formalización del entorno y los motores de búsqueda desde el núcleo local
from campusguard_engine import (
    CampusGuardProblem,     # Formalización matemática del problema (S, s0, ACTIONS, RESULT, GOAL, c)
    breadth_first_search,   # Implementación de Búsqueda Ciega en Anchura (Grafo / FIFO)
    depth_first_search,     # Implementación de Búsqueda Ciega en Profundidad (Grafo / LIFO)
    astar_search            # Implementación de Búsqueda Heurística Informada A*
)


def ejecutar_benchmark():
    """
    Función controladora principal del experimento.
    Instancia el caso de estudio crítico, ejecuta secuencialmente los tres algoritmos,
    recolecta los indicadores de desempeño y genera el reporte comparativo por consola.
    """
    # 1. Instanciación del problema con el estudiante crítico formulado en el Corte 1:
    # Estado s0: Riesgo 'Alto', 35% de inasistencia, 2 materias reprobadas/críticas, etapa 'Sin_Intervencion'.
    problema = CampusGuardProblem(initial=('Alto', 35, 2, 'Sin_Intervencion'))
    
    # Lista auxiliar para almacenar los diccionarios con las métricas recolectadas de cada algoritmo
    resultados = []

    # =========================================================================
    # 1. EVALUACIÓN DE BÚSQUEDA EN ANCHURA (BFS)
    # =========================================================================
    # BFS explora el espacio nivel por nivel mediante una cola FIFO (First-In, First-Out).
    # Desempaquetamos la tupla retornada: (nodo_meta, nodos_expandidos, tiempo_cpu_ms)
    nodo_bfs, exp_bfs, t_bfs = breadth_first_search(problema)
    
    # Registro de resultados de BFS
    resultados.append({
        'Algoritmo de Búsqueda': 'BFS (Búsqueda en Anchura)',
        'Nodos Expandidos': exp_bfs,                                        # Total de nodos extraídos de la frontera
        'Tiempo CPU (ms)': f"{t_bfs:.3f}",                                  # Tiempo de procesamiento formateado a 3 decimales
        'Costo Camino g(n)': f"{nodo_bfs.path_cost} h" if nodo_bfs else "N/A",  # Horas acumuladas de gestión institucional
        # BFS garantiza la ruta con menor número de aristas, pero NO la de menor costo cuando los pesos no son unitarios
        '¿Optimalidad?': 'No (Costos No Unitarios)',
        # Reconstrucción de la secuencia de acciones usando el método solution() del nodo
        'Ruta Obtenida': ' -> '.join(nodo_bfs.solution()) if nodo_bfs else "N/A"
    })

    # =========================================================================
    # 2. EVALUACIÓN DE BÚSQUEDA EN PROFUNDIDAD (DFS)
    # =========================================================================
    # DFS explora hacia la rama más profunda primero mediante una pila LIFO (Last-In, First-Out).
    # Desempaquetamos la tupla retornada: (nodo_meta, nodos_expandidos, tiempo_cpu_ms)
    nodo_dfs, exp_dfs, t_dfs = depth_first_search(problema)
    
    # Registro de resultados de DFS
    resultados.append({
        'Algoritmo de Búsqueda': 'DFS (Búsqueda en Profundidad)',
        'Nodos Expandidos': exp_dfs,                                        # Total de nodos extraídos de la frontera
        'Tiempo CPU (ms)': f"{t_dfs:.3f}",                                  # Tiempo de CPU medido con time.perf_counter()
        'Costo Camino g(n)': f"{nodo_dfs.path_cost} h" if nodo_dfs else "N/A",  # Costo acumulado en horas
        # DFS no es admisible ni óptimo; la solución encontrada depende estrictamente del orden de ramificación
        '¿Optimalidad?': 'No',
        'Ruta Obtenida': ' -> '.join(nodo_dfs.solution()) if nodo_dfs else "N/A"
    })

    # =========================================================================
    # 3. EVALUACIÓN DE BÚSQUEDA HEURÍSTICA INFORMADA (A*)
    # =========================================================================
    # A* prioriza nodos con base en la función de evaluación f(n) = g(n) + h(n),
    # donde g(n) es el costo real acumulado y h(n) es la cota inferior heurística admisible.
    # Desempaquetamos la tupla retornada: (nodo_meta, nodos_expandidos, tiempo_cpu_ms)
    nodo_astar, exp_astar, t_astar = astar_search(problema)
    
    # Registro de resultados de A*
    resultados.append({
        'Algoritmo de Búsqueda': 'A* (Búsqueda Informada)',
        'Nodos Expandidos': exp_astar,                                      # Cantidad de nodos necesarios tras aplicar poda heurística
        'Tiempo CPU (ms)': f"{t_astar:.3f}",                                # Tiempo de procesamiento en milisegundos
        'Costo Camino g(n)': f"{nodo_astar.path_cost} h" if nodo_astar else "N/A",  # Costo óptimo garantizado (menor horas de respuesta)
        # Al ser h(n) admisible (h(n) <= h*(n)) y consistente, A* garantiza matemáticamente encontrar la solución óptima
        '¿Optimalidad?': 'Sí (h Admisible y Consistente)',
        'Ruta Obtenida': ' -> '.join(nodo_astar.solution()) if nodo_astar else "N/A"
    })

    # =========================================================================
    # REPORTE Y FORMATEO DE RESULTADOS TABULARES
    # =========================================================================
    # Conversión de la lista de diccionarios en un DataFrame de pandas para presentación estructurada
    df = pd.DataFrame(resultados)
    
    # Impresión del encabezado del informe experimental
    print("\n" + "=" * 85)
    print("      TABLA BENCHMARK EXPERIMENTAL - CAMPUSGUARD (UNIVERSIDAD MILITAR)")
    print("=" * 85)
    
    # Despliegue de la tabla comparativa con las columnas solicitadas en la rúbrica del docente
    columnas_principales = ['Algoritmo de Búsqueda', 'Nodos Expandidos', 'Tiempo CPU (ms)', 'Costo Camino g(n)', '¿Optimalidad?']
    print(df[columnas_principales].to_string(index=False))
    
    # Detalle analítico de las secuencias de intervención encontradas por cada algoritmo
    print("\nDetalle de Trayectorias de Intervención:")
    for _, row in df.iterrows():
        # Itera por fila imprimiendo la ruta paso a paso y el impacto en tiempo operacional acumulado
        print(f"• {row['Algoritmo de Búsqueda']}: {row['Ruta Obtenida']} (Costo total: {row['Costo Camino g(n)']})")
    
    print("=" * 85 + "\n")


# Bloque de ejecución estándar en Python
if __name__ == '__main__':
    # Se asegura de que la función únicamente se dispare si el script es ejecutado
    # como programa principal (python benchmark.py) y no cuando sea importado como módulo
    ejecutar_benchmark()
