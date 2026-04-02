document.addEventListener('DOMContentLoaded', function() {
    
    /* =========================================
       1. Logika Collapsible Menu (Sidebar)
    ========================================= */
    const sidebar = document.getElementById('sidebar');
    const toggleBtn = document.getElementById('toggle-btn');

    if (toggleBtn && sidebar) {
        toggleBtn.addEventListener('click', function() {
            sidebar.classList.toggle('collapsed');
        });
    }

    /* =========================================
       2. Logika Modal Pop-up (Reusable)
    ========================================= */
    // Fungsi untuk menyambungkan tombol dengan modalnya
    function setupModal(buttonId, modalId) {
        const btn = document.getElementById(buttonId);
        const modal = document.getElementById(modalId);

        if (btn && modal) {
            const closeBtn = modal.querySelector('.close-btn');

            // Buka modal
            btn.addEventListener('click', function() {
                modal.style.display = 'flex';
            });

            // Tutup modal via tombol X
            if (closeBtn) {
                closeBtn.addEventListener('click', function() {
                    modal.style.display = 'none';
                });
            }

            // Tutup modal via klik area luar
            window.addEventListener('click', function(event) {
                if (event.target === modal) {
                    modal.style.display = 'none';
                }
            });
        }
    }

    // Inisialisasi semua modal yang ada di aplikasi
    setupModal('btn-tambah-transaksi', 'modal-transaksi');
    setupModal('btn-tambah-akun', 'modal-akun');
    setupModal('btn-tambah-kategori', 'modal-kategori');
    setupModal('btn-tambah-subkategori', 'modal-subkategori');

});