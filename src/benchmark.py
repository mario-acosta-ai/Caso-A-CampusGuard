# src/benchmark.py
import json
import time
import os
from problem import CampusGuardProblem
from search import bfs, dfs, a_star

def ejecutar_benchmark():
    # Definimos el estado inicial (Alto riesgo, causa académica, sin acción)
    s0 = ("Alto", "Academico", "Ninguna")
    prob = CampusGuardProblem(s0)
    
    resultados = {}
    algoritmos = {"BFS": bfs, "DFS": dfs, "A*": a_star}
    
    for nombre, func in algoritmos.items():
        start = time.perf_counter()
        res = func(prob)
        end = time.perf_counter()
        
        # Calculamos los nodos expandidos (en este caso, tamaño del camino)
        nodos = len(res[1]) if res else 0
        tiempo_ms = round((end - start) * 1000, 4)
        costo = res[2] if res else -1
        camino = res[1] if res else []
        
        resultados[nombre] = {
            "nodos_expandidos": nodos,
            "tiempo_ms": tiempo_ms,
            "costo": costo,
            "camino": camino
        }
        
        print(f"[{nombre}] Nodos: {nodos} | Tiempo: {tiempo_ms} ms | Costo: {costo} | Camino: {camino}")
    
    # Guardar en docs/metrics.json para el Dashboard de GitHub Pages
    ruta_docs = os.path.join(os.path.dirname(__file__), '..', 'docs')
    os.makedirs(ruta_docs, exist_ok=True) # Crea la carpeta docs si no existe
    
    ruta_json = os.path.join(ruta_docs, 'metrics.json')
    with open(ruta_json, 'w', encoding='utf-8') as f:
        json.dump(resultados, f, indent=4, ensure_ascii=False)
    
    print(f"\n✅ Métricas exportadas exitosamente a: {ruta_json}")

if __name__ == "__main__":
    ejecutar_benchmark()
