// ==========================================
// Nama File: dashboard.js
// Deskripsi: JS khusus halaman dashboard
// Penulis:   Fawwaz Yaqzhan
// Tanggal:   10-05-2026
// Catatan:
//   - Mengatur interaksi user di halaman dashboard
// ==========================================       

document.addEventListener('DOMContentLoaded', function() {
    
    const ctx = document.getElementById('subCategoryChart');
    
    // Cek apakah variabel Chart sudah terdefinisi
    if (typeof Chart === 'undefined') {
        console.error("Gagal memuat library Chart.js. Pastikan koneksi internet stabil.");
        return; 
    }

    const labels = JSON.parse(ctx.getAttribute('data-labels'));
    const values = JSON.parse(ctx.getAttribute('data-values'));

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: ['#4e73df', '#1cc88a', '#36b9cc', '#f6c23e', '#e74a3b'],
                borderWidth: 1
            }]
        },
        options: {
            maintainAspectRatio: false, // Wajib agar mengikuti tinggi div pembungkus
            plugins: {
                legend: {
                    position: 'right', // Pindahkan legenda ke samping agar tidak makan tempat
                }
            }
        }
    });    

});
