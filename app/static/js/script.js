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
