$(document).ready(function () {
    $(".message").each(function(index) {
        const $message = $(this);

        const removeMessage = () => {
            $message.removeClass('show').addClass('hide');
            setTimeout(() => $message.remove(), 1000);
        };

        setTimeout(() => $message.removeClass('hide').addClass('show'), index * 100);
        setTimeout(removeMessage, 3000 + (index * 100));

        $message.on('click', removeMessage);
    });
});
