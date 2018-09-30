$(function() {
  $('.menu__button').on('click', function () {
    $(this).next().toggleClass('active');
  });
});