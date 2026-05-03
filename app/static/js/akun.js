document.addEventListener('DOMContentLoaded', function() {

    /* =========================================
       Logika Modal Pop-up (Reusable)
    ========================================= */
    function setupModal(buttonId, modalId) {
        const btn = document.getElementById(buttonId);
        const modal = document.getElementById(modalId);

        if (btn && modal) {
            const closeBtn = modal.querySelector('.close-btn');

            btn.addEventListener('click', function() {
                modal.style.display = 'flex';
            });

            if (closeBtn) {
                closeBtn.addEventListener('click', function() {
                    modal.style.display = 'none';
                });
            }

            window.addEventListener('click', function(event) {
                if (event.target === modal) {
                    modal.style.display = 'none';
                }
            });
        }
    }

    setupModal('btn-tambah-akun', 'modal-akun');
    setupModal('btn-transfer', 'modal-transfer');

});
