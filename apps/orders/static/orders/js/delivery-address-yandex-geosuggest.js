(function () {
  const deliveryAddressInput = document.getElementById("delivery_address");
  const deliveryAddressSuggestionsList = document.getElementById("delivery_address_suggestions");

  if (!deliveryAddressInput || !deliveryAddressSuggestionsList) return;

  const wrapper = deliveryAddressInput.closest("[data-sitekey]");
  const GEOSUGGEST_KEY = wrapper?.dataset.sitekey || "";
  const LANGUAGE_CODE = wrapper?.dataset.language || "ru";

  if (!GEOSUGGEST_KEY) {
    console.warn("Yandex Suggest key is missing");
    return;
  }

  let debounceTimer = null;
  let currentController = null;

  function hideList() {
    deliveryAddressSuggestionsList.classList.add("hidden");
    deliveryAddressSuggestionsList.innerHTML = "";
  }

  function showList() {
    deliveryAddressSuggestionsList.classList.remove("hidden");
  }

  function renderSuggestions(items) {
    deliveryAddressSuggestionsList.innerHTML = "";
    if (!items || items.length === 0) {
      hideList();
      return;
    }

    items.forEach((item) => {
      const li = document.createElement("li");
      li.className = "p-4 cursor-pointer hover:bg-surface-dim text-sm first:rounded-t-box last:rounded-b-box";

      const title = item.title?.text || "";
      const subtitle = item.subtitle?.text || "";

      li.innerHTML = `
        <div class="font-bold text-on-surface">${title}</div>
        ${subtitle ? `<div class="text-on-surface/60 text-xs">${subtitle}</div>` : ""}
      `;

      li.addEventListener("mousedown", (e) => {
        e.preventDefault();
        deliveryAddressInput.value = subtitle ? `${subtitle}, ${title}` : title;
        hideList();
      });

      deliveryAddressSuggestionsList.appendChild(li);
    });

    showList();
  }

  async function fetchSuggestions(query) {
    if (currentController) currentController.abort();
    currentController = new AbortController();

    const url = new URL("https://suggest-maps.yandex.ru/v1/suggest");
    url.searchParams.set("apikey", GEOSUGGEST_KEY);
    url.searchParams.set("text", query);
    url.searchParams.set("lang", LANGUAGE_CODE);
    url.searchParams.set("results", "5");
    url.searchParams.set("types", "house,street,locality,entrance");

    try {
      const response = await fetch(url, { signal: currentController.signal });
      if (!response.ok) {
        console.error("Suggest API error:", response.status);
        return;
      }
      const data = await response.json();
      renderSuggestions(data.results || []);
    } catch (err) {
      if (err.name !== "AbortError") console.error(err);
    }
  }

  deliveryAddressInput.addEventListener("input", function () {
    const query = deliveryAddressInput.value.trim();
    clearTimeout(debounceTimer);
    if (query.length < 3) {
      hideList();
      return;
    }
    debounceTimer = setTimeout(() => fetchSuggestions(query), 250);
  });

  document.addEventListener("click", function (e) {
    if (!deliveryAddressSuggestionsList.contains(e.target) && e.target !== deliveryAddressInput) {
      hideList();
    }
  });
})();
