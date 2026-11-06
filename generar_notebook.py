"""
Módulo: generar_notebook.py
Proyecto Integrador: Modelado formal y arquitectónico del Agente Racional CampusGuard
Asignatura: Inteligencia Artificial I - Grupo D
Universidad Militar Nueva Granada (FAEDIS)

Este script construye programáticamente el archivo 'CampusGuard_Benchmark.ipynb' bajo el estándar
oficial de Jupyter Notebook (nbformat v4). Su propósito es garantizar la reproducibilidad
del entorno experimental, estructurando de manera ordenada:
  1. La metadata académica del Grupo D y la formalización matemática del quinteto P.
  2. La importación controlada de librerías y del motor 'campusguard_engine.py'.
  3. La instanciación y exploración del estado crítico del estudiante.
  4. La ejecución comparativa y tabulación de métricas (BFS vs DFS vs A*).
  5. La generación del gráfico comparativo de barras de nodos expandidos con Matplotlib.
  6. La sustentación asintótica en notación Big O y demostración de admisibilidad.
"""

# =============================================================================
# IMPORTACIÓN DE LIBRERÍAS
# =============================================================================
import json  # Módulo estándar para manipular y serializar estructuras de datos en formato JSON


# =============================================================================
# ESTRUCTURA DEL NOTEBOOK EN FORMATO JSON (NBFORMAT 4.2)
# =============================================================================
# Se define un diccionario que reproduce con exactitud el esquema oficial de Jupyter Notebooks.
# Cada elemento dentro de la lista 'cells' representa una celda individual (texto Markdown o código ejecutable).
notebook_content = {
 "cells": [
  # -------------------------------------------------------------------------
  # CELDA 1: Encabezado Institucional y Formalización del Problema (Markdown)
  # -------------------------------------------------------------------------
  {
   "cell_type": "markdown",  # Celda de texto formateado con sintaxis Markdown y LaTeX
   "metadata": {},           # Metadatos propios de la celda (vacío por defecto)
   "source": [
    "# Caso A: CampusGuard — Sistema de Acompañamiento e Intervención Académica\n",
    "### Proyecto Integrador: Inteligencia Artificial I — Grupo D\n",
    "**Institución:** Universidad Militar Nueva Granada (FAEDIS)  \n",
    "**Docente:** Oscar Iván Varela Vélez, Msc.  \n",
    "**Integrantes:**  \n",
    "- Angie Valentina Gonzalez Mongui (200616)\n",
    "- Jonhsef Estiven Acosta Quitian (200563)\n",
    "- Juan Guilermo Pulido Moreno (200580)\n",
    "- Mario Alberto Acosta Prieto (200571)\n",
    "- Omar David Rojas Rodriguez (200575)\n",
    "\n",
    "---\n",
    "## 1. Formalización del Espacio de Estados $\\mathcal{P} = \\langle S, s_0, ACTIONS, RESULT, GOAL, c \\rangle$\n",
    "- **Espacio de Estados ($S$):** Tupla de 4 dimensiones `(RiesgoAcademico, Inasistencias, MateriasCriticas, FaseIntervencion)`.\n",
    "- **Estado Inicial ($s_0$):** `('Alto', 35, 2, 'Sin_Intervencion')` — Estudiante crítico en alerta temprana.\n",
    "- **Acciones y Costos (horas):** `Notificar_Bienestar` (16h), `Agendar_Tutoria_LMS` (10h), `Reestructurar_Carga` (8h), `Cierre_Seguimiento` (4h).\n",
    "- **Prueba de Meta:** `Riesgo == 'Bajo'` $\\land$ `Inasistencias <= 20%` $\\land$ `MateriasCriticas <= 1`.\n",
    "- **Heurística Admisible $h(n)$:** Cota inferior optimista que garantiza $h(n) \\le h^*(n)$."
   ]
  },
  # -------------------------------------------------------------------------
  # CELDA 2: Importación de Dependencias y Motor del Problema (Código)
  # -------------------------------------------------------------------------
  {
   "cell_type": "code",          # Celda interactiva de código ejecutable en Python
   "execution_count": None,      # Se inicializa sin número de ejecución (se asignará al correr)
   "metadata": {},
   "outputs": [],                # Lista donde el kernel guardará las salidas tras ejecutar
   "source": [
    "import os\n",
    "import sys\n",
    "import pandas as pd\n",
    "import matplotlib.pyplot as plt\n",
    "from IPython.display import display\n",
    "\n",
    "# Asegurar carga del motor local incorporando el directorio raíz a sys.path\n",
    "sys.path.append(os.path.abspath('.'))\n",
    "\n",
    "# Importación de la clase del problema y los tres algoritmos desde campusguard_engine.py\n",
    "from campusguard_engine import (\n",
    "    CampusGuardProblem,\n",
    "    breadth_first_search,\n",
    "    depth_first_search,\n",
    "    astar_search\n",
    ")\n",
    "\n",
    "print('Motor campusguard_engine importado exitosamente para el Grupo D.')"
   ]
  },
  # -------------------------------------------------------------------------
  # CELDA 3: Instanciación del Problema e Inspección de Estados (Código)
  # -------------------------------------------------------------------------
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Instanciación con el estado inicial crítico formulado en el Corte 1\n",
    "problema = CampusGuardProblem(initial=('Alto', 35, 2, 'Sin_Intervencion'))\n",
    "\n",
    "# Inspección de variables del estado s0 y acciones iniciales legales\n",
    "print(f'Estado Inicial s0: {problema.initial}')\n",
    "print(f'Acciones Legales Iniciales: {problema.actions(problema.initial)}')\n",
    "print(f'Valor Heurístico Inicial h(s0): {problema.heuristic(problema.initial)} horas')"
   ]
  },
  # -------------------------------------------------------------------------
  # CELDA 4: Ejecución Experimental del Benchmark (BFS, DFS, A*) (Código)
  # -------------------------------------------------------------------------
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Ejecución experimental de los algoritmos de búsqueda (BFS, DFS, A*)\n",
    "resultados = []\n",
    "\n",
    "# 1. Búsqueda en Anchura (BFS): Evaluación ciega basada en cola FIFO\n",
    "nodo_bfs, exp_bfs, t_bfs = breadth_first_search(problema)\n",
    "resultados.append({\n",
    "    'Algoritmo': 'BFS (Anchura Ciega)',\n",
    "    'Nodos Expandidos': exp_bfs,\n",
    "    'Tiempo CPU (ms)': round(t_bfs, 3),\n",
    "    'Costo g(n) (h)': nodo_bfs.path_cost if nodo_bfs else None,\n",
    "    'Ruta Óptima de Intervención': ' -> '.join(nodo_bfs.solution()) if nodo_bfs else 'N/A',\n",
    "    'Garantiza Optimalidad': 'No (Costos no unitarios)'\n",
    "})\n",
    "\n",
    "# 2. Búsqueda en Profundidad (DFS): Exploración profunda basada en pila LIFO\n",
    "nodo_dfs, exp_dfs, t_dfs = depth_first_search(problema)\n",
    "resultados.append({\n",
    "    'Algoritmo': 'DFS (Profundidad Ciega)',\n",
    "    'Nodos Expandidos': exp_dfs,\n",
    "    'Tiempo CPU (ms)': round(t_dfs, 3),\n",
    "    'Costo g(n) (h)': nodo_dfs.path_cost if nodo_dfs else None,\n",
    "    'Ruta Óptima de Intervención': ' -> '.join(nodo_dfs.solution()) if nodo_dfs else 'N/A',\n",
    "    'Garantiza Optimalidad': 'No'\n",
    "})\n",
    "\n",
    "# 3. Búsqueda Informada A*: Exploración guiada por función f(n) = g(n) + h(n)\n",
    "nodo_astar, exp_astar, t_astar = astar_search(problema)\n",
    "resultados.append({\n",
    "    'Algoritmo': 'A* (Heurística Admisible)',\n",
    "    'Nodos Expandidos': exp_astar,\n",
    "    'Tiempo CPU (ms)': round(t_astar, 3),\n",
    "    'Costo g(n) (h)': nodo_astar.path_cost if nodo_astar else None,\n",
    "    'Ruta Óptima de Intervención': ' -> '.join(nodo_astar.solution()) if nodo_astar else 'N/A',\n",
    "    'Garantiza Optimalidad': 'Sí (h admisible)'\n",
    "})\n",
    "\n",
    "# Presentación tabular estructurada con pandas en el notebook\n",
    "df_benchmark = pd.DataFrame(resultados)\n",
    "display(df_benchmark[['Algoritmo', 'Nodos Expandidos', 'Tiempo CPU (ms)', 'Costo g(n) (h)', 'Garantiza Optimalidad']])"
   ]
  },
  # -------------------------------------------------------------------------
  # CELDA 5: Visualización Gráfica de Poda y Nodos Expandidos (Código)
  # -------------------------------------------------------------------------
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Visualización comparativa de Nodos Expandidos y Eficiencia de Búsqueda con Matplotlib\n",
    "fig, ax1 = plt.subplots(figsize=(9, 4.5))\n",
    "\n",
    "colores = ['#3498db', '#e67e22', '#2ecc71']  # Azul para BFS, Naranja para DFS, Verde para A*\n",
    "bars = ax1.bar(df_benchmark['Algoritmo'], df_benchmark['Nodos Expandidos'], color=colores, width=0.55)\n",
    "ax1.set_ylabel('Nodos Expandidos en Memoria', fontsize=11, fontweight='bold', color='#2c3e50')\n",
    "ax1.set_title('CampusGuard (Grupo D): Comparativa de Exploración y Eficiencia', fontsize=13, pad=12)\n",
    "ax1.grid(axis='y', linestyle='--', alpha=0.6)\n",
    "\n",
    "# Añadir etiquetas numéricas sobre cada barra\n",
    "for bar in bars:\n",
    "    yval = bar.get_height()\n",
    "    ax1.text(bar.get_x() + bar.get_width()/2, yval + 0.15, f'{int(yval)} nodos', ha='center', va='bottom', fontweight='bold')\n",
    "\n",
    "plt.tight_layout()\n",
    "plt.show()"
   ]
  },
  # -------------------------------------------------------------------------
  # CELDA 6: Sustentación Teórica y Complejidad Big O (Markdown)
  # -------------------------------------------------------------------------
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 2. Sustentación Teórica y Análisis de Complejidad Big O\n",
    "1. **Búsqueda en Anchura (BFS) - $\\mathcal{O}(b^d)$:** Almacena todos los nodos del nivel en una cola FIFO. En entornos con ramificación amplia agota la memoria RAM (`MemoryError`). Al existir costos de acción diferenciados (16h, 10h, 8h, 4h), encuentra la ruta con menos pasos pero con un costo subóptimo de **34 horas**.\n",
    "2. **Búsqueda en Profundidad (DFS) - $\\mathcal{O}(b \\cdot m)$:** Posee un consumo de memoria lineal, pero carece de garantía de optimalidad y puede quedar atrapada en ramas profundas no óptimas.\n",
    "3. **Búsqueda A\\* - $\\mathcal{O}(b^{d - k_h})$:** La heurística admisible actúa como mecanismo de poda al penalizar ramas costosas ($f(n) = g(n) + h(n)$), garantizando encontrar la ruta institucional óptima de **28 horas** en menos de 48 horas de tiempo de respuesta."
   ]
  }
 ],
 # Metadatos globales del notebook para el intérprete de Python
 "metadata": {
  "language_info": {
   "name": "python"
  }
 },
 # Versión del esquema JSON de Jupyter Notebook (versión 4.2)
 "nbformat": 4,
 "nbformat_minor": 2
}

# =============================================================================
# ESCRITURA Y SERIALIZACIÓN DEL ARCHIVO .IPYNB
# =============================================================================
# Se abre el archivo de destino con codificación UTF-8 para admitir tildes y caracteres matemáticos
with open("CampusGuard_Benchmark.ipynb", "w", encoding="utf-8") as f:
    # Se exporta el diccionario 'notebook_content' en formato JSON con indentación legible (1 espacio)
    json.dump(notebook_content, f, indent=1, ensure_ascii=False)

# Mensaje de confirmación en la consola
print("¡Archivo CampusGuard_Benchmark.ipynb generado exitosamente!")
