async function cargarDatos() {
    try {
        const response = await fetch('metrics.json');
        if (!response.ok) throw new Error("No se pudo cargar el archivo JSON");
        
        const data = await response.json();
        
        // Ocultar mensaje de carga
        document.getElementById('loading').style.display = 'none';
        
        // Mostrar contenedores
        document.getElementById('chartBox1').style.display = 'block';
        document.getElementById('chartBox2').style.display = 'block';
        document.getElementById('tableBox').style.display = 'block';

        const labels = Object.keys(data);
        const nodos = labels.map(l => data[l].nodos_expandidos);
        const tiempos = labels.map(l => data[l].tiempo_ms);

        // Llenar la Tabla Benchmark
        const tableBody = document.getElementById('tableBody');
        labels.forEach(algo => {
            const row = `
                <tr>
                    <td><strong>${algo}</strong></td>
                    <td>${data[algo].nodos_expandidos}</td>
                    <td>${data[algo].tiempo_ms}</td>
                    <td>${data[algo].costo}</td>
                    <td>${data[algo].camino.join(" → ") || "N/A"}</td>
                </tr>
            `;
            tableBody.innerHTML += row;
        });

        // Gráfico 1: Nodos Expandidos
        new Chart(document.getElementById('nodesChart'), {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Nodos Expandidos (Memoria)',
                    data: nodos,
                    backgroundColor: ['#FF6384', '#36A2EB', '#4BC0C0'],
                    borderRadius: 6
                }]
            },
            options: { plugins: { title: { display: true, text: 'Eficiencia en Memoria', font: {size: 16} } } }
        });

        // Gráfico 2: Tiempo CPU
        new Chart(document.getElementById('timeChart'), {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Tiempo de Ejecución (ms)',
                    data: tiempos,
                    borderColor: '#FF9F40',
                    backgroundColor: 'rgba(255, 159, 64, 0.2)',
                    fill: true,
                    tension: 0.3,
                    borderWidth: 3,
                    pointRadius: 6
                }]
            },
            options: { plugins: { title: { display: true, text: 'Rendimiento Temporal', font: {size: 16} } } }
        });

    } catch (error) {
        document.getElementById('loading').innerHTML = `<span style="color: red;">Error cargando métricas: ${error.message}</span>`;
        console.error("Error:", error);
    }
}

cargarDatos();
