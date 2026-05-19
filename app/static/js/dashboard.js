// ==========================================
// Nama File: dashboard.js
// Deskripsi: JS khusus halaman dashboard
// Penulis:   Fawwaz Yaqzhan
// Tanggal:   10-05-2026
// Catatan:
//   - Mengatur interaksi user di halaman dashboard
// ==========================================       

document.addEventListener("DOMContentLoaded", function () {
    
    // Konfigurasi Font Global Chart.js agar senada dengan CSS
    Chart.defaults.font.family = "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif";
    Chart.defaults.font.color = "#495057";

    // Helper Fungsi untuk Format Rupiah pada Tooltip & Sumbu Grafik
    const formatRupiah = (value) => {
        return 'Rp ' + Number(value).toLocaleString('id-ID', { minimumFractionDigits: 0 });
    };

    // ==========================================
    // IMPLEMENTASI GRAFIK 1: TREN ARUS KAS (LINE)
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
                        borderColor: '#28a745', // Match warna .card-income CSS
                        backgroundColor: 'rgba(40, 167, 69, 0.08)',
                        tension: 0.3, // Curve sedikit lebih smooth
                        fill: true,
                        borderWidth: 3,
                        pointRadius: 2,
                        pointHoverRadius: 6
                    },
                    {
                        label: 'Pengeluaran',
                        data: expenseData,
                        borderColor: '#dc3545', // Match warna .card-expense CSS
                        backgroundColor: 'rgba(220, 53, 69, 0.08)',
                        tension: 0.3,
                        fill: true,
                        borderWidth: 3,
                        pointRadius: 2,
                        pointHoverRadius: 6
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return ` ${context.dataset.label}: ${formatRupiah(context.raw)}`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        grid: { display: false } // Hilangkan garis vertikal agar clean
                    },
                    y: { 
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) { return formatRupiah(value); }
                        }
                    }
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
                    // Palet warna modern berkarakter pastel-bold yang kontras
                    backgroundColor: ['#4e73df', '#1cc88a', '#36b9cc', '#f6c23e', '#e74a3b', '#858796'],
                    borderWidth: 2,
                    borderColor: '#ffffff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { 
                        position: 'right',
                        labels: { boxWidth: 12, padding: 15 }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return ` ${context.label}: ${formatRupiah(context.raw)}`;
                            }
                        }
                    }
                },
                cutout: '70%' // Membuat lubang tengah donat sedikit lebih tipis & modern
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
                    backgroundColor: '#007bff', // Match warna .card-balance CSS
                    borderRadius: 6,
                    barThickness: 20 // Mengontrol ketebalan bar agar tidak terlalu gemuk
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return ` Saldo: ${formatRupiah(context.raw)}`;
                            }
                        }
                    }
                },
                scales: {
                    x: { 
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) { return formatRupiah(value); }
                        }
                    },
                    y: {
                        grid: { display: false } // Hilangkan garis horizontal di latar belakang bar
                    }
                }
            }
        });
    }
});
