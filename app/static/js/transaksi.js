// ==========================================
// Nama File: transaksi.js
// Deskripsi: JS khusus halaman transaksi
// Penulis:   Fawwaz Yaqzhan
// Tanggal:   06-05-2026
// Catatan:
//   - Mengatur interaksi user di halaman transaksi
// ==========================================

document.addEventListener('DOMContentLoaded', function () {
    /* =========================================
       Logika Modal Pop-up (Reusable)
    ========================================= */
    function setupModal(buttonId, modalId) {
        const btn = document.getElementById(buttonId);
        const modal = document.getElementById(modalId);

        if (btn && modal) {
            const closeBtn = modal.querySelector('.close-btn');

            btn.addEventListener('click', function () {
                modal.style.display = 'flex';
            });

            if (closeBtn) {
                closeBtn.addEventListener('click', function () {
                    modal.style.display = 'none';
                });
            }

            window.addEventListener('click', function (event) {
                if (event.target === modal) {
                    modal.style.display = 'none';
                }
            });
        }
    }

    setupModal('btn-tambah-transaksi', 'modal-transaksi');

    /* =========================================
       Logika Dropdown Menu
    ========================================= */
    const kategoriSelect = document.getElementById('kategori');
    const subkategoriSelect = document.getElementById('subcategory_id');
    const subOptions = subkategoriSelect.querySelectorAll('.sub-option');

    kategoriSelect.addEventListener('change', function () {
        const selectedCategoryId = this.value;

        subkategoriSelect.value = '';

        subOptions.forEach(function (opt) {
            if (opt.getAttribute('data-category') === selectedCategoryId) {
                opt.style.display = 'block';
            } else {
                opt.style.display = 'none';
            }
        });
    });
});
