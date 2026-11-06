# 🎓 CampusGuard AI - Agente Racional de Búsqueda

**Universidad Militar Nueva Granada**  
*Proyecto Integrador - Modelado formal y arquitectónico de un Agente Racional*  
**Asignatura:** Inteligencia Artificial I - Grupo D

**Integrantes:**
* Angie Valentina González Mongui (200616)
* Juan Guillermo Pulido Moreno (200580)
* Jonhsef Estiven Acosta Quitián (200563)
* Omar David Rojas Rodríguez (200575)
* Mario Alberto Acosta Prieto (200571)

---

## 📖 Descripción del Proyecto
CampusGuard es un sistema de alerta temprana diseñado para mitigar el 18% de deserción estudiantil. Este repositorio formaliza el entorno como un **espacio de estados determinista y discreto**, e implementa algoritmos de búsqueda para encontrar la ruta de intervención óptima (Tutoría, Bienestar o Ajuste de Materias) en menos de 48 horas.

## 📊 Dashboard de Métricas (GitHub Pages)
Hemos implementado un panel visual interactivo que ejecuta el motor de Python directamente en el navegador para comparar la eficiencia de los algoritmos.
👉 **[Ver Dashboard en vivo aquí](https://mario-acosta-ai.github.io/Caso-A-CampusGuard/)**

### 🤖 Agentes Implementados y Justificación
1. **BFS (Breadth-First Search):** Agente de búsqueda no informada. Garantiza encontrar la solución con el menor número de pasos (óptimo en costo uniforme), pero consume mucha memoria \(O(b^d)\) y es subóptimo con costos diferenciados.
2. **DFS (Depth-First Search):** Agente de búsqueda no informada. Ahorra memoria \(O(b \cdot m)\), pero no garantiza optimalidad y puede atascarse en ramas profundas.
3. **A* (A-Star):** Agente de búsqueda informada. Utiliza una **heurística admisible \(h(n)\)** (costo mínimo restante) para podar el árbol de búsqueda y garantizar la ruta más económica \(O(b^{d-k_h})\), encontrando la solución óptima de 28 horas.

## 🚀 ¿Cómo ejecutar localmente?
1. Clona el repositorio:
   ```bash
   git clone https://github.com/TU-USUARIO/CampusGuard-AI.git

## 🗂️ Estructura del Proyecto
```text
CampusGuard-AI/
│
├── docs/                       # Dashboard Web (GitHub Pages)
│   ├── index.html
│   ├── style.css
│   └── script.js
├── tests/                        
│   └── test_campusguard.py     # Pruebas unitarias de admisibilidad y consistencia
├── .gitignore
├── benchmark.py                # Script de benchmarking comparativo
├── CampusGuard_Benchmark.ipynb # Cuaderno experimental con tablas y gráficos
├── campusguard_engine.py       # Motor principal (Clase Problem + Algoritmos)
├── generar_notebook.py         # Script generador del cuaderno Jupyter
├── README.md
└── requirements.txt
