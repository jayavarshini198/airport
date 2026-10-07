document.addEventListener("DOMContentLoaded", function () {

    const flash = document.querySelector(".flash");

    if (flash) {

        setTimeout(function () {

            flash.style.display = "none";

        }, 4000);
    }

});
