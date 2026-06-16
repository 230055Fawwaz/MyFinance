// ==========================================
// Nama File: settings.js
// Deskripsi: JS khusus halaman dropdown
// Penulis:   Fawwaz Yaqzhan
// Tanggal:   10-05-2026
// Catatan:
//   - Mengatur interaksi user di halaman dropdown
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
                modal.classList.add('show');
            });

            if (closeBtn) {
                closeBtn.addEventListener('click', function () {
                    modal.classList.remove('show');
                });
            }

            window.addEventListener('click', function (event) {
                if (event.target === modal) {
                    modal.classList.remove('show');
                }
            });
        }
    }

    setupModal('btn-tambah-kategori', 'modal-kategori');
    setupModal('btn-tambah-subkategori', 'modal-subkategori');
});
