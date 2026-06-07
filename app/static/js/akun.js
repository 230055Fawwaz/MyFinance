// ==========================================
// Nama File: akun.js
// Deskripsi: JS khusus halaman akun
// Penulis:   Fawwaz Yaqzhan
// Tanggal:   06-05-2026
// Catatan:
//   - Mengatur interaksi user di halaman akun
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

    setupModal('btn-tambah-akun', 'modal-akun');
    setupModal('btn-transfer', 'modal-transfer');
});
