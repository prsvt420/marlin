$(document).ready(function () {
    $('.product__text-expander').on('click', function () {
        const textBlock = $(this).siblings('.product__text');
        const isCollapsed = textBlock.hasClass('product__text--collapsed');

        const showText = $(this).data('show');
        const hideText = $(this).data('hide');

        if (isCollapsed) {
            textBlock.removeClass('product__text--collapsed');
            $(this).text(hideText);
        } else {
            textBlock.addClass('product__text--collapsed');
            $(this).text(showText);
        }
    });
});
