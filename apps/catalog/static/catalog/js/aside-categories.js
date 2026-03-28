document.querySelectorAll("[data-aside-category-btn]").forEach(btn => {
  btn.addEventListener("click", function() {
    const ul = this.nextElementSibling;
    const svg = this.querySelector("svg");
    if (ul.style.maxHeight) {
      ul.style.maxHeight = null;
    } else {
      ul.style.maxHeight = ul.scrollHeight + "px";
    }
    btn.classList.toggle("link--active");
    svg.classList.toggle("rotate-180");
  });
});
