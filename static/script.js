document.addEventListener('DOMContentLoaded', function () {
    var dropdownToggle = document.querySelector('.dropdown-toggle');
    var dropdown = document.querySelector('.dropdown');

    dropdownToggle.addEventListener('click', function (event) {
        event.stopPropagation();
        dropdown.classList.toggle('show');
    });

    document.addEventListener('click', function () {
        dropdown.classList.remove('show');
    });
});
