$(document).ready(function () {
    $(".sidenav").sidenav({
        edge: "right"
    });
    $('select').formSelect();
});

$(document).ready(function () {
    const passwordInput = $('#password');
    const togglePassword = $('.toggle-password');

    togglePassword.click(function () {
        if (passwordInput.attr('type') === 'password') {
            passwordInput.attr('type', 'text');
            togglePassword.removeClass('fa-eye');
            togglePassword.addClass('fa-eye-slash');
        } else {
            passwordInput.attr('type', 'password');
            togglePassword.removeClass('fa-eye-slash');
            togglePassword.addClass('fa-eye');
        }
    });
});

$(document).ready(function () {
    $('.modal').modal();
});