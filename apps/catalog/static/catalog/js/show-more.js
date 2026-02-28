document.addEventListener("click", (event) => {
  const button = event.target.closest(".product__value-expander");
  if (!button) return;

  const targetId = button.getAttribute("aria-controls");
  const textBlock = document.getElementById(targetId);
  if (!textBlock) return;

  const isExpanded = button.getAttribute("aria-expanded") === "true";

  button.setAttribute("aria-expanded", String(!isExpanded));
  textBlock.classList.toggle("product__value--collapsed");

  button.textContent = isExpanded
    ? button.dataset.show
    : button.dataset.hide;
});
