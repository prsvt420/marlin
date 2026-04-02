document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".message").forEach((message, messageIndex) => {

    const removeMessage = () => {
      message.classList.remove("!translate-x-0", "!opacity-100", "!pointer-events-auto");
      message.classList.add("!translate-x-[120%]", "!opacity-0");
      setTimeout(() => message.remove(), 1000);
    };

    setTimeout(() => {
      message.classList.remove("!translate-x-[120%]", "!opacity-0");
      message.classList.add("!translate-x-0", "!opacity-100", "!pointer-events-auto");
    }, messageIndex * 100);

    setTimeout(removeMessage, 3000 + (messageIndex * 100));

    message.addEventListener("click", removeMessage);
  });
});
