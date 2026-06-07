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

    window.duplikatTransaksi = function duplikatTransaksi(accountId, categoryId, subcategoryId, amount, note) {
        document.getElementById('account_id').value = accountId;
        document.getElementById('kategori').value = categoryId;
        
        const event = new Event('change');
        document.getElementById('kategori').dispatchEvent(event);
        
        // Beri jeda 300 milidetik agar opsi sub-kategori sempat ter-render
        setTimeout(() => {
            document.getElementById('subcategory_id').value = subcategoryId;
        }, 300);
        
        document.getElementById('amount').value = amount;
        document.getElementById('note').value = note;
        
        const hariIni = new Date().toISOString().split('T')[0];
        document.getElementById('date').value = hariIni;
        
        document.getElementById('modal-transaksi').classList.add('show');
    }
});
