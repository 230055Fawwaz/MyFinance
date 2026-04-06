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
    setupModal('btn-transfer', 'modal-transfer');
    setupModal('btn-tambah-kategori', 'modal-kategori');
    setupModal('btn-tambah-subkategori', 'modal-subkategori');

    /* =========================================
       3. Logika 
    ========================================= */
    const kategoriSelect = document.getElementById('kategori');
    const subkategoriSelect = document.getElementById('subcategory_id');
    const subOptions = subkategoriSelect.querySelectorAll('.sub-option');

    kategoriSelect.addEventListener('change', function() {
        const selectedCategoryId = this.value;
        
        // Reset pilihan sub-kategori
        subkategoriSelect.value = "";
        
        // Tampilkan hanya sub-kategori yang sesuai dengan kategori induknya
        subOptions.forEach(function(opt) {
            if (opt.getAttribute('data-category') === selectedCategoryId) {
                opt.style.display = 'block';
            } else {
                opt.style.display = 'none';
            }
        });
    });

});