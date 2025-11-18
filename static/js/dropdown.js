document.addEventListener('DOMContentLoaded', () => {
    const dropdowns = document.querySelectorAll('.dropdown');

    dropdowns.forEach(dropdown => {
        const toggle = dropdown.querySelector(':scope > .dropdown__toggle');
        const menu = dropdown.querySelector(':scope > .dropdown__menu');

        if (!toggle || !menu) return;

        toggle.addEventListener('click', (e) => {
            e.stopPropagation();
            menu.classList.toggle('show');

            const siblings = dropdown.parentElement.querySelectorAll('.dropdown');
            siblings.forEach(other => {
                if (other !== dropdown) {
                    const otherMenu = other.querySelector(':scope > .dropdown__menu');
                    otherMenu?.classList.remove('show');
                }
            });
        });

        menu.addEventListener('click', (e) => {
            e.stopPropagation();
        });
    });

    document.addEventListener('click', () => {
        document.querySelectorAll('.dropdown__menu.show')
            .forEach(menu => menu.classList.remove('show'));
    });
});
