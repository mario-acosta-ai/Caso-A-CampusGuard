# 🎓 CampusGuard AI - Agente Racional de Búsqueda

**Universidad Militar Nueva Granada**  
*Proyecto Integrador - Modelado formal y arquitectónico de un Agente Racional*

## 📖 Descripción
CampusGuard es un agente racional diseñado para mitigar la deserción estudiantil (18% en primeros semestres). Este repositorio contiene la **abstracción formal del entorno** a un espacio de estados discreto y determinista, junto con la implementación de algoritmos de búsqueda no informada (BFS, DFS) e informada (A*) para encontrar la ruta óptima de intervención (Tutoría, Bienestar o Ajuste de Materias).

## 📊 Dashboard de Métricas (GitHub Pages)
Hemos implementado un panel visual interactivo que consume los resultados del benchmark para comparar la eficiencia de los algoritmos.
👉 [Ver Dashboard en vivo aquí] https://mario-acosta-ai.github.io/Caso-A-CampusGuard/

## 🗂️ Estructura del Proyecto
- `src/`: Contiene la lógica del agente, la clase del problema (AIMA) y los algoritmos.
- `docs/`: Código fuente del dashboard web (GitHub Pages) y los datos (`metrics.json`).
- `benchmark.py`: Ejecuta los 3 algoritmos sobre el mismo estado inicial y guarda las métricas.

## 🚀 ¿Cómo ejecutar localmente?
1. Clona el repositorio:
   ```bash
   git clone https://github.com/mario-acosta-ai/Caso-A-CampusGuard
