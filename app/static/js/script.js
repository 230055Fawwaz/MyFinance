document.addEventListener('DOMContentLoaded', function () {
    /* =========================================
       Logika Collapsible Menu (Sidebar)
    ========================================= */
    const sidebar = document.getElementById('sidebar');
    const toggleBtn = document.getElementById('toggle-btn');

    if (toggleBtn && sidebar) {
        toggleBtn.addEventListener('click', function () {
            sidebar.classList.toggle('collapsed');
        });
    }

    /* =========================================
       Logika Navigasi Menu Aktif
    ========================================= */
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.sidebar-nav a');

    navLinks.forEach((link) => {
        const href = link.getAttribute('href');
        if (href && (currentPath === href || (currentPath === '/' && href.includes('dashboard')))) {
            link.classList.add('active');
        }
    });
});
