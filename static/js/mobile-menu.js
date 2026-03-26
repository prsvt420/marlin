(function () {
  const openMobileMenuBtn = document.getElementById("open-mobile-menu-btn");
  const closeMobileMenuBtn = document.getElementById("close-mobile-menu-btn");
  const mobileMenu = document.getElementById("mobile-menu");

  function openMobileMenu() {
    mobileMenu.classList.remove("translate-x-full");
    document.body.style.overflow = "hidden";
  }

  function closeMobileMenu() {
    mobileMenu.classList.add("translate-x-full");
    document.body.style.overflow = '';
  }

  openMobileMenuBtn.addEventListener("click", openMobileMenu);
  closeMobileMenuBtn.addEventListener("click", closeMobileMenu);
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closeMobileMenu();
  });
})();
