// ==========================================
// CAMPUSGUARD AI - DASHBOARD DE RENDIMIENTO
// ==========================================

let pyodide;
const runBtn = document.getElementById('runBtn');
const statusMsg = document.getElementById('statusMsg');
let chartNodos = null;
let chartTiempos = null;

// CONFIGURACIÓN GITHUB
const GITHUB_USER = 'mario-acosta-ai';
const GITHUB_REPO = 'Caso-A-CampusGuard';
const GITHUB_BRANCH = 'main'; 

// Ahora el motor está en la raíz, no en src/
const BASE_RAW_URL = `https://raw.githubusercontent.com/${GITHUB_USER}/${GITHUB_REPO}/${GITHUB_BRANCH}/CampusGuard_engine.py`;

async function initPyodide() {
    try {
        statusMsg.innerText = "Descargando entorno Python... (esto toma unos segundos)";
        pyodide = await loadPyodide();
        
        statusMsg.innerText = "Descargando motor desde el repositorio...";
        
        // Añadimos ?v=4 para forzar la recarga de caché
        const response = await fetch(`${BASE_RAW_URL}?v=4`);

        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status}. Verifica que campusguard_engine.py esté en la raíz.`);
        }

        const engineCode = await response.text();

        // Escribir en el sistema de archivos de Pyodide
        pyodide.FS.writeFile('campusguard_engine.py', engineCode);
        
        runBtn.disabled = false;
        runBtn.innerText = "▶ Ejecutar Benchmark";
        statusMsg.innerText = "¡Motor listo! Presiona el botón.";
        statusMsg.style.color = "#27ae60";
    } catch (error) {
        console.error("Error de inicialización:", error);
        runBtn.innerText = "❌ Error de carga";
        statusMsg.innerText = error.message;
        statusMsg.style.color = "#e74c3c";
    }
}

initPyodide();

runBtn.addEventListener('click', async () => {
    runBtn.disabled = true;
    runBtn.innerText = "⏳ Ejecutando...";
    statusMsg.innerText = "Ejecutando algoritmos...";
    statusMsg.style.color = "#333";

    try {
        const executionScript = `
import time
import json
from campusguard_engine import CampusGuardProblem, breadth_first_search, depth_first_search, astar_search

s0 = ('Alto', 35, 2, 'Sin_Intervencion')
problem = CampusGuardProblem(initial=s0)
algos = {"BFS": breadth_first_search, "DFS": depth_first_search, "A*": astar_search}
results = {}

for name, func in algos.items():
    nodo, exp, t = func(problem)
    
    results[name] = {
        "nodos": exp,
        "tiempo_ms": round(t, 3),
        "costo": nodo.path_cost if nodo else -1,
        "camino": nodo.solution() if nodo else []
    }
json.dumps(results)
        `;

        const resultJson = await pyodide.runPythonAsync(executionScript);
        const data = JSON.parse(resultJson);
        
        renderDashboard(data);
        statusMsg.innerText = "✅ Ejecución finalizada correctamente.";
        statusMsg.style.color = "#27ae60";
    } catch (error) {
        console.error("Error detallado de Python:", error);
        statusMsg.innerText = "❌ Error: " + (error.message || error);
        statusMsg.style.color = "#e74c3c";
    } finally {
        runBtn.innerText = "▶ Volver a Ejecutar";
        runBtn.disabled = false;
    }
});

function renderDashboard(data) {
    document.getElementById('chartsSection').style.display = 'grid';
    document.getElementById('tableSection').style.display = 'block';

    const labels = Object.keys(data);
    const tbody = document.getElementById('tableBody');
    tbody.innerHTML = '';
    
    labels.forEach(key => {
        tbody.innerHTML += `
            <tr>
                <td><strong>${key}</strong></td>
                <td>${data[key].nodos}</td>
                <td>${data[key].tiempo_ms}</td>
                <td>${data[key].costo}</td>
                <td>${data[key].camino.join(" → ")}</td>
            </tr>`;
    });

    if (chartNodos) chartNodos.destroy();
    if (chartTiempos) chartTiempos.destroy();

    chartNodos = new Chart(document.getElementById('nodesChart'), {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Nodos Expandidos',
                data: labels.map(l => data[l].nodos),
                backgroundColor: ['#FF6384', '#36A2EB', '#4BC0C0'],
                borderRadius: 6
            }]
        },
        options: { plugins: { legend: { display: false } } }
    });

    chartTiempos = new Chart(document.getElementById('timeChart'), {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Tiempo (ms)',
                data: labels.map(l => data[l].tiempo_ms),
                borderColor: '#f39c12',
                backgroundColor: 'rgba(243, 156, 18, 0.2)',
                fill: true,
                tension: 0.3,
                borderWidth: 3,
                pointRadius: 6,
                pointBackgroundColor: 'white'
            }]
        },
        options: { plugins: { legend: { display: false } } }
    });
}
