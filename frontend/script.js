
const API_URL = "http://127.0.0.1:8000";

async function loadDashboard() {
    try {
        // Fetch KPI data from the backend
        const response = await fetch(`${API_URL}/api/kpis`);

        if (!response.ok) {
            throw new Error("Failed to fetch dashboard data");
        }

        const data = await response.json();

        document.getElementById("production").textContent =
            Number(data.total_production).toLocaleString();

        document.getElementById("defects").textContent =
            Number(data.total_defects).toLocaleString();

        document.getElementById("defect-rate").textContent =
            `${Number(data.defect_rate).toFixed(2)}%`;

        document.getElementById("machines").textContent =
            Number(data.machines_monitored).toLocaleString();

        // Fetch machine performance data
        const machineResponse = await fetch(`${API_URL}/api/machines`);

        if (!machineResponse.ok) {
            throw new Error("Failed to fetch machine data");
        }

        const machines = await machineResponse.json();
        const table = document.getElementById("machine-table");

        table.replaceChildren();

        if (machines.length === 0) {
            table.innerHTML =
                '<tr><td colspan="4">No machine data found.</td></tr>';
            return;
        }

        machines.forEach((machine) => {
            const row = document.createElement("tr");

            const values = [
                machine.machine_id,
                Number(machine.production).toLocaleString(),
                Number(machine.defects).toLocaleString(),
                `${Number(machine.defect_rate).toFixed(2)}%`
            ];

            values.forEach((value) => {
                const cell = document.createElement("td");
                cell.textContent = value;
                row.appendChild(cell);
            });

            table.appendChild(row);
        });

    } catch (error) {
        console.error("Dashboard error:", error);

        document.getElementById("production").textContent = "Unavailable";
        document.getElementById("defects").textContent = "Unavailable";
        document.getElementById("defect-rate").textContent = "Unavailable";
        document.getElementById("machines").textContent = "Unavailable";

        document.getElementById("machine-table").innerHTML =
            '<tr><td colspan="4">Backend unavailable. Start the API and refresh.</td></tr>';
    }
}

loadDashboard();

async function loadProductionTrend() {
    const canvas = document.getElementById("productionChart");

    if (!canvas) return;

    try {
        const response = await fetch(
            `${API_URL}/api/production-trend`
        );

        if (!response.ok) {
            throw new Error("Could not load production trend");
        }

        const data = await response.json();

        new Chart(canvas, {
            type: "line",
            data: {
                labels: data.map(item => item.month),
                datasets: [{
                    label: "Monthly Production",
                    data: data.map(item => item.production),
                    borderColor: "#2563eb",
                    backgroundColor: "rgba(37, 99, 235, 0.12)",
                    borderWidth: 3,
                    fill: true,
                    tension: 0.3,
                    pointRadius: 3
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true,
                        position: "top"
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: "Production Quantity"
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: "Month"
                        }
                    }
                }
            }
        });

    } catch (error) {
        console.error("Production chart error:", error);
        canvas.parentElement.textContent =
            "Production trend unavailable. Check the API endpoint.";
    }
}

loadProductionTrend();
