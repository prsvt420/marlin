const searchInput = document.getElementById("search-input");
const searchForm = searchInput.closest("form");

searchForm.addEventListener("submit", (e) => {
  if (searchInput.value.trim().length < 2) {
    e.preventDefault();
    searchInput.classList.add("border", "border-error");
  }
});

searchInput.addEventListener("blur", () => {
  searchInput.classList.remove("border", "border-error");
});
