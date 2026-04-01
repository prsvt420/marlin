(function() {
  var scrollTopBtn = document.getElementById("scroll-top-btn");
  if (!scrollTopBtn) return;

  function toggleBtn() {
    if (window.scrollY > 300) {
      scrollTopBtn.classList.remove("opacity-0", "pointer-events-none");
      scrollTopBtn.classList.add("opacity-100");
    } else {
      scrollTopBtn.classList.add("opacity-0", "pointer-events-none");
      scrollTopBtn.classList.remove("opacity-100");
    }
  }

  toggleBtn();
  window.addEventListener("scroll", toggleBtn);

  scrollTopBtn.addEventListener("click", function() {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });
})();
