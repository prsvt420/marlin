(function () {
  const openMobileSearchBtn = document.getElementById("open-mobile-search-btn");
  const openMobileMenuBtn = document.getElementById("open-mobile-menu-btn");
  const mobileSearch = document.getElementById("mobile-search");
  const mobileSearchInput = document.getElementById("mobile-search-input");

  if (!openMobileSearchBtn || !mobileSearch || !mobileSearchInput) return;

  function setMobileSearchOpen(isOpen) {
    mobileSearch.classList.toggle("hidden", !isOpen);
    openMobileSearchBtn.setAttribute("aria-expanded", String(isOpen));

    if (isOpen) {
      window.requestAnimationFrame(() => mobileSearchInput.focus());
    }
  }

  function isMobileSearchOpen() {
    return !mobileSearch.classList.contains("hidden");
  }

  openMobileSearchBtn.addEventListener("click", () => {
    setMobileSearchOpen(!isMobileSearchOpen());
  });

  openMobileMenuBtn?.addEventListener("click", () => {
    setMobileSearchOpen(false);
  });

  document.addEventListener("click", (event) => {
    if (
      !isMobileSearchOpen() ||
      mobileSearch.contains(event.target) ||
      openMobileSearchBtn.contains(event.target)
    ) {
      return;
    }

    setMobileSearchOpen(false);
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      setMobileSearchOpen(false);
    }
  });
})();
