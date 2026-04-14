const searchInput = document.getElementById("search-input");
const searchForm = searchInput.closest("form");

searchForm.addEventListener("submit", (e) => {
  if (!searchInput.value.trim().length) {
    e.preventDefault();
  }
});
