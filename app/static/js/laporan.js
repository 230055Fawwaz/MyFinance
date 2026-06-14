// ==========================================
// Nama File: laporan.js
// Deskripsi: JS khusus halaman laporan
// Penulis:   Fawwaz Yaqzhan
// Tanggal:   10-05-2026
// Catatan:
//   - Mengatur interaksi user di halaman laporan
// ==========================================

document.addEventListener("DOMContentLoaded", function () {
  // 1. Ambil semua elemen yang dibutuhkan
  const filterForm = document.getElementById("filterForm");
  const startDateInput = document.getElementById("start_date");
  const endDateInput = document.getElementById("end_date");
  const shortcutButtons = document.querySelectorAll(".btn-shortcut");

  // 2. Cegah submit form jika tanggal kosong (Validasi Utama)
  if (filterForm) {
    filterForm.addEventListener("submit", function (event) {
      const startDate = startDateInput.value;
      const endDate = endDateInput.value;

      if (!startDate || !endDate) {
        event.preventDefault(); // Menghentikan pengiriman form ke Flask secara paksa
        alert(
          "Maaf, tanggal awal dan tanggal selesai harus diisi terlebih dahulu!",
        );
      }
    });
  }

  // 3. Fungsi bantu format tanggal YYYY-MM-DD lokal
  function formatKeInputDate(dateObj) {
    const tahun = dateObj.getFullYear();
    const bulan = String(dateObj.getMonth() + 1).padStart(2, "0");
    const hari = String(dateObj.getDate()).padStart(2, "0");
    return `${tahun}-${bulan}-${hari}`;
  }

  // 4. Pasang Event Listener ke Tombol Pintasan secara otomatis
  shortcutButtons.forEach((button) => {
    button.addEventListener("click", function () {
      // Mengambil tipe filter dari teks tombol atau fungsi parameter
      // Agar aman, kita cek teks tombolnya atau inline onclick bawaan HTML
      const tipeText = this.textContent.toLowerCase();
      let tipe = "";

      if (tipeText.includes("hari ini")) tipe = "hari_ini";
      else if (tipeText.includes("7 hari") || tipeText.includes("minggu"))
        tipe = "minggu";
      else if (tipeText.includes("bulan")) tipe = "bulan_ini";

      if (!tipe) return;

      const tglSekarang = new Date();
      let tglAwal = new Date();
      let tglAkhir = new Date();

      if (tipe === "hari_ini") {
        tglAwal = tglSekarang;
        tglAkhir = tglSekarang;
      } else if (tipe === "minggu") {
        tglAwal.setDate(tglSekarang.getDate() - 7);
        tglAkhir.setDate(tglSekarang.getDate() - 1);
      } else if (tipe === "bulan_ini") {
        tglAwal = new Date(
          tglSekarang.getFullYear(),
          tglSekarang.getMonth(),
          1,
        );
        tglAkhir = tglSekarang;
      }

      // Isi nilai ke input date
      startDateInput.value = formatKeInputDate(tglAwal);
      endDateInput.value = formatKeInputDate(tglAkhir);

      // Kirim form langsung ke Flask
      filterForm.submit();
    });
  });
});
