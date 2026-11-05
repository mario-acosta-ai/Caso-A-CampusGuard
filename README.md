# 🎓 CampusGuard AI - Agente Racional de Búsqueda

**Universidad Militar Nueva Granada**  
*Proyecto Integrador - Modelado formal y arquitectónico de un Agente Racional*

**Integrantes**
*Angie Valentina González Mongui | Juan Guillermo Pulido Moreno | Jonhsef Estiven Acosta Quitián | Omar David Rojas Rodríguez | Mario Alberto Acosta Prieto*


## 📖 Descripción del Proyecto
CampusGuard es un sistema de alerta temprana diseñado para mitigar el 18% de deserción estudiantil. Este repositorio formaliza el entorno como un **espacio de estados determinista y discreto**, e implementa algoritmos de búsqueda para encontrar la ruta de intervención óptima (Tutoría, Bienestar o Ajuste de Materias) en menos de 48 horas.

## 📊 Dashboard de Métricas (GitHub Pages)
Hemos implementado un panel visual interactivo que consume los resultados del benchmark para comparar la eficiencia de los algoritmos.
👉 [Ver Dashboard en vivo aquí] https://mario-acosta-ai.github.io/Caso-A-CampusGuard/

### 🤖 Agentes Implementados
1. **BFS (Breadth-First Search):** Agente de búsqueda no informada. Garantiza encontrar la solución con el menor número de pasos (óptimo en costo uniforme), pero consume mucha memoria \(O(b^d)\).
2. **DFS (Depth-First Search):** Agente de búsqueda no informada. Ahorra memoria \(O(b \cdot m)\), pero no garantiza optimalidad y puede atascarse en ramas infinitas.
3. **A* (A-Star):** Agente de búsqueda informada. Utiliza una **heurística admisible \(h(n)\)** (costo mínimo restante) para podar el árbol de búsqueda y encontrar la ruta más económica \(O(b^{d-k_h})\).

## 🚀 ¿Cómo ejecutar localmente?
1. Clona el repositorio:
   ```bash
   git clone https://github.com/mario-acosta-ai/Caso-A-CampusGuard

## 🗂️ Estructura del Proyecto
```text
CampusGuard-AI/
├── src/                  # Código fuente en Python
│   ├── __init__.py
│   ├── problem.py        # Clase CampusGuardProblem (Estructura AIMA)
│   ├── search.py         # Algoritmos BFS, DFS y A*
│   └── benchmark.py      # Script que ejecuta pruebas y exporta metrics.json
├── docs/                 # Carpeta para GitHub Pages (Dashboard)
│   ├── index.html        # Interfaz del dashboard
│   ├── style.css         # Estilos visuales
│   ├── script.js         # Lógica de gráficos (Chart.js + Pyodide)
│   └── metrics.json      # Datos generados por benchmark.py
├── CampusGuard_benchmark.ipynb  # Notebook de ejecución paso a paso
├── requirements.txt
└── README.md
