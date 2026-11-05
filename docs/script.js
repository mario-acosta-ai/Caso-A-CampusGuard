async function fetchData() {
    try {
        const response = await fetch('metrics.json');
        const data = await response.json();
        
        document.getElementById('loading').style.display = 'none';
        document.getElementById('chartBox1').style.display = 'block';
        document.getElementById('chartBox2').style.display = 'block';
        document.getElementById('tableBox').style.display = 'block';

        const labels = Object.keys(data);
        
        // Llenar Tabla
        const tbody = document.getElementById('tableBody');
        labels.forEach(key => {
            const row = `<tr>
                <td><strong>${key}</strong></td>
                <td>${data[key].nodos_expandidos}</td>
                <td>${data[key].tiempo_ms} ms</td>
                <td>${data[key].costo} horas</td>
                <td>${data[key].camino.join(" → ")}</td>
            </tr>`;
            tbody.innerHTML += row;
        });

        // Gráfico 1: Nodos
        new Chart(document.getElementById('nodesChart'), {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Nodos Expandidos',
                    data: labels.map(l => data[l].nodos_expandidos),
                    backgroundColor: ['#FF6384', '#36A2EB', '#4BC0C0']
                }]
            }
        });

        // Gráfico 2: Tiempos
        new Chart(document.getElementById('timeChart'), {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Tiempo de Ejecución (ms)',
                    data: labels.map(l => data[l].tiempo_ms),
                    backgroundColor: ['#FF9F40', '#FFCD56', '#4BC0C0']
                }]
            }
        });

    } catch (error) {
        document.getElementById('loading').innerText = "Error al cargar metrics.json. Asegúrate de que existe.";
    }
}
fetchData();
