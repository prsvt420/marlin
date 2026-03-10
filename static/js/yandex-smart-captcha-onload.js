function onloadYandexSmartCaptcha() {
  if (window.smartCaptcha) {
      const container = document.getElementById("yandex-smart-captcha-container");

      const widgetId = window.smartCaptcha.render(container, {
          sitekey: container.dataset.sitekey,
          hl: container.dataset.language,
          test: false,
      });
  }
}
