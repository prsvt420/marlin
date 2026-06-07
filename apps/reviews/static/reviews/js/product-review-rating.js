const setProductRatingStars = (control, rating) => {
  control.querySelectorAll("[data-rating-value]").forEach((button) => {
    const isActive = Number(button.dataset.ratingValue) <= rating;
    button.classList.toggle("text-accent", isActive);
    button.classList.toggle("text-on-surface/20", !isActive);
  });
};

document.addEventListener("pointerover", (event) => {
  const button = event.target.closest("[data-rating-value]");

  if (!button) {
    return;
  }

  const control = button.closest("[data-product-review-control]");
  setProductRatingStars(control, Number(button.dataset.ratingValue));
});

document.addEventListener("pointerout", (event) => {
  const button = event.target.closest("[data-rating-value]");

  if (!button) {
    return;
  }

  const stars = button.closest("[data-rating-stars]");

  if (stars.contains(event.relatedTarget)) {
    return;
  }

  const control = button.closest("[data-product-review-control]");
  setProductRatingStars(control, Number(control.dataset.currentRating));
});

document.addEventListener("focusin", (event) => {
  const button = event.target.closest("[data-rating-value]");

  if (!button) {
    return;
  }

  const control = button.closest("[data-product-review-control]");
  setProductRatingStars(control, Number(button.dataset.ratingValue));
});

document.addEventListener("focusout", (event) => {
  const button = event.target.closest("[data-rating-value]");

  if (!button) {
    return;
  }

  const stars = button.closest("[data-rating-stars]");

  if (stars.contains(event.relatedTarget)) {
    return;
  }

  const control = button.closest("[data-product-review-control]");
  setProductRatingStars(control, Number(control.dataset.currentRating));
});
