async function cargarDatos() {
    try {
        const response = await fetch('metrics.json');
        const data = await response.json();
        
        const labels = Object.keys(data);
        const nodos = labels.map(l => data[l].nodos_expandidos);
        const tiempos = labels.map(l => data[l].tiempo_ms);

        // Gráfico de Nodos Expandidos
        new Chart(document.getElementById('nodesChart'), {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Nodos Expandidos',
                    data: nodos,
                    backgroundColor: ['#FF6384', '#36A2EB', '#4BC0C0']
                }]
            },
            options: { plugins: { title: { display: true, text: 'Eficiencia en Memoria (Nodos)' } } }
        });

        // Gráfico de Tiempo CPU
        new Chart(document.getElementById('timeChart'), {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Tiempo CPU (ms)',
                    data: tiempos,
                    borderColor: '#FF9F40',
                    tension: 0.1
                }]
            },
            options: { plugins: { title: { display: true, text: 'Rendimiento Temporal' } } }
        });
    } catch (error) {
        console.error("Error cargando las métricas:", error);
    }
}
cargarDatos();
