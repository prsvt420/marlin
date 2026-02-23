$(document).ready(function () {
  $(".message").each(function(messageIndex) {
    const $message = $(this);

    const removeMessage = () => {
        $message.removeClass('message--show').addClass('message--hide');
        setTimeout(() => $message.remove(), 1000);
    };

    setTimeout(() => $message.removeClass('message--hide').addClass('message--show'), messageIndex * 100);
    setTimeout(removeMessage, 3000 + (messageIndex * 100));

    $message.on('click', removeMessage);
  });
});
