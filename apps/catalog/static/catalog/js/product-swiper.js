document.addEventListener("DOMContentLoaded", function() {
  const swiper = new Swiper(".product__swiper", {
    navigation: {
      nextEl: ".product__swiper-button--next",
      prevEl: ".product__swiper-button--prev",
    },
    pagination: {
      el: ".product__swiper-pagination",
      clickable: true,
    },
    watchOverflow: true,
  });
});
