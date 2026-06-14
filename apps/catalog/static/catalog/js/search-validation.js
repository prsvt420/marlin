document.querySelectorAll("[data-search-form]").forEach((searchForm) => {
  const searchInput = searchForm.querySelector("[data-search-input]");

  if (!searchInput) return;

  searchForm.addEventListener("submit", (e) => {
    if (!searchInput.value.trim().length) {
      e.preventDefault();
      searchInput.focus();
    }
  });
});
