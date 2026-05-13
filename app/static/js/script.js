// ==========================================
// Nama File: script.js
// Deskripsi: JS bagi bse.html
// Penulis:   Fawwaz Yaqzhan
// Tanggal:   01-04-2026
// Catatan:
//   - Mengatur interkasi user di base.html
// ==========================================

document.addEventListener('DOMContentLoaded', function() {
    
    /* =========================================
       Logika Collapsible Menu (Sidebar)
    ========================================= */
    const sidebar = document.getElementById('sidebar');
    const toggleBtn = document.getElementById('toggle-btn');

    if (toggleBtn && sidebar) {
        toggleBtn.addEventListener('click', function() {
            sidebar.classList.toggle('collapsed');
        });
    }

});
