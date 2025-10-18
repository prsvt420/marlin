document.addEventListener('DOMContentLoaded', function() {
  const swiper = new Swiper('.product__images', {
    navigation: {
      nextEl: '.product__images-button--next',
      prevEl: '.product__images-button--prev',
    },
    pagination: {
      el: '.product__images-pagination',
      clickable: true,
    },
    watchOverflow: true,
  });
});
