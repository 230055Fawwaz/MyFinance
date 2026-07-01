// ==========================================
// Nama File: dashboard.js
// Deskripsi: JS khusus halaman dashboard (Tema Finansial & Responsif Tema)
// Penulis:   Fawwaz Yaqzhan
// Tanggal:   10-05-2026
// Catatan:
//   - Mengatur interaksi user di halaman dashboard
//   - Responsif terhadap perubahan tema gelap/terang secara langsung
// ==========================================

document.addEventListener('DOMContentLoaded', function () {
    // Ambil warna tema saat ini dari dokumen
    const getThemeStyles = () => {
        const styles = getComputedStyle(document.documentElement);
        return {
            primary: styles.getPropertyValue('--primary-color').trim() || '#047857',
            success: styles.getPropertyValue('--success-color').trim() || '#10B981',
            danger: styles.getPropertyValue('--danger-color').trim() || '#EF4444',
            warning: styles.getPropertyValue('--warning-color').trim() || '#D97706',
            textMuted: styles.getPropertyValue('--chart-text').trim() || '#64748B',
            grid: styles.getPropertyValue('--chart-grid').trim() || '#E2E8F0',
            cardBg: styles.getPropertyValue('--card-bg').trim() || '#FFFFFF',
        };
    };

    let colors = getThemeStyles();

    // Konfigurasi Font Global Chart.js agar senada dengan CSS
    Chart.defaults.font.family = "'Plus Jakarta Sans', -apple-system, sans-serif";
    Chart.defaults.color = colors.textMuted;

    // Helper Fungsi untuk Format Rupiah pada Tooltip & Sumbu Grafik
    const formatRupiah = (value) => {
        return 'Rp ' + Number(value).toLocaleString('id-ID', { minimumFractionDigits: 0 });
    };

    let cashFlowChart, expenseChart, accountChart;

    // ==========================================
    // IMPLEMENTASI GRAFIK 1: TREN ARUS KAS (LINE)
    // ==========================================
    const cfCanvas = document.getElementById('cashFlowChart');
    if (cfCanvas) {
        const labels = JSON.parse(cfCanvas.getAttribute('data-labels'));
        const incomeData = JSON.parse(cfCanvas.getAttribute('data-income'));
        const expenseData = JSON.parse(cfCanvas.getAttribute('data-expense'));

        cashFlowChart = new Chart(cfCanvas, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Pemasukan',
                        data: incomeData,
                        borderColor: colors.success,
                        backgroundColor: 'rgba(16, 185, 129, 0.08)',
                        tension: 0.3,
                        fill: true,
                        borderWidth: 3,
                        pointRadius: 2,
                        pointHoverRadius: 6,
                    },
                    {
                        label: 'Pengeluaran',
                        data: expenseData,
                        borderColor: colors.danger,
                        backgroundColor: 'rgba(239, 68, 68, 0.08)',
                        tension: 0.3,
                        fill: true,
                        borderWidth: 3,
                        pointRadius: 2,
                        pointHoverRadius: 6,
                    },
                ],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: {
                            color: colors.textMuted,
                        },
                    },
                    tooltip: {
                        callbacks: {
                            label: function (context) {
                                return ` ${context.dataset.label}: ${formatRupiah(context.raw)}`;
                            },
                        },
                    },
                },
                scales: {
                    x: {
                        grid: { display: false },
                        ticks: { color: colors.textMuted },
                    },
                    y: {
                        beginAtZero: true,
                        grid: { color: colors.grid },
                        ticks: {
                            color: colors.textMuted,
                            callback: function (value) {
                                return formatRupiah(value);
                            },
                        },
                    },
                },
            },
        });
    }

    // ==========================================
    // IMPLEMENTASI GRAFIK 2: ALOKASI PENGELUARAN (DONUT)
    // ==========================================
    const expCanvas = document.getElementById('expenseChart');
    if (expCanvas) {
        const labels = JSON.parse(expCanvas.getAttribute('data-labels'));
        const values = JSON.parse(expCanvas.getAttribute('data-values'));

        // Palet warna modern keuangan
        const financialPalette = [
            '#047857', // Emerald Green
            '#0ea5e9', // Sky Blue
            '#6366f1', // Indigo
            '#f59e0b', // Amber
            '#8b5cf6', // Purple
            '#ec4899', // Pink
        ];

        expenseChart = new Chart(expCanvas, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [
                    {
                        data: values,
                        backgroundColor: financialPalette,
                        borderWidth: 2,
                        borderColor: colors.cardBg,
                    },
                ],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right',
                        labels: {
                            boxWidth: 12,
                            padding: 15,
                            color: colors.textMuted,
                        },
                    },
                    tooltip: {
                        callbacks: {
                            label: function (context) {
                                return ` ${context.label}: ${formatRupiah(context.raw)}`;
                            },
                        },
                    },
                },
                cutout: '70%',
            },
        });
    }

    // ==========================================
    // IMPLEMENTASI GRAFIK 3: SALDO AKUN (BAR HORIZONTAL)
    // ==========================================
    const accCanvas = document.getElementById('accountChart');
    if (accCanvas) {
        const labels = JSON.parse(accCanvas.getAttribute('data-labels'));
        const values = JSON.parse(accCanvas.getAttribute('data-values'));

        accountChart = new Chart(accCanvas, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Saldo Tersedia',
                        data: values,
                        backgroundColor: colors.primary,
                        borderRadius: 6,
                        barThickness: 20,
                    },
                ],
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: function (context) {
                                return ` Saldo: ${formatRupiah(context.raw)}`;
                            },
                        },
                    },
                },
                scales: {
                    x: {
                        beginAtZero: true,
                        grid: { color: colors.grid },
                        ticks: {
                            color: colors.textMuted,
                            callback: function (value) {
                                return formatRupiah(value);
                            },
                        },
                    },
                    y: {
                        grid: { display: false },
                        ticks: { color: colors.textMuted },
                    },
                },
            },
        });
    }

    // ==========================================
    // EVENT LISTENER UNTUK PERUBAHAN TEMA (DYNAMICS)
    // ==========================================
    window.addEventListener('themechange', function () {
        // Ambil variabel warna terkomputasi yang baru
        colors = getThemeStyles();

        // Perbarui warna default untuk masa mendatang
        Chart.defaults.color = colors.textMuted;

        if (cashFlowChart) {
            // Update Legend
            cashFlowChart.options.plugins.legend.labels.color = colors.textMuted;
            // Update Sumbu X
            cashFlowChart.options.scales.x.ticks.color = colors.textMuted;
            // Update Sumbu Y
            cashFlowChart.options.scales.y.grid.color = colors.grid;
            cashFlowChart.options.scales.y.ticks.color = colors.textMuted;
            // Update Dataset Pemasukan & Pengeluaran
            cashFlowChart.data.datasets[0].borderColor = colors.success;
            cashFlowChart.data.datasets[1].borderColor = colors.danger;
            cashFlowChart.update();
        }

        if (expenseChart) {
            // Update Legend
            expenseChart.options.plugins.legend.labels.color = colors.textMuted;
            // Update Batas Donat (agar menyatu dengan background kartu)
            expenseChart.data.datasets[0].borderColor = colors.cardBg;
            expenseChart.update();
        }

        if (accountChart) {
            // Update Sumbu X
            accountChart.options.scales.x.grid.color = colors.grid;
            accountChart.options.scales.x.ticks.color = colors.textMuted;
            // Update Sumbu Y
            accountChart.options.scales.y.ticks.color = colors.textMuted;
            // Update Warna Bar Utama
            accountChart.data.datasets[0].backgroundColor = colors.primary;
            accountChart.update();
        }
    });
});
