(function () {
  const methods = document.querySelectorAll(".js-delivery-method");
  const addressField = document.querySelector(".js-delivery-address-field");

  if (!addressField || methods.length === 0) return;

  function update() {
    const selected = document.querySelector(".js-delivery-method:checked");
    const value = selected ? selected.value : "courier";
    addressField.hidden = value !== "courier";
  }

  methods.forEach((el) => el.addEventListener("change", update));
  update();
})();
