let weightChart, weeklyChart, macrosChart;

// Initialize Dashboard Charts
function initDashboardCharts() {
    // Weight Progress Chart
    const weightCtx = document.getElementById('weightChart');
    if (weightCtx) {
        weightChart = new Chart(weightCtx, {
            type: 'line',
            data: {
                labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
                datasets: [{
                    label: 'Weight (kg)',
                    data: [75, 73.5, 72, 71],
                    borderColor: '#0d6efd',
                    backgroundColor: 'rgba(13, 110, 253, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { display: false } },
                scales: {
                    y: { beginAtZero: false }
                }
            }
        });
    }

    // Weekly Summary Chart
    const weeklyCtx = document.getElementById('weeklyChart');
    if (weeklyCtx) {
        weeklyChart = new Chart(weeklyCtx, {
            type: 'doughnut',
            data: {
                labels: ['Calories', 'Workouts', 'Water'],
                datasets: [{
                    data: [85, 70, 60],
                    backgroundColor: ['#0d6efd', '#198754', '#ffc107']
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { position: 'bottom' } }
            }
        });
    }

    // Macros Chart
    const macrosCtx = document.getElementById('macrosChart');
    if (macrosCtx) {
        macrosChart = new Chart(macrosCtx, {
            type: 'doughnut',
            data: {
                labels: ['Protein', 'Carbs', 'Fats'],
                datasets: [{
                    data: [30, 50, 20],
                    backgroundColor: ['#ff6b6b', '#4ecdc4', '#45b7d1']
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { position: 'bottom' } }
            }
        });
    }
}

// Update progress bars animation
function animateProgressBars() {
    document.querySelectorAll('.progress .progress-bar').forEach(bar => {
        const width = bar.style.width || '0%';
        bar.style.width = '0%';
        setTimeout(() => {
            bar.style.width = width;
        }, 100);
    });
}