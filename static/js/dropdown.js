document.addEventListener('DOMContentLoaded', () => {
    const dropdownBtn = document.getElementById('settings-dropdown');
    const dropdownMenu = document.getElementById('dropdown-menu');

    dropdownBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        dropdownMenu.classList.toggle('show');
    });

    document.addEventListener('click', (e) => {
        if (!dropdownMenu.contains(e.target)) {
            dropdownMenu.classList.remove('show');
        }
    });
});
