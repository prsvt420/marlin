document.querySelectorAll(".text-expander").forEach((el) => {
  el.classList.add("line-clamp-3");
});

document.addEventListener("click", (e) => {
  const textExpanderToggle = e.target.closest(".text-expander-toggle");
  if (!textExpanderToggle) return;

  const textExpander = textExpanderToggle.previousElementSibling;

  textExpander.classList.remove("line-clamp-3");
  textExpanderToggle.style.display = "none";
});
