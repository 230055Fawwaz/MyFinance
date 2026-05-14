// ==========================================
// Nama File: dashboard.js
// Deskripsi: JS khusus halaman dashboard
// Penulis:   Fawwaz Yaqzhan
// Tanggal:   10-05-2026
// Catatan:
//   - Mengatur interaksi user di halaman dashboard
// ==========================================       

document.addEventListener("DOMContentLoaded", function () {
    
    // ==========================================
    // INEPLEMENTASI GRAFIK 1: TREN ARUS KAS (LINE)
    // ==========================================
    const cfCanvas = document.getElementById('cashFlowChart');
    if (cfCanvas) {
        const labels = JSON.parse(cfCanvas.getAttribute('data-labels'));
        const incomeData = JSON.parse(cfCanvas.getAttribute('data-income'));
        const expenseData = JSON.parse(cfCanvas.getAttribute('data-expense'));

        new Chart(cfCanvas, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Pemasukan',
                        data: incomeData,
                        borderColor: '#2ecc71',
                        backgroundColor: 'rgba(46, 204, 113, 0.1)',
                        tension: 0.2,
                        fill: true
                    },
                    {
                        label: 'Pengeluaran',
                        data: expenseData,
                        borderColor: '#e74c3c',
                        backgroundColor: 'rgba(231, 76, 60, 0.1)',
                        tension: 0.2,
                        fill: true
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: { beginAtZero: true }
                }
            }
        });
    }

    // ==========================================
    // IMPLEMENTASI GRAFIK 2: ALOKASI PENGELUARAN (DONUT)
    // ==========================================
    const expCanvas = document.getElementById('expenseChart');
    if (expCanvas) {
        const labels = JSON.parse(expCanvas.getAttribute('data-labels'));
        const values = JSON.parse(expCanvas.getAttribute('data-values'));

        new Chart(expCanvas, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: values,
                    backgroundColor: ['#3498db', '#9b59b6', '#f1c40f', '#e67e22', '#1abc9c', '#95a5a6']
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'right' }
                }
            }
        });
    }

    // ==========================================
    // IMPLEMENTASI GRAFIK 3: SALDO AKUN (BAR HORIZONTAL)
    // ==========================================
    const accCanvas = document.getElementById('accountChart');
    if (accCanvas) {
        const labels = JSON.parse(accCanvas.getAttribute('data-labels'));
        const values = JSON.parse(accCanvas.getAttribute('data-values'));

        new Chart(accCanvas, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Saldo Tersedia',
                    data: values,
                    backgroundColor: '#34495e',
                    borderRadius: 5
                }]
            },
            options: {
                indexAxis: 'y', // Membuat bar chart menjadi horizontal
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: { beginAtZero: true }
                },
                plugins: {
                    legend: { display: false }
                }
            }
        });
    }
});
