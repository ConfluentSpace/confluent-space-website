document.addEventListener("DOMContentLoaded", function ()
{
    var menu = document.getElementById("menu");

    document.getElementById("menu-toggle").addEventListener("click", function ()
    {
        menu.classList.toggle("open");
    });
});
